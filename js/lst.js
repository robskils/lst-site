(function () {
  'use strict';

  // ── Scroll-aware header ──────────────────────────────────────────────────
  var header = document.querySelector('header');
  if (header) {
    function onScroll() {
      if (window.scrollY > 60) {
        header.style.backgroundColor = 'oklch(0.22 0.04 170 / 0.96)';
        header.style.backdropFilter = 'blur(12px)';
        header.style.boxShadow = '0 1px 0 oklch(1 0 0 / 0.06)';
      } else {
        header.style.backgroundColor = '';
        header.style.backdropFilter = '';
        header.style.boxShadow = '';
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

  // ── Contact form → Cloudflare Worker ────────────────────────────────────
  var form = document.querySelector('form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var raw = Object.fromEntries(new FormData(form));
      var btn = form.querySelector('button[type="submit"]');
      var orig = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }

      // Map contact form fields to worker payload
      var payload = {
        business:   'lst',
        fullName:   raw.name        || '',
        email:      raw.email       || '',
        date:       raw.dates       || null,
        groupSize:  raw.party       || null,
        additional: [raw.interests, raw.message].filter(Boolean).join('\n\n') || null,
      };

      fetch('https://enquiries.lisbonsintratours.com/api/enquiry', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          form.innerHTML = '<p style="font-family:var(--font-serif);font-size:1.5rem;color:var(--color-gold)">Thank you. We\'ll be in touch within one working day.</p>';
        })
        .catch(function () {
          if (btn) { btn.disabled = false; btn.textContent = orig; }
          alert('Sorry, something went wrong. Please email us directly at hello@lisbonsintratours.com');
        });
    });
  }
})();
