#!/usr/bin/env python3
"""
make_landing.py - the large-group landing pages.

Robin, 16 November 2026: "let's add the missing landing pages you mention.
And let's redesign the homepage a bit, to give more emphasis on the links to
those pages, and the emphasis on large group stuff."

WHY THESE PAGES EXIST. The business changed: groups of seven and up, anything
smaller handed to a guide. The site still sold "private, unhurried journeys"
to couples and said, on the About page, "never a coach" - which is now the
opposite of the job. Somebody searching for a coach for forty wedding guests
found nothing here that spoke to them.

WHY THEY ARE WRITTEN LIKE THIS. There are no photographs of a large group:
the only vehicle picture on the site is a seven-seat V-Class, which is the
wrong image for fifty people, and the shoot that would fix it may not happen.
So these pages earn their place on what they KNOW - the road up to Pena will
not take a full-size coach, every vehicle needs its own guide, the cost steps
rather than creeps - and they draw it rather than photograph it. Diagrams,
inline, in the site's own colours.

HOW IT BUILDS. The head, the nav and the footer are lifted from a page that
is already live, so they cannot go stale here. Only <main> is written.

ONE RULE WHEN EDITING THIS. The site's Tailwind is COMPILED - css/lst.css is
a finished stylesheet, not a runtime. A class nobody has used before does not
exist, and silently does nothing: h-[62vh] on the hero left a section with no
height at all, which looked like a broken image rather than a missing class.
Use classes that already appear elsewhere on the site, or inline the style.
"""

import os, re, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The blog post, because it is the only page carrying every head tag a new
# page needs - canonical, the Open Graph set, the alternates and a block of
# structured data. The about page has no structured data at all, so building
# from it silently produced pages with none.
SKELETON = os.path.join(ROOT, "blog", "large-private-group-tours-lisbon", "index.html")
SITE = "https://lisbonsintratours.com"


