---
layout: page
permalink: /presentations/
title: Presentations
description: Invited talks, contributed talks, and posters at conferences and workshops.
nav: true
nav_order: 3
---

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

<style>
  .presentations .year-heading {
    margin-top: 1.5rem;
    padding-bottom: 0.25rem;
    border-bottom: 1px solid var(--global-divider-color);
  }
  .presentations .talk {
    padding: 1rem 0 1rem 0.9rem;
    border-left: 3px solid transparent;
    border-bottom: 1px dashed var(--global-divider-color);
  }
  .presentations .talk:last-child { border-bottom: none; }
  .presentations .talk-title {
    font-weight: 600;
    font-size: 1.05rem;
    margin: 0.2rem 0;
  }
  .presentations .talk-meta {
    color: var(--global-text-color-light);
    font-size: 0.92rem;
  }
  .presentations .talk-authors {
    font-size: 0.9rem;
    color: var(--global-text-color-light);
  }
  .presentations .talk-abstract {
    font-size: 0.9rem;
    margin-top: 0.3rem;
  }
  .presentations .badge-type {
    display: inline-block;
    padding: 0.2em 0.6em;
    border-radius: 0.3em;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    color: #fff;
    margin-right: 0.4rem;
    vertical-align: 2px;
  }
  .presentations .badge-invited      { background: #b31b1b; }
  .presentations .badge-contributed  { background: #0d6efd; }
  .presentations .badge-poster       { background: #6c757d; }
  .presentations .talk-invited {
    background: rgba(179, 27, 27, 0.04);
    border-left-color: #b31b1b;
  }
  .presentations .talk-links a {
    font-size: 0.85rem;
    margin-right: 0.6rem;
  }
  .pin-marker { background: transparent; border: none; }
  .pin-marker svg {
    filter: drop-shadow(0 2px 3px rgba(0,0,0,0.35));
    transition: transform 0.15s ease;
  }
  .pin-marker:hover svg { transform: translateY(-2px) scale(1.08); }
  #presentations-map {
    height: 380px;
    width: 100%;
    margin-bottom: 1.5rem;
    border-radius: 8px;
    border: 1px solid var(--global-divider-color);
  }
  .map-legend {
    font-size: 0.85rem;
    color: var(--global-text-color-light);
    margin: -1rem 0 1rem 0;
  }
  .map-legend .dot {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin: 0 0.25rem 0 0.75rem;
    vertical-align: middle;
  }
</style>

<div class="presentations">

{% if site.data.presentations and site.data.presentations != empty %}

<div id="presentations-map"></div>
<div class="map-legend">
  <span class="dot" style="background:#b31b1b"></span>Invited
  <span class="dot" style="background:#0d6efd"></span>Talk
  <span class="dot" style="background:#6c757d"></span>Poster
</div>

<script>
(function () {
  const data = {{ site.data.presentations | jsonify }};
  const map = L.map('presentations-map', { scrollWheelZoom: false }).setView([20, 10], 2);
  map.on('click', function () { map.scrollWheelZoom.enable(); });
  map.on('mouseout', function () { map.scrollWheelZoom.disable(); });
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19
  }).addTo(map);
  const colorMap = { invited: '#b31b1b', contributed: '#0d6efd', poster: '#6c757d' };
  const typeRank = { invited: 0, contributed: 1, poster: 2 };
  function pinIcon(color, count) {
    const gid = 'g-' + color.replace('#','');
    let svg =
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 40" width="28" height="40">' +
        '<defs>' +
          '<radialGradient id="' + gid + '" cx="50%" cy="35%" r="65%">' +
            '<stop offset="0%" stop-color="white" stop-opacity="0.45"/>' +
            '<stop offset="55%" stop-color="' + color + '" stop-opacity="0"/>' +
          '</radialGradient>' +
        '</defs>' +
        '<path d="M14 1.5C7.649 1.5 2.5 6.649 2.5 13c0 4.79 3.63 10.4 7.1 14.49 1.77 2.08 3.54 3.82 4.4 4.63.86-.81 2.63-2.55 4.4-4.63C21.87 23.4 25.5 17.79 25.5 13c0-6.351-5.149-11.5-11.5-11.5z" ' +
          'fill="' + color + '" stroke="white" stroke-width="2" stroke-linejoin="round"/>' +
        '<path d="M14 1.5C7.649 1.5 2.5 6.649 2.5 13c0 4.79 3.63 10.4 7.1 14.49 1.77 2.08 3.54 3.82 4.4 4.63.86-.81 2.63-2.55 4.4-4.63C21.87 23.4 25.5 17.79 25.5 13c0-6.351-5.149-11.5-11.5-11.5z" ' +
          'fill="url(#' + gid + ')"/>' +
        '<circle cx="14" cy="13" r="4.2" fill="white"/>';
    if (count > 1) {
      svg +=
        '<circle cx="22" cy="6" r="6" fill="white" stroke="' + color + '" stroke-width="1.5"/>' +
        '<text x="22" y="8.6" text-anchor="middle" font-family="Arial,sans-serif" font-size="8" font-weight="700" fill="' + color + '">' + count + '</text>';
    }
    svg += '</svg>';
    return L.divIcon({
      html: svg,
      className: 'pin-marker',
      iconSize: [28, 40],
      iconAnchor: [14, 38],
      popupAnchor: [0, -34]
    });
  }
  // Group entries by rounded lat,lng so overlapping venues collapse into one marker
  const groups = {};
  data.forEach(function (t) {
    if (t.lat == null || t.lng == null) return;
    const key = t.lat.toFixed(3) + ',' + t.lng.toFixed(3);
    if (!groups[key]) groups[key] = { lat: t.lat, lng: t.lng, items: [] };
    groups[key].items.push(t);
  });
  const bounds = [];
  Object.keys(groups).forEach(function (key) {
    const g = groups[key];
    // Sort items: invited first, then contributed, then poster; within type by date desc
    g.items.sort(function (a, b) {
      const r = (typeRank[a.type] ?? 9) - (typeRank[b.type] ?? 9);
      if (r !== 0) return r;
      return (b.date || '').toString().localeCompare((a.date || '').toString());
    });
    const dominant = g.items[0].type;
    const color = colorMap[dominant] || '#0d6efd';
    const marker = L.marker([g.lat, g.lng], { icon: pinIcon(color, g.items.length) }).addTo(map);
    let html = '';
    if (g.items.length > 1) {
      html += '<div style="font-weight:600;margin-bottom:6px;color:#555;">' +
              g.items[0].location + ' &middot; ' + g.items.length + ' visits</div>';
    }
    g.items.forEach(function (t, i) {
      const dateStr = (t.date || '').toString().substring(0, 7);
      const badgeColor = colorMap[t.type] || '#0d6efd';
      const badgeText = t.type === 'invited' ? 'Invited' : (t.type === 'poster' ? 'Poster' : 'Talk');
      if (i > 0) html += '<hr style="margin:6px 0;border:none;border-top:1px dashed #ddd;">';
      html +=
        '<span style="display:inline-block;padding:1px 6px;border-radius:3px;font-size:.7rem;font-weight:700;color:#fff;background:' + badgeColor + ';text-transform:uppercase;">' + badgeText + '</span> ' +
        '<span style="color:#888;font-size:.75rem;">' + dateStr + '</span><br>' +
        '<strong>' + t.title + '</strong><br>' +
        '<em style="color:#666;font-size:.85rem;">' + t.conference + '</em>';
    });
    marker.bindPopup(html, { maxWidth: 320 });
    bounds.push([g.lat, g.lng]);
  });
  if (bounds.length > 0) {
    map.fitBounds(bounds, { padding: [30, 30], maxZoom: 5 });
  }
})();
</script>

