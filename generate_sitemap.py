#!/usr/bin/env python3
import glob, os
from datetime import date

DOMAIN = "https://lisbonsintratours.com"
DST = os.path.dirname(os.path.abspath(__file__))

# Priority rules
def priority(path):
    if path == "/": return "1.0"
    if path in ("/tours/", "/destinations/", "/contact/", "/about/"): return "0.9"
    if path in ("/pt/", "/pt/passeios/", "/pt/destinos/", "/pt/contacto/", "/pt/sobre-nos/"): return "0.9"
    if path.startswith("/tours/") or path.startswith("/destinations/"): return "0.8"
    if path.startswith("/pt/passeios/") or path.startswith("/pt/destinos/"): return "0.8"
    # Spanish and French were left out of every rule below, so their tours,
    # destinations and journal all came out at the default 0.5 while the same
    # pages in English and Portuguese were 0.6 to 0.9. Four languages, one set
    # of rules.
    if path in ("/es/", "/es/tours/", "/es/destinos/", "/es/contacto/", "/es/sobre-nosotros/"): return "0.9"
    if path in ("/fr/", "/fr/excursions/", "/fr/destinations/", "/fr/contact/", "/fr/a-propos/"): return "0.9"
    if path.startswith("/es/tours/") or path.startswith("/es/destinos/"): return "0.8"
    if path.startswith("/fr/excursions/") or path.startswith("/fr/destinations/"): return "0.8"
    if path in ("/blog/", "/pt/blog/", "/es/blog/", "/fr/blog/"): return "0.7"
    if any(path.startswith(b) for b in ("/blog/", "/pt/blog/", "/es/blog/", "/fr/blog/")): return "0.6"
    return "0.5"

def changefreq(path):
    weekly = ("/", "/tours/", "/destinations/", "/blog/")
    if path in weekly or any(path == "/" + l + w for l in ("pt", "es", "fr") for w in weekly): return "weekly"
    if any(path.startswith(b) for b in ("/blog/", "/pt/blog/", "/es/blog/", "/fr/blog/")): return "monthly"
    return "monthly"

# Collect all pages
urls = []
# Root index
urls.append("/")
# All folder-per-page indexes
for f in sorted(glob.glob(f"{DST}/**/index.html", recursive=True)):
    rel = f.replace(DST, "").replace("/index.html", "/")
    if rel == "/": continue
    urls.append(rel)

today = date.today().isoformat()

lines = ['<?xml version="1.0" encoding="UTF-8"?>']
lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
for url in sorted(urls):
    lines.append(f"""  <url>
    <loc>{DOMAIN}{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{changefreq(url)}</changefreq>
    <priority>{priority(url)}</priority>
  </url>""")
lines.append('</urlset>')

out = "\n".join(lines)
with open(f"{DST}/sitemap.xml", "w") as f:
    f.write(out)

print(f"Written {len(urls)} URLs to sitemap.xml")
