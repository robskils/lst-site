#!/usr/bin/env python3
"""
build_pt.py — Generate the /pt/ Portuguese mirror of lisbonsintratours.com
Run from the site root: python3 build_pt.py
Idempotent: safe to run multiple times.
"""

import os
import re
import shutil
from pathlib import Path

SITE_ROOT = Path(__file__).parent
BASE_URL = "https://lisbonsintratours.com"

# ---------------------------------------------------------------------------
# Internal-link prefixing regex
# Only prefix href values that start with / but NOT /css/, /js/, /images/, /favicon
# ---------------------------------------------------------------------------
INTERNAL_LINK_RE = re.compile(
    r'(href=")(/(?!css/|js/|images/|favicon)([^"]*?))(")'
)

def prefix_links(html: str) -> str:
    """Add /pt prefix to all internal content links in a PT page."""
    def replacer(m):
        href_val = m.group(2)  # e.g. /tours/
        # Don't double-prefix
        if href_val.startswith("/pt/"):
            return m.group(0)
        # Handle root
        if href_val == "/":
            return m.group(1) + "/pt/" + m.group(4)
        return m.group(1) + "/pt" + href_val + m.group(4)
    return INTERNAL_LINK_RE.sub(replacer, html)


# ---------------------------------------------------------------------------
# Hreflang tag injection
# ---------------------------------------------------------------------------
def make_hreflang_en(path: str) -> str:
    """Return hreflang tags for an EN page at /path/ ."""
    en_url = f"{BASE_URL}{path}"
    pt_url = f"{BASE_URL}/pt{path}"
    return (
        f'<link rel="alternate" hreflang="en" href="{en_url}"/>'
        f'<link rel="alternate" hreflang="pt" href="{pt_url}"/>'
        f'<link rel="alternate" hreflang="x-default" href="{en_url}"/>'
    )

def make_hreflang_pt(path: str) -> str:
    """Return hreflang + canonical tags for a PT page at /pt/path/ ."""
    en_url = f"{BASE_URL}{path}"
    pt_url = f"{BASE_URL}/pt{path}"
    return (
        f'<link rel="canonical" href="{pt_url}"/>'
        f'<link rel="alternate" hreflang="en" href="{en_url}"/>'
        f'<link rel="alternate" hreflang="pt" href="{pt_url}"/>'
        f'<link rel="alternate" hreflang="x-default" href="{en_url}"/>'
    )

def inject_hreflang_en(html: str, path: str) -> str:
    # Idempotent: only inject if not already present
    if 'hreflang="en"' in html:
        return html
    tags = make_hreflang_en(path)
    # Insert before </head>
    return html.replace("</head>", tags + "</head>", 1)

def inject_hreflang_pt(html: str, path: str) -> str:
    # Idempotent: only inject if not already present
    if 'hreflang="en"' in html:
        return html
    tags = make_hreflang_pt(path)
    return html.replace("</head>", tags + "</head>", 1)


# ---------------------------------------------------------------------------
# OG URL update for PT pages
# ---------------------------------------------------------------------------
def update_og_url(html: str, path: str) -> str:
    pt_url = f"{BASE_URL}/pt{path}"
    return re.sub(
        r'<meta property="og:url" content="[^"]*?"',
        f'<meta property="og:url" content="{pt_url}"',
        html
    )

def set_lang_pt(html: str) -> str:
    return html.replace('<html lang="en">', '<html lang="pt">', 1)


# ---------------------------------------------------------------------------
# Language toggle insertion
# ---------------------------------------------------------------------------
EN_TOGGLE_TEMPLATE = '<a href="/pt/{path}" style="margin-left:0.5rem;padding:0.2rem 0.55rem;border:1px solid rgba(245,240,232,0.35);border-radius:3px;font-size:0.65rem;letter-spacing:0.14em;color:rgba(245,240,232,0.7);text-decoration:none;font-family:var(--font-sans)" aria-label="Ver em Português">PT</a>'
PT_TOGGLE_TEMPLATE = '<a href="/{path}" style="margin-left:0.5rem;padding:0.2rem 0.55rem;border:1px solid rgba(245,240,232,0.35);border-radius:3px;font-size:0.65rem;letter-spacing:0.14em;color:rgba(245,240,232,0.7);text-decoration:none;font-family:var(--font-sans)" aria-label="View in English">EN</a>'

def add_en_toggle(html: str, equiv_pt_path: str) -> str:
    """Insert PT toggle button on EN page after Contact nav link. Idempotent."""
    # Check if already added
    if 'aria-label="Ver em Português"' in html:
        return html
    toggle = EN_TOGGLE_TEMPLATE.format(path=equiv_pt_path)
    target = '">Contact</a></nav>'
    replacement = target + toggle
    if target in html:
        return html.replace(target, replacement, 1)
    return html

def strip_pt_toggle(html: str) -> str:
    """Remove the PT toggle button from a page (used when building PT pages from EN source)."""
    return re.sub(
        r'<a [^>]*aria-label="Ver em Português"[^>]*>PT</a>',
        '',
        html
    )

def add_pt_toggle(html: str, equiv_en_path: str) -> str:
    """Insert EN toggle button on PT page after Contacto nav link. Idempotent."""
    if 'aria-label="View in English"' in html:
        return html
    toggle = PT_TOGGLE_TEMPLATE.format(path=equiv_en_path)
    target = '">Contacto</a></nav>'
    replacement = target + toggle
    if target in html:
        return html.replace(target, replacement, 1)
    return html


# ---------------------------------------------------------------------------
# Common nav/footer translations applied to ALL pages
# ---------------------------------------------------------------------------
COMMON_TRANSLATIONS = [
    # lang attribute set separately
    # Nav items
    ('>Home<', '>Início<'),
    ('>Tours<', '>Passeios<'),
    ('>Destinations<', '>Destinos<'),
    ('>Journal<', '>Diário<'),
    ('>About<', '>Sobre<'),
    ('>Contact<', '>Contacto<'),
    # CTA button
    ('Plan your journey', 'Planear a sua viagem'),
    # Logo aria-label (be specific to avoid replacing page titles)
    ('aria-label="Lisbon Sintra Tours — home"', 'aria-label="Lisbon Sintra Tours — início"'),
    ('aria-label="Toggle menu"', 'aria-label="Abrir menu"'),
    # Footer
    ('Portugal, unhurried.', 'Portugal, sem pressa.'),
    ('>Explore<', '>Explorar<'),
    ('Reach us', 'Contacte-nos'),
    ('Crafted in Portugal', 'Feito em Portugal'),
    ('All rights reserved.', 'Todos os direitos reservados.'),
    ('Bespoke private tours and curated travel experiences across Lisbon, Sintra, and beyond — designed for travellers who prefer the road less travelled.',
     'Passeios privados personalizados e experiências de viagem curadas por Lisboa, Sintra e além — concebidos para viajantes que preferem os caminhos menos percorridos.'),
    # Tour common
    ('>Private Tour<', '>Passeio Privado<'),
    ('>Private Tour', '>Passeio Privado'),
    ("What&#x27;s included", 'O que está incluído'),
    ("What's included", 'O que está incluído'),
    ('Good to know', 'Informações úteis'),
    ('<h2>Pricing</h2>', '<h2>Preços</h2>'),
    ('Send us an enquiry', 'Envie-nos uma mensagem'),
    ('All our tours are priced according to group size and the vehicle required.',
     'Todos os nossos passeios têm preço de acordo com o tamanho do grupo e o veículo necessário.'),
    ('Every cruise is priced according to group size and the vessel required.',
     'Cada cruzeiro tem preço de acordo com o tamanho do grupo e a embarcação necessária.'),
    ('we will come back to you with a proposal', 'entraremos em contacto com uma proposta'),
    ('Private guide and driver', 'Guia e condutor privados'),
    ('Private vehicle throughout', 'Veículo privado durante todo o passeio'),
    ('Hotel pick-up and drop-off in Lisbon, Cascais or Sintra', 'Recolha e regresso ao hotel em Lisboa, Cascais ou Sintra'),
    ('Hotel pick-up and drop-off in Lisbon', 'Recolha e regresso ao hotel em Lisboa'),
    ('Bottled water', 'Água engarrafada'),
    ('<strong>Duration:</strong>', '<strong>Duração:</strong>'),
    ('<strong>Departure:</strong>', '<strong>Partida:</strong>'),
    ('<strong>Group size:</strong>', '<strong>Tamanho do grupo:</strong>'),
    ('<strong>Languages:</strong>', '<strong>Idiomas:</strong>'),
    ('<strong>Note:</strong>', '<strong>Nota:</strong>'),
    ('<strong>Pickup:</strong>', '<strong>Recolha:</strong>'),
    ('<strong>Pace:</strong>', '<strong>Ritmo:</strong>'),
    ('private — your group only', 'privado — apenas o seu grupo'),
    ('approximately 8 hours', 'aproximadamente 8 horas'),
    ('approximately 4 hours', 'aproximadamente 4 horas'),
    ('flexible — typically 9am', 'flexível — habitualmente às 9h'),
    ('flexible — typically early evening to coincide with sunset', 'flexível — normalmente ao início da noite, ao pôr do sol'),
    ('English, Portuguese, Spanish, French, Italian', 'Inglês, Português, Espanhol, Francês, Italiano'),
    ('entrance fees to attractions are not included; we can assist with advance purchases',
     'as entradas nas atrações não estão incluídas; podemos ajudar com compras antecipadas'),
    ('accommodation in Porto is not included; we can advise on where to stay',
     'alojamento no Porto não está incluído; podemos aconselhar sobre onde ficar'),
    ('accommodation is not included; we can advise on where to stay',
     'alojamento não está incluído; podemos aconselhar sobre onde ficar'),
    ('we collect you from your hotel or accommodation in Lisbon',
     'recolhemo-lo no seu hotel ou alojamento em Lisboa'),
    ('Admission tickets for all monuments', 'Bilhetes de entrada para todos os monumentos'),
    ('Admission tickets for all sites', 'Bilhetes de entrada para todos os locais'),
    ('Admission tickets for key sites', 'Bilhetes de entrada para os locais principais'),
    ('WiFi on board', 'WiFi a bordo'),
    ('Private boat, exclusively for your group', 'Barco privado, exclusivamente para o seu grupo'),
    ('Drinks on board throughout', 'Bebidas a bordo durante todo o cruzeiro'),
    ('English-speaking host on board', 'Anfitrião com fluência em inglês a bordo'),
    ('Opportunity to take the helm', 'Oportunidade de assumir o leme'),
    ('2 days', '2 dias'),
    ('3 days', '3 dias'),
    ('flexible — typically 9am on day one', 'flexível — habitualmente às 9h no primeiro dia'),
    ('Read more →', 'Saiba mais →'),
    ('View all tours →', 'Ver todos os passeios →'),
    ('Guest Letters', 'Testemunhos'),
    ('>Begin<', '>Começar<'),
    ('Discover Tours', 'Descobrir Passeios'),
    ('Plan a Private Journey', 'Planear uma Viagem Privada'),
    ('Start the Conversation', 'Iniciar a Conversa'),
    ('Read the announcement →', 'Ler o anúncio →'),
    ('Best Bespoke Private Tour Operator', 'Melhor Operador de Passeios Privados Personalizados'),
    ('Tailor-Made Cultural Travel Excellence', 'Excelência em Viagens Culturais à Medida'),
    # Footer nav items that appear as link text
    ('>Tours</', '>Passeios</'),
    ('>Destinations</', '>Destinos</'),
    ('>About</', '>Sobre</'),
    ('>Contact</', '>Contacto</'),
    # Footer year
    ('© 2026 Lisbon Sintra Tours. All rights reserved.', '© 2026 Lisbon Sintra Tours. Todos os direitos reservados.'),
    # btn-ink plan your journey (already covered by Plan your journey above but may appear in article)
    ('"Plan your journey"', '"Planear a sua viagem"'),
    # Send enquiry button
    ('Send enquiry', 'Enviar mensagem'),
    ('btn-ink">Plan your journey', 'btn-ink">Planear a sua viagem'),
    ('Get in touch', 'Fale connosco'),
    # LUX awards — keep as-is (brand names), but translate surrounding English
    ('designed for a comfortable, unhurried experience', 'concebido para uma experiência confortável e sem pressa'),
]


