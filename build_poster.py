#!/usr/bin/env python3
"""Build poster.svg for the Global Edition of Thursday 26 Nov 2026.

Authoring tool (runs locally, never in the judge's sandbox): emits a
self-contained SVG broadsheet — 56 verified stories, 7 regions, a
dot-matrix world map, 16 front-page leads, weather and a date-check
box. generate.mjs then renders the SVG to entry.png with headless
Chromium, and main.ts (the competition program) only delivers that
PNG, byte for byte. Story data: SOURCES.md in this folder.
"""
from xml.sax.saxutils import escape as esc

REGIONS = [
    ("NORTH AMERICA", "#1f5fa6", [
        ("Abrego Garcia leaves US voluntarily for Spain", "NYT"),
        ("Sullivan concedes Alaska Senate race to Peltola", "NYT"),
        ("Alaska ends voter-list deal with Justice Dept.", "AP"),
        ("Justice Dept. apologises over Omar search claim", "NYT"),
        ("Charge dropped against Rep.-elect Womack", "Axios"),
        ("DOJ aide pressed review of Ahmed indictment", "NYT"),
        ("Giuliani awarded Medal of Freedom", "Politico"),
        ("Lutnick diverted agents for own security", "Atlantic"),
        ("US set to unveil tariffs on China, EU + 14 more", "AP"),
    ]),
    ("LATIN AMERICA & CARIBBEAN", "#2e8b57", [
        ("Car bomb hits governor's office in Meta, Colombia", "Al Jazeera"),
        ("WHO chief in Cuba urges US to lift fuel blockade", "Reuters"),
        ("Supercell storm devastates Tupancireta, Brazil", "Al Jazeera"),
        ("Chile convicts 7 over 2024 wildfire that killed 138", "PaiPee"),
        ("Mexico FDI hits record $43.09B in nine months", "Rio Times"),
        ("Argentina central bank lost $1.02B on gold deals", "Rio Times"),
        ("US pauses joint military ops with Ecuador", "Atlantic"),
    ]),
    ("EUROPE", "#5b4fa6", [
        ("Von der Leyen: Europe to join Ukraine peace talks", "Archynewsy"),
        ("Merz: Russia is 'escalating' threats to Europe", "Reuters"),
        ("German defence chiefs meet on US pullback", "Politico"),
        ("Russian strike kills 2 in Odesa; Kyiv flat ablaze", "Reuters"),
        ("Putin: Ukraine kept hitting refineries; payback due", "Reuters"),
        ("490,334 Russian soldiers dead since 2022, leak shows", "BBC"),
        ("Libya vows payback over drone hit on Russian ship", "AP/Reuters"),
        ("Latvia promises progress on Ukraine grain exports", "h.ua"),
        ("EU leaders to debate Costa budget cuts Thu-Fri", "Reuters"),
    ]),
    ("MIDDLE EAST & NORTH AFRICA", "#b3541e", [
        ("IRGC: two tankers hit mines in Hormuz, ablaze", "Reuters"),
        ("Iran VP: US blockade does not worry Tehran", "Reuters"),
        ("Houthis claim Ras Tanura refinery attack", "Reuters"),
        ("Houthi strike on Riyadh tower injures 11", "NYT"),
        ("Israel kills Hamas security chief Abuelouf + family", "Reuters"),
        ("Egypt urged to reverse Mada Masr closure", "Daily Plug"),
        ("Iran deploys new systems to control Hormuz", "Reuters"),
        ("Pezeshkian vows budget shift to poorer areas", "Reuters"),
    ]),
    ("SUB-SAHARAN AFRICA", "#967014", [
        ("RSF drone strikes kill 19 civilians in Sudan", "Reuters"),
        ("Amnesty seeks UN action over 14 deaths in Ethiopia", "Radio Gen."),
        ("DRC halts all cobalt exports from month-end", "Daily Plug"),
        ("S. Africa court voids Phala Phala report", "Daily Maverick"),
        ("Abiy proposes inclusive dialogue for Sudan", "Daily Plug"),
        ("Ethiopia launches polio drive for 11.3M children", "Addis Standard"),
        ("Nigeria holds interest rate at 23%", "NM Media"),
        ("Nollywood legend Pete Edochie dies", "AllAfrica"),
    ]),
    ("ASIA-PACIFIC", "#14828c", [
        ("Solomons + Australia sign treaty barring foreign base", "NYT"),
        ("Japan to fire missiles at Indian ranges", "Kilambi"),
        ("Air India targets Rs 6,000 crore cost savings", "Kilambi"),
        ("SK hynix advances KRW 100tn shareholder returns", "Kilambi"),
        ("26 miners trapped in flooded W. Java gold mine", "Kilambi"),
        ("Australia passes digital duty of care law", "Kilambi"),
        ("Danantara posts first profit: Rp259.6 trillion", "Kilambi"),
        ("Aramco, S-OIL open $7B Shaheen project in Seoul", "Kilambi"),
        ("Australia inflation beats forecasts", "Reuters"),
    ]),
    ("GLOBAL: MARKETS, CULTURE & SPORT", "#78285a", [
        ("Asian stocks tumble on tariff threat; KOSPI -5.8%", "Reuters"),
        ("Nasdaq futures -2% on tariff fears; Nvidia -5%", "Reuters"),
        ("Bitcoin falls 1% to $59,257", "Reuters"),
        ("Pope Leo XIV laments COP31 failure to agree", "AP"),
        ("AI staff: internal models too powerful to release", "Axios"),
        ("Palmeiras lose 3-0 at Chapecoense", "Rio Times"),
    ]),
]
PANELS = [
    (9, "US tariffs", "on 16 blocs"), (20, "Odesa strike", "2 killed"),
    (26, "Hormuz tankers", "ablaze"), (34, "Sudan drones", "19 killed"),
    (46, "Java mine", "26 trapped"), (51, "KOSPI -5.8%", "tariff shock"),
    (22, "490,334 dead", "leak shows"), (1, "Abrego Garcia", "leaves US"),
    (14, "Mexico FDI", "$43.09B record"), (36, "DRC cobalt", "exports halted"),
    (48, "Danantara profit", "Rp259.6tn"), (53, "Bitcoin", "$59,257"),
    (18, "Merz: Russia", "escalating"), (30, "Hamas chief", "killed"),
    (39, "Polio drive", "11.3M children"), (54, "Pope on COP31", "failure"),
]

