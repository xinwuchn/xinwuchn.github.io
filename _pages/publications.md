---
layout: page
permalink: /publications/
title: Publications
description:
nav: true
nav_order: 2
---

<style>
  a.btn.cite-count,
  a.btn.cite-count:hover,
  a.btn.cite-count:focus {
    background: transparent;
    color: #4285F4 !important;
    border: 1px solid #4285F4;
    font-weight: 500;
    font-size: 0.72rem;
    letter-spacing: 0.02em;
    padding: 0.15em 0.55em;
    box-shadow: none;
  }
  a.btn.cite-count strong {
    color: #4285F4;
    font-weight: 700;
    margin-left: 0.15em;
  }
  a.btn.cite-count:hover {
    background: #4285F4;
    color: #fff !important;
  }
  a.btn.cite-count:hover strong {
    color: #fff;
  }
  .featured-badge {
    display: inline-block;
    vertical-align: middle;
    margin-left: 0.4em;
    padding: 0.15em 0.55em;
    border-radius: 0.3em;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    color: #fff;
    background: linear-gradient(135deg, #f59e0b, #d97706);
    box-shadow: 0 1px 2px rgba(0,0,0,0.15);
  }

  /* ---- Publications overview ---- */
  .pub-overview {
    margin-bottom: 1.6rem;
  }
  .pub-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.8rem;
    margin-bottom: 1.2rem;
  }
  @media (max-width: 576px) {
    .pub-stats { grid-template-columns: repeat(2, 1fr); }
  }
  .pub-stat {
    text-align: center;
    padding: 0.9rem 0.5rem;
    border: 1px solid var(--global-divider-color, #e0e0e0);
    border-radius: 0.5rem;
    background: var(--global-card-bg-color, transparent);
  }
  .pub-stat .num {
    display: block;
    font-size: 1.9rem;
    font-weight: 700;
    line-height: 1.1;
    color: var(--global-theme-color, #4285F4);
  }
  .pub-stat .label {
    display: block;
    margin-top: 0.25rem;
    font-size: 0.72rem;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    color: var(--global-text-color-light, #828282);
  }
  .pub-filters {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.6rem;
    padding-top: 1.2rem;
  }
  .pub-filter {
    display: inline-flex;
    align-items: center;
    gap: 0.55em;
    cursor: pointer;
    border: 1px solid transparent;
    color: var(--global-text-color, #333);
    background: var(--global-code-bg-color, rgba(0, 0, 0, 0.04));
    border-radius: 2em;
    padding: 0.5em 0.7em 0.5em 1.1em;
    font-size: 0.85rem;
    font-weight: 500;
    line-height: 1;
    transition: color 0.18s ease, background 0.18s ease, box-shadow 0.18s ease;
  }
  .pub-filter:hover {
    background: rgba(66, 133, 244, 0.12);
    color: var(--global-theme-color, #4285F4);
  }
  .pub-filter.active {
    background: var(--global-theme-color, #4285F4);
    color: #fff;
    box-shadow: 0 2px 8px rgba(66, 133, 244, 0.28);
  }
  .pub-filter.empty {
    opacity: 0.4;
    pointer-events: none;
  }
  .pub-filter .count {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 1.8em;
    height: 1.6em;
    padding: 0 0.5em;
    border-radius: 1em;
    font-size: 0.72rem;
    font-weight: 700;
    background: var(--global-divider-color, rgba(0, 0, 0, 0.06));
    color: var(--global-text-color-light, #6b6b6b);
    transition: color 0.18s ease, background 0.18s ease;
  }
  .pub-filter:hover .count {
    background: rgba(66, 133, 244, 0.18);
    color: var(--global-theme-color, #4285F4);
  }
  .pub-filter.active .count {
    background: rgba(255, 255, 255, 0.24);
    color: #fff;
  }
  @media (max-width: 576px) {
    .pub-stat .num { font-size: 1.5rem; }
  }
</style>

<!-- _pages/publications.md -->

{%- comment -%}
  Profile-level metrics come from _data/scholar_stats.yml, which is refreshed
  automatically from Google Scholar by .github/workflows/update-scholar-stats.yml.
  The publication count is computed client-side from the rendered entries.
{%- endcomment -%}
{%- assign gs = site.data.scholar_stats -%}

<div class="pub-overview">
  <div class="pub-stats">
    <div class="pub-stat">
      <span class="num" id="pub-total">–</span>
      <span class="label">Publications</span>
    </div>
    <div class="pub-stat">
      <a href="https://scholar.google.com/citations?user={{ site.scholar_userid }}" target="_blank" rel="noopener" style="text-decoration:none;" title="Updated {{ gs.updated_at }}">
        <span class="num">{{ gs.citations | default: '–' }}</span>
        <span class="label">Citations</span>
      </a>
    </div>
    <div class="pub-stat">
      <span class="num">{{ gs.h_index | default: '–' }}</span>
      <span class="label">h-index</span>
    </div>
    <div class="pub-stat">
      <span class="num">{{ gs.i10_index | default: '–' }}</span>
      <span class="label">i10-index</span>
    </div>
  </div>
  <div class="pub-filters" id="pub-filters">
    <button class="pub-filter active" data-filter="all">All <span class="count"></span></button>
    <button class="pub-filter" data-filter="role-first">First author <span class="count"></span></button>
    <button class="pub-filter" data-filter="role-cofirst">Co-first author <span class="count"></span></button>
    <button class="pub-filter" data-filter="role-corresponding">Corresponding author <span class="count"></span></button>
    <button class="pub-filter" data-filter="role-collaborator">Co-author <span class="count"></span></button>
  </div>
</div>

<div class="publications">

<p>
† : Equal contribution  * : Corresponding  author.
</p>

{% bibliography %}

</div>

<script>
  (function () {
    function ready(fn) {
      if (document.readyState !== 'loading') { fn(); }
      else { document.addEventListener('DOMContentLoaded', fn); }
    }

    ready(function () {
      var container = document.querySelector('.publications');
      if (!container) return;
      var entries = Array.prototype.slice.call(container.querySelectorAll('.publication-entry'));

      // --- Publication count (citations / h-index / i10 come from scholar_stats.yml) ---
      var totalEl = document.getElementById('pub-total');
      if (totalEl) totalEl.textContent = entries.length;

      // --- Per-role counts on filter buttons ---
      var roles = ['role-first', 'role-cofirst', 'role-corresponding', 'role-collaborator'];
      var counts = { all: entries.length };
      roles.forEach(function (r) { counts[r] = 0; });
      entries.forEach(function (e) {
        roles.forEach(function (r) {
          if (e.classList.contains(r)) counts[r]++;
        });
      });
      document.querySelectorAll('.pub-filter').forEach(function (btn) {
        var f = btn.getAttribute('data-filter');
        var c = btn.querySelector('.count');
        if (c && counts[f] !== undefined) {
          c.textContent = counts[f];
          if (counts[f] === 0 && f !== 'all') btn.classList.add('empty');
        }
      });

      // --- Filtering ---
      function applyFilter(filter) {
        entries.forEach(function (e) {
          var li = e.closest('li') || e;
          var show = (filter === 'all') || e.classList.contains(filter);
          li.style.display = show ? '' : 'none';
        });
        // Hide year headings + lists that have no visible entries
        container.querySelectorAll('ol.bibliography').forEach(function (ol) {
          var anyVisible = Array.prototype.some.call(ol.children, function (li) {
            return li.style.display !== 'none';
          });
          ol.style.display = anyVisible ? '' : 'none';
          var heading = ol.previousElementSibling;
          if (heading && heading.tagName === 'H2') {
            heading.style.display = anyVisible ? '' : 'none';
          }
        });
      }

      document.querySelectorAll('.pub-filter').forEach(function (btn) {
        btn.addEventListener('click', function () {
          document.querySelectorAll('.pub-filter').forEach(function (b) { b.classList.remove('active'); });
          btn.classList.add('active');
          applyFilter(btn.getAttribute('data-filter'));
        });
      });
    });
  })();
</script>