# ---------------------------------------------------------------------------
# Per-page translations
# Each entry: (path_relative_to_site_root, list_of_(old,new)_pairs)
# ---------------------------------------------------------------------------
PER_PAGE_TRANSLATIONS = {

    # ---- HOME ----------------------------------------------------------------
    "index.html": [
        ('<title>Lisbon Sintra Tours — Private Tours &amp; Bespoke Journeys in Portugal</title>',
         '<title>Lisbon Sintra Tours — Passeios Privados e Viagens à Medida em Portugal</title>'),
        ('content="Bespoke private tours of Lisbon, Sintra, and Portugal. Curated, unhurried journeys with expert local guides and luxury transport."',
         'content="Passeios privados à medida por Lisboa, Sintra e Portugal. Viagens cuidadas e sem pressa com guias locais especializados e transporte de luxo."'),
        ('content="Lisbon Sintra Tours — Bespoke Journeys in Portugal"',
         'content="Lisbon Sintra Tours — Viagens à Medida em Portugal"'),
        (' Bespoke Private Journeys', ' Viagens Privadas à Medida'),
        ('at the pace of wonder.', 'ao ritmo da maravilha.'),
        ('Private tours and considered itineraries through Lisbon, Sintra, the Douro and beyond — handcrafted by guides who know every cobblestone.',
         'Passeios privados e itinerários cuidados por Lisboa, Sintra, o Douro e além — artesanados por guias que conhecem cada calçada.'),
        ('A welcome, an invitation.', 'Uma boas-vindas, um convite.'),
        ('Lisbon Sintra Tours is a Lisbon-based agency designing tailor-made private tours, events and experiences across Portugal — from the palaces of Sintra to the vineyards of the Douro.',
         'A Lisbon Sintra Tours é uma agência sediada em Lisboa que cria passeios privados, eventos e experiências à medida por todo o Portugal — dos palácios de Sintra aos vinhedos do Douro.'),
        ('Our guides are local storytellers, our itineraries shaped around your pace and interests, and our pricing kept honest without compromising the quality that defines us.',
         'Os nossos guias são contadores de histórias locais, os nossos itinerários moldados ao seu ritmo e interesses, e os nossos preços mantidos honestos sem comprometer a qualidade que nos define.'),
        ('Signature Journeys', 'Viagens Icónicas'),
        ('Three ways to fall for Portugal.', 'Três formas de se apaixonar por Portugal.'),
        ('Romanticist Sintra', 'Sintra Romântica'),
        ("Pena Palace, Quinta da Regaleira and the cliffs of Cabo da Roca — a single, elegant day in Sintra&#x27;s storybook landscape.",
         'O Palácio da Pena, a Quinta da Regaleira e as falésias do Cabo da Roca — um dia único e elegante na paisagem de conto de fadas de Sintra.'),
        ("From Alfama&#x27;s alleys to the Tower of Belém — the capital&#x27;s seven hills and the warmest pastel de nata in the city.",
         'Das ruelas da Alfama à Torre de Belém — as sete colinas da capital e o pastel de nata mais quentinho da cidade.'),
        ('The Sanctuary of Fátima, medieval Óbidos and the gothic monasteries of Batalha and Alcobaça.',
         'O Santuário de Fátima, Óbidos medieval e os mosteiros góticos de Batalha e Alcobaça.'),
        ('A country worth lingering in.', 'Um país que vale a pena saborear.'),
        ('Palaces in the mist', 'Palácios na névoa'),
        ('Trams &amp; azulejos', 'Elétricos &amp; azulejos'),
        ('Vineyards by the river', 'Vinhedos junto ao rio'),
        ('Where land ends', 'Onde a terra acaba'),
        ('Pilgrimage &amp; quiet', 'Peregrinação &amp; sossego'),
        ('Pastéis &amp; monasteries', 'Pastéis &amp; mosteiros'),
        ('Douro Valley', 'Vale do Douro'),
        ('The Experience', 'A Experiência'),
        ('Quietly luxurious, deeply personal.', 'Discretamente luxuoso, profundamente pessoal.'),
        ('English-speaking private guides', 'Guias privados com fluência em inglês'),
        ('Mercedes V-Class &amp; executive sedans', 'Mercedes V-Class &amp; berlinas executivas'),
        ('Advanced purchase tickets for key attractions', 'Bilhetes comprados antecipadamente para as principais atrações'),
        ('Hand-picked restaurants &amp; tastings', 'Restaurantes e provas cuidadosamente selecionados'),
        ('Itineraries refined entirely around you', 'Itinerários construídos inteiramente à sua medida'),
        ("&quot;Our day in Sintra felt like a private chapter from a novel. We&#x27;ve travelled everywhere — and we&#x27;ve never been so quietly looked after.&quot;",
         '&quot;O nosso dia em Sintra pareceu um capítulo privado de um romance. Viajámos por todo o lado — e nunca fomos tão discretamente bem tratados.&quot;'),
        ('Helena &amp; James · London', 'Helena &amp; James · Londres'),
        ("Tell us your Portugal — we&#x27;ll compose the journey.",
         'Diga-nos o seu Portugal — nós composemos a viagem.'),
        ('Bespoke private tours', 'Passeios privados personalizados'),
        ('Local expert guides', 'Guias locais especializados'),
    ],

    # ---- TOURS INDEX ---------------------------------------------------------
    "tours/index.html": [
        ('<title>Tours — Lisbon Sintra Tours</title>',
         '<title>Passeios Privados em Portugal — Lisbon Sintra Tours</title>'),
        ('Our Journeys', 'As Nossas Viagens'),
        ('Curated tours, composed for you.', 'Passeios cuidados, compostos para si.'),
        ('Each itinerary is a starting point — every detail tunable to your pace, your tastes, your time.',
         'Cada itinerário é um ponto de partida — cada detalhe ajustável ao seu ritmo, aos seus gostos, ao seu tempo.'),
        ('Full day · 8h', 'Dia completo · 8h'),
        ('Full day · 4h', 'Dia completo · 4h'),
        ('>Romanticist Sintra<', '>Sintra Romântica<'),
        ('Pena Palace, Quinta da Regaleira and the Romantic-era estates that made Sintra a UNESCO World Heritage Site.',
         'Palácio da Pena, Quinta da Regaleira e as quintas da época Romântica que tornaram Sintra Património Mundial da UNESCO.'),
        ('Pena Palace', 'Palácio da Pena'),
        ('Belém Tower', 'Torre de Belém'),
        ('Jerónimos Monastery', 'Mosteiro dos Jerónimos'),
        ('The capital from Alfama to Belém — miradouros, azulejos, the Tower, the Monastery and pastéis straight from the oven.',
         'A capital de Alfama a Belém — miradouros, azulejos, a Torre, o Mosteiro e pastéis acabados de sair do forno.'),
        ('The Sanctuary of Fátima paired with medieval Óbidos, the gothic monasteries of Batalha and Alcobaça, and Nazaré.',
         'O Santuário de Fátima a par com Óbidos medieval, os mosteiros góticos de Batalha e Alcobaça, e Nazaré.'),
        ('Sanctuary of Fátima', 'Santuário de Fátima'),
        ('Batalha Monastery', 'Mosteiro da Batalha'),
        ('The Algarve — three days of Atlantic coast, sea caves and golden beaches at a pace that lets you breathe.',
         'O Algarve — três dias na costa atlântica, grutas marinhas e praias douradas a um ritmo que deixa respirar.'),
        ('The Portuguese Riviera — Sintra, Cabo da Roca and Cascais in a single, unhurried day along the Atlantic coast.',
         'A Riviera Portuguesa — Sintra, Cabo da Roca e Cascais num único dia descontraído ao longo da costa atlântica.'),
        ('Lisbon Sunset Cruise — four private hours on the Tagus at golden hour.',
         'Cruzeiro ao Pôr do Sol em Lisboa — quatro horas privadas no Tejo à hora dourada.'),
        ('Porto and Aveiro — two cities shaped by water, visited over two unhurried days from Lisbon.',
         'Porto e Aveiro — duas cidades moldadas pela água, visitadas em dois dias tranquilos a partir de Lisboa.'),
        ('Porto — the UNESCO-listed medieval Ribeira, the port wine lodges of Gaia, and Livraria Lello, over two days.',
         'Porto — a Ribeira medieval classificada pela UNESCO, as caves de vinho do Porto em Gaia e a Livraria Lello, em dois dias.'),
        ('The Templars\' headquarters at Tomar, the castle of Almourol on its island, and the mysteries of the Order of Christ.',
         'A sede dos Templários em Tomar, o castelo de Almourol na sua ilha e os mistérios da Ordem de Cristo.'),
        ('Évora and the Alentejo — the Roman temple, the Chapel of Bones, and a winery tasting in the afternoon sun.',
         'Évora e o Alentejo — o templo romano, a Capela dos Ossos e uma prova de vinhos ao sol da tarde.'),
        ('Fátima and Central Portugal — the Sanctuary, Batalha, Alcobaça and Óbidos in a single extraordinary day.',
         'Fátima e Portugal Central — o Santuário, Batalha, Alcobaça e Óbidos num único dia extraordinário.'),
        ('Portugal in three days — Lisbon, Sintra, Fátima and Óbidos at a pace designed for ease and pleasure.',
         'Portugal em três dias — Lisboa, Sintra, Fátima e Óbidos a um ritmo concebido para facilidade e prazer.'),
        ('Read more', 'Saiba mais'),
        ('Enquire', 'Contactar'),
        ('Day Tours', 'Passeios de Um Dia'),
        ('Multi-Day', 'Vários Dias'),
        ('Speciality', 'Especiais'),
        ('All Tours', 'Todos os Passeios'),
        # Tour page names in list
        ('Lisbon &amp; Belém', 'Lisboa &amp; Belém'),
        ('Lisbon Sunset Cruise', 'Cruzeiro ao Pôr do Sol em Lisboa'),
        ('Porto and Aveiro', 'Porto e Aveiro'),
        ('Porto City', 'Cidade do Porto'),
        ('Relaxing Algarve', 'Algarve Relaxante'),
        ('Relaxing Portugal', 'Portugal Relaxante'),
        ('Templar Portugal', 'Portugal dos Templários'),
        ('Royal Sintra', 'Sintra Real'),
        ('The Portuguese Riviera', 'A Riviera Portuguesa'),
        ('Évora and Alentejo', 'Évora e o Alentejo'),
        ('Fátima &amp; Central Portugal', 'Fátima &amp; Portugal Central'),
    ],

    # ---- ABOUT ---------------------------------------------------------------
    "about/index.html": [
        ('<title>About — Lisbon Sintra Tours</title>',
         '<title>Sobre Nós — Lisbon Sintra Tours</title>'),
        ('content="Nearly two decades of designing private, unhurried journeys through Portugal."',
         'content="Quase duas décadas a criar viagens privadas e sem pressa por Portugal."'),
        ('Our Story', 'A Nossa História'),
        ('A small house, a quiet craft.', 'Uma pequena casa, um ofício tranquilo.'),
        ('Founded in Lisbon in 2008 — guides, drivers and storytellers, working in service of slower, more thoughtful travel.',
         'Fundados em Lisboa em 2008 — guias, condutores e contadores de histórias, ao serviço de uma viagem mais lenta e mais pensada.'),
        ('The House', 'A Casa'),
        ('An atelier of journeys.', 'Um ateliê de viagens.'),
        ('We began as a single guide and a small Mercedes parked outside Rossio station. Today we are a small team of licensed guides, drivers and itinerary planners — but the way we work has not changed.',
         'Começámos como um único guia e um pequeno Mercedes estacionado fora da estação do Rossio. Hoje somos uma pequena equipa de guias licenciados, condutores e planeadores de itinerários — mas a forma como trabalhamos não mudou.'),
        ('Every traveller is met by name. Every tour begins with a conversation, not a checklist. And every journey is shaped, by hand, around the people who will live it.',
         'Cada viajante é recebido pelo nome. Cada passeio começa com uma conversa, não com uma lista. E cada viagem é moldada, à mão, em torno das pessoas que a vão viver.'),
        ('We are members of APAVT, fully insured, and proudly local. Lisbon is our home; Portugal is the story we love most to tell.',
         'Somos membros da APAVT, totalmente segurados e orgulhosamente locais. Lisboa é a nossa casa; Portugal é a história que mais amamos contar.'),
        ('Our Promise', 'A Nossa Promessa'),
        ('Five quiet commitments.', 'Cinco compromissos silenciosos.'),
        ('Always private. Never a coach, never a crowd.', 'Sempre privados. Nunca autocarro, nunca multidão.'),
        ('Always licensed. Every guide is officially accredited.', 'Sempre licenciados. Cada guia está oficialmente acreditado.'),
        ('Always punctual. Door-to-door, on the dot.', 'Sempre pontuais. Porta a porta, na hora certa.'),
        ('Always honest pricing. No hidden fees, no commissions.', 'Sempre preços honestos. Sem taxas ocultas, sem comissões.'),
        ('Always reachable. A real person, every day, around the clock during your trip.',
         'Sempre acessíveis. Uma pessoa real, todos os dias, a qualquer hora durante a sua viagem.'),
        ("Shall we start with a conversation?", 'Começamos com uma conversa?'),
    ],

    # ---- CONTACT -------------------------------------------------------------
    "contact/index.html": [
        ('<title>Contact — Lisbon Sintra Tours</title>',
         '<title>Contacto — Lisbon Sintra Tours</title>'),
        ('content="Begin planning your private tour of Portugal. We reply within one working day."',
         'content="Comece a planear o seu passeio privado por Portugal. Respondemos num dia útil."'),
        ('>Begin<', '>Começar<'),
        ('Tell us about your Portugal.', 'Conte-nos sobre o seu Portugal.'),
        ('A few details — we&#x27;ll write back within one working day with thoughts, an outline, and a quiet recommendation or two.',
         'Alguns detalhes — responderemos num dia útil com ideias, um esboço e uma ou duas recomendações.'),
        ('Reach us directly', 'Contacte-nos diretamente'),
        ('Some journeys begin with a letter.', 'Algumas viagens começam com uma carta.'),
        ('>Email<', '>Email<'),
        ('Office hours', 'Horário de atendimento'),
        ('Mon–Sat, 09:00 – 19:00 WET', 'Seg–Sáb, 09:00 – 19:00 WET'),
        ('>Atelier<', '>Ateliê<'),
        ('Full Name', 'Nome Completo'),
        ('Your full name', 'O seu nome completo'),
        ('Email Address', 'Endereço de Email'),
        ('Tour Date', 'Data do Passeio'),
        ('Number of Guests', 'Número de Convidados'),
        ('Children in the group?', 'Crianças no grupo?'),
        ('How many?', 'Quantas?'),
        ('Ages needed for car seat requirements', 'Idades necessárias para requisitos de cadeira de automóvel'),
        ('Mobile / Cell Number', 'Número de Telemóvel'),
        ('Please include your country code', 'Por favor inclua o código do país'),
        ('This number has WhatsApp', 'Este número tem WhatsApp'),
        ('Tour(s) of Interest', 'Passeio(s) de Interesse'),
        ('Select one or more — optional', 'Selecione um ou mais — opcional'),
        ('Day Tours', 'Passeios de Um Dia'),
        ('Multi-Day', 'Vários Dias'),
        ('Lisbon &amp; Belém', 'Lisboa &amp; Belém'),
        ("data-tour=\"Lisbon Sunset Cruise\"", 'data-tour="Cruzeiro ao Pôr do Sol"'),
        ("data-tour=\"Relaxing Algarve\"", 'data-tour="Algarve Relaxante"'),
        ("data-tour=\"Relaxing Portugal\"", 'data-tour="Portugal Relaxante"'),
        ('Lisbon Address', 'Morada em Lisboa'),
        ("Where you'd like to be picked up from — if you know",
         'Onde deseja ser recolhido — se souber'),
        ('Hotel name or address', 'Nome do hotel ou morada'),
        ('>Message<', '>Mensagem<'),
        ('Any other details, wishes, or specific needs', 'Quaisquer outros detalhes, desejos ou necessidades específicas'),
        ('Tell us a little about the trip you have in mind…', 'Conte-nos um pouco sobre a viagem que tem em mente…'),
    ],

    # ---- TOUR PAGES ----------------------------------------------------------
    "tours/romanticist-sintra/index.html": [
        ('<title>Romanticist Sintra | Pena, Monseratte, Cascais &amp; Cabo da Roca</title>',
         '<title>Sintra Romântica | Pena, Monseratte, Cascais &amp; Cabo da Roca</title>'),
        ('content="A private day tour through Romantic Sintra — Pena Palace and Monseratte, the historic town and National Palace, then west to Cabo da Roca at the edge of Europe and south along the coast to Cascais."',
         'content="Um passeio privado de um dia pela Sintra Romântica — Palácio da Pena e Monseratte, a vila histórica e o Palácio Nacional, depois para oeste até ao Cabo da Roca no extremo da Europa e para sul ao longo da costa até Cascais."'),
        ('content="Romanticist Sintra | Pena, Monseratte, Cascais &amp; Cabo da Roca"',
         'content="Sintra Romântica | Pena, Monseratte, Cascais &amp; Cabo da Roca"'),
        ('>Private Tour<', '>Passeio Privado<'),
        ('Sintra, a Romanticist Dream', 'Sintra, um Sonho Romântico'),
        ('Embark on the Romanticist Sintra day tour, exploring the enchanting Portuguese town known for its fairy-tale architecture and lush landscapes. Visit the colorful Pena Palace, wander Sintra\'s charming historic centre, and marvel at the amazing Palace of Monseratte and its wonderful gardens. Discover Sintra\'s romantic allure, steeped in history and natural beauty.',
         'Embarque no passeio de um dia pela Sintra Romântica, explorando a encantadora vila portuguesa conhecida pela sua arquitetura de conto de fadas e paisagens exuberantes. Visite o colorido Palácio da Pena, percorra o charmoso centro histórico de Sintra e maravilhe-se com o magnífico Palácio de Monseratte e os seus jardins extraordinários. Descubra o romantismo de Sintra, impregnado de história e beleza natural.'),
        ('Sintra was the obsession of the Romantics — Byron called it a "glorious Eden", and the Portuguese nobility built their fantasy palaces here through the nineteenth century, competing with each other in extravagance and invention. The result is unlike anywhere else in Europe: a mountain town covered in palaces, its atmosphere hovering somewhere between fairytale and dream.',
         'Sintra foi a obsessão dos Românticos — Byron chamou-lhe um "Éden glorioso", e a nobreza portuguesa construiu aqui os seus palácios de fantasia ao longo do século XIX, competindo uns com os outros em extravagância e invenção. O resultado é único na Europa: uma vila serrana coberta de palácios, com uma atmosfera suspensa algures entre o conto de fadas e o sonho.'),
        ('This day takes in the two great Romantic commissions — the Pena Palace, its towers and turrets erupting from the hilltop in yellow and terracotta, and Monseratte, an Orientalist confection deep in the park with its own extraordinary gardens. Between them, time in the historic town centre, where the Sintra National Palace has stood since the Moorish era. Then the road west to Cabo da Roca — the true edge of Europe — and south along the coast to Cascais before the drive back to Lisbon.',
         'Este dia inclui as duas grandes obras Românticas — o Palácio da Pena, com as suas torres e torreões a emergir do cimo da colina em amarelo e terracota, e o Monseratte, uma confeitaria orientalista no coração do parque com os seus jardins extraordinários. Entre eles, tempo no centro histórico, onde o Palácio Nacional de Sintra se erguia desde a era moura. Depois a estrada para oeste até ao Cabo da Roca — o verdadeiro fim da Europa — e para sul ao longo da costa até Cascais antes de regressar a Lisboa.'),
        ('The day covers a lot of ground but never feels hurried. The landscapes between stops — the pinewoods on the way to the cape, the coastal road south through Estoril — are part of the experience.',
         'O dia percorre muito terreno mas nunca se sente apressado. As paisagens entre paragens — os pinheais no caminho para o cabo, a estrada costeira para sul através do Estoril — fazem parte da experiência.'),
    ],

    "tours/royal-sintra/index.html": [
        ('<title>Royal Sintra | Queluz, Mafra, Sintra &amp; Pena Palace</title>',
         '<title>Sintra Real | Queluz, Mafra, Sintra &amp; Palácio da Pena</title>'),
        ('content="A private day tour tracing the Portuguese monarchy\'s great building works — the Baroque palace at Queluz, the vast monastery-palace at Mafra, the Sintra National Palace, and Pena Palace above the hills."',
         'content="Um passeio privado de um dia a traçar as grandes obras da monarquia portuguesa — o palácio Barroco de Queluz, o vasto mosteiro-palácio de Mafra, o Palácio Nacional de Sintra e o Palácio da Pena acima das colinas."'),
        ('content="Royal Sintra | Queluz, Mafra, Sintra &amp; Pena Palace"',
         'content="Sintra Real | Queluz, Mafra, Sintra &amp; Palácio da Pena"'),
        ('The Royal Sintra Tour', 'O Passeio Real por Sintra'),
        ('Discover Portugal&#x27;s regal heritage on a Royal Sintra Tour. Visit the elegant **Queluz Palace**, known as the "Portuguese Versailles," and the grand **Mafra Palace**, a Baroque masterpiece. Explore the enchanting **Sintra National Palace** in the town\'s historic center, then ascend to the breathtaking **Pena Palace**, perched above Sintra\'s lush hills. Immerse yourself in history, architecture, and stunning landscapes on this unforgettable journey.',
         'Descubra o património real de Portugal neste Passeio Real por Sintra. Visite o elegante **Palácio de Queluz**, conhecido como o "Versailles português", e o grandioso **Palácio de Mafra**, uma obra-prima Barroca. Explore o encantador **Palácio Nacional de Sintra** no centro histórico da vila, e depois suba ao deslumbrante **Palácio da Pena**, erguido acima das colinas verdejantes de Sintra.'),
        ('The Portuguese monarchy spent four centuries building in and around the Sintra hills, and the scale of their ambition is still visible today. This day traces that tradition from its most playful — Queluz, the pink Baroque palace that served as the royal summer retreat — to its most monumental.',
         'A monarquia portuguesa passou quatro séculos a construir nas colinas de Sintra e arredores, e a escala da sua ambição ainda é visível hoje. Este dia traça essa tradição desde a sua expressão mais lúdica — Queluz, o palácio Barroco cor-de-rosa que servia de retiro real de verão — até à mais monumental.'),
        ('Queluz comes first, its gardens laid out in the French manner, fountains playing in the morning quiet. Then north to Mafra, where King João V built a palace-monastery-basilica complex to rival anything in Europe, completing it with a workforce of fifty thousand. The Mafra Library alone — two storeys of carved cherrywood, thirty-six thousand rare volumes — is worth the journey. The afternoon brings Sintra itself: the Sintra National Palace in the town square, medieval and complex, its twin chimneys rising above the rooftops; and the Pena Palace above it all, the most exuberant building in Portugal.',
         'Queluz vem primeiro, com os seus jardins traçados à maneira francesa, fontanários a jogar no silêncio da manhã. Depois para norte até Mafra, onde o Rei D. João V construiu um complexo palácio-mosteiro-basílica para rivalizar com qualquer coisa na Europa, completando-o com uma mão-de-obra de cinquenta mil pessoas. Só a Biblioteca de Mafra — dois andares de cerejeira entalhada, trinta e seis mil volumes raros — vale a viagem. A tarde traz a própria Sintra: o Palácio Nacional de Sintra na praça da vila, medieval e complexo, com as suas duas chaminés a elevar-se acima dos telhados; e o Palácio da Pena acima de tudo, o edifício mais exuberante de Portugal.'),
        ('The tour is long but the stops are well-paced, and each place is so different from the last that the day never feels repetitive.',
         'O passeio é longo, mas as paragens têm um ritmo equilibrado, e cada lugar é tão diferente do anterior que o dia nunca se torna repetitivo.'),
        ('Admission tickets for all sites', 'Bilhetes de entrada para todos os locais'),
    ],

    "tours/lisbon-and-belem/index.html": [
        ('<title>Lisbon and Belém | Private Day Tour</title>',
         '<title>Lisboa e Belém — Passeio Privado de Um Dia</title>'),
        ('content="A private day tour through old Lisbon — Alfama, the grand squares of Baixa, and west along the Tagus to Belém, where the Jerónimos Monastery, Belém Tower, and the original pastéis de nata all wait."',
         'content="Um passeio privado pela Lisboa antiga — Alfama, as grandes praças da Baixa, e para oeste ao longo do Tejo até Belém, onde o Mosteiro dos Jerónimos, a Torre de Belém e os originais pastéis de nata aguardam."'),
        ('content="Lisbon and Belém | Private Day Tour"',
         'content="Lisboa e Belém | Passeio Privado de Um Dia"'),
        ('>Lisbon and Belém<', '>Lisboa e Belém<'),
        ('Discover the best of Lisbon and Belém on a one-day tour. Explore Lisbon\'s historic neighbourhoods like Alfama and Baixa, marvel at landmarks like Praça do Comércio and São Jorge Castle, and enjoy breathtaking views. In Belém, visit iconic sites like Jerónimos Monastery and Belém Tower. Don\'t miss tasting the famous *pastéis de Belém*. A perfect blend of history, culture, and delicious treats awaits you in this unforgettable day.',
         'Descubra o melhor de Lisboa e Belém neste passeio de um dia. Explore os bairros históricos de Lisboa como a Alfama e a Baixa, maravilhe-se com monumentos como a Praça do Comércio e o Castelo de São Jorge, e desfrute de vistas deslumbrantes. Em Belém, visite locais icónicos como o Mosteiro dos Jerónimos e a Torre de Belém. Não perca a prova dos famosos *pastéis de Belém*. Uma combinação perfeita de história, cultura e iguarias deliciosas aguarda-o neste dia inesquecível.'),
        ('Lisbon rewards those who walk it slowly. This day does exactly that — beginning in the old Moorish quarter of Alfama, where the streets narrow to the width of a cart and the city opens below in sudden views, then descending through the great squares of Baixa before heading west along the river to Belém.',
         'Lisboa recompensa quem a percorre devagar. Este dia faz exatamente isso — começa no antigo bairro mourisco da Alfama, onde as ruas se estreitam até à largura de uma carroça e a cidade se abre em baixo em vistas repentinas, depois descendo pelas grandes praças da Baixa antes de seguir para oeste ao longo do rio até Belém.'),
        ('Belém is where the Age of Discovery launched from. The Jerónimos Monastery was built to celebrate Vasco da Gama\'s return from India; Belém Tower stood as the last thing sailors saw as they left, and the first thing they saw on returning. The Monument to the Discoveries traces the faces of those who made the voyages possible. It is a compact but extraordinarily rich quarter — and the pastel de nata at the original Pastéis de Belém bakery, eaten with cinnamon and powdered sugar, is reason enough to make the journey.',
         'Belém é o ponto de partida da Época dos Descobrimentos. O Mosteiro dos Jerónimos foi construído para celebrar o regresso de Vasco da Gama da Índia; a Torre de Belém era a última coisa que os marinheiros viam ao partir e a primeira ao regressar. O Padrão dos Descobrimentos traça os rostos de quem tornou as viagens possíveis. É um bairro compacto mas extraordinariamente rico — e o pastel de nata na pastelaria original dos Pastéis de Belém, comido com canela e açúcar em pó, é razão suficiente para fazer a viagem.'),
        ('The day is structured but unhurried, with time built in for the moments that can\'t be scheduled — the viewpoint that stops you, the café that calls you in.',
         'O dia é estruturado mas sem pressa, com tempo reservado para os momentos que não se podem agendar — o miradouro que nos detém, o café que nos chama.'),
    ],

    "tours/fatima-central-portugal/index.html": [
        ('<title>Fátima, Batalha, Alcobaça &amp; Óbidos | Private Day Tour from Lisbon</title>',
         '<title>Fátima, Batalha, Alcobaça e Óbidos — Passeio Privado de Um Dia a partir de Lisboa</title>'),
        ('content="A private day tour through central Portugal — the Sanctuary of Fátima, the Gothic monastery at Batalha, the royal tombs at Alcobaça, and the medieval walled village of Óbidos."',
         'content="Um passeio privado pelo centro de Portugal — o Santuário de Fátima, o mosteiro gótico de Batalha, os túmulos reais de Alcobaça e a aldeia medieval muralhada de Óbidos."'),
        ('Fátima and Central Portugal', 'Fátima e Portugal Central'),
        ('Discover the spiritual heart of Portugal with our *Fátima and Central Portugal Tour from Lisbon*. Visit the renowned Sanctuary of Fátima, a world-famous pilgrimage site, and explore charming medieval towns like Batalha, Alcobaça, and Óbidos. Marvel at stunning monasteries, lush landscapes, and captivating coastal views. Perfect for history lovers, culture enthusiasts, and spiritual travelers.',
         'Descubra o coração espiritual de Portugal com o nosso *Passeio por Fátima e Portugal Central a partir de Lisboa*. Visite o afamado Santuário de Fátima, local de peregrinação de renome mundial, e explore encantadoras vilas medievais como Batalha, Alcobaça e Óbidos. Maravilhe-se com mosteiros deslumbrantes, paisagens exuberantes e vistas costeiras cativantes. Perfeito para amantes da história, entusiastas da cultura e viajantes espirituais.'),
        ('Central Portugal is a region of monasteries and medieval towns — places built with conviction, in stone that has outlasted the kingdoms that commissioned them. This day links four of the finest: Fátima, Batalha, Alcobaça, and Óbidos.',
         'O centro de Portugal é uma região de mosteiros e vilas medievais — lugares construídos com convicção, em pedra que sobreviveu aos reinos que os encomendaram. Este dia liga quatro dos mais notáveis: Fátima, Batalha, Alcobaça e Óbidos.'),
        ('Fátima needs little introduction. The Sanctuary draws millions of pilgrims each year, but the basilica square has a grandeur that transcends denomination — vast, still, and strangely moving. Batalha\'s monastery is a masterpiece of Manueline Gothic, its unfinished chapels open to the sky as if still awaiting their roof. Alcobaça holds the tombs of Portugal\'s earliest kings and queens, the stone carved with a fineness that still astonishes. Óbidos ends the day gently: a walled medieval village where the main street is lined with white houses and bougainvillea, and the local cherry liqueur is served in a chocolate cup.',
         'Fátima não precisa de grande apresentação. O Santuário atrai milhões de peregrinos por ano, mas a praça da basílica tem uma grandiosidade que transcende a denominação — vasta, silenciosa e estranhamente comovente. O mosteiro de Batalha é uma obra-prima do Gótico Manuelino, as suas capelas inacabadas abertas ao céu como se ainda aguardassem o telhado. Alcobaça alberga os túmulos dos primeiros reis e rainhas de Portugal, a pedra esculpida com uma fineza que ainda hoje surpreende. Óbidos encerra o dia com suavidade: uma aldeia medieval muralhada onde a rua principal é ladeada de casas brancas e buganvílias, e a ginjinha local é servida numa chávena de chocolate.'),
        ('The route traces the spine of central Portugal, through landscapes that open and close as the hills roll past.',
         'O percurso traça a espinha dorsal do centro de Portugal, através de paisagens que se abrem e fecham à medida que as colinas se sucedem.'),
    ],

    "tours/evora-and-alentejo/index.html": [
        ('<title>Évora and Alentejo | Private Day Tour from Lisbon</title>',
         '<title>Évora e Alentejo — Passeio Privado de Um Dia a partir de Lisboa</title>'),
        ('content="A private day tour from Lisbon into the Alentejo — UNESCO-listed Évora, the Roman Temple, the Chapel of Bones, and the open plain beyond, with a winery or estate tasting in the afternoon."',
         'content="Um passeio privado de Lisboa ao Alentejo — Évora Património Mundial da UNESCO, o Templo Romano, a Capela dos Ossos, e a planície aberta, com uma prova de vinhos à tarde."'),
        ('Évora and Alentejo', 'Évora e o Alentejo'),
        ('Discover the charm of Évora and Alentejo on this enriching day tour from Lisbon. Explore Évora\'s UNESCO-listed historic center, marvel at the Roman Temple and the eerie Chapel of Bones, and stroll its medieval streets. Venture into Alentejo\'s countryside, renowned for rolling vineyards and olive groves. Enjoy local wines, traditional cuisine, and stunning landscapes, offering a perfect blend of history, culture, and natural beauty on this unforgettable journey.',
         'Descubra o encanto de Évora e do Alentejo neste enriquecedor passeio de um dia a partir de Lisboa. Explore o centro histórico de Évora, classificado pela UNESCO, maravilhe-se com o Templo Romano e a inquietante Capela dos Ossos, e passeie pelas suas ruas medievais. Aventure-se pela campo alentejano, famoso pelas suas vinhas e olivais. Desfrute de vinhos locais, gastronomia tradicional e paisagens deslumbrantes.'),
        ('Évora sits an hour and a half east of Lisbon, beyond the soft hills where the city gives way to open plain. It is one of Portugal\'s best-preserved medieval cities — a UNESCO World Heritage Site that wears its history lightly, its whitewashed streets punctuated by a Roman temple that has stood since the first century.',
         'Évora fica a hora e meia a leste de Lisboa, além das suaves colinas onde a cidade dá lugar à planície aberta. É uma das cidades medievais mais bem preservadas de Portugal — Património Mundial da UNESCO que usa a sua história com leveza, as suas ruas caiadas pontuadas por um templo romano que se ergue desde o século I.'),
        ('The day takes in the temple, the cathedral, and the extraordinary Chapel of Bones — a Franciscan meditation on mortality, its walls lined with the remains of monks. Then out into the Alentejo proper: rolling cork oak and olive groves, a winery or estate for a tasting, the particular quiet of a landscape that has barely changed in centuries.',
         'O dia inclui o templo, a catedral e a extraordinária Capela dos Ossos — uma meditação franciscana sobre a mortalidade, com as paredes revestidas pelos restos de monges. Depois, para o interior do Alentejo: sobreiros e olivais ondulantes, uma quinta ou herdade para uma prova, a quietude peculiar de uma paisagem que quase não mudou em séculos.'),
        ('It is a day that moves between the ancient and the pastoral, between stone and open sky. The return to Lisbon comes as the light is changing over the plain.',
         'É um dia que se move entre o antigo e o pastoril, entre a pedra e o céu aberto. O regresso a Lisboa chega quando a luz está a mudar sobre a planície.'),
    ],

    "tours/lisbon-sunset-cruise/index.html": [
        ('<title>Lisbon Sunset Cruise | Private Sailing on the Tagus</title>',
         '<title>Cruzeiro ao Pôr do Sol em Lisboa — Vela Privada no Rio Tejo</title>'),
        ('content="A private sailing experience on the Tagus at golden hour. Four unhurried hours, your group only — past Belém Tower, the 25 de Abril Bridge, and Lisbon\'s riverfront at its most beautiful."',
         'content="Uma experiência de vela privada no Tejo à hora dourada. Quatro horas sem pressa, apenas para o seu grupo — junto à Torre de Belém, a Ponte 25 de Abril e a frente ribeirinha de Lisboa na sua hora mais bela."'),
        ('Lisbon Sunset Cruise', 'Cruzeiro ao Pôr do Sol em Lisboa'),
        ('The Tagus at golden hour — Belém glowing from the water, the 25 de Abril Bridge burning copper, the city quietly magnificent from the river that made it.',
         'O Tejo à hora dourada — Belém a brilhar sobre a água, a Ponte 25 de Abril em cobre ardente, a cidade magnificentemente silenciosa vista do rio que a moldou.'),
        ('There is a particular quality to Lisbon seen from the water at the end of the day. The light turns amber, the hills soften, and the city — which can feel so alive and frenetic on foot — becomes something quieter and more elemental. The Sunset Cruise is built around that moment.',
         'Há uma qualidade particular em Lisboa vista da água no fim do dia. A luz fica âmbar, as colinas suavizam-se, e a cidade — que pode parecer tão viva e frenética a pé — torna-se algo mais quieto e mais elementar. O Cruzeiro ao Pôr do Sol é construído em torno desse momento.'),
        ('Over four unhurried hours, we sail the Tagus on a private boat — your group only, no strangers. The route takes you past the great monuments of the riverfront: Belém Tower rising from the water\'s edge, the Discoveries Monument catching the last of the light, the 25 de Abril Bridge burning copper against the sky. There is no commentary to follow and no fixed itinerary to keep to. Just the river, the wine, and the city at its most beautiful.',
         'Ao longo de quatro horas sem pressa, navegamos o Tejo num barco privado — apenas o seu grupo, sem estranhos. O percurso leva-o pelos grandes monumentos da frente ribeirinha: a Torre de Belém a elevar-se da margem da água, o Padrão dos Descobrimentos apanhando os últimos raios de luz, a Ponte 25 de Abril em cobre ardente contra o céu. Não há comentários a seguir nem itinerário fixo a cumprir. Apenas o rio, o vinho e a cidade no seu momento mais belo.'),
        ('The captain handles the sailing. But if you would like to take the helm for a stretch — and most guests do — that is entirely possible.',
         'O capitão trata da navegação. Mas se desejar assumir o leme por um trecho — e a maioria dos convidados faz-o — isso é inteiramente possível.'),
    ],

    "tours/portuguese-riviera/index.html": [
        ('<title>The Portuguese Riviera | Sintra, Cabo da Roca &amp; Cascais</title>',
         '<title>A Riviera Portuguesa — Sintra, Cabo da Roca e Cascais</title>'),
        ('content="A private day tour along the Portuguese Riviera — the palaces of Sintra, Cabo da Roca at the edge of Europe, and Cascais before the coast road home to Lisbon."',
         'content="Um passeio privado ao longo da Riviera Portuguesa — os palácios de Sintra, o Cabo da Roca no extremo ocidental da Europa e Cascais antes da estrada costeira de regresso a Lisboa."'),
        ('The Portuguese Riviera', 'A Riviera Portuguesa'),
        ('Discover elegance and charm on The Portuguese Riviera Tour. Explore glamorous Cascais, with its beautiful beaches and vibrant marina, and stroll through the enchanting streets of Sintra, home to fairytale palaces and lush gardens. Visit Cabo da Roca, the westernmost point of Europe, for stunning ocean views. This tour combines natural beauty, historical treasures, and coastal sophistication, offering a memorable journey along Portugal\'s breathtaking Riviera.',
         'Descubra elegância e encanto na Riviera Portuguesa. Explore a glamorosa Cascais, com as suas belas praias e marina vibrante, e percorra as ruas encantadoras de Sintra, lar de palácios de conto de fadas e jardins exuberantes. Visite o Cabo da Roca, o ponto mais ocidental da Europa, com vistas deslumbrantes sobre o oceano. Este passeio combina beleza natural, tesouros históricos e sofisticação costeira, oferecendo uma viagem memorável ao longo da deslumbrante Riviera portuguesa.'),
        ('The thirty kilometres between Lisbon and Cabo da Roca — the westernmost point of mainland Europe — contain more beauty than most regions manage in a hundred. This day traces the coast through Sintra, out to the cape, and back along the Estoril line through Cascais: three utterly different places, unified by the Atlantic light.',
         'Os trinta quilómetros entre Lisboa e o Cabo da Roca — o ponto mais ocidental da Europa continental — contêm mais beleza do que a maioria das regiões consegue em cem. Este dia traça a costa por Sintra, até ao cabo e de volta pela linha do Estoril através de Cascais: três lugares absolutamente diferentes, unificados pela luz atlântica.'),
        ('Sintra is the centrepiece. The hills above the town are thick with palaces — the Pena with its fantastic colours, the Regaleira with its spiral well descending into the earth, the Sintra National Palace in the town square with its two great conical chimneys. Then the road west through the pines to Cabo da Roca, where the cliffs fall to the sea and the next land is the Americas.',
         'Sintra é o ponto central. As colinas acima da vila estão repletas de palácios — a Pena com as suas cores fantásticas, a Regaleira com o seu poço em espiral que desce à terra, o Palácio Nacional de Sintra na praça da vila com as suas duas grandes chaminés cónicas. Depois a estrada para oeste pelos pinheais até ao Cabo da Roca, onde os penhascos caem para o mar e a próxima terra são as Américas.'),
        ('Cascais feels like a gentle landing after all that drama — a seaside town that was once the summer retreat of the Portuguese royal family and still carries that air of unhurried elegance. The marina, Boca do Inferno, the streets behind the main square. The coast road back to Lisbon follows the railway line all the way, the sea never far from view.',
         'Cascais parece uma aterragem suave depois de todo esse drama — uma vila costeira que foi outrora o retiro de verão da família real portuguesa e que ainda carrega esse ar de elegância sem pressa. A marina, a Boca do Inferno, as ruas atrás da praça principal. A estrada costeira de regresso a Lisboa segue a linha de comboio até ao fim, com o mar nunca longe da vista.'),
    ],

    "tours/porto-and-aveiro/index.html": [
        ('<title>Porto and Aveiro | Two-Day Private Tour from Lisbon</title>',
         '<title>Porto e Aveiro — Passeio Privado de Dois Dias a partir de Lisboa</title>'),
        ('content="A two-day private tour from Lisbon — day one in UNESCO-listed Porto, with the Ribeira, the port wine lodges and Livraria Lello; day two in Aveiro, the lagoon city of moliceiro boats."',
         'content="Dois dias a partir de Lisboa — o primeiro no Porto Património Mundial da UNESCO, com a Ribeira, as caves de vinho do Porto e a Livraria Lello; o segundo em Aveiro, a cidade-lagoa dos barcos moliceiros."'),
        ('Porto and Aveiro', 'Porto e Aveiro'),
        ('Embark on a scenic two-day tour from Lisbon to Porto and Aveiro. Start by exploring Porto\'s historic Ribeira district, tasting port wine, and admiring the Douro River views. Next, visit Aveiro, known as the &quot;Venice of Portugal,&quot; with its colorful moliceiro boats and charming canals. Return to Lisbon, soaking in Portugal\'s rich history, culture, and landscapes along the way. A perfect blend of relaxation and adventure!',
         'Embarque num pitoresco passeio de dois dias de Lisboa ao Porto e Aveiro. Comece por explorar o histórico bairro da Ribeira no Porto, provar vinho do Porto e admirar as vistas sobre o Douro. De seguida, visite Aveiro, conhecida como a &quot;Veneza de Portugal,&quot; com os seus coloridos barcos moliceiros e encantadores canais. Regresse a Lisboa absorvendo a rica história, cultura e paisagens de Portugal. Uma combinação perfeita de descanso e aventura!'),
        ('Two cities in two days — Porto and Aveiro — both shaped by water, both utterly themselves. Porto sits above the Douro, its medieval Ribeira quarter reflected in the river, the port wine lodges of Vila Nova de Gaia just across the water. Aveiro spreads along a lagoon, its painted moliceiro boats drifting between banks of salt pans and art nouveau houses.',
         'Duas cidades em dois dias — Porto e Aveiro — ambas moldadas pela água, ambas absolutamente elas próprias. O Porto ergue-se sobre o Douro, com o seu bairro medieval da Ribeira refletido no rio, as caves de vinho do Porto de Vila Nova de Gaia mesmo do outro lado. Aveiro estende-se ao longo de uma lagoa, com os seus barcos moliceiros pintados a derivar entre margens de salinas e casas Arte Nova.'),
        ('Day one is Porto. The Ribeira district is a UNESCO World Heritage Site, its coloured facades facing the riverfront. São Bento station covers its walls in forty thousand azulejo tiles depicting the history of Portugal. The Clérigos Tower has watched over the city since 1763. Livraria Lello, one of the world\'s most celebrated bookshops, has been selling books since 1906. Across the Dom Luís I Bridge, the wine lodges of Gaia offer some of the finest port tastings in the country.',
         'O primeiro dia é o Porto. O bairro da Ribeira é Património Mundial da UNESCO, com as suas fachadas coloridas voltadas para a margem do rio. A estação de São Bento reveste as suas paredes com quarenta mil azulejos que retratam a história de Portugal. A Torre dos Clérigos vigia a cidade desde 1763. A Livraria Lello, uma das livrarias mais celebradas do mundo, vende livros desde 1906. Do outro lado da Ponte Dom Luís I, as caves de Gaia oferecem algumas das melhores provas de vinho do Porto do país.'),
        ('Day two turns south to Aveiro. A boat along the canals, the egg-yolk sweetness of ovos moles, the striped beach houses of Costa Nova just beyond the salt flats. Then the long road back to Lisbon as the light drops behind Portugal.',
         'O segundo dia vira para sul, em direção a Aveiro. Um barco pelos canais, a doçura de gema de ovo dos ovos moles, as casas de praia às riscas da Costa Nova mesmo além das salinas. Depois a longa estrada de regresso a Lisboa enquanto a luz cai por detrás de Portugal.'),
    ],

    "tours/porto-city/index.html": [
        ('<title>Porto City | Two-Day Private Tour from Lisbon</title>',
         '<title>Cidade do Porto — Passeio Privado de Dois Dias a partir de Lisboa</title>'),
        ('content="A two-day private tour from Lisbon to Porto — the UNESCO-listed Ribeira quarter, São Bento station, the Clérigos Tower, the port wine lodges of Vila Nova de Gaia and Livraria Lello."',
         'content="Um passeio privado de dois dias de Lisboa ao Porto — o bairro da Ribeira classificado pela UNESCO, a estação de São Bento, a Torre dos Clérigos, as caves de vinho do Porto em Vila Nova de Gaia e a Livraria Lello."'),
        ('Porto City', 'Cidade do Porto'),
        ('Experience a luxurious private Porto City car tour from Lisbon, combining comfort with adventure. Travel in style with a personal guide, stopping at iconic landmarks like the Ribeira District, Clérigos Tower, and the Dom Luís I Bridge. Explore hidden gems at your own pace and savour port wine tastings. Perfect for those seeking an intimate, flexible journey to uncover Porto\'s charm before a seamless return to Lisbon.',
         'Viva um luxuoso passeio privado de automóvel pela Cidade do Porto a partir de Lisboa, combinando conforto e aventura. Viaje em estilo com um guia pessoal, parando em marcos icónicos como o Bairro da Ribeira, a Torre dos Clérigos e a Ponte Dom Luís I. Explore tesouros escondidos ao seu próprio ritmo e saboreie provas de vinho do Porto. Perfeito para quem procura uma viagem íntima e flexível para descobrir o encanto do Porto antes de um regresso tranquilo a Lisboa.'),
        ('Porto is the kind of city that takes people by surprise. They expect something provincial and find something grand — a UNESCO-listed medieval quarter overhanging the Douro, a train station whose walls are covered in forty thousand azulejo tiles, a bookshop that has been selling books since 1906, wine cellars ageing port in the same dark warehouses for centuries.',
         'O Porto é o tipo de cidade que surpreende as pessoas. Esperam algo provincial e encontram algo grandioso — um bairro medieval classificado pela UNESCO debruçado sobre o Douro, uma estação de comboio cujas paredes estão cobertas com quarenta mil azulejos, uma livraria que vende livros desde 1906, caves de vinho a envelhecer porto nos mesmos armazéns escuros há séculos.'),
        ('This two-day private tour from Lisbon gives the city its proper due. The drive north takes around three hours; the route is straightforward and the countryside shifts — cork oak, vineyards, eucalyptus — as Portugal rolls past the windows. Arriving in Porto, the day opens at whatever pace suits your group. The Ribeira. The Dom Luís I Bridge. The wine lodges of Vila Nova de Gaia. The Clérigos Tower standing above the rooftops. Livraria Lello. São Bento station, where even arriving feels like an event.',
         'Este passeio privado de dois dias a partir de Lisboa dá à cidade o que lhe é devido. A viagem para norte demora cerca de três horas; o percurso é direto e a paisagem muda — sobreiros, vinhas, eucaliptos — enquanto Portugal passa pelas janelas. Chegando ao Porto, o dia abre-se ao ritmo que melhor convém ao seu grupo. A Ribeira. A Ponte Dom Luís I. As caves de Vila Nova de Gaia. A Torre dos Clérigos erguida acima dos telhados. A Livraria Lello. A estação de São Bento, onde até a chegada parece um acontecimento.'),
        ('The second day is yours to use — perhaps the Foz do Douro at the river\'s mouth, or Matosinhos for lunch by the sea, or simply more time in the streets. The return to Lisbon follows in the afternoon.',
         'O segundo dia é seu — talvez a Foz do Douro na foz do rio, ou Matosinhos para almoçar junto ao mar, ou simplesmente mais tempo nas ruas. O regresso a Lisboa segue-se à tarde.'),
        ('Admission tickets for key sites', 'Bilhetes de entrada para os locais principais'),
    ],

    "tours/relaxing-algarve/index.html": [
        ('<title>Relaxing Algarve | A Three-Day Private Tour</title>',
         '<title>Algarve Relaxante — Passeio Privado de Três Dias</title>'),
        ('content="A relaxed three-day private tour of Portugal\'s southern coast — beaches and sea caves, the cliffs of Sagres, Benagil, the Ria Formosa and Algarve food, at a pace that leaves room for doing nothing at all."',
         'content="Três dias na costa sul de Portugal — praias e grutas marinhas, as falésias de Sagres, Benagil, a Ria Formosa e a gastronomia do Algarve, ao ritmo de quem não tem pressa."'),
        ('Relaxing Algarve', 'Algarve Relaxante'),
        ('Escape to the Algarve for a relaxing 3-day retreat. Unwind on golden beaches, stroll through charming coastal towns, and savor fresh seafood. Spend leisurely afternoons exploring hidden coves, taking gentle boat rides, or lounging by the pool. Enjoy serene sunsets and the tranquil pace of life. Perfect for those seeking a peaceful getaway with no rush—just pure relaxation and the beauty of Portugal\'s stunning southern coast.',
         'Fuja para o Algarve num retiro de 3 dias. Descanse em praias douradas, passeie por encantadoras vilas costeiras e saboreie marisco fresco. Passe tardes descontraídas a explorar enseadas escondidas, a fazer passeios de barco suaves ou simplesmente a relaxar. Desfrute de pores do sol serenos e do ritmo tranquilo da vida algarvia. Perfeito para quem procura um escape pacífico sem pressa — pura relaxação e a beleza da deslumbrante costa sul de Portugal.'),
        ('The Algarve is best taken slowly. Three days of Atlantic coast, whitewashed fishing towns, and food that tastes of the sea — this itinerary is built for those who want to move at their own speed, with the landscape doing the work.',
         'O Algarve é melhor saboreado devagar. Três dias de costa atlântica, aldeias piscatórias caiadas e comida que sabe a mar — este itinerário é feito para quem quer mover-se ao seu próprio ritmo, com a paisagem a fazer o trabalho.'),
        ('The first day is arrival: settling into accommodation in Lagos, Albufeira or Vilamoura, finding the beach, remembering what unhurried feels like. Day two opens up the coast — the dramatic sea caves and cathedral rocks between Lagos and Ponta da Piedade, perhaps a boat along the water to reach the Benagil cave from the sea. The Fortress of Sagres, standing on its own promontory at the corner of Europe. Dinner of cataplana or grilled fish where the catch is always fresh.',
         'O primeiro dia é a chegada: instalar-se no alojamento em Lagos, Albufeira ou Vilamoura, encontrar a praia, recordar como se sente a vida sem pressa. O segundo dia abre a costa — as dramáticas grutas marinhas e rochas em catedral entre Lagos e a Ponta da Piedade, talvez um barco pela água até à gruta de Benagil pelo mar. A Fortaleza de Sagres, erguida no seu próprio promontório no canto da Europa. Jantar de cataplana ou peixe grelhado onde a apanha é sempre fresca.'),
        ('The third morning is for the Ria Formosa — the long, quiet lagoon that runs along the eastern Algarve — or a last beach, a last coffee in a harbour square. The drive back to Lisbon passes through a different Portugal: inland, agricultural, slower.',
         'A manhã do terceiro dia é para a Ria Formosa — a longa e calma lagoa que corre ao longo do Algarve oriental — ou uma última praia, um último café numa praça de porto. A viagem de regresso a Lisboa passa por um Portugal diferente: interior, agrícola, mais lento.'),
    ],

    "tours/relaxing-portugal/index.html": [
        ('<title>Relaxing Portugal | A Three-Day Private Tour</title>',
         '<title>Portugal Relaxante — Passeio Privado de Três Dias</title>'),
        ('content="A comfortable three-day private tour through Portugal\'s highlights — Lisbon and Belém, Sintra and Cascais, Fátima and Óbidos — at a pace that leaves room for lunch, lingering, and the unscheduled moments."',
         'content="Um passeio privado confortável de três dias pelos destaques de Portugal — Lisboa e Belém, Sintra e Cascais, Fátima e Óbidos — a um ritmo que deixa espaço para o almoço, o descanso e os momentos imprevistos."'),
        ('Relaxing Portugal', 'Portugal Relaxante'),
        ('Experience the best of Portugal with this relaxed 3-day tour designed for seniors. Explore Lisbon\'s historic landmarks, enjoy the fairytale charm of Sintra and Cascais, and visit the serene Sanctuary of Fátima. Discover the medieval beauty of Óbidos and savor traditional Portuguese cuisine. With a comfortable pace and handpicked highlights, this journey offers a perfect blend of culture, history, and scenic relaxation.',
         'Viva o melhor de Portugal com este passeio relaxante de 3 dias. Explore os marcos históricos de Lisboa, aprecie o encanto de conto de fadas de Sintra e Cascais, e visite o sereno Santuário de Fátima. Descubra a beleza medieval de Óbidos e saboreie a gastronomia portuguesa tradicional. Com um ritmo confortável e destaques criteriosamente selecionados, esta viagem oferece uma combinação perfeita de cultura, história e relaxação paisagística.'),
        ('This three-day tour was designed with ease in mind — for those who want to see Portugal\'s finest places without being rushed through them. The pace is deliberate, the distances manageable, and the itinerary has been chosen for its balance of the extraordinary and the restful.',
         'Este passeio de três dias foi concebido com conforto em mente — para quem quer ver os lugares mais belos de Portugal sem ser apressado. O ritmo é deliberado, as distâncias são geríveis, e o itinerário foi escolhido pelo seu equilíbrio entre o extraordinário e o repousante.'),
        ('Day one stays close to Lisbon — Belém\'s Jerónimos Monastery and the Tower, the long sweep of Eduardo VII Park up to the viewpoint above the city, a riverside dinner as the evening comes in. Day two ventures to Sintra, where the palaces are genuinely fantastic in the original sense — the Pena Palace perched above cloud, the gardens of the Regaleira hiding their secrets — before coming down to the sea at Cascais for the afternoon. Day three takes a different direction entirely: north to Fátima, where the basilica square has a particular stillness, and then to the medieval village of Óbidos, its white walls and cobbled streets unchanged in centuries.',
         'O primeiro dia fica perto de Lisboa — o Mosteiro dos Jerónimos de Belém e a Torre, o longo traçado do Parque Eduardo VII até ao miradouro acima da cidade, um jantar à beira-rio ao cair da tarde. O segundo dia aventura-se até Sintra, onde os palácios são genuinamente fantásticos no sentido original — o Palácio da Pena pousado acima das nuvens, os jardins da Regaleira a esconder os seus segredos — antes de descer ao mar em Cascais pela tarde. O terceiro dia toma uma direção completamente diferente: para norte até Fátima, onde a praça da basílica tem uma imobilidade particular, e depois até à aldeia medieval de Óbidos, com as suas paredes brancas e ruas de calçada inalteradas ao longo dos séculos.'),
        ('Each day has space built into it — for lunch, for a long look at something, for sitting in a square with a glass of something cold.',
         'Cada dia tem espaço construído — para o almoço, para uma longa contemplação, para se sentar numa praça com um copo de algo fresco.'),
        ('Admission tickets for key sites', 'Bilhetes de entrada para os locais principais'),
        ('designed for a comfortable, unhurried experience', 'concebido para uma experiência confortável e sem pressa'),
    ],

    "tours/templar-portugal/index.html": [
        ('<title>Templar Portugal | Tomar and Almourol</title>',
         '<title>Portugal dos Templários — Tomar e Almourol</title>'),
        ('content="A private day tour following the Knights Templar through Portugal — the Convent of Christ in Tomar, the castle of Almourol on its island in the Tagus, and the legacy of the Order of Christ."',
         'content="Um passeio privado de um dia a seguir os Cavaleiros Templários por Portugal — o Convento de Cristo em Tomar, o castelo de Almourol na sua ilha no Tejo, e o legado da Ordem de Cristo."'),
        ('Templar Portugal', 'Portugal dos Templários'),
        ('Uncover the secrets of the Knights Templar on a captivating 1-day tour of Templar Portugal. Visit Tomar\'s Convent of Christ, a UNESCO World Heritage Site and Templar stronghold. Explore the medieval Castle of Almourol, perched on a river island, and learn about the Templars\' fascinating history. Stroll through Tomar\'s historic streets and discover the legacy of one of Europe\'s most enigmatic medieval orders.',
         'Descubra os segredos dos Cavaleiros Templários neste cativante passeio de 1 dia pelo Portugal dos Templários. Visite o Convento de Cristo em Tomar, Património Mundial da UNESCO e fortaleza templária. Explore o medieval Castelo de Almourol, erguido numa ilha fluvial, e conheça a fascinante história dos Templários. Passeie pelas ruas históricas de Tomar e descubra o legado de uma das ordens medievais mais enigmáticas da Europa.'),
        ('The Knights Templar arrived in Portugal in the twelfth century and never really left. The Order was dissolved everywhere else in Europe, but in Portugal it simply changed its name — becoming the Order of Christ — and kept its headquarters in Tomar, where it continued to shape the country for another three hundred years. This day follows that thread.',
         'Os Cavaleiros Templários chegaram a Portugal no século XII e nunca partiram verdadeiramente. A Ordem foi dissolvida em todo o resto da Europa, mas em Portugal simplesmente mudou de nome — tornando-se a Ordem de Cristo — e manteve a sua sede em Tomar, onde continuou a moldar o país por mais trezentos anos. Este dia segue esse fio.'),
        ('Tomar is built around the Convent of Christ, a UNESCO World Heritage Site that contains nine centuries of Portuguese history within a single complex. The Templar Charola — the octagonal rotunda at its heart, modelled on the Church of the Holy Sepulchre — is still standing. The Manueline window on the chapter house is one of the most extraordinary carvings in Portugal: stone worked to the point where it seems to dissolve into rope and coral and armillary spheres. From Tomar, the route drops down to the Tagus at Almourol, where a Templar castle occupies its own island in the middle of the river — accessible only by boat, and all the more atmospheric for it.',
         'Tomar está construída em torno do Convento de Cristo, Património Mundial da UNESCO que contém nove séculos de história portuguesa num único complexo. A Charola Templária — a rotunda octogonal no seu coração, modelada na Igreja do Santo Sepulcro — ainda está de pé. A janela Manuelina da sala do capítulo é uma das talhas mais extraordinárias de Portugal: pedra trabalhada até ao ponto em que parece dissolver-se em corda e coral e esferas armilares. De Tomar, o percurso desce até ao Tejo em Almourol, onde um castelo templário ocupa a sua própria ilha no meio do rio — acessível apenas de barco, e tanto mais atmosférico por isso.'),
        ('The return passes through the quiet towns of the Ribatejo, the landscape flat and open, the river wide beside the road.',
         'O regresso passa pelas vilas tranquilas do Ribatejo, a paisagem plana e aberta, o rio largo à beira da estrada.'),
        ('Admission tickets for all sites', 'Bilhetes de entrada para todos os locais'),
    ],

    # ---- DESTINATIONS INDEX --------------------------------------------------
    "destinations/index.html": [
        ('<title>Destinations — Lisbon Sintra Tours</title>',
         '<title>Destinos — Lisbon Sintra Tours</title>'),
        ('content="From the cliffs of Sintra to the vineyards of the Douro — discover the destinations we love most."',
         'content="Das falésias de Sintra aos vinhedos do Douro — descubra os destinos que mais amamos."'),
        ('The Portugal worth knowing.', 'O Portugal que vale a pena conhecer.'),
        ('From the Atlantic cliffs of Cabo da Roca to the schist villages of the Douro Valley — these are the places we return to again and again.',
         'Das falésias atlânticas do Cabo da Roca às aldeias de xisto do Vale do Douro — estes são os lugares a que voltamos sempre.'),
    ],

    # ---- BLOG INDEX ----------------------------------------------------------
    "blog/index.html": [
        ('<title>Travel Journal — Lisbon Sintra Tours</title>',
         '<title>Diário de Viagem — Lisbon Sintra Tours</title>'),
        ('content="Stories, guides and insider notes from Lisbon, Sintra and across Portugal — written by our local guides."',
         'content="Histórias, guias e notas privilegiadas de Lisboa, Sintra e por todo o Portugal — escritas pelos nossos guias locais."'),
        ('Travel Journal', 'Diário de Viagem'),
        ('Stories and insider notes from the field.', 'Histórias e notas privilegiadas do terreno.'),
        ('Read more', 'Saiba mais'),
    ],

    # ---- PRIVACY POLICY ------------------------------------------------------
    "privacy-policy/index.html": [
        ('<title>Privacy Policy | Lisbon Sintra Tours</title>',
         '<title>Política de Privacidade | Lisbon Sintra Tours</title>'),
        ('Privacy Policy', 'Política de Privacidade'),
        ('This privacy policy sets out how', 'Esta política de privacidade descreve como'),
        ('uses and protects any information that you give', 'utiliza e protege quaisquer informações que nos forneça'),
        ('when you use this website or business services.', 'quando utiliza este website ou os nossos serviços.'),
    ],

    # ---- THANK YOU -----------------------------------------------------------
    "thank-you/index.html": [
        ('<title>Thank You — Lisbon Sintra Tours</title>',
         '<title>Obrigado — Lisbon Sintra Tours</title>'),
        ('Thank you.', 'Obrigado.'),
        ("Thank you for your enquiry. We&#x27;ll be in touch within one working day.",
         'Obrigado pela sua mensagem. Entraremos em contacto dentro de um dia útil.'),
        ("We'll be in touch soon.", 'Entraremos em contacto em breve.'),
        ('Return home', 'Voltar ao início'),
    ],

    # ---- LANDING PAGES -------------------------------------------------------
    "car-service/index.html": [
        ('<title>Private Car Service - Lisbon &amp; Portugal</title>',
         '<title>Serviço de Automóvel Privado - Lisboa &amp; Portugal</title>'),
        ('Private Car Service', 'Serviço de Automóvel Privado'),
        ('Private Car Services in Lisbon and Portugal with professional drivers.',
         'Serviços de Automóvel Privado em Lisboa e Portugal com condutores profissionais.'),
        ('airport transfers', 'transferes aeroportuários'),
        ('city transfers', 'transferes entre cidades'),
        ('Reliable Airport Transfers in Lisbon', 'Transferes Aeroportuários Fiáveis em Lisboa'),
    ],

    "sintra-tours/index.html": [
        ('<title>Our Sintra Tour Selection | Lisbon Sintra Tours</title>',
         '<title>A Nossa Seleção de Passeios em Sintra | Lisbon Sintra Tours</title>'),
        ('The Sintra Selection', 'A Seleção de Sintra'),
    ],

    "private-tours-sintra/index.html": [
        ('<title>Private Tours Sintra | Lisbon Sintra Tours</title>',
         '<title>Passeios Privados em Sintra | Lisbon Sintra Tours</title>'),
        ('Private Tours - Sintra', 'Passeios Privados — Sintra'),
    ],

    "transport-services/index.html": [
        ('<title>Transport Services - Group Transfers, City &amp; Airport Transfers</title>',
         '<title>Serviços de Transporte — Transferes, Cidades e Aeroportos</title>'),
        ('Transport Services', 'Serviços de Transporte'),
    ],

    "luxury-private-transport/index.html": [
        ('<title>Luxury Private Transport in Lisbon – VIP Services</title>',
         '<title>Transporte Privado de Luxo em Lisboa — Serviços VIP</title>'),
        ('Luxury Private Transport in Lisbon – VIP Services', 'Transporte Privado de Luxo em Lisboa — Serviços VIP'),
    ],

    "one-day-tours-from-lisbon/index.html": [
        ('<title>Our Day Tours from Lisbon | Lisbon Sintra Tours</title>',
         '<title>Os Nossos Passeios de Um Dia a partir de Lisboa | Lisbon Sintra Tours</title>'),
        ('Single Day Tours from Lisbon', 'Passeios de Um Dia a partir de Lisboa'),
    ],

    "next-day-and-same-day-sintra-tours/index.html": [
        ('<title>Next Day and Same Day Sintra Tours</title>',
         '<title>Passeios a Sintra no Próprio Dia e no Dia Seguinte</title>'),
        ('Next Day and Same Day Sintra Tours', 'Passeios a Sintra no Próprio Dia e no Dia Seguinte'),
    ],

    "lisbon-wine-tours/index.html": [
        ('<title>Lisbon Wine Tours | LST Blog</title>',
         '<title>Provas de Vinho em Lisboa | Lisbon Sintra Tours</title>'),
        ('Lisbon Wine Tours', 'Provas de Vinho em Lisboa'),
    ],

    "lisbon-art-tours/index.html": [
        ('<title>Lisbon Art Tours | LST Blog</title>',
         '<title>Passeios de Arte em Lisboa | Lisbon Sintra Tours</title>'),
        ('Lisbon Art Tours', 'Passeios de Arte em Lisboa'),
    ],

    "lisbon-festivals-and-events/index.html": [
        ('<title>Lisbon Festivals and Events | LST Blog</title>',
         '<title>Festivais e Eventos em Lisboa | Lisbon Sintra Tours</title>'),
        ('Lisbon Festivals and Events', 'Festivais e Eventos em Lisboa'),
    ],

    "car-tours-from-lisbon-to-sintra/index.html": [
        ('<title>Car Tours From Lisbon to Sintra</title>',
         '<title>Passeios de Automóvel de Lisboa a Sintra</title>'),
        ('Car Tours From Lisbon to Sintra', 'Passeios de Automóvel de Lisboa a Sintra'),
    ],

    "private-group-tours-portugal/index.html": [
        ('<title>Private Group Tours in Portugal: Make the most of your Trip</title>',
         '<title>Passeios em Grupo Privado em Portugal — Aproveite ao Máximo a sua Viagem</title>'),
        ('Private Group Tours in Portugal: Make your Trip An Unforgettable Experience',
         'Passeios em Grupo Privado em Portugal: Torne a sua Viagem numa Experiência Inesquecível'),
    ],

    # ---- DESTINATIONS --------------------------------------------------------
    "destinations/lisbon/index.html": [
        ('<title>Lisbon City Guide  | Lisbon Sintra Tours</title>',
         '<title>Guia da Cidade de Lisboa | Lisbon Sintra Tours</title>'),
        ('Lisbon City Guide', 'Guia da Cidade de Lisboa'),
        ('A city of seven hills, three rivers, and a thousand shades of blue and gold.',
         'Uma cidade de sete colinas, três rios e mil tons de azul e dourado.'),
    ],

    "destinations/algarve/index.html": [
        ('<title>The Algarve — Lisbon Sintra Tours</title>',
         '<title>O Algarve — Lisbon Sintra Tours</title>'),
        ('>The Algarve<', '>O Algarve<'),
    ],

    "destinations/arrabida/index.html": [
        ('<title>Arrábida — Lisbon Sintra Tours</title>',
         '<title>Arrábida — Lisbon Sintra Tours</title>'),
    ],

    "destinations/cabo-da-roca/index.html": [
        ('<title>All about Cabo da Roca in Portugal</title>',
         '<title>Tudo sobre o Cabo da Roca em Portugal</title>'),
        ('All about Cabo da Roca in Portugal', 'Tudo sobre o Cabo da Roca em Portugal'),
    ],

    "destinations/coimbra/index.html": [
        ('<title>Coimbra — Lisbon Sintra Tours</title>',
         '<title>Coimbra — Lisbon Sintra Tours</title>'),
    ],

    "destinations/evora/index.html": [
        ('<title>Évora — Lisbon Sintra Tours</title>',
         '<title>Évora — Lisbon Sintra Tours</title>'),
    ],

    "destinations/fatima/index.html": [
        ('<title>Fátima, the Catholic Pilgrimage Site</title>',
         '<title>Fátima, o Local de Peregrinação Católica</title>'),
        ('Fátima, the Catholic Pilgrimage Site', 'Fátima, o Local de Peregrinação Católica'),
    ],

    "destinations/jeronimos-monastery/index.html": [
        ('<title>Jerónimos Monastery | LST Blog</title>',
         '<title>Mosteiro dos Jerónimos | Lisbon Sintra Tours</title>'),
        ('Jerónimos Monastery', 'Mosteiro dos Jerónimos'),
    ],

    "destinations/nazare/index.html": [
        ('<title>Nazaré — Lisbon Sintra Tours</title>',
         '<title>Nazaré — Lisbon Sintra Tours</title>'),
    ],

    "destinations/obidos/index.html": [
        ('<title>Óbidos — Lisbon Sintra Tours</title>',
         '<title>Óbidos — Lisbon Sintra Tours</title>'),
    ],

    "destinations/porto/index.html": [
        ('<title>Porto City Guide  | Lisbon Sintra Tours</title>',
         '<title>Guia da Cidade do Porto | Lisbon Sintra Tours</title>'),
        ('Porto City Guide', 'Guia da Cidade do Porto'),
    ],

    "destinations/romanticism-in-portugal/index.html": [
        ('<title>Romanticism in Portugal | LST Blog</title>',
         '<title>O Romantismo em Portugal | Lisbon Sintra Tours</title>'),
        ('Romanticism in Portugal', 'O Romantismo em Portugal'),
    ],

    "destinations/the-castles-and-palaces-of-sintra/index.html": [
        ('<title>The Castles and Palaces of Sintra</title>',
         '<title>Os Castelos e Palácios de Sintra</title>'),
        ('The Castles and Palaces of Sintra', 'Os Castelos e Palácios de Sintra'),
    ],

    "destinations/the-portuguese-riviera/index.html": [
        ('<title>The Portuguese Riviera | LST Blog</title>',
         '<title>A Riviera Portuguesa | Lisbon Sintra Tours</title>'),
        ('The Portuguese Riviera', 'A Riviera Portuguesa'),
    ],

    "destinations/tomar-and-the-knights-templar/index.html": [
        ('<title>Tomar and the Knights Templar | LST Blog</title>',
         '<title>Tomar e os Cavaleiros Templários | Lisbon Sintra Tours</title>'),
        ('Tomar and the Knights Templar', 'Tomar e os Cavaleiros Templários'),
    ],

    "destinations/tomar/index.html": [
        ('<title>Tomar — Lisbon Sintra Tours</title>',
         '<title>Tomar — Lisbon Sintra Tours</title>'),
    ],

    # ---- BLOG POSTS ----------------------------------------------------------
    "blog/getting-around-in-style/index.html": [
        ('<title>Luxury Private Travel in Portugal</title>',
         '<title>Viagem Privada de Luxo em Portugal</title>'),
        ('Getting Around in Style: Luxury Private Transport in Portugal',
         'Mover-se em Estilo: Transporte Privado de Luxo em Portugal'),
    ],

    "blog/have-you-discovered-braga/index.html": [
        ('<title>Have You Discovered Braga? | LST Blog</title>',
         '<title>Já Descobriu Braga? | Lisbon Sintra Tours</title>'),
        ('Have You Discovered Braga?', 'Já Descobriu Braga?'),
    ],

    "blog/how-to-get-from-lisbon-to-sintra/index.html": [
        ('<title>How to get from Lisbon to Sintra</title>',
         '<title>Como ir de Lisboa a Sintra</title>'),
        ('How to get from Lisbon to Sintra', 'Como ir de Lisboa a Sintra'),
    ],

    "blog/how-to-plan-a-stress-free-senior-friendly-trip-to-portugal/index.html": [
        ('<title>How to Plan a Stress-Free, Senior-Friendly Trip to Portugal</title>',
         '<title>Como Planear uma Viagem a Portugal Sem Stress, Adequada a Seniores</title>'),
        ('How to Plan a Stress-Free, Senior-Friendly Trip to Portugal',
         'Como Planear uma Viagem a Portugal Sem Stress, Adequada a Seniores'),
    ],

    "blog/lisbon-tops-the-happiest-city-index/index.html": [
        ('<title>Lisbon Tops The Happiest City Index</title>',
         '<title>Lisboa Lidera o Índice das Cidades Mais Felizes</title>'),
        ('Lisbon Tops The Happiest City Index', 'Lisboa Lidera o Índice das Cidades Mais Felizes'),
    ],

    "blog/lisbons-alternative-neighbourhoods/index.html": [
        ('<title>A Tour of Lisbon&#x27;s Alternative Neighbourhoods</title>',
         '<title>Um Passeio pelos Bairros Alternativos de Lisboa</title>'),
        ("A Tour of Lisbon's Alternative Neighbourhoods",
         'Um Passeio pelos Bairros Alternativos de Lisboa'),
    ],

    "blog/lisbons-hidden-gems/index.html": [
        ('<title>Lisbon&#x27;s Hidden Gems | LST Blog</title>',
         '<title>As Joias Escondidas de Lisboa | Lisbon Sintra Tours</title>'),
        ("Lisbon's Hidden Gems", 'As Joias Escondidas de Lisboa'),
    ],

    "blog/lisbons-luxury-private-events/index.html": [
        ('<title>Luxury Private Events in Lisbon: Venues, Planning &amp; What to Expect</title>',
         '<title>Eventos Privados de Luxo em Lisboa: Locais, Planeamento e O Que Esperar</title>'),
        ('Luxury Private Events in Lisbon: A Complete Planning Guide',
         'Eventos Privados de Luxo em Lisboa: Um Guia Completo de Planeamento'),
    ],

    "blog/lux-global-excellence-awards-2025/index.html": [
        ('<title>Lisbon Sintra Tours Wins Two LUX Global Excellence Awards 2025</title>',
         '<title>Lisbon Sintra Tours Ganha Dois LUX Global Excellence Awards 2025</title>'),
        ('Two LUX Global Excellence Awards 2025', 'Dois LUX Global Excellence Awards 2025'),
        ('Lisbon Sintra Tours Wins Two LUX Global Excellence Awards 2025',
         'Lisbon Sintra Tours Ganha Dois LUX Global Excellence Awards 2025'),
    ],

    "blog/one-day-in-sintra/index.html": [
        ('<title>One Day in Sintra: The Perfect Itinerary | Lisbon Sintra Tours</title>',
         '<title>Um Dia em Sintra: O Itinerário Perfeito | Lisbon Sintra Tours</title>'),
        ('One Day in Sintra: The Perfect Itinerary', 'Um Dia em Sintra: O Itinerário Perfeito'),
    ],

    "blog/the-best-day-trips-from-lisbon/index.html": [
        ('<title>The Best Day Trips from Lisbon</title>',
         '<title>Os Melhores Passeios de Um Dia a partir de Lisboa</title>'),
        ('The Best Day Trips from Lisbon', 'Os Melhores Passeios de Um Dia a partir de Lisboa'),
    ],

    "blog/the-best-hotels-in-lisbon/index.html": [
        ('<title>The Best Hotels in Lisbon: Top Stays for Every Traveler</title>',
         '<title>Os Melhores Hotéis em Lisboa: As Melhores Estadias para Todo o Tipo de Viajante</title>'),
        ('The Best Hotels in Lisbon', 'Os Melhores Hotéis em Lisboa'),
    ],

    "blog/the-best-hotels-in-sintra/index.html": [
        ('<title>The Best Hotels in Sintra Portugal | LST Blog</title>',
         '<title>Os Melhores Hotéis em Sintra, Portugal | Lisbon Sintra Tours</title>'),
        ('The Best Hotels in Sintra Portugal', 'Os Melhores Hotéis em Sintra, Portugal'),
    ],

    "blog/the-best-restaurants-in-sintra-with-a-view/index.html": [
        ('<title>The Best Restaurants in Sintra with a View</title>',
         '<title>Os Melhores Restaurantes em Sintra com Vista</title>'),
        ('The Best Restaurants in Sintra with a View', 'Os Melhores Restaurantes em Sintra com Vista'),
    ],

    "blog/the-best-restaurants-in-sintra/index.html": [
        ('<title>The Best Restaurants in Sintra</title>',
         '<title>Os Melhores Restaurantes em Sintra</title>'),
        ('The Best Restaurants in Sintra', 'Os Melhores Restaurantes em Sintra'),
    ],

    "blog/the-top-tourist-attractions-in-portugal/index.html": [
        ('<title>The Top Tourist Attractions in Portugal</title>',
         '<title>As Principais Atrações Turísticas de Portugal</title>'),
        ('The Top Tourist Attractions in Portugal', 'As Principais Atrações Turísticas de Portugal'),
    ],

    "blog/web-summit-2022/index.html": [
        ('<title>Lisbon Web Summit | LST Blog</title>',
         '<title>Web Summit Lisboa | Lisbon Sintra Tours</title>'),
        ('Web Summit 2022', 'Web Summit 2022'),
    ],

    "blog/why-portugal-is-the-ideal-destination-for-history-loving-seniors/index.html": [
        ('<title>Why Portugal is the Ideal Destination for History-Loving Seniors</title>',
         '<title>Por Que Portugal é o Destino Ideal para Seniores Amantes da História</title>'),
        ('Why Portugal is the Ideal Destination for History-Loving Seniors',
         'Por Que Portugal é o Destino Ideal para Seniores Amantes da História'),
    ],

    "blog/why-visit-cascais/index.html": [
        ('<title>Why Visit Cascais | Lisbon Sintra Tours Blog</title>',
         '<title>Por Que Visitar Cascais | Lisbon Sintra Tours</title>'),
        ('Why Visit Cascais', 'Por Que Visitar Cascais'),
    ],

    "blog/wine-tourism-in-portugal/index.html": [
        ('<title>Wine Tourism in Portugal | LST Blog</title>',
         '<title>Turismo Vínico em Portugal | Lisbon Sintra Tours</title>'),
        ('Wine Tourism in Portugal', 'Turismo Vínico em Portugal'),
    ],

    "blog/winter-tours-to-sintra/index.html": [
        ('<title>Winter Tours to Sintra | LST Blog</title>',
         '<title>Passeios de Inverno a Sintra | Lisbon Sintra Tours</title>'),
        ('Winter Tours to Sintra', 'Passeios de Inverno a Sintra'),
    ],
}