{% assign sorted = site.data.presentations | sort: "date" | reverse %}
{% assign years = sorted | map: "year" | uniq %}

{% for year in years %}
  <h2 class="year-heading">{{ year }}</h2>
  {% assign items = sorted | where: "year", year %}
  {% for t in items %}
    <div class="talk {% if t.type == 'invited' %}talk-invited{% endif %}">
      <span class="badge-type badge-{{ t.type }}">
        {% if t.type == 'invited' %}Invited{% elsif t.type == 'poster' %}Poster{% else %}Talk{% endif %}
      </span>
      <div class="talk-title">{{ t.title }}</div>
      {% if t.authors %}<div class="talk-authors">{{ t.authors | replace: "Xin Wu", "<u>Xin Wu</u>" }}</div>{% endif %}
      <div class="talk-meta">
        {% if t.url %}<a href="{{ t.url }}" target="_blank" rel="noopener"><em>{{ t.conference }}</em></a>{% else %}<em>{{ t.conference }}</em>{% endif %} &middot; {{ t.location }} &middot; {{ t.date | date: "%b %Y" }}
      </div>
      {% if t.abstract %}<div class="talk-abstract"><em>{{ t.abstract }}</em></div>{% endif %}
      {% if t.slides %}
        <div class="talk-links mt-1">
          <a href="{{ t.slides | relative_url }}" target="_blank" rel="noopener">📄 Slides</a>
        </div>
      {% endif %}
    </div>
  {% endfor %}
{% endfor %}
{% else %}
<p><em>No presentations to display yet.</em></p>
{% endif %}

</div>