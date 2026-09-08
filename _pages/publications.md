---
layout: page
permalink: /publications/
title: Publications
description: Publications in computational materials science and thermal transport.
nav: true
nav_order: 2
---

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
    <button class="pub-filter active" aria-pressed="true" data-filter="all">All <span class="count"></span></button>
    <button class="pub-filter" aria-pressed="false" data-filter="role-first">First author <span class="count"></span></button>
    <button class="pub-filter" aria-pressed="false" data-filter="role-cofirst">Co-first author <span class="count"></span></button>
    <button class="pub-filter" aria-pressed="false" data-filter="role-corresponding">Corresponding author <span class="count"></span></button>
    <button class="pub-filter" aria-pressed="false" data-filter="role-collaborator">Co-author <span class="count"></span></button>
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
          if (counts[f] === 0 && f !== 'all') { btn.classList.add('empty'); btn.disabled = true; }
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
          document.querySelectorAll('.pub-filter').forEach(function (b) { b.classList.remove('active'); b.setAttribute('aria-pressed', 'false'); });
          btn.classList.add('active');
          btn.setAttribute('aria-pressed', 'true');
          applyFilter(btn.getAttribute('data-filter'));
        });
      });
    });
  })();
</script>
