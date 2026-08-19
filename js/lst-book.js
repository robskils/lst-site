/* Strings come from window.BK_T, set by each page. */
var T = window.BK_T || {};

/* ── Multi-step enquiry ───────────────────────────────────────────────────
   Three steps: the trip, how the day works, who you are. The party is four
   age counts rather than one number, because the bands decide both the entry
   ticket prices and the child seats that have to be in the vehicle.

   This registers before /js/lst-v10.js (which is deferred) and the form is
   marked data-multistep, so the site-wide single-page handler stands down. */
(function () {
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
    /* The guide-and-driver note and the dedicated-guide upgrade have both come
       off the form. Explaining the arrangement to somebody who has not spoken
       to anybody yet, in a box on a form, asked them to weigh something they
       had no way to ask about. Vitor covers it in his first reply. */
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
    /* Step 2 has gone: it held the guide-and-driver note and the dedicated
       guide upgrade, and with both moved into Vitor's first reply there was
       nothing left in it but a rule and a gap. Nothing here may assume a step
       or a dot is on the page. */
    [1, 2, 3].forEach(function (i) {
      var el = $('bk-s' + i);
      if (el) el.classList.toggle('is-on', i === to);
      var d = $('bk-d' + i);
      if (!d) return;
      d.classList.toggle('is-on', i === to);
      d.classList.toggle('is-done', i < to);
    });
    var name = $('bk-stepname');
    if (name) name.textContent = T.steps[to - 1] || '';
    if (to === 3) summary();
    var f = $('lst-book');
    if (f) window.scrollTo({ top: f.getBoundingClientRect().top + window.pageYOffset - 100, behavior: 'smooth' });
  };

  // Say the chosen date back in words. The picker's own format follows the
  // visitor's browser, so 02/10 reads as October in London and February in
  // New York — this removes the doubt without overriding anything.
  function echoDate() {
    var el = $('date-said'), v = $('f-dates') ? $('f-dates').value : '';
    if (!el) return;
    if (!v) { el.textContent = ''; return; }
    var d = new Date(v + 'T12:00:00');
    el.textContent = isNaN(d) ? '' : d.toLocaleDateString(T.locale || 'en-GB',
      { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  }

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
    var ex = [];
    document.querySelectorAll('[data-extra]').forEach(function (b) {
      if (b.checked) ex.push(b.parentNode.querySelector('b').textContent);
    });
    if (ex.length) rows.push([T.sumExtras || 'Also', ex.join(', ')]);
    $('bk-summary').innerHTML = rows.map(function (r) {
      return '<div><span>' + r[0] + '</span><span>' + r[1].replace(/</g, '&lt;') + '</span></div>';
    }).join('');
  }

  // Tours are multi-select: people rarely want exactly one.
  /* Which add-ons are ticked. */
  function chosenExtras() {
    var out = [];
    var boxes = document.querySelectorAll('[data-extra]');
    for (var i = 0; i < boxes.length; i++) {
      if (boxes[i].checked) out.push(boxes[i].getAttribute('data-extra'));
    }
    return out;
  }

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
    echoDate();
      });
    });
  }

  /* ── THE DATE PICKER ──────────────────────────────────────────────────────
     A native <input type="date"> starts its week on whichever day the visitor's
     own browser locale says, so an American visitor sees a calendar beginning on
     Sunday. Our weeks start on Monday, here as everywhere else, and that is not
     something the native control can be told. So the field gets its own.

     The original input stays in the page, hidden. Everything downstream reads
     f-dates.value and listens for its change event, and none of it has to know
     the calendar in front of it was replaced. Month and weekday names come from
     the page's own locale, so pt, fr and es get their own words for free. */

  function pad(v) { return (v < 10 ? '0' : '') + v; }
  function ymd(d) { return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }

  // Parsed at midday so a timezone west of UTC cannot roll the date back a day.
  function parseYmd(s) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(s || '')) return null;
    var d = new Date(s + 'T12:00:00');
    return isNaN(d) ? null : d;
  }

  var DP_CSS = [
    '.dp{position:relative}',
    '.dp-field{width:100%;text-align:left;cursor:pointer;font:inherit}',
    '.dp-field[data-empty="1"]{color:oklch(0.55 0.02 170)}',
    '.dp-pop{position:absolute;z-index:60;top:calc(100% + 6px);left:0;width:322px;max-width:100%;',
      'background:#fff;border:1px solid oklch(0.88 0.01 85);border-radius:6px;padding:14px;',
      'box-shadow:0 12px 34px rgba(0,0,0,.14);display:none}',
    '.dp-pop.is-on{display:block}',
    '.dp-head{display:flex;align-items:center;gap:8px;margin-bottom:10px}',
    '.dp-title{flex:1;text-align:center;font-family:var(--font-serif),Georgia,serif;font-size:1.05rem;',
      'color:oklch(0.28 0.03 170)}',
    /* Only the first letter: capitalize would give "Agosto De 2026". */
    '.dp-title::first-letter{text-transform:uppercase}',
    '.dp-nav{width:34px;height:34px;border:1px solid oklch(0.9 0.01 85);border-radius:4px;background:#fff;',
      'cursor:pointer;font-size:1rem;line-height:1;color:oklch(0.4 0.02 170)}',
    '.dp-nav:hover:not(:disabled){border-color:var(--color-gold,#b8932a);color:var(--color-gold,#b8932a)}',
    '.dp-nav:disabled{opacity:.32;cursor:default}',
    '.dp-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:2px}',
    '.dp-dow{text-align:center;font-size:0.68rem;letter-spacing:.08em;text-transform:uppercase;',
      'color:oklch(0.55 0.02 170);padding:4px 0 6px}',
    '.dp-dow.dp-we{color:var(--color-gold,#b8932a)}',
    '.dp-day{height:40px;border:none;background:none;border-radius:4px;cursor:pointer;font:inherit;',
      'font-size:0.92rem;color:oklch(0.28 0.03 170)}',
    '.dp-day:hover:not(:disabled){background:oklch(0.95 0.01 85)}',
    '.dp-day:disabled{color:oklch(0.82 0.01 170);cursor:default}',
    '.dp-day.is-today{box-shadow:inset 0 0 0 1px var(--color-gold,#b8932a)}',
    '.dp-day.is-on{background:oklch(0.28 0.03 170);color:#fff}',
    '.dp-empty{height:40px}',
    '@media (max-width:420px){.dp-pop{width:100%}.dp-day,.dp-empty{height:44px}}',
  ].join('');

  function buildPicker() {
    var input = $('f-dates');
    if (!input || input.getAttribute('data-dp') === '1') return;
    input.setAttribute('data-dp', '1');

    if (!document.getElementById('dp-css')) {
      var st = document.createElement('style');
      st.id = 'dp-css'; st.textContent = DP_CSS;
      document.head.appendChild(st);
    }

    var loc = T.locale || document.documentElement.lang || 'en-GB';
    var today = new Date(); today.setHours(12, 0, 0, 0);

    var wrap = document.createElement('div');
    wrap.className = 'dp';
    input.parentNode.insertBefore(wrap, input);
    input.style.display = 'none';
    wrap.appendChild(input);

    var field = document.createElement('button');
    field.type = 'button';
    field.className = 'lst-input dp-field';
    field.setAttribute('aria-haspopup', 'dialog');
    wrap.appendChild(field);

    var pop = document.createElement('div');
    pop.className = 'dp-pop';
    pop.setAttribute('role', 'dialog');
    wrap.appendChild(pop);

    // Weekday initials taken off a known Monday, so the order is ours and the
    // words are the visitor's.
    var MONDAY = new Date(2024, 0, 1);   // a Monday
    var dows = [];
    for (var i = 0; i < 7; i++) {
      var d = new Date(MONDAY); d.setDate(MONDAY.getDate() + i);
      /* Trimmed to three letters: "short" is already Mon and lun, but in
         Portuguese it is the whole word - segunda, terça - which will not fit a
         seventh of the calendar. Three letters is the usual abbreviation there
         anyway, and leaves the short locales untouched. */
      dows.push(d.toLocaleDateString(loc, { weekday: 'short' }).replace(/\.$/, '').slice(0, 3));
    }

    var view = null;      // month on show
    var picked = null;    // chosen day

    function label() {
      if (!picked) {
        field.setAttribute('data-empty', '1');
        field.textContent = T.datePick || 'Choose a date';
        return;
      }
      field.removeAttribute('data-empty');
      field.textContent = picked.toLocaleDateString(loc,
        { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
    }

    function draw() {
      var y = view.getFullYear(), m = view.getMonth();
      var first = new Date(y, m, 1);
      // Monday-first: JavaScript counts Sunday as 0, so shift the week round.
      var lead = (first.getDay() + 6) % 7;
      var days = new Date(y, m + 1, 0).getDate();
      var atStart = y === today.getFullYear() && m === today.getMonth();

      var html = '<div class="dp-head">'
        + '<button type="button" class="dp-nav" data-go="-1" aria-label="Previous month"'
        + (atStart ? ' disabled' : '') + '>&#8249;</button>'
        + '<span class="dp-title">' + first.toLocaleDateString(loc, { month: 'long', year: 'numeric' }) + '</span>'
        + '<button type="button" class="dp-nav" data-go="1" aria-label="Next month">&#8250;</button>'
        + '</div><div class="dp-grid">';

      for (var i = 0; i < 7; i++) {
        html += '<div class="dp-dow' + (i > 4 ? ' dp-we' : '') + '">' + dows[i] + '</div>';
      }
      for (var b = 0; b < lead; b++) html += '<div class="dp-empty"></div>';
      for (var day = 1; day <= days; day++) {
        var cell = new Date(y, m, day, 12);
        var past = cell < today;
        var cls = 'dp-day';
        if (ymd(cell) === ymd(today)) cls += ' is-today';
        if (picked && ymd(cell) === ymd(picked)) cls += ' is-on';
        html += '<button type="button" class="' + cls + '" data-d="' + ymd(cell) + '"'
             + (past ? ' disabled' : '') + '>' + day + '</button>';
      }
      pop.innerHTML = html + '</div>';
    }

    function open() {
      view = new Date(picked || today); view.setDate(1);
      draw();
      pop.classList.add('is-on');
    }
    function close() { pop.classList.remove('is-on'); }

    field.addEventListener('click', function () {
      if (pop.classList.contains('is-on')) close(); else open();
    });

    pop.addEventListener('click', function (e) {
      var nav = e.target.closest ? e.target.closest('.dp-nav') : null;
      if (nav) {
        view.setMonth(view.getMonth() + parseInt(nav.getAttribute('data-go'), 10));
        draw();
        return;
      }
      var cell = e.target.closest ? e.target.closest('.dp-day') : null;
      if (!cell || cell.disabled) return;
      picked = parseYmd(cell.getAttribute('data-d'));
      input.value = cell.getAttribute('data-d');
      label();
      close();
      // The summary, the validation and the payload all hang off this event.
      input.dispatchEvent(new Event('change', { bubbles: true }));
    });

    document.addEventListener('click', function (e) {
      if (!wrap.contains(e.target)) close();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });

    // Honour anything already in the field, in case the browser restored it.
    picked = parseYmd(input.value);
    label();
  }

  function init() {
    buildPicker();
    // Ticking one changes the summary, so it has to redraw.
    document.querySelectorAll('[data-extra]').forEach(function (b) {
      b.addEventListener('change', function () { summary(); });
    });

    ['p-adults', 'p-youth', 'p-seniors', 'p-children'].forEach(function (id) {
      var el = $(id); if (el) el.addEventListener('input', recompute);
    });
    $('bk-ages').addEventListener('input', function () {});
    wireTours();
    recompute();
    // No steps to move between, so the summary keeps itself current.
    ['f-dates'].forEach(function (id) {
      var el = $(id); if (el) el.addEventListener('change', function () { summary(); echoDate(); });
    });
    ['p-adults', 'p-youth', 'p-seniors', 'p-children'].forEach(function (id) {
      var el = $(id); if (!el) return;
      el.addEventListener('input', summary);

      /* The 0 is a placeholder, and a placeholder stays put until you type -
         so clicking into the box left a cursor blinking beside a nought. It is
         taken away while the box has focus and put back when you leave, and a
         0 somebody typed is cleared too, so typing 2 gives 2 and not 02. */
      el.addEventListener('focus', function () {
        this.dataset.ph = this.dataset.ph || this.getAttribute('placeholder') || '';
        this.setAttribute('placeholder', '');
        if (this.value === '0') { this.value = ''; recompute(); summary(); }
      });
      el.addEventListener('blur', function () {
        if (this.dataset.ph !== undefined) this.setAttribute('placeholder', this.dataset.ph);
      });
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
        /* Add-ons, ticked on the form. Sent by key rather than by label so the
           four language versions all arrive as the same three words. */
        extras:         chosenExtras(),
        childrenAges:   collectAges(),
        phone:          $('f-phone').value || null,
        hasWhatsApp:    $('f-whatsapp').checked,
        tour:           chosen.join(', ') || null,
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
