#!/usr/bin/env python3
import os, re, shutil

SRC = "/Users/robinlumley-savile/Documents/GitHub"
DST = "/Users/robinlumley-savile/Documents/GitHub/lst-site"

# filename → folder path (empty string = root index.html)
URL_MAP = {
    "index.html": "",
    "about.html": "about",
    "blog.html": "blog",
    "contact.html": "contact",
    "tours.html": "tours",
    "destinations.html": "destinations",
    "privacy-policy.html": "privacy-policy",
    "transport-services.html": "transport-services",
    "car-service.html": "car-service",
    "car-tours-from-lisbon-to-sintra.html": "car-tours-from-lisbon-to-sintra",
    "sintra-tours.html": "sintra-tours",
    "private-tours-sintra.html": "private-tours-sintra",
    "private-group-tours-portugal.html": "private-group-tours-portugal",
    "next-day-and-same-day-sintra-tours.html": "next-day-and-same-day-sintra-tours",
    "one-day-tours-from-lisbon.html": "one-day-tours-from-lisbon",
    "lisbon-art-tours.html": "lisbon-art-tours",
    "lisbon-wine-tours.html": "lisbon-wine-tours",
    "lisbon-festivals-and-events.html": "lisbon-festivals-and-events",
    "luxury-private-transport-in-lisbon-–-vip-services.html": "luxury-private-transport",
    # Tour detail pages
    "romanticist-sintra-tour.html": "tours/romanticist-sintra",
    "lisbon-and-belem-tour.html": "tours/lisbon-and-belem",
    "fatima-central-portugal-tour.html": "tours/fatima-central-portugal",
    "portuguese-riviera-tour.html": "tours/portuguese-riviera",
    "evora-and-alentejo-tour.html": "tours/evora-and-alentejo",
    "royal-sintra-tour.html": "tours/royal-sintra",
    "templar-portugal-tour.html": "tours/templar-portugal",
    "lisbon-sunset-cruise.html": "tours/lisbon-sunset-cruise",
    "porto-and-aveiro-tour.html": "tours/porto-and-aveiro",
    "porto-city-tour.html": "tours/porto-city",
    "relaxing-portugal-tour.html": "tours/relaxing-portugal",
    "relaxing-algarve-tour.html": "tours/relaxing-algarve",
    # Destination pages
    "lisbon.html": "destinations/lisbon",
    "porto.html": "destinations/porto",
    "evora.html": "destinations/evora",
    "cabo-da-roca.html": "destinations/cabo-da-roca",
    "jeronimos-monastery.html": "destinations/jeronimos-monastery",
    "fatima-the-catholic-pilgrimage-site.html": "destinations/fatima",
    "the-castles-and-palaces-of-sintra.html": "destinations/the-castles-and-palaces-of-sintra",
    "the-portuguese-riviera.html": "destinations/the-portuguese-riviera",
    "tomar-and-the-knights-templar.html": "destinations/tomar-and-the-knights-templar",
    "romanticism-in-portugal.html": "destinations/romanticism-in-portugal",
    # Blog posts
    "getting-around-in-style-luxury-private-transport-in-portugal.html": "blog/getting-around-in-style",
    "have-you-discovered-braga.html": "blog/have-you-discovered-braga",
    "how-to-get-from-lisbon-to-sintra.html": "blog/how-to-get-from-lisbon-to-sintra",
    "how-to-plan-a-stress-free-senior-friendly-trip-to-portugal.html": "blog/how-to-plan-a-stress-free-senior-friendly-trip-to-portugal",
    "lisbon-tops-the-happiest-city-index.html": "blog/lisbon-tops-the-happiest-city-index",
    "lisbon’s-luxury-private-events-planning-your-dream-occasion.html": "blog/lisbons-luxury-private-events",
    "lisbons-alternative-neighbourhoods.html": "blog/lisbons-alternative-neighbourhoods",
    "lisbons-hidden-gems.html": "blog/lisbons-hidden-gems",
    "the-best-day-trips-from-lisbon.html": "blog/the-best-day-trips-from-lisbon",
    "the-best-hotels-in-lisbon.html": "blog/the-best-hotels-in-lisbon",
    "the-best-hotels-in-sintra.html": "blog/the-best-hotels-in-sintra",
    "the-best-restaurants-in-sintra-with-a-view.html": "blog/the-best-restaurants-in-sintra-with-a-view",
    "the-best-restaurants-in-sintra.html": "blog/the-best-restaurants-in-sintra",
    "the-top-tourist-attractions-in-portugal.html": "blog/the-top-tourist-attractions-in-portugal",
    "web-summit-2022.html": "blog/web-summit-2022",
    "why-portugal-is-the-ideal-destination-for-history-loving-seniors.html": "blog/why-portugal-is-the-ideal-destination-for-history-loving-seniors",
    "why-visit-cascais.html": "blog/why-visit-cascais",
    "wine-tourism-in-portugal.html": "blog/wine-tourism-in-portugal",
    "winter-tours-to-sintra.html": "blog/winter-tours-to-sintra",
}

# Build reverse map: filename -> canonical URL
def url_for(filename):
    path = URL_MAP.get(filename)
    if path is None:
        return None
    return "/" if path == "" else f"/{path}/"

def clean_html(html):
    # Remove TanStack dev stylesheet
    html = re.sub(r'<link[^>]+data-tanstack-router-dev-styles[^>]*/>', '', html)
    html = re.sub(r'<link[^>]+data-tanstack-router-dev-styles[^>]*>', '', html)

    # Fix stylesheet reference
    html = html.replace('href="src/styles.css"', 'href="/css/lst.css"')

    # Fix asset paths (src= and href= for preloads)
    html = re.sub(r'(src|href)="src/assets/([^"]+)"', r'\1="/images/\2"', html)

    # Fix internal .html links
    def relink(m):
        fname = m.group(1)
        url = url_for(fname)
        return f'href="{url}"' if url else m.group(0)
    html = re.sub(r'href="([^"#?]+\.html)"', relink, html)

    # Strip React/TanStack hydration scripts (all <script> tags)
    html = re.sub(r'<script\b[^>]*>[\s\S]*?</script>', '', html)

    # Remove React rendering markers and artifacts
    html = html.replace('<!--$-->', '').replace('<!--/$-->', '')
    html = re.sub(r'<!-- -->', '', html)

    # Remove React-specific attributes
    html = re.sub(r'\s*data-status="[^"]*"', '', html)
    html = re.sub(r'\s*data-precedence="[^"]*"', '', html)

    # Add our JS before </body>
    html = html.replace('</body>', '<script src="/js/lst.js" defer></script>\n</body>')

    return html

# Process each file
ok = 0
missing = []
for filename, path in URL_MAP.items():
    src_file = os.path.join(SRC, filename)
    if not os.path.exists(src_file):
        missing.append(filename)
        continue

    with open(src_file, 'r', encoding='utf-8') as f:
        html = f.read()

    html = clean_html(html)

    if path == "":
        dst_file = os.path.join(DST, "index.html")
    else:
        dst_dir = os.path.join(DST, path)
        os.makedirs(dst_dir, exist_ok=True)
        dst_file = os.path.join(dst_dir, "index.html")

    with open(dst_file, 'w', encoding='utf-8') as f:
        f.write(html)
    ok += 1
    print(f"  ✓  {filename}")

if missing:
    print(f"\nMISSING ({len(missing)}):")
    for m in missing:
        print(f"  ✗  {m}")

print(f"\nDone: {ok} pages written.")
