#!/usr/bin/env python3
"""
notrack.py - keeps Robin's own visits out of the analytics.

Robin, 2026-11-27: "I don't want my visits to register!"

A tiny script runs first in <head> and sets window.LST_TRACK from the
localStorage key "lst_notrack". Visiting /notrack/ sets the key (that page is
never counted itself); /notrack/?undo=1 clears it. Google Analytics
(G-3T9Z2G3GS1) and Visitor Tracking are injected only when LST_TRACK allows.

This site's HTML is the source (no full build), so this script rewrites every
page in place and is safe to run again: it only touches the raw, ungated
snippets. The blog generator (pull_posts.py) and make_landing.py copy their
<head> from an existing post, so new pages inherit the gate.

Run: python3 _build/notrack.py
"""

import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRACK_GATE = ("<script>window.LST_TRACK=(function(){try{var k='lst_notrack',p=location.pathname;"
              "if(p==='/notrack/'){if(/[?&]undo=1/.test(location.search))localStorage.removeItem(k);"
              "else localStorage.setItem(k,'1');return false;}"
              "return localStorage.getItem(k)!=='1';}catch(e){return true;}})();</script>")

RAW_GTAG = ('<script async src="https://www.googletagmanager.com/gtag/js?id=G-3T9Z2G3GS1"></script>'
            '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
            'gtag("js",new Date());gtag("config","G-3T9Z2G3GS1");</script>')
GATED_GTAG = ('<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
              'if(window.LST_TRACK){var ga=document.createElement("script");ga.async=true;'
              'ga.src="https://www.googletagmanager.com/gtag/js?id=G-3T9Z2G3GS1";document.head.appendChild(ga);'
              'gtag("js",new Date());gtag("config","G-3T9Z2G3GS1");}</script>')

RAW_VT = ('<script async defer src="https://app.visitortracking.com/assets/js/tracer.js"></script>'
          '<script>function init_tracer(){new Tracer({websiteId:"96ad94ee-3304-4122-91a9-7b013c24c493",async:true,debug:false});}</script>')
GATED_VT = ('<script>function init_tracer(){new Tracer({websiteId:"96ad94ee-3304-4122-91a9-7b013c24c493",async:true,debug:false});}'
            'if(window.LST_TRACK){var vt=document.createElement("script");vt.async=true;vt.defer=true;'
            'vt.src="https://app.visitortracking.com/assets/js/tracer.js";document.head.appendChild(vt);}</script>')


def gate(html: str) -> str:
    html = html.replace(RAW_GTAG, GATED_GTAG).replace(RAW_VT, GATED_VT)
    if ('LST_TRACK' in html) and TRACK_GATE not in html:
        # First thing in <head>, before any tracker.
        html = re.sub(r'<head>', '<head>' + TRACK_GATE, html, count=1)
    return html


NOTRACK_MAIN = """<main class="flex-1 flex items-center justify-center" style="min-height:100vh"><div class="container-page py-32" style="max-width:44rem">
<div id="nt-off">
<h1 class="display text-5xl md:text-6xl" style="font-family:var(--font-serif);color:var(--color-primary)">Not counted</h1>
<p class="mt-8 leading-relaxed" style="font-size:1.2rem;color:var(--color-primary)">This browser is no longer counted on lisbonsintratours.com. Google Analytics and Visitor Tracking will not load here, so your own visits stay out of the numbers.</p>
<p class="mt-5 leading-relaxed" style="font-size:1.2rem;color:var(--color-primary)">Open this page once in every browser and on every device you use. Clearing this browser's site data switches counting back on.</p>
<div class="flex flex-wrap gap-4" style="margin-top:2.5rem"><a href="/" class="btn-ink">Go to the home page</a><a href="/notrack/?undo=1" class="nt-alt">Count this browser again</a></div>
</div>
<div id="nt-on" hidden>
<h1 class="display text-5xl md:text-6xl" style="font-family:var(--font-serif);color:var(--color-primary)">Counted again</h1>
<p class="mt-8 leading-relaxed" style="font-size:1.2rem;color:var(--color-primary)">This browser is counted again on lisbonsintratours.com. Google Analytics and Visitor Tracking load as normal from the next page you open.</p>
<div class="flex flex-wrap gap-4" style="margin-top:2.5rem"><a href="/notrack/" class="btn-ink">Stop counting this browser</a><a href="/" class="nt-alt">Go to the home page</a></div>
</div>
<script>if(/[?&]undo=1/.test(location.search)){document.getElementById('nt-off').hidden=true;document.getElementById('nt-on').hidden=false;}</script>
</div></main>"""

NOTRACK_STYLE = ("<style>header{background-color:oklch(0.22 0.04 170)!important}"
                 ".nt-alt{display:inline-flex;align-items:center;letter-spacing:0.16em;"
                 "text-transform:uppercase;font-weight:500;padding:0.75rem 1.25rem;"
                 "border:1px solid var(--color-primary);color:var(--color-primary);text-decoration:none}"
                 "main .btn-ink,.nt-alt{font-size:1rem}"
                 ".nt-alt:hover{background:var(--color-primary);color:var(--color-ivory)}</style>")


def notrack_page():
    # The site's own shell: head, header and footer from the thank-you page.
    s = open(os.path.join(ROOT, 'thank-you', 'index.html'), encoding='utf-8').read()
    s = s.replace('https://lisbonsintratours.com/thank-you/', 'https://lisbonsintratours.com/notrack/')
    s = re.sub(r'<title>.*?</title>', '<title>Not counted - Lisbon Sintra Tours</title>', s, count=1)
    s = re.sub(r'<meta name="description"[^>]*/>', '', s, count=1)
    s = re.sub(r'<meta property="og:[^>]*/>|<meta name="twitter:image"[^>]*/>', '', s)
    s = re.sub(r'<link rel="alternate"[^>]*/>|<link rel="alternate" ', '', s)
    s = s.replace('</head>', NOTRACK_STYLE + '</head>', 1)
    s = re.sub(r'<main.*?</main>', lambda m: NOTRACK_MAIN, s, count=1, flags=re.S)
    assert 'name="robots" content="noindex"' in s
    os.makedirs(os.path.join(ROOT, 'notrack'), exist_ok=True)
    with open(os.path.join(ROOT, 'notrack', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(s)


def main():
    changed = 0
    for path in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
        if '/.git/' in path or '/notrack/' in path:
            continue
        old = open(path, encoding='utf-8').read()
        new = gate(old)
        if new != old:
            open(path, 'w', encoding='utf-8').write(new)
            changed += 1
    notrack_page()
    print(f'gated {changed} pages; wrote notrack/index.html')


if __name__ == '__main__':
    main()
