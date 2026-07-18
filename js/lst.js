(function () {
  'use strict';

  // ── Scroll-aware header ──────────────────────────────────────────────────
  var header = document.querySelector('header');
  var sintraSpan = document.querySelector('header a[aria-label] span');
  if (header) {
    function onScroll() {
      if (window.scrollY > 60) {
        header.style.backgroundColor = 'oklch(0.22 0.04 170 / 0.96)';
        header.style.backdropFilter = 'blur(12px)';
        header.style.boxShadow = '0 1px 0 oklch(1 0 0 / 0.06)';
        if (sintraSpan) sintraSpan.style.color = 'var(--color-gold)';
      } else {
        header.style.backgroundColor = 'oklch(0.18 0.04 170 / 0.35)';
        header.style.backdropFilter = 'blur(4px)';
        header.style.boxShadow = '';
        if (sintraSpan) sintraSpan.style.color = 'var(--color-ivory)';
      }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // ── Mobile nav ───────────────────────────────────────────────────────────
  var menuBtn = document.querySelector('button[aria-label="Toggle menu"]');
  if (menuBtn && header) {
    // Build mobile menu from desktop nav links
    var desktopNav = header.querySelector('nav');
    var mobileMenu = document.createElement('div');
    mobileMenu.id = 'mobile-menu';
    mobileMenu.setAttribute('aria-hidden', 'true');
    mobileMenu.style.cssText = [
      'display:none',
      'position:fixed',
      'inset:0',
      'z-index:40',
      'background:oklch(0.18 0.04 170)',
      'flex-direction:column',
      'align-items:center',
      'justify-content:center',
      'gap:2rem',
      'padding:2rem',
    ].join(';');

    if (desktopNav) {
      var links = desktopNav.querySelectorAll('a');
      links.forEach(function (a) {
        var link = document.createElement('a');
        link.href = a.href;
        link.textContent = a.textContent;
        link.style.cssText = 'font-size:1.5rem;letter-spacing:0.2em;text-transform:uppercase;color:var(--color-ivory);text-decoration:none;font-family:var(--font-serif)';
        if (a.getAttribute('aria-current') === 'page') {
          link.style.color = 'var(--color-gold)';
        }
        mobileMenu.appendChild(link);
      });
    }

    // Close button inside menu
    var closeBtn = document.createElement('button');
    closeBtn.textContent = '✕';
    closeBtn.setAttribute('aria-label', 'Close menu');
    closeBtn.style.cssText = 'position:absolute;top:1.5rem;right:1.5rem;background:none;border:none;color:var(--color-ivory);font-size:1.5rem;cursor:pointer;line-height:1';
    mobileMenu.appendChild(closeBtn);

    document.body.appendChild(mobileMenu);

    function openMenu() {
      mobileMenu.style.display = 'flex';
      mobileMenu.setAttribute('aria-hidden', 'false');
      menuBtn.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
    }
    function closeMenu() {
      mobileMenu.style.display = 'none';
      mobileMenu.setAttribute('aria-hidden', 'true');
      menuBtn.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    }

    menuBtn.addEventListener('click', openMenu);
    closeBtn.addEventListener('click', closeMenu);
    mobileMenu.addEventListener('click', function (e) {
      if (e.target === mobileMenu) closeMenu();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMenu();
    });
  }

  // ── Fade-up animations (IntersectionObserver) ────────────────────────────
  var fadeEls = document.querySelectorAll('.fade-up');
  if (fadeEls.length && 'IntersectionObserver' in window) {
    // Elements in the hero (above the fold) should be visible immediately
    fadeEls.forEach(function (el) {
      var rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight) {
        el.classList.add('is-visible');
      }
    });

    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    fadeEls.forEach(function (el) {
      if (!el.classList.contains('is-visible')) obs.observe(el);
    });
  } else {
    // No observer support — show everything
    fadeEls.forEach(function (el) { el.classList.add('is-visible'); });
  }

  // ── Children section (contact form) ─────────────────────────────────────
  var hasChildrenCb = document.getElementById('f-has-children');
  var childrenSection = document.getElementById('children-section');
  var childCountSel = document.getElementById('f-child-count');
  var childAgesWrap = document.getElementById('child-ages-wrap');

  function buildChildAgeInputs(count) {
    if (!childAgesWrap) return;
    // preserve existing ages
    var oldAges = [];
    childAgesWrap.querySelectorAll('input').forEach(function(inp) { oldAges.push(inp.value); });
    childAgesWrap.innerHTML = '';
    for (var i = 1; i <= count; i++) {
      var row = document.createElement('div');
      row.style.cssText = 'display:flex;align-items:center;gap:8px;margin-bottom:6px';
      var lbl = document.createElement('span');
      lbl.textContent = 'Child ' + i;
      lbl.style.cssText = 'font-size:13px;color:oklch(0.52 0.015 85);width:56px;flex-shrink:0';
      var input = document.createElement('input');
      input.type = 'number';
      input.min = '0';
      input.max = '17';
      input.placeholder = 'age';
      input.id = 'child-age-' + i;
      input.value = oldAges[i - 1] || '';
      input.style.cssText = 'width:80px;padding:5px 8px;border:1.5px solid oklch(0.22 0.04 170 / 0.22);border-radius:4px;font-size:14px;font-family:var(--font-sans);background:oklch(0.985 0.004 85);outline:none;box-sizing:border-box';
      var badge = document.createElement('span');
      badge.textContent = '🪑 car seat';
      badge.style.cssText = 'font-size:12px;color:#e07b00;background:#fff3cd;padding:2px 7px;border-radius:10px;white-space:nowrap;display:' + (input.value !== '' && parseInt(input.value) < 12 ? 'inline' : 'none');
      input.addEventListener('input', function(b) {
        return function() {
          var age = parseInt(this.value);
          b.style.display = (!isNaN(age) && age < 12) ? 'inline' : 'none';
        };
      }(badge));
      row.appendChild(lbl);
      row.appendChild(input);
      row.appendChild(badge);
      childAgesWrap.appendChild(row);
    }
  }

  function collectChildrenAges() {
    if (!hasChildrenCb || !hasChildrenCb.checked) return null;
    var count = parseInt(childCountSel ? childCountSel.value : 0) || 0;
    var ages = [];
    for (var i = 1; i <= count; i++) {
      var inp = document.getElementById('child-age-' + i);
      ages.push(inp && inp.value !== '' ? inp.value : '?');
    }
    return ages.length ? ages.join(', ') : null;
  }

  if (childCountSel) {
    for (var c = 1; c <= 10; c++) {
      var opt = document.createElement('option');
      opt.value = c; opt.textContent = c;
      childCountSel.appendChild(opt);
    }
    buildChildAgeInputs(1);
    childCountSel.addEventListener('change', function() {
      buildChildAgeInputs(parseInt(this.value));
    });
  }

  if (hasChildrenCb && childrenSection) {
    hasChildrenCb.addEventListener('change', function() {
      childrenSection.style.display = this.checked ? 'block' : 'none';
    });
  }

  // ── Tour pill selector ───────────────────────────────────────────────────
  var pillBtns = document.querySelectorAll('.tour-pill-btn');
  var tourHidden = document.getElementById('tour-hidden');
  if (pillBtns.length && tourHidden) {
    var selected = [];
    pillBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var tour = btn.getAttribute('data-tour');
        var idx = selected.indexOf(tour);
        if (idx === -1) {
          selected.push(tour);
          btn.classList.add('is-selected');
        } else {
          selected.splice(idx, 1);
          btn.classList.remove('is-selected');
        }
        tourHidden.value = selected.join(', ');
      });
    });
  }

  // ── Language switcher ────────────────────────────────────────────────────
  (function () {
    if (!header) return;
    var path = window.location.pathname;
    var lang = 'en';
    var canonical = path;
    if (path === '/pt/' || path === '/pt') { lang = 'pt'; canonical = '/'; }
    else if (path.startsWith('/pt/')) { lang = 'pt'; canonical = path.slice(3); }
    else if (path === '/es/' || path === '/es') { lang = 'es'; canonical = '/'; }
    else if (path.startsWith('/es/')) { lang = 'es'; canonical = path.slice(3); }
    else if (path === '/fr/' || path === '/fr') { lang = 'fr'; canonical = '/'; }
    else if (path.startsWith('/fr/')) { lang = 'fr'; canonical = path.slice(3); }
    if (canonical !== '/' && !canonical.endsWith('/')) canonical += '/';

    var langs = [
      { code: 'en', label: 'EN', href: canonical },
      { code: 'pt', label: 'PT', href: '/pt' + canonical },
      { code: 'es', label: 'ES', href: '/es' + canonical },
      { code: 'fr', label: 'FR', href: '/fr' + canonical },
    ];

    var existing = null;
    var headerLinks = header.querySelectorAll('a');
    for (var i = 0; i < headerLinks.length; i++) {
      var txt = headerLinks[i].textContent.trim();
      if (/^(EN|PT|ES|FR)$/.test(txt) && headerLinks[i].style.border) {
        existing = headerLinks[i]; break;
      }
    }
    if (!existing) return;

    var wrap = document.createElement('span');
    wrap.style.cssText = 'display:inline-flex;align-items:center;gap:3px;margin-left:0.5rem';
    var base = 'padding:0.2rem 0.42rem;border:1px solid rgba(245,240,232,0.35);border-radius:3px;font-size:0.65rem;letter-spacing:0.14em;text-decoration:none;font-family:var(--font-sans)';
    langs.forEach(function (l) {
      var a = document.createElement('a');
      a.href = l.href;
      a.textContent = l.label;
      a.style.cssText = base + ';color:' + (l.code === lang ? 'rgba(245,240,232,0.95);background:rgba(245,240,232,0.1)' : 'rgba(245,240,232,0.42)');
      if (l.code !== lang) {
        a.addEventListener('mouseover', function () { this.style.color = 'rgba(245,240,232,0.75)'; });
        a.addEventListener('mouseout',  function () { this.style.color = 'rgba(245,240,232,0.42)'; });
      }
      wrap.appendChild(a);
    });
    existing.parentNode.replaceChild(wrap, existing);
  }());

  // ── Contact form → Cloudflare Worker ────────────────────────────────────
  var form = document.querySelector('form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var raw = Object.fromEntries(new FormData(form));
      var btn = form.querySelector('button[type="submit"]');
      var orig = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }

      var payload = {
        business:      'lst',
        fullName:      raw.name     || '',
        email:         raw.email    || '',
        date:          raw.dates    || null,
        groupSize:     parseInt(raw.party) || null,
        childrenAges:  collectChildrenAges(),
        phone:         raw.phone    || null,
        hasWhatsApp:   document.getElementById('f-whatsapp') ? document.getElementById('f-whatsapp').checked : false,
        tour:          raw.tour     || null,
        additional:    [raw.pickup, raw.message].filter(Boolean).join('\n\n') || null,
      };

      fetch('https://enquiries.lisbonsintratours.com/api/enquiry', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          window.location.href = '/thank-you/';
        })
        .catch(function () {
          if (btn) { btn.disabled = false; btn.textContent = orig; }
          alert('Sorry, something went wrong. Please email us directly at hello@lisbonsintratours.com');
        });
    });
  }
})();
