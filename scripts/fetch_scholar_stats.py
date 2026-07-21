#!/usr/bin/env python3
"""Fetch Google Scholar data in a single pass and write two data files:

  _data/scholar_stats.yml  profile-level metrics (citations, h-index, i10-index)
  _data/citations.yml      per-article citation counts, keyed by google_scholar_id

The keys in citations.yml match the `google_scholar_id` field on each entry in
_bibliography/papers.bib; _layouts/bib.liquid looks counts up by that field.

Two sources, tried in order:

  1. Scraping the public profile page. Free, but Google Scholar often serves a
     captcha page to datacenter IPs, which is exactly what GitHub Actions runs
     on. A blocked response looks like a valid 200, so it is detected by the
     absence of the metrics block and retried.
  2. SerpAPI's google_scholar_author endpoint, used only if SERPAPI_KEY is set.
     Not blockable; one call per run stays inside the 100/month free tier.

Designed to fail safe: if no source yields data, both files are left untouched,
so the last-known-good values keep showing, and the caller gets a non-zero exit
so the failure is visible rather than looking like "no change".
"""
import datetime
import json
import os
import random
import re
import sys
import time
import urllib.parse
import urllib.request

SCHOLAR_ID = os.environ.get("SCHOLAR_USERID", "CF7dea8AAAAJ")
STATS_PATH = os.environ.get("SCHOLAR_STATS_PATH", "_data/scholar_stats.yml")
CITES_PATH = os.environ.get("SCHOLAR_CITES_PATH", "_data/citations.yml")
SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "").strip()

PAGE_SIZE = 100
PROFILE_URL = (
    "https://scholar.google.com/citations"
    "?user={user}&hl=en&cstart={cstart}&pagesize={pagesize}"
)
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

ROW_RE = re.compile(r'class="gsc_a_tr"(.*?)(?=class="gsc_a_tr"|</tbody>)', re.S)
ARTID_RE = re.compile(r'citation_for_view=[^:&"]+:([^&"\s]+)')
CITES_RE = re.compile(r'class="gsc_a_ac[^"]*"[^>]*>\s*(\d*)\s*<')