# ---------------------------------------------------------------------------
# Path utility
# ---------------------------------------------------------------------------
def get_url_path(rel_path: str) -> str:
    """Convert relative file path to URL path, e.g. 'tours/index.html' -> '/tours/'"""
    if rel_path == "index.html":
        return "/"
    # strip trailing index.html
    parts = rel_path.replace("\\", "/")
    if parts.endswith("/index.html"):
        parts = parts[:-len("index.html")]
    elif parts == "index.html":
        return "/"
    return "/" + parts


def get_pt_equiv_path(url_path: str) -> str:
    """For PT toggle: strip leading slash for template fill, but keep for proper URL."""
    if url_path == "/":
        return ""
    return url_path.lstrip("/")


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------
def process_en_page(src_path: Path, rel_path: str) -> str:
    """Read EN page, add hreflang tags and PT toggle, return modified HTML."""
    html = src_path.read_text(encoding="utf-8")
    url_path = get_url_path(rel_path)
    equiv_pt = get_pt_equiv_path(url_path)

    # 1. Add hreflang
    html = inject_hreflang_en(html, url_path)
    # 2. Add PT toggle to nav
    html = add_en_toggle(html, equiv_pt)
    return html


def process_pt_page(src_path: Path, rel_path: str) -> str:
    """Create PT version of a page with translations and correct links."""
    html = src_path.read_text(encoding="utf-8")
    url_path = get_url_path(rel_path)
    equiv_en = get_pt_equiv_path(url_path)

    # 1. Set lang="pt"
    html = set_lang_pt(html)

    # 2. Apply common translations first
    for old, new in COMMON_TRANSLATIONS:
        html = html.replace(old, new)

    # 3. Apply per-page translations
    page_key = rel_path.replace("\\", "/")
    if page_key in PER_PAGE_TRANSLATIONS:
        for old, new in PER_PAGE_TRANSLATIONS[page_key]:
            html = html.replace(old, new)

    # 4. Prefix all internal links with /pt
    html = prefix_links(html)

    # 5. Add hreflang + canonical
    html = inject_hreflang_pt(html, url_path)

    # 6. Update og:url to PT version
    html = update_og_url(html, url_path)

    # 7. Strip the PT toggle that was on the EN source page, then add EN toggle
    html = strip_pt_toggle(html)
    html = add_pt_toggle(html, equiv_en)

    return html