WEATHER = ("WEATHER (Open-Meteo, 25 Nov 17:30 UTC) - New York 6C overcast - "
           "Sao Paulo 28C overcast - London 6C overcast - Tokyo 5C clear - "
           "Sydney 17C overcast - Mumbai 28C overcast - Singapore 24C drizzle - "
           "Quito 15C showers")

MAP_ROWS = [
    "        ####  ##                                                        ",
    "      ############        #####   #######  ########                     ",
    "     ##############      ##################################  ####       ",
    "      ############        #####################################         ",
    "       #########           ##################################  ##       ",
    "        ######   #          ###############################             ",
    "         ####  ####          ################  ##########               ",
    "          ##  ######          ##############      ######                ",
    "              ######           ##########        ####  ##               ",
    "              #####             ########          ##                    ",
    "               ####              ######           ##   #                ",
    "               ###                ####            #  ####               ",
    "                ##                 ##                 #####             ",
    "                #                                      ######           ",
    "                                                         ####    #      ",
    "                                                          ##   ###      ",
    "                                                               ###      ",
    "                                                                #       ",
]
PINS = [(13, 3, 1), (17, 12, 2), (47, 2, 3), (54, 6, 4),
        (50, 11, 5), (66, 6, 6), (36, 16, 7)]

INK, MUTE, ACCENT, PAPER2 = "#1a1a1e", "#605c54", "#b22222", "#eee7d8"
SANS = "DejaVu Sans, sans-serif"
out = []

def text(x, y, s, size, fill=INK, bold=False, anchor="start"):
    w = ' font-weight="bold"' if bold else ""
    out.append('<text x="%d" y="%d" font-family="%s" font-size="%d" '
               'fill="%s"%s text-anchor="%s">%s</text>'
               % (x, y, SANS, size, fill, w, anchor, esc(s)))

def rect(x, y, w, h, fill=None, stroke=None, sw=1):
    f = ' fill="%s"' % fill if fill else ' fill="none"'
    s = ' stroke="%s" stroke-width="%d"' % (stroke, sw) if stroke else ""
    out.append('<rect x="%d" y="%d" width="%d" height="%d"%s%s/>'
               % (x, y, w, h, f, s))