def fetch_html(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def fetch_with_retry(url, attempts=4):
    """Fetch until the page actually contains the metrics block.

    A captcha/consent interstitial comes back as a normal 200, so a successful
    request is not the same as a usable one; both cases retry with backoff.
    """
    last_err = None
    for i in range(attempts):
        try:
            html = fetch_html(url)
            if "gsc_rsb_std" in html:
                return html
            last_err = "page returned without metrics block (blocked or empty)"
        except Exception as exc:  # noqa: BLE001
            last_err = exc
        sys.stderr.write("attempt {}/{} failed: {}\n".format(i + 1, attempts, last_err))
        time.sleep(random.uniform(3.0, 8.0) * (i + 1))
    raise RuntimeError(last_err)


def parse_metrics(html):
    """Return (citations, h_index, i10_index) from the 'All' column.

    The profile renders six <td class="gsc_rsb_std"> cells in row-major order:
    Citations(All), Citations(Since), h-index(All), h-index(Since),
    i10-index(All), i10-index(Since). We take the 'All' values: indices 0, 2, 4.
    """
    cells = re.findall(r'class="gsc_rsb_std">\s*([\d,]+)\s*<', html)
    nums = [int(c.replace(",", "")) for c in cells]
    if len(nums) < 6:
        raise ValueError("expected >=6 metric cells, got {}: {}".format(len(nums), nums))
    return nums[0], nums[2], nums[4]


def parse_articles(html):
    """Return {article_id: citation_count} for one page of the profile listing.

    An article with zero citations renders an empty cell; we record it as 0.
    """
    out = {}
    for row in ROW_RE.findall(html):
        m_id = ARTID_RE.search(row)
        if not m_id:
            continue
        m_cites = CITES_RE.search(row)
        out[m_id.group(1)] = int(m_cites.group(1)) if (m_cites and m_cites.group(1)) else 0
    return out


def fetch_direct():
    """Scrape the public profile. Returns (metrics, articles); raises if blocked."""
    articles = {}
    metrics = None
    cstart = 0
    while True:
        url = PROFILE_URL.format(user=SCHOLAR_ID, cstart=cstart, pagesize=PAGE_SIZE)
        html = fetch_with_retry(url)
        if metrics is None:
            metrics = parse_metrics(html)
        page = parse_articles(html)
        articles.update(page)
        if len(page) < PAGE_SIZE:
            break
        cstart += PAGE_SIZE
        time.sleep(random.uniform(2.0, 4.0))
    return metrics, articles


def fetch_serpapi():
    """Same data via SerpAPI. Returns (metrics, articles); raises on any problem.

    `citation_id` comes back as "<user_id>:<article_id>"; the second half is the
    `google_scholar_id` used in the bibliography.
    """
    articles = {}
    metrics = None
    start = 0
    while True:
        query = urllib.parse.urlencode(
            {
                "engine": "google_scholar_author",
                "author_id": SCHOLAR_ID,
                "api_key": SERPAPI_KEY,
                "hl": "en",
                "num": PAGE_SIZE,
                "start": start,
            }
        )
        req = urllib.request.Request("https://serpapi.com/search.json?" + query)
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8", "replace"))

        if data.get("error"):
            raise RuntimeError("SerpAPI error: {}".format(data["error"]))

        if metrics is None:
            # cited_by.table is a list of single-key dicts, each holding an
            # {"all": N, "since_YYYY": M} pair. We want the "all" figures.
            table = {}
            for row in data.get("cited_by", {}).get("table", []):
                table.update(row)
            try:
                metrics = (
                    int(table["citations"]["all"]),
                    int(table["h_index"]["all"]),
                    int(table["i10_index"]["all"]),
                )
            except (KeyError, TypeError) as exc:
                raise RuntimeError("SerpAPI response missing metrics: {}".format(exc))

        page = data.get("articles", [])
        for art in page:
            cid = art.get("citation_id", "")
            if ":" not in cid:
                continue
            articles[cid.split(":", 1)[1]] = int(art.get("cited_by", {}).get("value") or 0)

        if len(page) < PAGE_SIZE:
            break
        start += PAGE_SIZE

    return metrics, articles


def main():
    sources = [("direct scrape", fetch_direct)]
    if SERPAPI_KEY:
        sources.append(("SerpAPI", fetch_serpapi))
    else:
        sys.stderr.write("note: SERPAPI_KEY unset, no fallback if Scholar blocks us\n")

    metrics = articles = None
    for name, fetch in sources:
        try:
            metrics, articles = fetch()
            sys.stderr.write("source: {} succeeded\n".format(name))
            break
        except Exception as exc:  # noqa: BLE001
            sys.stderr.write("source: {} failed: {}\n".format(name, exc))

    if not articles or metrics is None:
        sys.stderr.write("ERROR: every source failed; refusing to overwrite data files\n")
        return 1

    citations, h_index, i10_index = metrics
    today = datetime.date.today().isoformat()
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    with open(STATS_PATH, "w", encoding="utf-8") as fh:
        fh.write(
            "# Auto-generated by scripts/fetch_scholar_stats.py — do not edit by hand.\n"
            "# Profile-level Google Scholar metrics ('All' column).\n"
            "citations: {}\n"
            "h_index: {}\n"
            "i10_index: {}\n"
            "updated_at: '{}'\n".format(citations, h_index, i10_index, today)
        )

    with open(CITES_PATH, "w", encoding="utf-8") as fh:
        fh.write(
            "# Auto-generated by scripts/fetch_scholar_stats.py — do not edit by hand.\n"
            "# Per-article Google Scholar citation counts, keyed by google_scholar_id.\n"
            "updated_at: '{}'\n"
            "counts:\n".format(now)
        )
        for artid in sorted(articles, key=lambda k: (-articles[k], k)):
            fh.write("  {}: {}\n".format(artid, articles[artid]))

    sys.stdout.write(
        "OK citations={} h_index={} i10_index={} articles={} -> {}, {}\n".format(
            citations, h_index, i10_index, len(articles), STATS_PATH, CITES_PATH
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
