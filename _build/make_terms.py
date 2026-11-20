#!/usr/bin/env python3
"""
Booking Terms & Conditions -> lst-terms.pdf

THIS FILE EXISTS BECAUSE THE LAST ONE DID NOT.
The terms were a PDF and nothing else: no source, no words anyone could edit,
no record of what they said before. Changing one line meant rebuilding the
whole document from a picture of it. So the words live here now, in TERMS
below, and the PDF is something this script makes.

    python3 _build/make_terms.py        # writes ../lst-terms.pdf

Rewritten 20 November 2026 for the large-groups-only model: seven and up,
every vehicle with its own guide, and smaller parties passed straight to an
independent guide. The old document was written around a car with four people
in it and said so in half a dozen places.

Typography follows the May 2026 document it replaces, which was also ReportLab:
Helvetica, A4, 85pt margins, gold #c8a852, roman numeral folios.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as rl_canvas

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(ROOT, 'lst-terms.pdf')
LOGO = os.path.join(ROOT, 'images', 'logo.png')

PAGE_W, PAGE_H = A4
MARGIN   = 85
COL_W    = PAGE_W - 2 * MARGIN
TOP_Y    = PAGE_H - 84
BOTTOM   = 86                     # text stops here; the footer lives below it

GOLD   = HexColor('#c8a852')
INK    = HexColor('#2c2c2c')
BODY   = HexColor('#3d3d3d')
MUTED  = HexColor('#6b6b6b')
FAINT  = HexColor('#989898')
RULE   = HexColor('#d8d2c4')

SANS = 'Helvetica'
BOLD = 'Helvetica-Bold'

ROMAN = ['', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii']


# ── THE WORDS ───────────────────────────────────────────────────────────────
# Every section is (title, [blocks]). A block is one of:
#   ('p',     text)                 a justified paragraph
#   ('label', text)                 letterspaced gold capitals
#   ('q',     text)                 a question, in the On the Day section
#   ('rows',  [(left, right), …])   an indented two-column list
#   ('gap',   points)

TERMS = [
("Fares & Prices", [
  ('p', "All fares and prices quoted are subject to availability. Prices may change "
        "until the deposit is received and the booking confirmed. Unless we advise "
        "otherwise, quoted prices include all applicable taxes and fees."),
  ('p', "Price is set by the size of your party, because the size of your party sets "
        "the vehicles and the vehicles set the guides. It does not rise smoothly with "
        "the number of people: it steps, at the point where one more guest needs a "
        "second vehicle, and therefore a second guide. We will tell you where the "
        "nearest step is before you commit, not after."),
  ('p', "Collection and drop-off at any hotel in Lisbon, Sintra or Cascais is "
        "complimentary. For any other location, please enquire."),
  ('p', "Prices are quoted for a full day (8 hours) or a half day (4 hours). A tour "
        "may be extended by agreement with the lead guide on the day, or with your "
        "booking manager in advance. An additional charge will apply."),
]),

("Your Party, and Final Numbers", [
  ('p', "We run private tours for groups of seven and up, and nothing else. Smaller "
        "parties are passed straight to a trusted independent guide who looks after "
        "you directly, with no mark-up and no middleman."),
  ('p', "Final numbers are due 21 days before the tour. We buy vehicles, guides and "
        "timed admission tickets against that figure, and it is the figure your final "
        "invoice is drawn on."),
  ('p', "Guests may be added after that date subject to the availability of a seat, a "
        "guide and a ticket for the same entrance time as the rest of your group. "
        "Where an addition crosses a vehicle threshold, the price steps, and we will "
        "say so in writing before anything is booked."),
  ('p', "Where numbers fall after that date, the price does not fall below the "
        "vehicles, guides and tickets already committed on your behalf."),
]),

("Entrance to Attractions", [
  ('p', "Admission fees to attractions are not included in our tour prices unless your "
        "quote says otherwise. For groups we will normally buy timed tickets on your "
        "behalf and itemise them, because the palaces at Sintra sell out and a timed "
        "slot for forty people is not something to leave until the week before."),
  ('p', "Tickets are non-refundable once bought, whether we bought them for you or you "
        "bought them yourself."),
]),

("Your Departure Point", [
  ('p', "Certain areas of Lisbon have restricted vehicular access. Where our vehicle "
        "cannot reach your hotel or accommodation directly, we will suggest the "
        "nearest suitable meeting point."),
  ('label', "THE ONE WORTH READING TWICE"),
  ('p', "A full-size coach cannot reach Pena Palace. The road up through the park is "
        "narrow and steep and has turns a long vehicle cannot take. Vehicles of about "
        "twenty-two seats and under go to the gate. Anything larger sets down in "
        "Sintra town and the group transfers up by shuttle, which works perfectly well "
        "and takes about forty minutes out of the day."),
  ('p', "Where this applies to your group it is written into your plan before you book. "
        "We would far rather you knew now than at ten past ten on the morning."),
]),

("Availability", [
  ('p', "All travel products and services offered through our site are subject to "
        "availability and may be withdrawn without notice. A date is held for you only "
        "once the deposit has been received."),
]),

("Cancellation Policy", [
  ('p', "We maintain a flexible cancellation policy for your comfort. Plans change, and "
        "we are happy to move your booking to another date, subject to availability, at "
        "no extra charge."),
  ('gap', 6),
  ('label', "IF YOU CANCEL"),
  ('rows', [
     ("Cancelled 45 days or more before the trip", "100% refund"),
     ("Cancelled between 45 and 14 days before",   "50% refund"),
     ("Cancelled less than 14 days before",        "No refund"),
  ]),
  ('gap', 10),
  ('label', "GENERAL"),
  ('p', "No-shows are non-refundable. Tickets to events or attractions are "
        "non-refundable. Hotel reservations are non-refundable unless we have specified "
        "otherwise in writing."),
  ('gap', 10),
  ('label', "IF WE CANCEL"),
  ('p', "If we cancel your tour, which is rare and would be for reasons of safety or "
        "something genuinely outside our control, you may take another date or have "
        "every euro back. The choice is yours, not ours."),
]),

("Payment", [
  ('p', "A deposit of 30% confirms your booking and holds the date. The balance is due "
        "14 days before the tour. Where a booking is made inside 14 days, the full "
        "amount is due at the time of booking."),
  ('p', "We accept payment by bank transfer. We hold accounts in EUR, USD, GBP and AUD, "
        "with other currencies available on request. Full account details are provided "
        "on the accompanying Bank Payment Details sheet."),
  ('p', "We offer accounts in several countries and currencies to minimise your fees. "
        "Where transfer fees apply, they must be covered at your end, as we need to "
        "receive the full amount stated in your quote."),
  ('p', "Exceptionally, for last-minute bookings and with the booking manager's express "
        "consent, payment may be made in cash on the day of the tour."),
]),

("Booking Fees & Taxes", [
  ('p', "All reservations include applicable taxes and VAT. As we do not accept card "
        "payments, a small booking fee is applied and itemised on your quote."),
]),

("On the Day", [
  ('q', "What type of vehicle will it be?"),
  ('p', "The size of your party decides it, and your quote names the vehicle. Recent "
        "models, clean, comfortable and air-conditioned throughout."),
  ('rows', [
     ("Up to 7 guests",  "Mercedes V-Class"),
     ("8 to 15",         "Sprinter van"),
     ("16 to 22",        "Midi-coach"),
     ("23 and above",    "More than one vehicle, each with its own guide"),
  ]),
  ('gap', 8),
  ('q', "Will the guide come into the attractions with us?"),
  ('p', "Yes. Your guide is with you inside, not waiting at the vehicle. Where your "
        "group fills more than one vehicle there is a guide in each of them, because a "
        "guide cannot be in two coaches at once and half a group without one is not a "
        "private tour."),
  ('q', "How much of the day is the road?"),
  ('p', "Between Lisbon and Sintra we allow a full hour each way, whichever end you "
        "start from. It is forty minutes on a quiet Tuesday in February and an hour and "
        "a quarter on a Saturday in May, and a plan built on the forty is a plan that "
        "runs late all day. On a full day, two of the eight hours are the road."),
  ('q', "Is lunch included?"),
  ('p', "Unless explicitly agreed with your booking manager, meals are not included in "
        "the price. We are happy to arrange it. For a larger group a set menu agreed "
        "beforehand is not a downgrade - it is the only thing that works, as most of "
        "the places a small party would love cannot seat a large one and will not take "
        "the booking."),
  ('q', "What about tipping?"),
  ('p', "If you are happy with your day, tipping is welcome and entirely at your "
        "discretion. As a guide, we suggest €50 for each guide and €30 for each "
        "driver. On a day with more than one vehicle, that is one of each per vehicle."),
]),
]

INTRO = ("A plain reading of how a booking works with us: numbers, payment, "
         "cancellation, and what to expect on the day. Written to be re-read; "
         "nothing here is buried in small print.")


# ── THE TYPESETTER ──────────────────────────────────────────────────────────

class Doc:
    def __init__(self, path):
        self.c = rl_canvas.Canvas(path, pagesize=A4)
        self.c.setTitle('Booking Terms & Conditions')
        self.c.setAuthor('Lisbon Sintra Tours')
        self.c.setSubject('Lisbon Sintra Tours - Booking Terms & Conditions')
        self.page = 0
        self.y = TOP_Y

    # Letterspaced text. setCharSpace adds the space AFTER every glyph including
    # the last, so the measured width overshoots by one space; take it off again
    # or centred labels sit a hair left of centre.
    def spaced(self, text, x, y, font, size, colour, space, align='l'):
        w = stringWidth(text, font, size) + space * (len(text) - 1)
        if align == 'c':
            x -= w / 2
        elif align == 'r':
            x -= w
        # Character spacing lives on a text object, not on the canvas - and it
        # is graphics state, so it stays set for everything drawn afterwards
        # unless it is put back. Left set, it letterspaced the entire document
        # and starved the justifier, which measures with stringWidth and so
        # had no idea the glyphs had grown.
        t = self.c.beginText(x, y)
        t.setFont(font, size)
        t.setFillColor(colour)
        t.setCharSpace(space)
        t.textOut(text)
        t.setCharSpace(0)
        self.c.drawText(t)
        return w

    def wrap(self, text, font, size, width):
        words, lines, cur = text.split(), [], []
        for word in words:
            trial = cur + [word]
            if stringWidth(' '.join(trial), font, size) <= width or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = [word]
        if cur:
            lines.append(cur)
        return lines

    def para(self, text, size=9.6, leading=14.2, colour=BODY, font=SANS,
             indent=0, justify=True, space_after=9):
        width = COL_W - indent
        lines = self.wrap(text, font, size, width)
        self.c.setFillColor(colour)
        for i, words in enumerate(lines):
            self.room(leading)
            last = (i == len(lines) - 1)
            self.c.setFont(font, size)
            if justify and not last and len(words) > 1:
                plain = stringWidth(''.join(words), font, size)
                gap = (width - plain) / (len(words) - 1)
                x = MARGIN + indent
                for w in words:
                    self.c.drawString(x, self.y, w)
                    x += stringWidth(w, font, size) + gap
            else:
                self.c.drawString(MARGIN + indent, self.y, ' '.join(words))
            self.y -= leading
        self.y -= space_after

    def room(self, need):
        """Break the page when the next line would cross into the footer."""
        if self.y - need < BOTTOM:
            self.end_page()
            self.new_page()

    def rows(self, pairs, indent=34, size=9.3, leading=15.5):
        # A list of four broke after the second one and finished the vehicle
        # ladder on the next page. Short blocks move whole or not at all.
        self.room(leading * len(pairs))
        label_w = max(stringWidth(a, SANS, size) for a, _ in pairs) + 16
        for left, right in pairs:
            self.c.setFont(SANS, size)
            self.c.setFillColor(BODY)
            self.c.drawString(MARGIN + indent, self.y, left)
            self.c.setFillColor(MUTED)
            self.c.drawString(MARGIN + indent + label_w, self.y, '-')
            self.c.setFillColor(INK)
            self.c.drawString(MARGIN + indent + label_w + 14, self.y, right)
            self.y -= leading
        self.y -= 4

    def label(self, text, space_before=4, space_after=9):
        self.room(20)
        self.y -= space_before
        self.spaced(text, MARGIN, self.y, SANS, 8, GOLD, 1.6)
        self.y -= space_after + 5

    def question(self, text):
        # Keep with what follows. A question needs its answer beside it, so it
        # claims room for itself plus a few lines; otherwise it sits alone at
        # the foot of a page asking nothing.
        self.room(104)
        self.y -= 4
        self.c.setFont(SANS, 10.6)
        self.c.setFillColor(INK)
        self.c.drawString(MARGIN, self.y, text)
        self.y -= 16

    def section(self, number, title, first):
        # A heading alone at the foot of a page is a heading in the wrong place.
        if not first:
            self.room(96)
            self.y -= 14
            self.c.setStrokeColor(RULE)
            self.c.setLineWidth(0.6)
            self.c.line(MARGIN, self.y, PAGE_W - MARGIN, self.y)
            self.y -= 26
        self.spaced('§   ' + ROMAN[number], MARGIN, self.y, SANS, 8, GOLD, 1.4)
        self.y -= 26
        self.c.setFont(SANS, 19.5)
        self.c.setFillColor(INK)
        self.c.drawString(MARGIN, self.y, title)
        self.y -= 25

    # ── pages ──
    def new_page(self):
        self.y = TOP_Y

    def end_page(self):
        self.page += 1
        c = self.c
        c.setStrokeColor(RULE)
        c.setLineWidth(0.6)
        c.line(MARGIN - 8, 54, PAGE_W - MARGIN + 8, 54)
        c.setFont(SANS, 7.4)
        c.setFillColor(FAINT)
        c.drawString(MARGIN - 8, 42, 'Lisbon Sintra Tours')
        c.drawCentredString(PAGE_W / 2, 42, 'Booking Terms & Conditions')
        c.drawRightString(PAGE_W - MARGIN + 8, 42, 'lisbonsintratours.com')
        self.spaced(ROMAN[self.page], PAGE_W / 2, 28, SANS, 7.4, GOLD, 1.0, 'c')
        c.showPage()

    def cover(self):
        c = self.c
        if os.path.exists(LOGO):
            size = 128
            c.drawImage(ImageReader(LOGO), (PAGE_W - size) / 2, PAGE_H - 290,
                        width=size, height=size, mask='auto')
        self.spaced('THE PARTICULARS', PAGE_W / 2, PAGE_H - 338, SANS, 9.4, GOLD, 3.2, 'c')
        c.setFillColor(INK)
        c.setFont(SANS, 31)
        c.drawCentredString(PAGE_W / 2, PAGE_H - 392, 'Booking Terms')
        c.drawCentredString(PAGE_W / 2, PAGE_H - 432, '& Conditions')
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.7)
        c.line(MARGIN + 33, PAGE_H - 466, PAGE_W - MARGIN - 33, PAGE_H - 466)

        c.setFillColor(BODY)
        y = PAGE_H - 500
        for words in self.wrap(INTRO, SANS, 9.6, COL_W - 110):
            c.setFont(SANS, 9.6)
            c.drawCentredString(PAGE_W / 2, y, ' '.join(words))
            y -= 15

        self.spaced("WHAT'S INSIDE", PAGE_W / 2, 252, SANS, 9.4, GOLD, 3.2, 'c')

        # TWO COLUMNS, LEFT-ALIGNED INSIDE EACH, THE PAIR CENTRED.
        # Nine titles down one centred column reached y=12 and ran through the
        # address and the footer rule. Two of nine words each centred on their
        # own line is also a ragged mess. Columns of five and four, aligned on
        # their numerals, fit in 90pt and read as a list.
        titles = [s[0] for s in TERMS]
        num_w  = max(stringWidth(ROMAN[i + 1], SANS, 8.4) for i in range(len(titles)))
        split  = (len(titles) + 1) // 2
        cols   = [titles[:split], titles[split:]]
        col_w  = max(stringWidth(t, SANS, 9.6) for t in titles) + num_w + 9
        gutter = 34
        x0     = PAGE_W / 2 - (col_w * 2 + gutter) / 2
        for ci, col in enumerate(cols):
            x = x0 + ci * (col_w + gutter)
            y = 222
            for ri, t in enumerate(col):
                num = ROMAN[(0 if ci == 0 else split) + ri + 1]
                c.setFont(SANS, 8.4)
                c.setFillColor(GOLD)
                c.drawRightString(x + num_w, y, num)
                c.setFont(SANS, 9.6)
                c.setFillColor(INK)
                c.drawString(x + num_w + 9, y, t)
                y -= 18

        c.setFont(SANS, 7.8)
        c.setFillColor(FAINT)
        for i, line in enumerate(['Lisbon Sintra Tours',
                                  'Rua das Trinas 79, 1200-856 Lisboa, Portugal',
                                  'lisbonsintratours.com']):
            c.drawCentredString(PAGE_W / 2, 108 - i * 11, line)
        self.end_page()
        self.new_page()

    def closing(self):
        self.room(104)
        self.y -= 20
        self.c.setStrokeColor(GOLD)
        self.c.setLineWidth(0.7)
        self.c.line(MARGIN, self.y, PAGE_W - MARGIN, self.y)
        self.y -= 32
        self.c.setFont(SANS, 10)
        self.c.setFillColor(INK)
        self.c.drawCentredString(PAGE_W / 2, self.y, 'Any other questions? Write to us.')
        self.y -= 30
        self.spaced('LST CUSTOMER SUPPORT', PAGE_W / 2, self.y, SANS, 9, GOLD, 3.0, 'c')
        self.y -= 24
        self.c.setFont(SANS, 10)
        self.c.setFillColor(INK)
        self.c.drawCentredString(PAGE_W / 2, self.y, 'hello@lisbonsintratours.com')

    def build(self):
        self.cover()
        for n, (title, blocks) in enumerate(TERMS, start=1):
            self.section(n, title, first=(n == 1))
            for kind, value in blocks:
                if   kind == 'p':     self.para(value)
                elif kind == 'label': self.label(value)
                elif kind == 'q':     self.question(value)
                elif kind == 'rows':  self.rows(value)
                elif kind == 'gap':   self.y -= value
        self.closing()
        self.end_page()
        self.c.save()


if __name__ == '__main__':
    Doc(OUT).build()
    print('Wrote %s (%d bytes)' % (OUT, os.path.getsize(OUT)))
