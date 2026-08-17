/* Strings come from window.BK_T, set by each page. */
var T = window.BK_T || {};

/* ── Multi-step enquiry ───────────────────────────────────────────────────
   Three steps: the trip, how the day works, who you are. The party is four
   age counts rather than one number, because the bands decide both the entry
   ticket prices and the child seats that have to be in the vehicle.

   This registers before /js/lst-v10.js (which is deferred) and the form is
   marked data-multistep, so the site-wide single-page handler stands down. */
(function () {
  var DEDICATED_MAX = 8;   // above this the guide is not driving anyway
  var step = 1, chosen = [];

  function $(id) { return document.getElementById(id); }
  function n(id) { var v = parseInt(($(id) || {}).value, 10); return isNaN(v) || v < 0 ? 0 : v; }

  function party() {
    var c = { adults: n('p-adults'), youth: n('p-youth'), seniors: n('p-seniors'), children: n('p-children') };
    c.total = c.adults + c.youth + c.seniors + c.children;
    return c;
  }

  // Age boxes appear as the counts change and keep whatever was typed.
  function ages(kind, count, label, min, max) {
    var wrap = $('bk-ages'), box = $('ages-' + kind);
    if (!count) { if (box) box.parentNode.removeChild(box); return; }
    if (!box) { box = document.createElement('div'); box.id = 'ages-' + kind; wrap.appendChild(box); }
    var had = [].map.call(box.querySelectorAll('input'), function (i) { return i.value; });
    box.innerHTML = '<div class="bk-agelabel">' + label + T.agesWord + '</div>';
    for (var i = 1; i <= count; i++) {
      var row = document.createElement('div');
      row.className = 'bk-agerow';
      row.innerHTML = '<span>' + label + ' ' + i + '</span>';
      var inp = document.createElement('input');
      inp.type = 'number'; inp.min = min; inp.max = max; inp.placeholder = 'age';
      inp.id = 'age-' + kind + '-' + i; inp.value = had[i - 1] || '';
      row.appendChild(inp); box.appendChild(row);
    }
  }

  function recompute() {
    var c = party();
    ages('youth', c.youth, T.youthLabel, 6, 17);
    ages('child', c.children, T.childLabel, 0, 5);
    var bits = [];
    if (c.adults)   bits.push(c.adults + (c.adults === 1 ? T.adult : T.adults));
    if (c.youth)    bits.push(c.youth + T.youth);
    if (c.seniors)  bits.push(c.seniors + (c.seniors === 1 ? T.senior : T.seniors));
    if (c.children) bits.push(c.children + T.under6);
    $('bk-total').innerHTML = c.total
      ? '<b>' + c.total + (c.total === 1 ? T.guest : T.guests) + '</b> — ' + bits.join(', ')
      : T.noGuests;
    if (c.total) err('e-party', false);

    // The guide note is only true for a small group, so only show it then.
    var small = c.total > 0 && c.total <= DEDICATED_MAX;
    $('bk-guide-note').style.display = small ? '' : 'none';
    $('bk-upgrade').style.display    = small ? '' : 'none';
    if (!small && $('f-dedicated').checked) { $('f-dedicated').checked = false; $('bk-upgrade').classList.remove('is-on'); }
  }

  function collectAges() {
    var c = party(), out = [];
    for (var i = 1; i <= c.youth; i++)    out.push(($('age-youth-' + i) || {}).value || '?');
    for (var j = 1; j <= c.children; j++) out.push(($('age-child-' + j) || {}).value || '?');
    return out.length ? out.join(', ') : null;
  }

  function err(id, on) { var e = $(id); if (e) e.classList[on ? 'add' : 'remove']('is-on'); }

  function valid(s) {
    var ok = true;
    if (s === 1) {
      if (!$('f-dates').value) { err('e-date', true); ok = false; } else err('e-date', false);
      if (party().total < 1)   { err('e-party', true); ok = false; } else err('e-party', false);
      if (!chosen.length)      { err('e-tour', true); ok = false; } else err('e-tour', false);
    }
    return ok;
  }

  // Kept because the markup still calls it from the old Continue buttons,
  // which are now hidden. Harmless, and removing it would mean touching four
  // pages of markup for no gain.
  window.bkGo = function (to) {
    if (to > step && !valid(step)) return;
    step = to;
    [1, 2, 3].forEach(function (i) {
      $('bk-s' + i).classList.toggle('is-on', i === to);
      var d = $('bk-d' + i);
      d.classList.toggle('is-on', i === to);
      d.classList.toggle('is-done', i < to);
    });
    $('bk-stepname').textContent = T.steps[to - 1];
    if (to === 3) summary();
    var f = $('lst-book');
    if (f) window.scrollTo({ top: f.getBoundingClientRect().top + window.pageYOffset - 100, behavior: 'smooth' });
  };

  function summary() {
    var c = party(), bits = [];
    if (c.adults)   bits.push(c.adults + (c.adults === 1 ? T.adult : T.adults));
    if (c.youth)    bits.push(c.youth + T.youth617);
    if (c.seniors)  bits.push(c.seniors + (c.seniors === 1 ? T.senior : T.seniors) + ' (65+)');
    if (c.children) bits.push(c.children + T.under6);
    var d = $('f-dates').value, rows = [];
    if (chosen.length) rows.push([T.sumTours, chosen.join(', ')]);
    if (d) rows.push([T.sumDate, new Date(d + 'T12:00:00').toLocaleDateString(T.locale, { day:'numeric', month:'long', year:'numeric' })]);
    if (c.total) rows.push([T.sumGuests, c.total + ' — ' + bits.join(', ')]);
    if ($('f-dedicated').checked) rows.push([T.sumGuide, T.sumGuideVal]);
    $('bk-summary').innerHTML = rows.map(function (r) {
      return '<div><span>' + r[0] + '</span><span>' + r[1].replace(/</g, '&lt;') + '</span></div>';
    }).join('');
  }

  // Tours are multi-select: people rarely want exactly one.
  function wireTours() {
    [].forEach.call(document.querySelectorAll('.tour-pill-btn'), function (b) {
      b.addEventListener('click', function () {
        var name = b.getAttribute('data-tour');
        var at = chosen.indexOf(name);
        if (at === -1) { chosen.push(name); b.classList.add('is-active'); }
        else { chosen.splice(at, 1); b.classList.remove('is-active'); }
        $('tour-hidden').value = chosen.join(', ');
        if (chosen.length) err('e-tour', false);
        summary();
      });
    });
  }

  function init() {
    ['p-adults', 'p-youth', 'p-seniors', 'p-children'].forEach(function (id) {
      var el = $(id); if (el) el.addEventListener('input', recompute);
    });
    $('bk-ages').addEventListener('input', function () {});
    $('f-dedicated').addEventListener('change', function () {
      $('bk-upgrade').classList.toggle('is-on', this.checked);
    });
    wireTours();
    recompute();
    // No steps to move between, so the summary keeps itself current.
    ['f-dates', 'f-dedicated'].forEach(function (id) {
      var el = $(id); if (el) el.addEventListener('change', summary);
    });
    ['p-adults', 'p-youth', 'p-seniors', 'p-children'].forEach(function (id) {
      var el = $(id); if (el) el.addEventListener('input', summary);
    });
    summary();

    $('lst-book').addEventListener('submit', function (e) {
      e.preventDefault();
      e.stopImmediatePropagation();          // the site-wide handler must not also fire
      var name = $('f-name').value.trim(), email = $('f-email').value.trim(), ok = true;
      // Everything is on one page now, so everything is checked here.
      if (!$('f-dates').value) { err('e-date', true); ok = false; } else err('e-date', false);
      if (party().total < 1)   { err('e-party', true); ok = false; } else err('e-party', false);
      if (!chosen.length)      { err('e-tour', true); ok = false; } else err('e-tour', false);
      if (!name) { err('e-name', true); ok = false; } else err('e-name', false);
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { err('e-email', true); ok = false; } else err('e-email', false);
      if (!ok) {
        var first = document.querySelector('.bk-err.is-on');
        if (first) first.scrollIntoView({ behavior:'smooth', block:'center' });
        return;
      }

      var btn = $('lst-book').querySelector('button[type="submit"]');
      var orig = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = T.sending; }

      var c = party();
      var payload = {
        business:       'lst',
        enquiryType:    'tour',
        fullName:       name,
        email:          email,
        date:           $('f-dates').value || null,
        groupSize:      c.total || null,
        adultsCount:    c.adults,
        youthCount:     c.youth,
        seniorsCount:   c.seniors,
        infantsCount:   c.children,
        childrenAges:   collectAges(),
        phone:          $('f-phone').value || null,
        hasWhatsApp:    $('f-whatsapp').checked,
        tour:           chosen.join(', ') || null,
        dedicatedGuide: $('f-dedicated').checked ? 1 : 0,
        /* We never handle ticket money: collected for entry tickets it counts
           as our revenue and is taxed as though we kept it. Clients buy their
           own and we send them the links after they book, so the form does not
           ask about it at all. */
        ticketsRequired: 0,
        stayingAt:      $('f-pickup').value || null,
        additional:     $('f-message').value || null,
      };

      fetch('https://enquiries.lisbonsintratours.com/api/enquiry', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload),
      }).then(function (r) {
        if (!r.ok) throw new Error(r.status);
        window.location.href = T.thanks;
      }).catch(function () {
        if (btn) { btn.disabled = false; btn.textContent = orig; }
        alert(T.failed);
      });
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