def esc(s):
    return (str(s or "").replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


# ── the drawings ──────────────────────────────────────────────────────────
def svg_ladder():
    """What party size means in vehicles. The whole pricing story in one look."""
    rows = [("1 to 7", 1, "Mercedes V-Class", 1), ("8 to 15", 1, "Sprinter van", 1),
            ("16 to 22", 1, "Midi-coach", 1), ("23 to 44", 2, "Two vehicles", 2),
            ("45 to 66", 3, "Three vehicles", 3), ("67 to 88", 4, "Four vehicles", 4)]
    out = ['<svg viewBox="0 0 680 330" role="img" aria-label="How party size decides the number of vehicles and guides" class="w-full h-auto">']
    out.append('<style>.lb{font:500 13px Inter,sans-serif;fill:currentColor}'
               '.ls{font:13px Inter,sans-serif;fill:currentColor;opacity:.62}'
               '.lv{fill:var(--color-gold)}.lg{fill:currentColor;opacity:.3}</style>')
    y = 18
    for label, n, name, guides in rows:
        out.append(f'<text x="0" y="{y+16}" class="lb">{label}</text>')
        for i in range(n):
            out.append(f'<rect x="{110 + i*52}" y="{y}" width="44" height="22" rx="4" class="lv"/>')
        for i in range(guides):
            out.append(f'<circle cx="{124 + i*52}" cy="{y+32}" r="5" class="lg"/>')
        out.append(f'<text x="{110 + max(n,guides)*52 + 14}" y="{y+16}" class="ls">{name}'
                   f'{"" if guides == 1 else f" &#183; {guides} guides"}</text>')
        y += 52
    out.append('<text x="0" y="325" class="ls">Gold: vehicles. Grey: guides - one in each, '
               'because a guide cannot be in two coaches at once.</text>')
    out.append('</svg>')
    return "".join(out)


def svg_pena():
    """The constraint nobody mentions until it is too late to change it."""
    return (
        '<svg viewBox="0 0 680 250" role="img" aria-label="The road to Pena Palace takes '
        'vehicles up to 22 seats; larger coaches stop below and transfer" class="w-full h-auto">'
        '<style>.pt{font:500 13px Inter,sans-serif;fill:currentColor}'
        '.ps{font:13px Inter,sans-serif;fill:currentColor;opacity:.62}'
        '.pl{stroke:currentColor;opacity:.3;fill:none;stroke-width:1.5}'
        '.pg{stroke:var(--color-gold);fill:none;stroke-width:2.5}</style>'
        '<path d="M20 215 C 170 215, 250 150, 330 120 S 520 70, 650 55" class="pl"/>'
        '<path d="M20 215 C 170 215, 250 150, 330 120" class="pg"/>'
        '<circle cx="20" cy="215" r="6" fill="currentColor"/>'
        '<circle cx="330" cy="120" r="6" fill="var(--color-gold)"/>'
        '<circle cx="650" cy="55" r="6" fill="currentColor"/>'
        '<text x="10" y="240" class="pt">Sintra town</text>'
        '<text x="268" y="100" class="pt">The turning</text>'
        '<text x="268" y="146" class="ps">Full-size coaches stop here</text>'
        '<text x="556" y="38" class="pt">Pena Palace</text>'
        '<text x="470" y="92" class="ps">Up to 22 seats only</text>'
        '</svg>')


def svg_day():
    """Where the hours actually go on a Lisbon day from Sintra."""
    blocks = [("Collection", 60, False), ("Belem", 150, True), ("Lunch", 90, True),
              ("The city", 120, True), ("Home", 60, False)]
    total = sum(b[1] for b in blocks)
    out = ['<svg viewBox="0 0 680 150" role="img" aria-label="How an eight-hour day '
           'divides between driving and stops" class="w-full h-auto">']
    out.append('<style>.dt{font:500 13px Inter,sans-serif;fill:currentColor}'
               '.ds{font:12px Inter,sans-serif;fill:currentColor;opacity:.62}</style>')
    x = 0
    for name, mins, stop in blocks:
        w = 680 * mins / total
        fill = 'var(--color-gold)' if stop else 'currentColor'
        dim  = '' if stop else ' opacity="0.28"'
        out.append(f'<rect x="{x:.0f}" y="30" width="{w-4:.0f}" height="40" rx="3" '
                   f'fill="{fill}"{dim}/>')
        out.append(f'<text x="{x:.0f}" y="24" class="dt">{name}</text>')
        hm = f'{mins//60}h' + ('' if mins % 60 == 0 else f' {mins % 60}m')
        out.append(f'<text x="{x:.0f}" y="88" class="ds">{hm}</text>')
        x += w
    out.append('<text x="0" y="126" class="ds">An hour each way between Lisbon and Sintra, '
               'whichever end you start at. Two of the eight hours are the road.</text>')
    out.append('</svg>')
    return "".join(out)


DIAGRAMS = {"ladder": svg_ladder, "pena": svg_pena, "day": svg_day}


# ── the page shell ────────────────────────────────────────────────────────
def section_html(sec):
    kind = sec.get("kind", "prose")
    if kind == "prose":
        body = "".join(f"<p>{p}</p>" for p in sec["paras"])
        return (f'<section class="container-page py-20 md:py-28 grid gap-12 md:grid-cols-12 items-start">'
                f'<div class="md:col-span-5"><div class="eyebrow"><span class="rule mr-3"></span>'
                f'{esc(sec["eyebrow"])}</div>'
                f'<h2 class="display text-4xl md:text-5xl mt-5">{esc(sec["title"])}</h2></div>'
                f'<div class="md:col-span-6 md:col-start-7 text-lg leading-relaxed '
                f'text-muted-foreground space-y-6">{body}</div></section>')
    if kind == "diagram":
        return (f'<section class="bg-secondary/60 py-20 md:py-28"><div class="container-page">'
                f'<div class="eyebrow"><span class="rule mr-3"></span>{esc(sec["eyebrow"])}</div>'
                f'<h2 class="display text-3xl md:text-5xl mt-5 max-w-3xl">{esc(sec["title"])}</h2>'
                f'<p class="mt-6 max-w-2xl text-lg leading-relaxed text-muted-foreground">'
                f'{sec["lede"]}</p>'
                f'<div class="mt-10 max-w-3xl">{DIAGRAMS[sec["figure"]]()}</div>'
                f'</div></section>')
    if kind == "list":
        items = "".join(
            '<li class="flex gap-4 items-start"><span class="mt-3 h-px w-6 flex-shrink-0" '
            'style="background:var(--color-gold)"></span>'
            f'<span class="leading-relaxed"><strong>{esc(t)}</strong> {b}</span></li>'
            for t, b in sec["items"])
        return (f'<section class="container-page py-20 md:py-28">'
                f'<div class="eyebrow"><span class="rule mr-3"></span>{esc(sec["eyebrow"])}</div>'
                f'<h2 class="display text-3xl md:text-5xl mt-5 max-w-3xl">{esc(sec["title"])}</h2>'
                f'<ul class="mt-10 space-y-6 text-lg text-muted-foreground max-w-3xl">{items}</ul>'
                f'</section>')
    if kind == "table":
        head = "".join(f'<th class="text-left font-medium pb-3 pr-8">{esc(h)}</th>' for h in sec["head"])
        rows = "".join(
            "<tr class='border-t border-border'>" + "".join(
                f'<td class="py-4 pr-8" style="vertical-align:top">{c}</td>' for c in r) + "</tr>"
            for r in sec["rows"])
        return (f'<section class="container-page py-20 md:py-28">'
                f'<div class="eyebrow"><span class="rule mr-3"></span>{esc(sec["eyebrow"])}</div>'
                f'<h2 class="display text-3xl md:text-5xl mt-5 max-w-3xl">{esc(sec["title"])}</h2>'
                f'<p class="mt-6 max-w-2xl text-lg leading-relaxed text-muted-foreground">{sec["lede"]}</p>'
                f'<div class="mt-10" style="overflow-x:auto"><table class="w-full text-base md:text-lg '
                f'text-muted-foreground"><thead class="text-foreground"><tr>{head}</tr></thead>'
                f'<tbody>{rows}</tbody></table></div>'
                f'<p class="mt-8 max-w-2xl text-sm leading-relaxed text-muted-foreground">'
                f'{sec["foot"]}</p></section>')
    if kind == "links":
        cards = "".join(
            f'<a href="{esc(h)}" class="group block border-t border-border pt-5 '
            'hover:border-foreground transition-colors">'
            f'<h3 class="display text-2xl group-hover:text-gold transition-colors leading-tight">'
            f'{esc(t)}</h3><p class="mt-3 text-base text-muted-foreground">{esc(d)}</p>'
            '<span class="mt-4 inline-block text-[0.65rem] uppercase tracking-[0.28em] text-primary '
            'group-hover:text-gold transition-colors">Read &rarr;</span></a>'
            for t, d, h in sec["items"])
        return (f'<section class="bg-secondary/60 py-20 md:py-28"><div class="container-page">'
                f'<div class="eyebrow"><span class="rule mr-3"></span>{esc(sec["eyebrow"])}</div>'
                f'<h2 class="display text-3xl md:text-5xl mt-5 max-w-3xl">{esc(sec["title"])}</h2>'
                f'<div class="mt-10 grid gap-10 md:grid-cols-3">{cards}</div></div></section>')
    raise ValueError(kind)


def build(skeleton, page):
    url = f'{SITE}/{page["slug"]}/'
    s = skeleton

    s = re.sub(r"<title>.*?</title>",
               lambda _: f'<title>{esc(page["title"])}</title>', s, count=1, flags=re.S)
    s = re.sub(r'(<meta name="description" content=")[^"]*(")',
               lambda m: m.group(1) + esc(page["desc"]) + m.group(2), s, count=1)
    for prop in ("og:title", "twitter:title"):
        s = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*(")',
                   lambda m: m.group(1) + esc(page["title"]) + m.group(2), s, count=1)
    for prop in ("og:description", "twitter:description"):
        s = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*(")',
                   lambda m: m.group(1) + esc(page["desc"]) + m.group(2), s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*(")',
               lambda m: m.group(1) + url + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
               lambda m: m.group(1) + url + m.group(2), s, count=1)
    s = re.sub(r'(<link rel="preload" as="image" href=")[^"]*(")',
               lambda m: m.group(1) + page["hero"] + m.group(2), s, count=1)
    for prop in ("og:image", "twitter:image"):
        s = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*(")',
                   lambda m: m.group(1) + SITE + page["hero"] + m.group(2), s, count=1)

    # A service page is not an article.
    s = s.replace('<meta property="og:type" content="article"/>',
                  '<meta property="og:type" content="website"/>')

    # English only, so no alternates are claimed that would 404.
    s = re.sub(r'\s*<link rel="alternate" hreflang="(?:pt|es|fr)"[^>]*/>', "", s)
    s = re.sub(r'(<link rel="alternate" hreflang="(?:en|x-default)" href=")[^"]*(")',
               lambda m: m.group(1) + url + m.group(2), s)
    s = re.sub(r'(href=")/(pt|es|fr)/[^"]*(")',
               lambda m: m.group(1) + "/" + m.group(2) + "/" + m.group(3), s)

    # One block of structured data, replacing whatever the skeleton carried.
    ld = {
        "@context": "https://schema.org", "@type": "Service",
        "name": page["h1"], "serviceType": page["service"],
        "description": page["desc"], "url": url,
        "areaServed": [{"@type": "City", "name": n} for n in ("Lisbon", "Sintra", "Cascais")],
        "provider": {"@type": "TravelAgency", "name": "Lisbon Sintra Tours",
                     "url": SITE, "telephone": "+351 912 164 220",
                     "address": {"@type": "PostalAddress", "addressLocality": "Lisbon",
                                 "addressCountry": "PT"}},
    }
    if page.get("faq"):
        ld = [ld, {"@context": "https://schema.org", "@type": "FAQPage",
                   "mainEntity": [{"@type": "Question", "name": q,
                                   "acceptedAnswer": {"@type": "Answer", "text": a}}
                                  for q, a in page["faq"]]}]
    block = ('<script type="application/ld+json">'
             + json.dumps(ld, ensure_ascii=False) + "</script>")
    if re.search(r'<script type="application/ld\+json">', s):
        s = re.sub(r'<script type="application/ld\+json">.*?</script>',
                   lambda _: block, s, count=1, flags=re.S)
    else:
        s = s.replace("</head>", block + "</head>", 1)

    main = (
        '<main class="flex-1">'
        '<section class="relative h-[68vh] min-h-[480px] w-full overflow-hidden">'
        '<div class="absolute inset-0">'
        # object-position, because object-cover centres the crop and the
        # subject of a photograph is rarely in the middle of it: centred, the
        # coaches at Belem fell out of the bottom of the frame and the hero
        # was a picture of a tower.
        f'<img src="{page["hero"]}" alt="{esc(page.get("hero_alt", ""))}" '
        # ken-burns is the site's signature drift on a scenic hero, and it is
        # wrong on one with a subject: the slow zoom walked the coaches out of
        # the bottom of the frame a few seconds after the page loaded. A photo
        # that is ABOUT something holds still.
        f'class="absolute inset-0 h-full w-full object-cover'
        f'{"" if page.get("hero_pos") else " ken-burns"}"'
        f'{" style=" + chr(34) + "object-position:" + page["hero_pos"] + chr(34) if page.get("hero_pos") else ""}/>'
        # The wash is inline rather than a class: these heroes sit over Pena in
        # full sun, where the site's standard gradient leaves white text on a
        # pale wall. Inline also means it cannot be a class that was never
        # compiled.
        '<div class="absolute inset-0" style="background:linear-gradient(to bottom,'
        'rgba(0,0,0,.42) 0%,rgba(0,0,0,.34) 35%,rgba(0,0,0,.62) 72%,rgba(0,0,0,.78) 100%)"></div>'
        '</div>'
        '<div class="relative h-full container-page flex flex-col justify-end pb-20 md:pb-24" '
        'style="color:var(--color-ivory)">'
        f'<div class="eyebrow fade-up" style="color:var(--color-gold)">{esc(page["eyebrow"])}</div>'
        f'<h1 class="display text-5xl md:text-7xl mt-5 max-w-4xl fade-up fade-up-delay-1" '
        f'style="color:var(--color-ivory)">{esc(page["h1"])}</h1>'
        f'<p class="mt-6 max-w-2xl text-base md:text-lg leading-relaxed text-ivory/85 '
        f'fade-up fade-up-delay-2">{esc(page["stand"])}</p>'
        '</div></section>'
        + "".join(section_html(sec) for sec in page["sections"])
        + '<section class="container-page py-20 md:py-28 text-center">'
          '<div class="eyebrow">Next</div>'
          f'<h2 class="display text-4xl md:text-6xl mt-6 max-w-3xl mx-auto">{esc(page["cta"])}</h2>'
          f'<p class="mt-6 max-w-xl mx-auto text-lg text-muted-foreground">{page["cta_sub"]}</p>'
          '<div class="mt-10"><a href="/contact/" class="btn-ink">Tell us about your group</a></div>'
          '</section>'
        + '</main>')
    s = re.sub(r'<main class="flex-1">.*?</main>', lambda _: main, s, count=1, flags=re.S)
    return s


def main():
    from landing_content import PAGES
    skeleton = open(SKELETON, encoding="utf-8").read()
    for page in PAGES:
        folder = os.path.join(ROOT, page["slug"])
        os.makedirs(folder, exist_ok=True)
        html = build(skeleton, page)
        with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  {page['slug']}/  {len(html):,} bytes")
    print(f"{len(PAGES)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