def get_all_html_files():
    """Return all HTML file relative paths, sorted."""
    files = []
    for p in SITE_ROOT.rglob("*.html"):
        rel = str(p.relative_to(SITE_ROOT)).replace("\\", "/")
        # Skip any existing /pt/ files
        if rel.startswith("pt/"):
            continue
        files.append(rel)
    return sorted(files)


def main():
    html_files = get_all_html_files()
    print(f"Found {len(html_files)} HTML files to process.\n")

    created_count = 0
    updated_en_count = 0
    errors = []

    for rel_path in html_files:
        src_path = SITE_ROOT / rel_path

        try:
            # --- Update EN page in-place (add hreflang + PT toggle) ---
            en_html = process_en_page(src_path, rel_path)
            src_path.write_text(en_html, encoding="utf-8")
            updated_en_count += 1

            # --- Create PT version ---
            pt_rel_path = "pt/" + rel_path
            pt_path = SITE_ROOT / pt_rel_path
            pt_path.parent.mkdir(parents=True, exist_ok=True)

            pt_html = process_pt_page(src_path, rel_path)
            pt_path.write_text(pt_html, encoding="utf-8")
            created_count += 1

        except Exception as e:
            errors.append((rel_path, str(e)))

    print(f"Updated {updated_en_count} EN pages (hreflang + PT toggle).")
    print(f"Created {created_count} PT pages.")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for path, err in errors:
            print(f"  {path}: {err}")
    else:
        print("\nNo errors.")

    # --- Update sitemap ---
    update_sitemap()

    print("\nDone.")


