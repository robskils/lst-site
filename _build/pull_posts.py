#!/usr/bin/env python3
"""
pull_posts.py - the bridge between the CRM's blog queue and this site.

Robin asked for posts that publish themselves twice a week: "push one live
twice a week, automated. Optimised to hell. So even if I forget about it, it
keeps happening."

Half of that was built. The CRM holds the queue, writes the next post every
Tuesday and Friday morning, and serves what it has written at
/api/blog-feed. Nothing then carried it the last step, because this site is
static HTML committed to a repo and the worker has no way to commit. So the
posts piled up in the CRM marked "written" and never reached the web.

This is the last step, and it runs in GitHub Actions rather than in the
worker, because Actions is the thing that is allowed to push.

WHAT IT DOES
  1. Reads the feed.
  2. For any post whose folder does not exist, writes blog/<slug>/index.html.
  3. Adds a card to the blog index, newest first.
  4. Leaves everything else alone.

It never overwrites a post that is already on disk. A page that has been
edited here by hand is the better copy by definition, and a job that runs
unattended twice a week must not be able to undo an edit.

The page is built from an existing post used as a skeleton, so the head, the
nav and the footer are always whatever the rest of the site currently has,
rather than a copy that slowly goes stale in this file.
"""

import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone

# Overridable so the generator can be exercised against a fixture before it
# is ever let loose on the live queue.
FEED = os.environ.get("BLOG_FEED", "https://lst-pp-admin.rls-6d4.workers.dev/api/blog-feed")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKELETON = os.path.join(ROOT, "blog", "large-private-group-tours-lisbon", "index.html")
INDEX = os.path.join(ROOT, "blog", "index.html")
SITE = "https://lisbonsintratours.com"

# A hero that does not argue with the post. There is no photograph of a coach
# on this site - the only vehicle image is a seven-seat V-Class, which is the
# wrong picture for a piece about moving fifty people - so a post gets a
# landscape until there is a real one. Replace these the day after the shoot.
HEROES = [
    ("sintra", "/images/sintra-pena-palace.jpg"),
    ("pena", "/images/sintra-pena-palace.jpg"),
    ("regaleira", "/images/sintra-quinta-regaleira.jpg"),
    ("lisbon", "/images/lisbon-tram.jpg"),
    ("belem", "/images/pastel.jpg"),
    ("fatima", "/images/fatima.jpg"),
    ("evora", "/images/evora.jpg"),
    ("cascais", "/images/cabo-da-roca.jpg"),
    ("wedding", "/images/sintra-monserrate.jpg"),
]
HERO_DEFAULT = "/images/hero-sintra.jpg"


def hero_for(title: str) -> str:
    t = (title or "").lower()
    for word, img in HEROES:
        if word in t:
            return img
    return HERO_DEFAULT