def circle(cx, cy, r, fill):
    out.append('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (cx, cy, r, fill))

# ------------------------------------------------------------------ page
out.append('<svg xmlns="http://www.w3.org/2000/svg" width="1024" '
           'height="1024" viewBox="0 0 1024 1024">')
rect(0, 0, 1024, 1024, fill="#f7f3ea")
text(24, 42, "THE WORLD IN ONE DAY", 34, bold=True)
text(24, 64, "Global Edition - Thursday 26 November 2026 - 56 stories - "
             "7 regions - every story sourced", 13, fill=MUTE)
rect(24, 70, 976, 3, fill=ACCENT)

# map
for r, row in enumerate(MAP_ROWS):
    for c, ch in enumerate(row):
        if ch == "#":
            circle(26 + c * 10, 86 + r * 6, 2, "#78766e")
for col, row, num in PINS:
    x, y = 24 + col * 10, 84 + row * 6
    circle(x, y, 8, ACCENT)
    text(x, y + 4, str(num), 11, fill="#ffffff", bold=True, anchor="middle")
text(776, 94, "REGIONS", 11, bold=True)
names = ["North America", "Latin America", "Europe", "Middle East & N. Africa",
         "Sub-Saharan Africa", "Asia-Pacific", "Global"]
counts = [9, 7, 9, 8, 8, 9, 6]
for i, (nm, ct) in enumerate(zip(names, counts)):
    yy = 104 + i * 13
    circle(780, yy - 3, 5, ACCENT)
    text(780, yy, str(i + 1), 8, fill="#ffffff", bold=True, anchor="middle")
    text(790, yy, "%s - %d" % (nm, ct), 10)

# front-page panels
text(24, 214, "FRONT PAGE - 16 LEADS", 11, fill=ACCENT, bold=True)
for i, (num, l1, l2) in enumerate(PANELS):
    x = 24 + (i % 8) * 122
    y = 222 + (i // 8) * 40
    rect(x, y, 116, 34, fill=PAPER2, stroke=MUTE)
    text(x + 5, y + 22, str(num), 17, fill=ACCENT, bold=True)
    text(x + 30, y + 14, l1, 9)
    text(x + 30, y + 25, l2, 9)

def region(x, y, w, idx, start_no):
    name, color, stories = REGIONS[idx]
    rect(x, y, w, 19, fill=color)
    text(x + 6, y + 14, "%s - %d STORIES" % (name, len(stories)), 13,
         fill="#ffffff", bold=True)
    y += 24
    no = start_no
    for headline, tag in stories:
        text(x + 2, y + 11, "%d. %s - %s" % (no, headline, tag), 12)
        y += 15
        no += 1
    return y + 6, no

y, _ = region(24, 302, 476, 0, 1)
y, _ = region(24, y, 476, 1, 10)
y, _ = region(24, y, 476, 2, 17)
# left-out box under the left column
lines = [
    ("LEFT OUT & WHY - DATE CHECK", True, ACCENT),
    ("Held back: anything filed before 25 Nov 2026 UTC - an item is", False, INK),
    ("only on this page if it belongs to the 26 Nov (Asia) cycle.", False, INK),
    ("Just Security's Early Edition for 26 Nov was not yet out at", False, INK),
    ("build time, so this page anchors on its 25 Nov edition plus", False, INK),
    ("the wires it aggregates (Reuters, AP, NYT, BBC, others).", False, INK),
]
rect(24, y + 2, 476, 12 + len(lines) * 13, stroke=ACCENT)
for i, (ln, bold, col) in enumerate(lines):
    text(30, y + 17 + i * 13, ln, 11 if bold else 10, fill=col, bold=bold)

y2, _ = region(524, 302, 476, 3, 26)
y2, _ = region(524, y2, 476, 4, 34)
y2, _ = region(524, y2, 476, 5, 42)
y2, _ = region(524, y2, 476, 6, 51)

rect(24, 926, 976, 1, fill=MUTE)
text(24, 946, "BY THE NUMBERS - 56 stories - 7 regions - 16 leads - "
              "25+ outlets - 1 news day", 11, bold=True)
_cut = WEATHER.rindex(" - ", 0, 118)
text(24, 968, WEATHER[:_cut], 11)
text(24, 982, WEATHER[_cut + 3:], 11)
text(24, 1006, "Sources: Just Security Early Edition (25 Nov 2026), Reuters, "
               "AP, NYT, BBC, Al Jazeera + more - full list in SOURCES.md",
     10, fill=MUTE)
out.append("</svg>")

with open("poster.svg", "w") as f:
    f.write("\n".join(out) + "\n")
print("poster.svg written:", len("\n".join(out)), "bytes")
