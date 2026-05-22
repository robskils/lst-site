#!/usr/bin/env python3
import glob, os
from datetime import date

DOMAIN = "https://lisbonsintratours.com"
DST = os.path.dirname(os.path.abspath(__file__))

# Priority rules
def priority(path):
    if path == "/": return "1.0"
    if path in ("/tours/", "/destinations/", "/contact/", "/about/"): return "0.9"
    if path in ("/pt/", "/pt/tours/", "/pt/destinations/", "/pt/contact/", "/pt/about/"): return "0.9"
    if path.startswith("/tours/") or path.startswith("/destinations/"): return "0.8"
    if path.startswith("/pt/tours/") or path.startswith("/pt/destinations/"): return "0.8"
    if path == "/blog/": return "0.7"
    if path == "/pt/blog/": return "0.7"
    if path.startswith("/blog/") or path.startswith("/pt/blog/"): return "0.6"
    return "0.5"

def changefreq(path):
    if path in ("/", "/tours/", "/destinations/", "/blog/", "/pt/", "/pt/tours/", "/pt/destinations/", "/pt/blog/"): return "weekly"
    if path.startswith("/blog/") or path.startswith("/pt/blog/"): return "monthly"
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