def esc(s: str) -> str:
    return (str(s or "").replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def fetch():
    req = urllib.request.Request(FEED, headers={"User-Agent": "lst-site-build"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8")).get("posts", [])


def first_paragraph(html: str) -> str:
    """The standfirst under the headline, taken from the post's own opening."""
    m = re.search(r"<p>(.*?)</p>", html, re.S)
    text = re.sub(r"<[^>]+>", "", m.group(1)) if m else ""
    text = re.sub(r"\s+", " ", text).strip()
    return text[:240]


def build_page(skeleton: str, post: dict) -> str:
    slug = post["slug"]
    title = post["title"]
    desc = post.get("meta_desc") or first_paragraph(post.get("body", ""))
    url = f"{SITE}/blog/{slug}/"
    hero = hero_for(title)
    stand = first_paragraph(post.get("body", ""))
    when = (post.get("published_at") or datetime.now(timezone.utc).isoformat())[:10]

    s = skeleton

    # ── head ───────────────────────────────────────────────────────────────
    s = re.sub(r"<title>.*?</title>",
               f"<title>{esc(title)} | Lisbon Sintra Tours</title>", s, count=1, flags=re.S)
    s = re.sub(r'(<meta name="description" content=")[^"]*(")',
               lambda m: m.group(1) + esc(desc) + m.group(2), s, count=1)
    for prop in ("og:title", "twitter:title"):
        s = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*(")',
                   lambda m: m.group(1) + esc(title) + " | Lisbon Sintra Tours" + m.group(2), s, count=1)
    for prop in ("og:description", "twitter:description"):
        s = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*(")',
                   lambda m: m.group(1) + esc(desc) + m.group(2), s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*(")',
               lambda m: m.group(1) + url + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
               lambda m: m.group(1) + url + m.group(2), s, count=1)
    s = re.sub(r'(<link rel="preload" as="image" href=")[^"]*(")',
               lambda m: m.group(1) + hero + m.group(2), s, count=1)
    for prop in ("og:image", "twitter:image"):
        s = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*(")',
                   lambda m: m.group(1) + SITE + hero + m.group(2), s, count=1)

    # A new post exists in English only. Claiming a Portuguese version that is
    # not there would send Google to a 404, so the alternates are dropped and
    # x-default points at the only page that exists.
    s = re.sub(r'\s*<link rel="alternate" hreflang="(?:pt|es|fr)"[^>]*/>', "", s)

    # The language switcher in the nav is a link to THIS article in another
    # language, and on a fresh post there is no such article - left alone it
    # carried the skeleton's own Portuguese URL, so clicking PT on a new piece
    # landed the reader on a different one. Until a translation exists it goes
    # to that language's blog index, which is at least about the same subject.
    s = re.sub(r'(href=")/(pt|es|fr)/blog/[^"]*(")',
               lambda m: m.group(1) + "/" + m.group(2) + "/blog/" + m.group(3), s)
    s = re.sub(r'(<link rel="alternate" hreflang="(?:en|x-default)" href=")[^"]*(")',
               lambda m: m.group(1) + url + m.group(2), s)

    # ── structured data ────────────────────────────────────────────────────
    def fix_ld(m):
        try:
            data = json.loads(m.group(1))
        except Exception:
            return m.group(0)

        def walk(node):
            if isinstance(node, dict):
                if "headline" in node:
                    node["headline"] = title
                if "description" in node:
                    node["description"] = desc
                for k in ("datePublished", "dateModified"):
                    if k in node:
                        node[k] = when
                if node.get("@type") in ("BlogPosting", "Article", "WebPage"):
                    node["url"] = url
                    if "mainEntityOfPage" in node:
                        node["mainEntityOfPage"] = url
                    if "image" in node:
                        node["image"] = SITE + hero
                for v in node.values():
                    walk(v)
            elif isinstance(node, list):
                for v in node:
                    walk(v)

        walk(data)
        return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"

    s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix_ld, s, count=1, flags=re.S)

    # ── the page itself ────────────────────────────────────────────────────
    main = (
        '<main class="flex-1">'
        '<section class="relative h-[68vh] min-h-[480px] w-full overflow-hidden">'
        '<div class="absolute inset-0">'
        f'<img src="{hero}" alt="" class="absolute inset-0 h-full w-full object-cover ken-burns"/>'
        '<div class="absolute inset-0 bg-gradient-to-b from-black/45 via-black/30 to-black/60"></div>'
        '</div>'
        '<div class="relative h-full container-page flex flex-col justify-end pb-20 md:pb-24" '
        'style="color:var(--color-ivory)">'
        '<div class="eyebrow fade-up" style="color:var(--color-gold)">Travel Journal</div>'
        f'<h1 class="display text-5xl md:text-7xl mt-5 max-w-4xl fade-up fade-up-delay-1" '
        f'style="color:var(--color-ivory)">{esc(title)}</h1>'
        f'<p class="mt-6 max-w-2xl text-base md:text-lg leading-relaxed text-ivory/85 '
        f'fade-up fade-up-delay-2">{esc(stand)}</p>'
        '</div></section>'
        '<article class="container-page py-20 md:py-28">'
        '<div class="grid md:grid-cols-12 gap-12">'
        '<div class="md:col-span-8 md:col-start-3 lst-prose">'
        + post.get("body", "") +
        '</div></div></article></main>'
    )
    s = re.sub(r"<main class=\"flex-1\">.*?</main>", lambda _: main, s, count=1, flags=re.S)
    return s


def add_to_index(index_html: str, post: dict) -> str:
    """One card, newest first, in the shape the page already uses."""
    slug, title = post["slug"], post["title"]
    if f'href="/blog/{slug}/"' in index_html:
        return index_html
    desc = post.get("meta_desc") or first_paragraph(post.get("body", ""))
    card = (
        f'<a href="/blog/{slug}/" class="group block border-t border-border pt-5 '
        'hover:border-foreground transition-colors">'
        f'<h3 class="display text-2xl group-hover:text-gold transition-colors leading-tight">{esc(title)}</h3>'
        f'<p class="mt-3 text-sm text-muted-foreground line-clamp-3">{esc(desc)}</p>'
        '<span class="mt-4 inline-block text-[0.65rem] uppercase tracking-[0.28em] text-primary '
        'group-hover:text-gold transition-colors">Read →</span></a>'
    )
    # In front of the first existing card, so the newest post leads the page.
    m = re.search(r'<a href="/blog/[^"]+/" class="group block', index_html)
    if not m:
        print("  ! could not find where the cards go; index left alone", file=sys.stderr)
        return index_html
    return index_html[:m.start()] + card + index_html[m.start():]


def main() -> int:
    try:
        posts = fetch()
    except Exception as e:
        print(f"could not read the feed: {e}", file=sys.stderr)
        return 1

    if not posts:
        print("nothing written yet; nothing to publish")
        return 0

    if not os.path.exists(SKELETON):
        print(f"no skeleton at {SKELETON}", file=sys.stderr)
        return 1
    skeleton = open(SKELETON, encoding="utf-8").read()
    index_html = open(INDEX, encoding="utf-8").read()
    before = index_html
    added = []

    # Oldest first, so the newest ends up at the top of the index.
    for post in sorted(posts, key=lambda p: p.get("published_at") or ""):
        slug = (post.get("slug") or "").strip()
        if not slug or not post.get("body"):
            continue
        folder = os.path.join(ROOT, "blog", slug)
        page = os.path.join(folder, "index.html")
        if os.path.exists(page):
            continue                      # already here, and the copy on disk wins
        os.makedirs(folder, exist_ok=True)
        with open(page, "w", encoding="utf-8") as f:
            f.write(build_page(skeleton, post))
        index_html = add_to_index(index_html, post)
        added.append(slug)
        print(f"  + blog/{slug}/")

    if index_html != before:
        with open(INDEX, "w", encoding="utf-8") as f:
            f.write(index_html)

    print(f"{len(added)} new post{'' if len(added) == 1 else 's'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
