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
        # Rua Augusta towards the Arco, 19 November 2026. The two coaches at
        # Belem were here before and did not survive the shape of a hero:
        # that photograph is 3:2 with its subject in the bottom third and the
        # tower top right, so cropped to a wide band it gave either coach
        # flank or empty sky, and the dark wash the white text needs took the
        # golden light out of whichever you chose. Robin: "large group tours
        # lisbon image isn't doing it for me, can we try another one?"
        #
        # This one is built the right way round for the job: interest across
        # the whole width, the arch holding the centre, the calcada running
        # out of the bottom of the frame, and people at the scale the page is
        # actually about. It sells the day rather than the vehicle, which is
        # also the honest order - nobody books a coach, they book Lisbon.
        #
        # hero_pos is set rather than left out even though 50% is the centre,
        # because the template only switches the ken-burns drift off when a
        # position is given, and a photograph that is ABOUT something holds
        # still.
        "hero": "/images/lisbon-rua-augusta.jpg",
        "hero_alt": "Rua Augusta in Lisbon, busy with people, looking towards the Arco da Rua Augusta",
        "hero_pos": "center 50%",
        # Bright, busy and lit from the far end: the standfirst sat across a
        # crowd with almost no wash on it. This adds one on the left only.
        "hero_wash_left": True,
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
             "party needs with a guide in each. Larger numbers are possible with "
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
        # A full-size coach outside a terminal with the holds open, suitcases
        # on the pavement and people loading them. Pexels, free for commercial
        # use, no attribution required:
        # pexels.com/photo/modern-coach-bus-at-airport-terminal-40919466/
        #
        # It is a delegate day in one frame - the transfer, the luggage, the
        # size of vehicle that moves forty people - which is what this page is
        # about. It is Spain rather than Portugal and the coach carries
        # another operator's name on the rear flank; Robin's own test applies,
        # "to give an impression more than an actuality".
        "hero": "/images/coach-luggage.jpg",
        "hero_alt": "Passengers loading luggage into a full-size coach outside a terminal",
        "hero_pos": "center 66%",
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
                 "One figure for the day, covering the vehicles, the guides, fuel, "
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
             "Yes. Eighty people is four vehicles and four guides, and it needs "
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
        # A close crop of a coach flank. Robin: "the wheel arch one we can
        # use, I don't mind." It is the right subject for the page that is
        # about what vehicles cost, and at hero scale the detail reads as
        # texture rather than as a photograph of a bus.
        #
        # The crop starts below the top third on purpose: there is a third
        # company's slogan across the top of the source, and a name that is
        # not ours has no business in our hero.
        "hero": "/images/coach-detail.jpg",
        "hero_alt": "The flank of a midi-coach",
        "hero_pos": "center 62%",
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
             "lede": ("Each step is a vehicle and the guide who has to be in it. "
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
                 ("In: a guide in each one.",
                  "In English - other languages on request and with "
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
             "midi-coaches and two guides, which is about &euro;36 a head. Entry "
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
    # ──────────────────────────────────────────────────────────────────────
    # Robin, 27 November 2026: "Let's big up those boat services on LST. We
    # want a slice of that action!" and "We're not calling it Skipper Pedro
    # explicitly." So: no names of the skipper or of the boats, and no fleet
    # claimed - we place the party on the boat that fits. Figures (up to 200,
    # Tagus and Sado, crew/fuel/insurance in the price, Doca de Santo Amaro
    # and Belem, the sizes 18/80/200) are the skipper's own, from
    # skipperpedro-site. Unlike the car pages, any size is ours here: a boat
    # enquiry is never forwarded on the small-job rule (lst-pp-admin
    # forwardPlan), and it reaches the form pre-set to "Boat trip".
    {
        "slug": "private-boat-trips-lisbon",
        "title": "Private Boat Trips in Lisbon | Sunset Sails to 200-Guest Parties",
        "desc": ("Private boats on the Tagus and the Sado for any size of party: sunset sails, "
                 "birthdays, company days and dolphin trips, from two guests to two hundred. "
                 "Crew, fuel and insurance in every price."),
        "service": "Private boat trips and events",
        "eyebrow": "On the water",
        "h1": "Private boats on the Tagus, for two guests or two hundred.",
        "stand": ("Lisbon was built to be seen from the river. We find the boat that fits the "
                  "day - a sailing yacht for a few friends, a catamaran for a birthday, a river "
                  "boat with a bar and a dance floor for the whole company - and bring the "
                  "crew, the food and the plan."),
        # Wide, sharp and full of the thing itself: the tall ship under sail
        # is the only boat photograph big enough to hold a full-width hero.
        "hero": "/images/boat-tall-ship.jpg",
        "hero_alt": "A three-masted tall ship under sail on the Tagus, with guests on deck",
        "hero_pos": "center 55%",
        "hero_wash_left": True,
        "cta": "Tell us the number, the date and the occasion.",
        "cta_sub": ("We will come back with the boat that fits, what it can do with your time, "
                    "and a price for all of it."),
        "cta_href": "/contact/?tour=Boat%20trip",
        "cta_button": "Ask about a boat",
        "sections": [
            {"kind": "prose", "eyebrow": "Why the river",
             "title": "The best view of Lisbon is from the water.",
             "paras": [
                 "From the Tagus the whole city lines up for you: the Pra&ccedil;a do Com&eacute;rcio "
                 "arcades, Alfama climbing to the castle, the 25 de Abril bridge overhead, and "
                 "Bel&eacute;m with its tower and its monument to the navigators. Every one of them "
                 "was built to be seen from a ship.",
                 "For a group there is a second reason. On a boat everybody is in one place, "
                 "sitting down, with a drink, and nobody is queuing for anything. It is the "
                 "easiest few hours of a group day to run, and usually the one they talk about "
                 "afterwards.",
                 "Boats leave from the marinas at Doca de Santo Amaro and Doca de Bel&eacute;m in "
                 "Lisbon, and from Set&uacute;bal on the Sado for the dolphins. We confirm the "
                 "meeting point when you book."]},
            {"kind": "photos", "items": [
                ("/images/boat-sunset.jpg", "A sailing boat on the Tagus at sunset, with Lisbon behind",
                 "Sunset on the Tagus: two golden hours past the city and under the bridge.", "center 50%"),
                ("/images/boat-catamaran.jpg", "A catamaran full of guests under sail on the Tagus",
                 "A catamaran for a birthday, a hen party or a long afternoon with friends.", "center 50%"),
                ("/images/boat-praca-comercio.jpg", "A sailing yacht passing the Praca do Comercio in Lisbon",
                 "The Praça do Comércio from the river, the way it was meant to be arrived at.", "center 60%"),
            ]},
            {"kind": "table", "eyebrow": "The right boat",
             "title": "The boat follows the party.",
             "lede": ("We are not tied to one boat. We find the one that fits the number, the date "
                      "and the mood, from a yacht for a handful to a river boat for two hundred."),
             "head": ["Guests", "The kind of boat", "Good for"],
             "rows": [
                 ["Up to 18", "Sailing yachts and catamarans",
                  "Sunset sails, proposals, families, a few friends"],
                 ["19 to 80", "Large catamarans and party boats, with a bar and room to dance",
                  "Birthdays, hen and stag parties, team afternoons"],
                 ["81 to 200", "River boats with a saloon, and tall ships",
                  "Company parties, banquets, wedding welcome evenings"],
             ],
             "foot": ("Crew, fuel and insurance are in every price. Food, drink and music are "
                      "arranged to suit the occasion, from a bar and canap&eacute;s to a seated dinner.")},
            {"kind": "list", "eyebrow": "Ways to spend the time",
             "title": "An hour, an afternoon or a whole day.",
             "items": [
                 ("Sunset on the Tagus.",
                  "About two hours past the Pra&ccedil;a do Com&eacute;rcio, under the bridge and "
                  "along Bel&eacute;m, timed for the light."),
                 ("Cascais and the coast.",
                  "About four hours out past the Bugio lighthouse, to swim, paddleboard and have "
                  "lunch at anchor off Cascais."),
                 ("Arr&aacute;bida, Sesimbra and the dolphins of the Sado.",
                  "A full day south from Set&uacute;bal: turquoise coves, a long lunch and the "
                  "estuary's resident dolphins."),
                 ("Celebrations.",
                  "Birthdays, anniversaries, hen and stag parties and proposals, with the music "
                  "and the food to match."),
                 ("Company days.",
                  "Team building on deck, a launch, a results party or a conference dinner on "
                  "the water."),
                 ("Take the helm.",
                  "Anyone who wants to can steer for a while, and sailing lessons can be arranged "
                  "for those who want to learn properly."),
             ]},
            {"kind": "photos", "eyebrow": "On board", "title": "Room for a proper party.",
             "items": [
                ("/images/boat-saloon-dining.jpg", "A boat saloon set for a seated dinner",
                 "A saloon set for dinner, with the river on every side.", "center 50%"),
                ("/images/boat-company-day.jpg", "A company group in matching shirts on deck",
                 "A company day: one team, one boat, one afternoon.", "center 40%"),
                ("/images/boat-dolphins.jpg", "Dolphins swimming beside a catamaran",
                 "The Sado's dolphins, an hour south of Lisbon.", "center 50%"),
             ]},
            {"kind": "prose", "eyebrow": "Land and water",
             "title": "Put a boat at the end of a day on land.",
             "paras": [
                 "The river works best as the last chapter of a day we are already running. "
                 "Sintra's palaces in the morning, lunch, and then down to Bel&eacute;m for the "
                 "boat as the light goes gold. Or a Lisbon walking morning and an afternoon at "
                 "anchor off Cascais.",
                 "We plan both halves together, so the coach meets the boat and the boat meets "
                 "the dinner, and you have one person to call about all of it.",
                 "If the wind is too strong to sail safely, the skipper decides on the day, and "
                 "we move the trip to another time. You will hear from us early, not at the "
                 "marina."]},
            {"kind": "links", "eyebrow": "More",
             "title": "If you are planning for a group.",
             "items": [
                 ("Large group tours",
                  "Days on land for ten to eighty people, and what changes above a dozen.",
                  "/large-group-tours-lisbon/"),
                 ("Corporate days out of Lisbon",
                  "Conference groups, incentives and team days, with a boat to finish.",
                  "/corporate-day-trips-lisbon/"),
                 ("Wedding guests",
                  "A welcome evening on the river, and getting everyone to the quinta and home.",
                  "/wedding-guest-transport-lisbon-sintra/")]},
        ],
        "faq": [
            ("How many people can come on a private boat trip in Lisbon?",
             "Anything from two guests to about two hundred. Up to eighteen fits a sailing yacht "
             "or catamaran, up to eighty a large catamaran or party boat, and up to two hundred "
             "a river boat or tall ship."),
            ("Where do the boats leave from?",
             "In Lisbon from the marinas at Doca de Santo Amaro and Doca de Belém. Trips to "
             "see the dolphins leave from Setúbal, on the Sado. We confirm the meeting point "
             "when you book."),
            ("What is included in the price?",
             "The boat, the skipper and crew, fuel and insurance. Food, drink and music are "
             "arranged to order and quoted with the boat, so you have one price for the day."),
            ("What happens if the weather is bad?",
             "If the wind is too strong to sail safely, the skipper decides on the day and we "
             "move the trip to another time. We tell you as early as we can."),
            ("Can a boat trip be added to a tour?",
             "Yes, and it is often the best part of the day: a sunset sail from Belém after "
             "a morning in Sintra, or an afternoon off Cascais after a Lisbon morning. We plan "
             "both together."),
        ],
    },
]
