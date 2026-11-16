#!/usr/bin/env python3
"""
landing_content.py - what the large-group pages say.

Separate from the generator because the words are the part worth arguing
about and the HTML is not. Robin can rewrite any of this without going near
the builder.

The voice: say the thing that is true and awkward before the thing that
sells. Somebody planning a day for forty people has been quoted by three
companies who did not mention that the coach cannot reach the palace.
"""

PAGES = [
    # ──────────────────────────────────────────────────────────────────────
    {
        "slug": "large-group-tours-lisbon",
        "title": "Large Group Tours in Lisbon & Sintra | 10 to 80 People",
        "desc": ("Private day tours from Lisbon and Sintra for groups of ten to eighty. "
                 "How the vehicles work, why the road to Pena Palace limits coach size, "
                 "what a day actually costs, and the questions to ask before you book."),
        "service": "Private large group tours",
        "eyebrow": "Groups of 7 and up",
        "h1": "Large private group tours, run properly.",
        "stand": ("Twenty people is not two groups of ten. Past the size of a single "
                  "vehicle a private day becomes a different exercise - and there is a "
                  "constraint at the top of the hill in Sintra that almost nobody "
                  "mentions until it is too late to change it."),
        # Two coaches at Belem Tower - our transport partner's, used with their
# permission. It is the page in one picture: the right city, the right
# vehicles, and two of them, which is the whole "a guide in every
# vehicle" argument before a word is read.
        "hero": "/images/coaches-belem.jpg",
        "hero_alt": "Two coaches parked in front of Bel\u00e9m Tower in Lisbon",
        "hero_pos": "center 76%",
        "cta": "Tell us the number and the date.",
        "cta_sub": ("Those two facts decide almost everything else. We will come back with "
                    "the vehicles, the guides and a price - not a brochure."),
        "sections": [
            {"kind": "prose", "eyebrow": "The short answer",
             "title": "What changes above a dozen people.",
             "paras": [
                 "Up to seven, a private tour is a car and a guide who drives it. That is one "
                 "person, one conversation, one set of decisions. It is also what most of the "
                 "private tour market is built around.",
                 "Above that, three things change at once. The vehicle becomes a van, then a "
                 "midi-coach, then more than one of them. Every vehicle needs its own guide, "
                 "because a guide cannot be in two coaches at once. And the day itself has to "
                 "be planned around what a larger vehicle can physically do - which roads it "
                 "fits on, where it can set down, how long forty people take to get off and on.",
                 "None of that makes a large group harder to enjoy. It makes it harder to "
                 "improvise. The work moves from the day itself to the fortnight before it."]},
            {"kind": "diagram", "eyebrow": "The ladder", "figure": "ladder",
             "title": "Party size decides the vehicles, and the vehicles decide the cost.",
             "lede": ("The price does not rise smoothly with the number of people. It steps, "
                      "at the point where one more guest needs a second vehicle and a second "
                      "guide. Twenty-two people and twenty-three people are a long way apart; "
                      "twenty-three and forty-four are not.")},
            {"kind": "diagram", "eyebrow": "The constraint nobody mentions", "figure": "pena",
             "title": "A full-size coach cannot reach Pena Palace.",
             "lede": ("The road up through the park is narrow, steep and has turns a long "
                      "vehicle cannot take. Vehicles of about twenty-two seats and under go to "
                      "the gate. Anything larger stops in the town below, and the group "
                      "transfers up by shuttle - which works, and takes about forty minutes "
                      "out of the day that nobody has budgeted for. We would rather you knew "
                      "now than at ten past ten on the morning.")},
            {"kind": "list", "eyebrow": "Before you book",
             "title": "Five questions worth asking any company.",
             "items": [
                 ("How many vehicles, and how many guides?",
                  "If the answer is one guide for two coaches, half your group spends the day "
                  "without one."),
                 ("What size vehicle, exactly?",
                  "Ask for seats, not adjectives. &quot;A coach&quot; covers everything from "
                  "nineteen seats to fifty-five, and only one of those gets up to Pena."),
                 ("Are the palace tickets timed, and are they bought?",
                  "Pena and Quinta da Regaleira sell out. A timed slot for forty is not "
                  "something to leave until the week before."),
                 ("Where does lunch happen?",
                  "Most of the places a small group would love cannot seat a large one, and "
                  "will not take a booking for it. A set menu arranged ahead is not a "
                  "downgrade; it is the only thing that works."),
                 ("What happens if six people drop out, or six more arrive?",
                  "The honest answer is that the price may step. Ask where the steps are "
                  "before you commit, not after.")]},
            {"kind": "diagram", "eyebrow": "The shape of a day", "figure": "day",
             "title": "Where the eight hours actually go.",
             "lede": ("Between Lisbon and Sintra we allow a full hour each way, whichever end "
                      "you start from. It is forty minutes on a quiet Tuesday in February and "
                      "an hour and a quarter on a Saturday in May, and a plan built on the "
                      "forty is a plan that runs late all day.")},
            {"kind": "prose", "eyebrow": "How we work",
             "title": "Seven and up, and nothing else.",
             "paras": [
                 "We have made large private groups the whole of what we do. Smaller parties "
                 "are passed straight to a trusted independent guide who looks after them "
                 "directly - no mark-up, no middleman, and a better day than we could give "
                 "them while thinking about a coach.",
                 "What that buys you: vehicles and guides we have run with for years, tickets "
                 "booked in the right names at the right times, a plan written hour by hour "
                 "before you arrive, and one person answering the phone on the day.",
                 "We are licensed, insured, APAVT members, and based in Lisbon. Portugal is "
                 "not a destination we cover; it is where we live."]},
            {"kind": "links", "eyebrow": "More",
             "title": "If this is the kind of day you are planning.",
             "items": [
                 ("What a group day costs",
                  "Worked examples at twenty-five, forty and seventy people, and where the "
                  "price steps.", "/group-tour-prices/"),
                 ("Corporate days out of Lisbon",
                  "Conference groups, incentives and team days - timings, invoicing and what "
                  "to brief us on.", "/corporate-day-trips-lisbon/"),
                 ("Wedding guest transport",
                  "Getting sixty guests to a Sintra quinta and home again, on time and in one "
                  "piece.", "/wedding-guest-transport-lisbon-sintra/")]},
        ],
        "faq": [
            ("How many people can you take on a private tour?",
             "From seven up to around eighty in a single day, using as many vehicles as the "
             "party needs with a licensed guide in each. Larger numbers are possible with "
             "more notice."),
            ("Can a coach get to Pena Palace in Sintra?",
             "Vehicles of roughly twenty-two seats and under reach the palace gate. Full-size "
             "coaches stop in Sintra town and the group transfers up by shuttle, which adds "
             "about forty minutes to the day."),
            ("Do we need more than one guide?",
             "One guide per vehicle. A guide cannot be in two vehicles at once, so a party "
             "that needs two coaches needs two guides."),
            ("How long does it take to get from Lisbon to Sintra?",
             "We allow a full hour each way. The drive can be forty minutes on a quiet "
             "morning, but it is routinely longer in season and a plan built on forty minutes "
             "runs late all day."),
        ],
    },
    # ──────────────────────────────────────────────────────────────────────
    {
        "slug": "corporate-day-trips-lisbon",
        "title": "Corporate Day Trips & Incentive Tours from Lisbon",
        "desc": ("Private day trips from Lisbon for conference groups, incentives and team "
                 "days: thirty to eighty delegates, a guide in every vehicle, timings that "
                 "hold, and one invoice at the end."),
        "service": "Corporate group day trips and incentive tours",
        "eyebrow": "For conference and incentive groups",
        "h1": "A day out that runs to time.",
        "stand": ("A delegate day is judged on two things: whether the coach left when it "
                  "said it would, and whether anybody was left behind. Everything else is "
                  "the pleasant part."),
        "hero": "/images/sintra-quinta-regaleira.jpg",
        "cta": "Send us the brief.",
        "cta_sub": ("Numbers, hotel, the time they have to be back, and anything the agenda "
                    "will not move. We will come back with a plan and a single price."),
        "sections": [
            {"kind": "prose", "eyebrow": "What we are usually asked for",
             "title": "The three shapes a corporate day takes.",
             "paras": [
                 "<strong>The half day between sessions.</strong> Thirty to sixty delegates, "
                 "out at two, back by six-thirty for a dinner nobody can be late for. Usually "
                 "Lisbon and Bel&#233;m, because it is the one that is genuinely reliable "
                 "against a clock.",
                 "<strong>The full day after the conference.</strong> Sintra, which is the "
                 "better day by some distance, and which needs the whole eight hours because "
                 "two of them are the road.",
                 "<strong>The incentive day.</strong> Smaller, usually, and the one where the "
                 "budget is real - a winery, a private room for lunch, a boat on the river at "
                 "the end. Tell us what the trip is rewarding and we will build around it."]},
            {"kind": "list", "eyebrow": "What matters on the day",
             "title": "The parts that decide whether it went well.",
             "items": [
                 ("A guide in every vehicle.",
                  "Not one guide on a microphone in the lead coach. Three coaches means three "
                  "guides, and the group in the third one has the same day as the first."),
                 ("A hard return time, planned backwards.",
                  "If they must be back at six-thirty, the day is built from six-thirty "
                  "outwards, with the last stop chosen because it is on the way home."),
                 ("Lunch that can seat the whole group at once.",
                  "Sixty people arriving at a restaurant without a set menu agreed is ninety "
                  "minutes, not sixty, and somebody always ends up eating alone at the bar."),
                 ("A register, taken by the guide.",
                  "It sounds like school. It is the reason nobody is left at Cabo da Roca."),
                 ("One invoice, with a NIF on it.",
                  "Issued properly for your finance team, before or after the day, in euros, "
                  "with everything itemised. No per-head cash on the coach.")]},
            {"kind": "diagram", "eyebrow": "Planning against a clock", "figure": "day",
             "title": "Two of the eight hours are the road.",
             "lede": ("This is the single most useful thing to know when an agenda has to "
                      "hold. Between Lisbon and Sintra we allow a full hour each way - and "
                      "a group of sixty takes ten to fifteen minutes to board, every time, "
                      "which is another half hour across a day with four stops in it.")},
            {"kind": "prose", "eyebrow": "The commercial part",
             "title": "How we quote, and what is in it.",
             "paras": [
                 "One figure for the day, covering the vehicles, the licensed guides, fuel, "
                 "tolls, parking and the driver's hours. Entry tickets are quoted separately "
                 "and at cost, because they change by site and by age band and we would "
                 "rather show you the real number than bury a margin in it.",
                 "Deposit to hold the date, balance before the day. We issue a proper invoice "
                 "with our tax number on it; recibos verdes or a company invoice, whichever "
                 "your finance team needs.",
                 "If the final headcount moves, tell us as early as you can. Between "
                 "twenty-three and forty-four people the price barely moves; crossing either "
                 "of those lines changes the vehicle count, and that is where a quote "
                 "changes."]},
            {"kind": "links", "eyebrow": "More",
             "title": "Worth reading before you brief us.",
             "items": [
                 ("What a group day costs",
                  "Worked examples at twenty-five, forty and seventy people.",
                  "/group-tour-prices/"),
                 ("Large group tours",
                  "The vehicles, the guides, and the constraint at the top of the hill in "
                  "Sintra.", "/large-group-tours-lisbon/"),
                 ("Wedding guest transport",
                  "The other kind of group day that has to run exactly to time.",
                  "/wedding-guest-transport-lisbon-sintra/")]},
        ],
        "faq": [
            ("Can you handle a conference group of eighty?",
             "Yes. Eighty people is four vehicles and four licensed guides, and it needs "
             "more notice than a smaller group because the vehicles and the timed tickets "
             "both have to be held."),
            ("Will we get an invoice for our finance team?",
             "Yes - a proper invoice in euros with our Portuguese tax number on it, itemised, "
             "issued before or after the day as you prefer."),
            ("Can the day work around a fixed dinner time?",
             "That is the normal case. We build the day backwards from the time they have to "
             "be back, and choose the last stop because it is on the way home."),
        ],
    },
    # ──────────────────────────────────────────────────────────────────────
    {
        "slug": "wedding-guest-transport-lisbon-sintra",
        "title": "Wedding Guest Transport, Lisbon & Sintra",
        "desc": ("Coaches and guides for wedding guests between Lisbon, Sintra and Cascais: "
                 "shuttles to the ceremony, a guest day out, and getting everybody home "
                 "afterwards. Sixty to a hundred people, planned to the minute."),
        "service": "Wedding guest transport and guest day tours",
        "eyebrow": "For weddings",
        "h1": "Everybody there, on time, and home again.",
        "stand": ("Wedding transport is the one job where arriving late is not a "
                  "disappointment, it is a disaster. It is also, almost always, the last "
                  "thing anybody books."),
        "hero": "/images/sintra-monserrate.jpg",
        "cta": "Tell us the date and the venue.",
        "cta_sub": ("Even if the guest numbers are still moving. The date is what we need to "
                    "hold the vehicles, and the good ones go early in the season."),
        "sections": [
            {"kind": "prose", "eyebrow": "The three journeys",
             "title": "Most weddings here need all three.",
             "paras": [
                 "<strong>Guests to the ceremony.</strong> Usually from two or three hotels in "
                 "Lisbon to a quinta in Sintra or on the Cascais coast. The whole job is "
                 "arriving together, twenty minutes early, with nobody still at the second "
                 "hotel.",
                 "<strong>The day before, or the day after.</strong> Sixty guests with a free "
                 "afternoon in a country most of them do not know. A guided day out is the "
                 "kindest thing you can put in a welcome bag, and it keeps everybody in one "
                 "place and out of trouble.",
                 "<strong>Home at the end.</strong> The one that goes wrong. A single late "
                 "coach at one in the morning leaves people stranded at a quinta twenty "
                 "minutes from the nearest taxi, so we run staggered departures - one at "
                 "eleven for the families, one at one, one at the very end."]},
            {"kind": "list", "eyebrow": "What we have learned",
             "title": "Things worth deciding early.",
             "items": [
                 ("Pick-up from two hotels, not five.",
                  "Each extra stop is fifteen minutes and one more chance for somebody to be "
                  "in the shower. Two points, and a walk for the rest, beats five."),
                 ("Build in half an hour you do not need.",
                  "The coach that leaves at four for a five o'clock ceremony arrives at "
                  "twenty to five and everybody relaxes. The one that leaves at half four "
                  "has no margin at all."),
                 ("A quinta drive is not a coach drive.",
                  "Several of the loveliest venues around Sintra are up lanes a full-size "
                  "coach cannot enter. We will tell you which, and bring smaller vehicles "
                  "instead - two twenty-two seaters rather than one fifty."),
                 ("Name a point of contact who is not the couple.",
                  "On the day, nobody should be ringing the bride about a coach. Give us a "
                  "best man, a planner, a sister - anybody with a phone and a list."),
                 ("Late departures need to be booked, not hoped for.",
                  "Drivers have legal hours. A coach that collects at four in the afternoon "
                  "cannot also take everybody home at two in the morning; that is a second "
                  "driver, and it has to be arranged in advance.")]},
            {"kind": "diagram", "eyebrow": "If the guests want a day out", "figure": "ladder",
             "title": "Sixty guests is three vehicles and three guides.",
             "lede": ("The same arithmetic as any large group. Worth knowing before the "
                      "welcome email goes out and eighty people reply yes to an afternoon in "
                      "Sintra.")},
            {"kind": "links", "eyebrow": "More",
             "title": "The rest of it.",
             "items": [
                 ("What a group day costs",
                  "Worked examples at twenty-five, forty and seventy people.",
                  "/group-tour-prices/"),
                 ("Large group tours",
                  "What changes above a dozen people, and the road to Pena Palace.",
                  "/large-group-tours-lisbon/"),
                 ("Corporate day trips",
                  "The other kind of day that has to run exactly to time.",
                  "/corporate-day-trips-lisbon/")]},
        ],
        "faq": [
            ("Can you collect wedding guests from more than one hotel?",
             "Yes, though we recommend two pick-up points rather than four or five: each "
             "extra stop adds about fifteen minutes and one more chance of a late guest."),
            ("Can a coach reach a quinta in the Sintra hills?",
             "Some, not all. Several of the best venues are up lanes a full-size coach cannot "
             "enter, and we use two smaller vehicles instead. Tell us the venue and we will "
             "say which it is."),
            ("Can you take guests home late at night?",
             "Yes, with staggered departures - typically one around eleven and one at the "
             "end. Driver hours are regulated, so the late run is a separate booking rather "
             "than the same coach waiting."),
        ],
    },
    # ──────────────────────────────────────────────────────────────────────
    {
        "slug": "group-tour-prices",
        "title": "What a Private Group Tour Costs in Lisbon & Sintra",
        "desc": ("How private group tour pricing actually works in Lisbon and Sintra: why "
                 "the cost steps rather than rises per head, worked examples at twenty-five, "
                 "forty and seventy people, and what is and is not included."),
        "service": "Private group tour pricing",
        "eyebrow": "Pricing, explained",
        "h1": "What a day actually costs, and why.",
        "stand": ("Group tour pricing looks arbitrary from the outside. It is not - it is "
                  "almost entirely decided by how many vehicles your party needs and how "
                  "many guides have to be in them."),
        "hero": "/images/cabo-da-roca.jpg",
        "cta": "Want the real number for your group?",
        "cta_sub": ("Send the date and the headcount. A quote takes us an afternoon, not a "
                    "fortnight, and it comes itemised."),
        "sections": [
            {"kind": "prose", "eyebrow": "The principle",
             "title": "You are not buying seats. You are buying vehicles.",
             "paras": [
                 "A per-head price makes sense for a scheduled bus tour, where you fill the "
                 "empty seats with strangers. A private day has no strangers in it, so the "
                 "cost of the vehicle is the same whether twelve people or twenty-two travel "
                 "in it.",
                 "That is why the price per person falls as the group grows - right up until "
                 "one more guest needs a second vehicle, at which point it jumps. Twenty-two "
                 "and twenty-three people are a long way apart. Twenty-three and forty-four "
                 "are almost the same day.",
                 "If you are close to one of those lines, it is worth knowing before you "
                 "confirm numbers. We will always tell you where the nearest line is."]},
            {"kind": "diagram", "eyebrow": "The ladder", "figure": "ladder",
             "title": "Where the steps are.",
             "lede": ("Each step is a vehicle and the licensed guide who has to be in it. "
                      "Everything else - fuel, tolls, parking, the driver's day - scales with "
                      "the vehicles too.")},
            {"kind": "table", "eyebrow": "Worked examples",
             "title": "Three real shapes of day.",
             "lede": ("A full day of eight hours from Lisbon or Sintra, guided. Figures are "
                      "indicative and move with the season, the date and what the day "
                      "contains - but the shape of them does not change."),
             "head": ["Party", "Vehicles and guides", "Roughly", "Per person"],
             "rows": [
                 ["25 people", "1 midi-coach + 1 van, 2 guides", "&#8364;1,100 &ndash; 1,400",
                  "about &#8364;50"],
                 ["40 people", "2 midi-coaches, 2 guides", "&#8364;1,300 &ndash; 1,600",
                  "about &#8364;36"],
                 ["70 people", "2 full-size coaches, 2 guides", "&#8364;2,300 &ndash; 2,900",
                  "about &#8364;37"]],
             "foot": ("Note the middle row. Forty people often costs less per head than "
                      "twenty-five, because twenty-five is the awkward number that needs two "
                      "vehicles without filling either. Entry tickets are extra and quoted at "
                      "cost: Pena Palace is &#8364;20 an adult, Quinta da Regaleira "
                      "&#8364;20, J&#233;ronimos &#8364;18.")},
            {"kind": "list", "eyebrow": "The small print, said plainly",
             "title": "What is in the figure, and what is not.",
             "items": [
                 ("In: the vehicles.",
                  "Fuel, tolls, parking, insurance and the driver's hours, for as many "
                  "vehicles as the party needs."),
                 ("In: a licensed guide in each one.",
                  "Officially accredited, in English - other languages on request and with "
                  "notice."),
                 ("In: the planning.",
                  "An hour-by-hour plan before you arrive, tickets booked in the right names "
                  "at the right times, and one person answering the phone on the day."),
                 ("Not in: entry tickets.",
                  "Quoted separately and at cost. They vary by site and by age band, and "
                  "burying them in a day rate only makes the day rate look strange."),
                 ("Not in: lunch.",
                  "We arrange it - usually a set menu, which for a large group is the only "
                  "thing that genuinely works - and it is billed at what it costs."),
                 ("Not in: gratuities.",
                  "Never expected, always passed on in full if offered.")]},
            {"kind": "links", "eyebrow": "More",
             "title": "The rest of the picture.",
             "items": [
                 ("Large group tours",
                  "What changes above a dozen people, and why a coach cannot reach Pena.",
                  "/large-group-tours-lisbon/"),
                 ("Corporate day trips",
                  "Delegate days, incentives, and one invoice at the end.",
                  "/corporate-day-trips-lisbon/"),
                 ("Wedding guest transport",
                  "Shuttles, guest days and the late run home.",
                  "/wedding-guest-transport-lisbon-sintra/")]},
        ],
        "faq": [
            ("How much is a private tour for a group of forty?",
             "Indicatively &euro;1,300 to &euro;1,600 for a full guided day with two "
             "midi-coaches and two licensed guides, which is about &euro;36 a head. Entry "
             "tickets and lunch are extra and billed at cost."),
            ("Why does the price per person go up for a smaller group?",
             "Because you are paying for vehicles, not seats. A party of twenty-five needs "
             "two vehicles without filling either, so it can cost more per head than forty "
             "people in two full ones."),
            ("Are entry tickets included?",
             "No - they are quoted separately and charged at cost, because they vary by site "
             "and age band. Pena Palace is &euro;20 an adult, Quinta da Regaleira &euro;20, "
             "J&eacute;ronimos &euro;18."),
        ],
    },
]