def update_sitemap():
    sitemap_path = SITE_ROOT / "sitemap.xml"
    if not sitemap_path.exists():
        print("Sitemap not found, skipping.")
        return

    original = sitemap_path.read_text(encoding="utf-8")

    # Find all already-present URLs (so we don't duplicate)
    existing_locs = set(re.findall(r'<loc>(.*?)</loc>', original))

    # Parse EN URL blocks
    url_blocks = re.findall(r'<url>.*?</url>', original, re.DOTALL)

    new_entries = []

    for block in url_blocks:
        loc_match = re.search(r'<loc>(.*?)</loc>', block)
        if not loc_match:
            continue
        loc = loc_match.group(1)

        path_match = re.match(r'https?://(?:www\.)?lisbonsintratours\.com(/.*)', loc)
        if not path_match:
            continue
        path = path_match.group(1)

        # Skip if already a /pt/ URL
        if path.startswith("/pt/"):
            continue

        # Build the PT URL to add
        pt_path = "/pt" + path
        pt_url = f"https://www.lisbonsintratours.com{pt_path}"

        # Skip if already present
        if pt_url in existing_locs:
            continue

        # Get priority and lastmod from original
        priority_match = re.search(r'<priority>(.*?)</priority>', block)
        lastmod_match = re.search(r'<lastmod>(.*?)</lastmod>', block)
        priority = priority_match.group(1) if priority_match else "0.5"
        lastmod = lastmod_match.group(1) if lastmod_match else "2026-05-22"

        new_entry = f"""  <url>
    <loc>{pt_url}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
  </url>"""
        new_entries.append(new_entry)

    if new_entries:
        # Insert before closing </urlset>
        new_sitemap = original.replace(
            "</urlset>",
            "\n".join(new_entries) + "\n</urlset>"
        )
        sitemap_path.write_text(new_sitemap, encoding="utf-8")
        print(f"\nSitemap updated: added {len(new_entries)} PT URL entries.")
    else:
        print("\nSitemap: no new PT entries needed (already up to date).")


if __name__ == "__main__":
    main()
