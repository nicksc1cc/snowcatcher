"""Atomic question bank for the Portes du Soleil linked domain.

Writes data/question_bank.csv and data/question_bank.json. Run: python3 scripts/build_question_bank.py

Questions come from four sources, each a distinct research need:
  1. Domain level questions, written one by one.
  2. A sector profile template applied to each working sector (each sector is a different place, so each answer differs).
  3. A connection template applied to each modelled inter sector connection.
  4. A base template applied to each base village, and a traveller template applied to each traveller segment.
Status and evidence ids come from the first research pass (20 October 2026).
"""
import csv, json, os

HERE = os.path.dirname(__file__)
DOMAIN = "portes-du-soleil"

FIELDS = ["question_id", "domain_id", "category", "subcategory", "question", "question_type", "geographic_scope",
          "traveller_segments", "variables_required", "definitions_and_units", "data_source_candidates", "research_method",
          "expected_output_type", "time_period_or_freshness_requirement", "dependencies", "evidence_required",
          "confidence_method", "limitations", "content_use", "public_page_destination", "refresh_frequency", "status",
          "evidence_ids", "priority", "last_verified_at"]

SRC = {
    "official": "Official domain site (portesdusoleil.com); resort lift companies",
    "prices": "Official price lists (domain PDF; Les Gets; Portes du Soleil Suisse SA)",
    "map": "Official piste map 2026/27; OpenStreetMap via Overpass",
    "osm": "OpenStreetMap via Overpass; Copernicus DEM via Open-Meteo elevation API",
    "skiresort": "skiresort.com",
    "era5": "Open-Meteo historical API (ERA5, ERA5-Land); Copernicus CDS ERA5-Land",
    "stations": "MeteoSwiss open data; SLF IMIS; Météo-France climatological data; Meteostat",
    "forecast": "Open-Meteo forecast API; MeteoSwiss; Météo-France",
    "reports": "Official lift and piste status page; resort snow reports; webcams",
    "avalanche": "Météo-France avalanche bulletin (Chablais massif); SLF avalanche bulletin",
    "transport": "SNCF, SBB, Geneva airport, transfer operators, resort bus timetables",
    "tourism": "Resort tourist offices; Portes du Soleil site",
    "reviews": "Legally accessible review sites and forums, sampled and dated",
}

DEFAULTS = {
    "factual": dict(research_method="Read the primary source and record the value with its date",
                    expected_output_type="value with unit", confidence_method="Source tier and agreement between sources"),
    "comparative": dict(research_method="Compute from the evidence register and compare like with like",
                        expected_output_type="table", confidence_method="Consistency of definitions across compared items"),
    "analytical": dict(research_method="Model or calculate from open data, then check against official sources",
                       expected_output_type="calculated result with method note", confidence_method="Model checks and agreement with official sources"),
    "temporal": dict(research_method="Assemble a dated time series and summarise it",
                     expected_output_type="time series and statistics", confidence_method="Record length, homogeneity, data type"),
    "operational": dict(research_method="Collect current operator data on a schedule",
                        expected_output_type="live status record", confidence_method="Report timestamp and source tier"),
    "traveller-specific": dict(research_method="Combine sector, network and facility evidence for one traveller type",
                               expected_output_type="assessment with evidence links", confidence_method="Number and tier of supporting evidence records"),
}

DEST = {"overview": "Domain overview", "map": "Interactive domain map", "network": "How the network works",
        "sectors": "Sector comparison", "snow": "Snow and weather intelligence", "terrain": "Terrain and mountain character",
        "pass": "Pass value and usable terrain", "stay": "Where to stay", "who": "Who the domain suits",
        "food": "Food, après and non skiing", "travel": "Getting around", "tradeoffs": "Trade offs and limitations",
        "notes": "Research notes and data freshness"}

ROWS = []


def add(category, subcategory, question, qtype, scope, sources, dest, variables="", units="", segments="all",
        freshness="per season", refresh="annually", status="unresearched", evidence="", priority=2, deps="",
        limits="", content_use="", evidence_req="One primary source, dated"):
    d = DEFAULTS[qtype]
    ROWS.append({
        "domain_id": DOMAIN, "category": category, "subcategory": subcategory, "question": question,
        "question_type": qtype, "geographic_scope": scope, "traveller_segments": segments,
        "variables_required": variables, "definitions_and_units": units,
        "data_source_candidates": "; ".join(SRC[s] for s in sources), "research_method": d["research_method"],
        "expected_output_type": d["expected_output_type"], "time_period_or_freshness_requirement": freshness,
        "dependencies": deps, "evidence_required": evidence_req, "confidence_method": d["confidence_method"],
        "limitations": limits, "content_use": content_use or subcategory, "public_page_destination": DEST[dest],
        "refresh_frequency": refresh, "status": status, "evidence_ids": evidence, "priority": priority,
        "last_verified_at": "2026-10-20" if status in ("evidenced", "disputed") else "",
    })


# ---------------------------------------------------------------- 1. Domain level questions
D = []  # (category, subcategory, question, type, scope, sources, dest, variables, units, status, evidence, priority)
def d(*a): D.append(a)

# A. Identity and boundaries
d("A identity", "name", "What is the official name of the domain as used by the operator in 2026/27?", "factual", "domain", ["official"], "overview", "name", "", "evidenced", "E001", 1)
d("A identity", "countries", "Which countries does the domain cover?", "factual", "domain", ["official"], "overview", "country list", "", "evidenced", "E001", 1)
d("A identity", "resorts", "Which 12 resorts does the operator list as members?", "factual", "domain", ["official"], "overview", "resort list", "", "evidenced", "E001", 1)
d("A identity", "valleys", "Which valleys does the domain span (Aulps, Dranse, Abondance, Val d'Illiez, Morgins, Torgon)?", "factual", "domain", ["official", "osm"], "overview", "valley list", "", "researching", "", 2)
d("A identity", "massif", "Which mountain massif and sub ranges contain the domain?", "factual", "domain", ["osm", "official"], "overview", "massif names", "", "unresearched", "", 3)
d("A identity", "physical links", "Which resorts are physically connected to the main network by lift or piste?", "analytical", "domain", ["osm", "map", "skiresort"], "network", "resort to network links", "", "evidenced", "E035;E048", 1)
d("A identity", "pass only", "Which resorts share the pass but have no lift or piste link?", "analytical", "domain", ["osm", "skiresort", "official"], "network", "resort list", "", "evidenced", "E035", 1)
d("A identity", "pass only access", "How do skiers reach each pass only resort (bus, car), and how long does it take?", "factual", "domain", ["transport", "official"], "travel", "transfer time", "minutes", "unresearched", "", 1)
d("A identity", "subdomains", "Which local sub areas sell their own pass (Les Gets-Morzine, Swiss 3CM, Avoriaz, Châtel and others)?", "factual", "domain", ["prices"], "pass", "pass products", "", "researching", "E027;E030", 1)
d("A identity", "piste length official", "What piste length does the operator publish, and where?", "factual", "domain", ["official"], "overview", "km", "km of piste", "disputed", "E002;E004", 1)
d("A identity", "piste length measured", "What piste length do independent measurements give?", "factual", "domain", ["skiresort", "osm"], "overview", "km", "km measured along centre line", "evidenced", "E003;E005", 1)
d("A identity", "piste length method", "How does the operator count piste kilometres (length of each run, area, or including itineraries)?", "factual", "domain", ["official"], "notes", "method", "", "unresearched", "", 2)
d("A identity", "run count", "How many runs does the domain have, and why do official pages give 296, 307 and 308?", "comparative", "domain", ["official"], "notes", "run count", "runs", "disputed", "E006;E007;E008", 2)
d("A identity", "run colours", "How many green, blue, red and black runs are there?", "factual", "domain", ["official"], "terrain", "run counts by colour", "runs", "evidenced", "E006", 1)
d("A identity", "lift count", "How many lifts are there, and why do sources give 163, 202, 208 and 209?", "comparative", "domain", ["official", "skiresort", "osm"], "notes", "lift count", "lifts", "disputed", "E009;E010;E011;E012", 2)
d("A identity", "area", "What surface area does the domain claim, and how is it defined (400 km2)?", "factual", "domain", ["official"], "notes", "area", "km2", "researching", "", 3)
d("A identity", "altitude range", "What are the lowest and highest lift served points?", "comparative", "domain", ["official", "skiresort", "osm"], "overview", "elevation", "m above sea level", "disputed", "E014;E015;E016", 1)
d("A identity", "history links", "When was each international link built?", "temporal", "domain", ["official"], "overview", "dates", "", "researching", "E042;E043", 3)
d("A identity", "first pass", "When was the shared pass created?", "factual", "domain", ["official"], "overview", "year", "", "evidenced", "E044", 3)
d("A identity", "changes", "Which lifts and links are new or removed for 2026/27?", "factual", "domain", ["official", "skiresort"], "notes", "lift changes", "", "researching", "E045", 1)
d("A identity", "claims", "Does the advertised 600 km match what is open on a typical mid season day?", "analytical", "domain", ["reports", "official"], "tradeoffs", "open km by day", "km open", "unresearched", "", 1)
d("A identity", "largest claim", "On what basis does the operator call the domain the largest cross border area, and is the claim checkable?", "comparative", "domain", ["official", "skiresort"], "notes", "comparison basis", "", "unresearched", "", 3)

# B. Network topology (domain level)
d("B network", "graph build", "Can the lift and piste network be modelled from open map data, and how complete is it?", "analytical", "domain", ["osm"], "notes", "node and edge counts", "", "evidenced", "E005", 1)
d("B network", "two networks", "Is there any lift or piste link between the Les Gets-Morzine side and the Avoriaz side other than through Morzine town?", "analytical", "domain", ["osm", "map"], "network", "connectivity", "", "evidenced", "E048", 1)
d("B network", "Morzine transfer", "How do skiers cross Morzine between the Pléney and Super-Morzine lifts (walk, bus, road train), and how long does it take?", "factual", "connection", ["transport", "tourism"], "network", "transfer mode and time", "minutes", "unresearched", "", 1)
d("B network", "Morzine return", "How do skiers return from Avoriaz to Morzine when no piste reaches the Super-Morzine base?", "analytical", "connection", ["osm", "skiresort", "official"], "network", "return options", "", "evidenced", "E036;E048", 1)
d("B network", "end to end lifts", "What is the minimum number of lift rides to cross the domain from Les Gets to Torgon?", "analytical", "domain", ["osm"], "network", "lift count", "lift rides", "evidenced", "E039", 1)
d("B network", "end to end time", "How long does the fastest end to end route take in good conditions?", "analytical", "domain", ["osm", "official"], "network", "route time", "hours", "unresearched", "", 1)
d("B network", "circuit", "Is there a recognised circuit that returns to the start without repeating lifts, and what is it?", "analytical", "domain", ["osm", "map", "official"], "network", "route", "", "unresearched", "", 2)
d("B network", "critical lifts", "Which single lift closures cut the most sector to sector routes?", "analytical", "domain", ["osm"], "network", "pairs lost per lift", "ordered sector pairs", "evidenced", "E049", 1)
d("B network", "wind closures", "Which exposed lifts most often close in wind, and what do their closures cut?", "analytical", "domain", ["reports", "osm"], "tradeoffs", "closure frequency", "days per season", "unresearched", "", 1)
d("B network", "blue route", "Can the main international circuit be skied on blue runs only?", "analytical", "domain", ["osm", "map"], "network", "reachability on green and blue", "", "researching", "", 1)
d("B network", "red needed", "Which inter sector links require a red or black run?", "analytical", "domain", ["osm", "map"], "network", "link difficulty", "", "researching", "", 1)
d("B network", "drag lifts on links", "Which inter sector links depend on drag lifts?", "analytical", "domain", ["osm", "map"], "network", "lift types on links", "", "researching", "", 1)
d("B network", "flat sections", "Where are the flat traverses that snowboarders must push or skate?", "analytical", "domain", ["osm", "reviews", "map"], "network", "flat section list", "", "unresearched", "", 1)
d("B network", "last lifts", "What are the last lift times that decide whether skiers can get home to each base?", "operational", "domain", ["official"], "network", "last lift times", "local time", "researching", "E020", 1)
d("B network", "orientation", "How easy is the domain to navigate, and where do skiers commonly take wrong turns?", "analytical", "domain", ["reviews", "skiresort"], "network", "navigation issues", "", "unresearched", "", 2)
d("B network", "map vs practice", "Where does the official piste map show links that are walks, buses or seasonal only?", "comparative", "domain", ["map", "official"], "network", "link type", "", "unresearched", "", 1)

# C. Geography and aspect
d("D geography", "aspect", "What share of the piste network faces north, east, south and west?", "analytical", "domain", ["osm"], "terrain", "aspect share", "% of piste length", "unresearched", "", 2)
d("D geography", "tree line", "Which sectors lie mostly below the tree line, giving shelter in bad visibility?", "analytical", "domain", ["osm", "skiresort"], "terrain", "share of piste below tree line", "%", "unresearched", "", 2)
d("D geography", "inversions", "Where do temperature inversions occur, and how often?", "temporal", "domain", ["stations", "era5"], "snow", "inversion days", "days per season", "unresearched", "", 3)
d("D geography", "flat light", "Which routes are most exposed to flat light (open, above the trees)?", "analytical", "domain", ["osm"], "tradeoffs", "route exposure", "", "unresearched", "", 2)
d("D geography", "low returns", "Which village return runs end below 1,200 m?", "analytical", "domain", ["osm"], "snow", "piste end elevations", "m", "researching", "", 1)
d("D geography", "highest points", "Where are the highest lift served points, and how high are they?", "factual", "domain", ["osm", "skiresort"], "terrain", "elevation", "m", "evidenced", "E015;E016", 1)

# Snow, weather and data sources
d("S snow data", "API coverage", "Which snow and weather APIs cover the domain, and which variables does each provide?", "comparative", "domain", ["era5", "stations", "forecast"], "notes", "API inventory", "", "evidenced", "E053;E054;E055", 1)
d("S snow data", "licence", "Which data sources can legally be stored and shown on a commercial site?", "comparative", "domain", ["era5", "stations"], "notes", "licence terms", "", "researching", "E053", 1)
d("S snow data", "grid resolution", "How many ERA5 and ERA5-Land grid cells cover the domain?", "analytical", "domain", ["era5"], "notes", "cell count", "cells", "evidenced", "E050", 1)
d("S snow data", "stations", "Which measuring stations with snow depth lie within 15 km of the domain, and at what elevations?", "factual", "domain", ["stations"], "snow", "station list", "m", "unresearched", "", 1)
d("S snow data", "operator reports", "Do the domain and each resort publish daily snow depth, and at which measuring points?", "factual", "domain", ["reports"], "snow", "report fields", "cm", "unresearched", "", 1)
d("S snow data", "archived reports", "Are past daily resort snow reports archived anywhere that can be used legally?", "factual", "domain", ["reports", "skiresort"], "snow", "archive availability", "", "unresearched", "", 2)
d("S snow data", "webcams", "Which webcams can be linked to corroborate conditions, and on what terms?", "factual", "domain", ["reports"], "snow", "webcam list", "", "unresearched", "", 3)
d("S snow data", "avalanche bulletins", "Which avalanche bulletins cover each part of the domain (Météo-France Chablais, SLF)?", "factual", "domain", ["avalanche"], "snow", "bulletin regions", "", "researching", "", 1)
d("S snow data", "forecast models", "Which forecast models cover the domain at what resolution, and how do they differ?", "comparative", "domain", ["forecast"], "snow", "model list", "km", "researching", "", 2)
d("S snow data", "forecast validation", "How well did archived forecasts predict snowfall here in recent winters?", "analytical", "domain", ["forecast", "era5", "stations"], "notes", "forecast error", "cm", "unresearched", "", 3)
d("S snow history", "seasonal snowfall", "What is the median seasonal snowfall at 1,100, 1,600 and 2,100 m (1991 to 2020)?", "temporal", "elevation band", ["era5"], "snow", "seasonal snowfall", "cm, Nov to Apr", "evidenced", "E050", 1)
d("S snow history", "change", "How has seasonal snowfall changed since 1961 to 1990 at each elevation?", "temporal", "elevation band", ["era5"], "snow", "median change", "cm", "evidenced", "E051", 1)
d("S snow history", "poor seasons", "How often has a season fallen below the lower quartile of 1991 to 2020?", "temporal", "elevation band", ["era5"], "snow", "frequency", "seasons", "evidenced", "E050", 1)
d("S snow history", "warming", "How fast have winter temperatures risen over the domain since 1950?", "temporal", "domain", ["era5"], "snow", "trend", "C per decade", "evidenced", "E052", 1)
d("S snow history", "rain", "How much winter rain falls at 1,100 m compared with 1,600 m?", "temporal", "elevation band", ["era5"], "snow", "rain Dec to Mar", "mm", "evidenced", "E050", 1)
d("S snow history", "snow depth", "What is the typical snow depth by week at representative elevations?", "temporal", "elevation band", ["era5", "stations"], "snow", "snow depth", "cm", "researching", "", 1)
d("S snow history", "thresholds", "On how many days per season does modelled snow depth exceed 30, 50 and 100 cm?", "temporal", "elevation band", ["era5", "stations"], "snow", "days above threshold", "days", "researching", "", 1)
d("S snow history", "cover duration", "How long does continuous snow cover last at each elevation?", "temporal", "elevation band", ["era5", "stations"], "snow", "cover duration", "days", "researching", "", 1)
d("S snow history", "first snow", "When does the first meaningful snowfall usually arrive?", "temporal", "elevation band", ["era5"], "snow", "first 5 cm day", "days after 1 Nov", "evidenced", "E050", 2)
d("S snow history", "big storms", "How many days per season bring 10 cm or more of snow?", "temporal", "elevation band", ["era5"], "snow", "days", "days", "evidenced", "E050", 2)
d("S snow history", "worst seasons", "Which recent seasons were poorest, and how did the domain operate in them?", "temporal", "domain", ["era5", "reports"], "snow", "season list", "", "researching", "", 2)
d("S snow history", "snowmaking", "What share of pistes and which links have snowmaking, by sector?", "factual", "domain", ["official", "skiresort"], "snow", "snowmaking coverage", "% of piste", "researching", "E047", 1)
d("S snow history", "modelled vs measured", "How does ERA5-Land snow depth compare with station measurements nearby?", "comparative", "domain", ["era5", "stations"], "notes", "bias", "cm", "unresearched", "", 1)
d("S current", "pipeline", "What schedule and storage are needed to collect daily snow reports and forecasts?", "operational", "domain", ["reports", "forecast"], "notes", "pipeline spec", "", "researching", "", 1)
d("S current", "forecast snapshot", "What does the current seven day forecast show at low, mid and high points?", "operational", "point", ["forecast"], "snow", "forecast values", "cm, C, km/h", "evidenced", "", 2)
d("S current", "freezing level", "What is the forecast freezing level each day?", "operational", "domain", ["forecast"], "snow", "freezing level", "m", "evidenced", "", 2)
d("S current", "open terrain", "What share of lifts and pistes is open today in each sector?", "operational", "sector", ["reports"], "snow", "open counts", "lifts, km", "unresearched", "", 1)

# Pass and economics
d("C pass", "day price", "What does a one day adult domain pass cost online and at the ticket office in 2026/27?", "factual", "domain", ["prices"], "pass", "price", "EUR", "evidenced", "E021;E022", 1)
d("C pass", "six day price", "What does a six day adult domain pass cost online and at the ticket office in 2026/27?", "factual", "domain", ["prices"], "pass", "price", "EUR", "evidenced", "E023;E024", 1)
d("C pass", "late season", "How much cheaper are passes from 20 March 2027?", "comparative", "domain", ["prices"], "pass", "price difference", "EUR, %", "evidenced", "E025", 2)
d("C pass", "Swiss prices", "What do the same passes cost in CHF from the Swiss operator?", "factual", "domain", ["prices"], "pass", "price", "CHF", "evidenced", "E029;E031", 2)
d("C pass", "currency", "Is it cheaper to buy in France or Switzerland at the current exchange rate?", "comparative", "domain", ["prices"], "pass", "price difference", "EUR", "unresearched", "", 2)
d("C pass", "local vs full French", "How much more does the full domain pass cost than the Les Gets-Morzine pass for six days?", "comparative", "domain", ["prices"], "pass", "price difference", "EUR, %", "evidenced", "E024;E027", 1)
d("C pass", "local vs full Swiss", "How much more does the full domain day pass cost than the Swiss 3CM pass?", "comparative", "domain", ["prices"], "pass", "price difference", "CHF, %", "evidenced", "E029;E030", 1)
d("C pass", "Avoriaz pass", "Does Avoriaz sell a local pass for 2026/27, and at what price?", "factual", "sector", ["prices"], "pass", "price", "EUR", "unresearched", "", 1)
d("C pass", "Châtel pass", "Does Châtel sell a local pass for 2026/27, and at what price?", "factual", "sector", ["prices"], "pass", "price", "EUR", "unresearched", "", 1)
d("C pass", "beginner passes", "Which beginner passes exist, and which lifts do they cover?", "factual", "domain", ["prices"], "pass", "pass coverage", "", "researching", "", 1)
d("C pass", "children", "Which ages count as child, youth and senior, and do French and Swiss age bands differ?", "comparative", "domain", ["prices"], "pass", "age bands", "years", "evidenced", "E021;E029", 1)
d("C pass", "family offers", "Which family discounts apply, and what are their conditions?", "factual", "domain", ["prices", "official"], "pass", "discounts", "%", "researching", "", 2)
d("C pass", "card fee", "What does the hands free card cost, and when is it compulsory?", "factual", "domain", ["official"], "pass", "fee", "EUR, CHF", "evidenced", "E033", 3)
d("C pass", "season pass", "What does an adult season pass cost, and when are early prices available?", "factual", "domain", ["prices"], "pass", "price", "EUR", "evidenced", "E032", 3)
d("C pass", "break even", "How many days of crossing into other sectors make the full pass worth it compared with a local pass?", "analytical", "domain", ["prices", "osm"], "pass", "break even", "days", "researching", "", 1)
d("C pass", "usable share", "How much of the network can a skier based in each village reach and return from in a day?", "analytical", "base", ["osm"], "pass", "reachable km", "km", "researching", "", 1)
d("C pass", "pass only value", "Do visitors to Abondance, La Chapelle or Saint-Jean-d'Aulps get value from the full pass?", "analytical", "base", ["prices", "osm", "transport"], "pass", "value assessment", "", "unresearched", "", 2)
d("C pass", "insurance", "What lift pass insurance is offered, and what does it cover?", "factual", "domain", ["prices"], "pass", "cover", "", "unresearched", "", 3)
d("C pass", "buy channel", "Which sales channels give the lowest price (online, office, package, flash sale)?", "comparative", "domain", ["prices", "official"], "pass", "price by channel", "EUR", "researching", "E022;E021", 2)

# Traveller suitability at domain level (segment detail in section 4)
d("T suitability", "beginner zones", "Where are the beginner zones and free or cheap beginner lifts in each resort?", "factual", "domain", ["official", "prices"], "who", "zone list", "", "researching", "", 1)
d("T suitability", "families label", "Which resorts hold the Famille Plus label, and what does the label audit?", "factual", "domain", ["official"], "who", "label list", "", "evidenced", "E040", 2)
d("T suitability", "experts", "Where is the steepest lift served terrain, and how hard is it?", "factual", "domain", ["skiresort", "official"], "terrain", "run list", "gradient %", "evidenced", "E038", 1)
d("T suitability", "freeride", "Which areas are known for lift accessed freeride, and what guiding exists?", "factual", "domain", ["official", "reviews"], "terrain", "area list", "", "unresearched", "", 2)
d("T suitability", "parks", "How many snowparks are there, and which are the largest?", "factual", "domain", ["official", "skiresort"], "terrain", "park list", "", "disputed", "E013", 2)
d("T suitability", "nordic", "How many Nordic areas are there, and how many km of trails?", "factual", "domain", ["official"], "food", "trail km", "km", "researching", "E041", 3)
d("T suitability", "accessibility", "Which resorts offer adaptive skiing, and which lifts are step free?", "factual", "domain", ["official", "tourism"], "who", "facility list", "", "unresearched", "", 2)

# Food, après, non ski
d("F food", "mountain restaurants", "How many mountain restaurants are there in each sector?", "factual", "sector", ["official", "tourism"], "food", "count", "restaurants", "unresearched", "", 2)
d("F food", "prices", "What do a main course and a coffee cost on the mountain compared with the village?", "comparative", "domain", ["tourism", "reviews"], "food", "prices", "EUR, CHF", "unresearched", "", 2)
d("F food", "local food", "Which regional dishes and cheeses (Abondance, raclette) are typical?", "factual", "domain", ["tourism"], "food", "dish list", "", "unresearched", "", 3)
d("F food", "après", "Where are the main après bars, and do they sit on the way home?", "factual", "domain", ["tourism", "reviews"], "food", "bar list", "", "unresearched", "", 2)
d("F food", "bad weather", "What indoor activities exist for bad weather days (Aquariaz, cinema, spa)?", "factual", "domain", ["tourism", "official"], "food", "activity list", "", "researching", "", 2)
d("F food", "non skiers meet", "Where can non skiers ride lifts to meet skiers for lunch, and what do pedestrian passes cost?", "factual", "domain", ["prices", "tourism"], "food", "pedestrian prices", "EUR, CHF", "researching", "", 2)

# Transport
d("G transport", "airports", "What are the road transfer times from Geneva airport to each base?", "factual", "base", ["transport"], "travel", "transfer time", "minutes", "unresearched", "", 1)
d("G transport", "rail", "Which bases can be reached by train, and how far are the stations from the lifts?", "factual", "base", ["transport"], "travel", "rail access", "km", "unresearched", "", 1)
d("G transport", "buses", "Which free ski buses link the bases, and how often do they run?", "factual", "domain", ["transport", "tourism"], "travel", "bus routes", "minutes between buses", "unresearched", "", 1)
d("G transport", "car free", "Which bases work without a car for a full week?", "analytical", "base", ["transport", "osm"], "travel", "assessment", "", "unresearched", "", 2)
d("G transport", "border", "What documents and currency issues arise when skiing into Switzerland?", "factual", "domain", ["official", "tourism"], "travel", "rules", "", "unresearched", "", 2)
d("G transport", "parking", "Where are the main car parks at lift bases, and what do they cost?", "factual", "base", ["official", "tourism"], "travel", "parking", "EUR per day", "unresearched", "", 3)
d("G transport", "stranded", "What happens to a skier who misses the last lift home on the other side of the domain?", "operational", "domain", ["transport", "official"], "tradeoffs", "options and cost", "", "unresearched", "", 1)

# Reviews
for topic in ["connectivity and navigation", "snow quality", "queues and crowding", "lift quality", "terrain variety", "mountain food", "value for money", "family suitability", "snowboarder experience", "après and atmosphere", "bad weather days"]:
    d("H reviews", topic, f"What do dated visitor reviews say about {topic}, and from how many reviews?", "analytical", "domain", ["reviews"], "who", "theme summary", "count of reviews", "unresearched", "", 3)

for x in D:
    cat, sub, q, t, scope, src, dest, var, units, status, ev, pr = x
    fresh = "current season" if cat in ("C pass", "S current") else ("historical record" if cat == "S snow history" else "per season")
    refresh = "daily" if cat == "S current" else ("annually" if cat != "S snow history" else "annually after each season")
    limits = "Modelled data, roughly 25 km grid; not a piste measurement" if cat == "S snow history" else ""
    add(cat, sub, q, t, scope, src, dest, var, units, freshness=fresh, refresh=refresh, status=status, evidence=ev, priority=pr, limits=limits)

# ---------------------------------------------------------------- 2. Sector profiles
SECTORS = {
    "Les Gets: Mont Chéry": "mont-chery", "Les Gets: Chavannes and Ranfoilly": "les-gets", "Morzine: Nyon and Pointe de Nyon": "nyon-pointe",
    "Morzine: Pléney": "pleney", "Morzine: Super-Morzine and Zore": "super-morzine", "Avoriaz": "avoriaz",
    "Montriond: Les Lindarets and Ardent": "lindarets-brochaux", "Châtel: Linga and Pré la Joux": "linga-pre-la-joux",
    "Châtel: Super-Châtel and Barbossine": "super-chatel", "Torgon": "torgon", "La Chapelle d'Abondance: Crêt Béni": "la-chapelle",
    "La Chapelle d'Abondance: Panthiaz and Braitaz": "panthiaz-braitaz", "Abondance": "abondance", "Saint-Jean-d'Aulps: Roc d'Enfer": "roc-d-enfer",
    "Morgins: Foilleuse": "morgins-foilleuse", "Morgins: Corbeau": "morgins-corbeau", "Champoussin": "champoussin",
    "Les Crosets": "les-crosets", "Champéry: Planachaux and Grand Paradis": "champery-planachaux",
}
SECTOR_Q = [
    ("C sector", "access", "Which lifts give access to {s} from the valley, and from which villages?", "factual", ["osm", "map"], "sectors", "access lifts", "", "researching", 1),
    ("C sector", "base elevation", "What is the lowest lift base elevation in {s}?", "factual", ["osm"], "sectors", "elevation", "m", "evidenced", 1),
    ("C sector", "top elevation", "What is the highest lift top elevation in {s}?", "factual", ["osm"], "sectors", "elevation", "m", "evidenced", 1),
    ("C sector", "vertical", "What is the longest continuous vertical drop available in {s}?", "analytical", ["osm"], "terrain", "vertical", "m", "unresearched", 2),
    ("C sector", "piste km", "How many kilometres of piste does {s} have, by colour?", "factual", ["osm", "official"], "sectors", "km by colour", "km", "researching", 1),
    ("C sector", "lift types", "How many lifts of each type serve {s}?", "factual", ["osm", "skiresort"], "sectors", "lift counts", "lifts", "evidenced", 1),
    ("C sector", "drag share", "What share of uphill capacity in {s} comes from drag lifts?", "analytical", ["osm"], "sectors", "share", "% of lifts", "researching", 1),
    ("C sector", "lift age", "How old are the main lifts in {s}, and are replacements planned?", "factual", ["skiresort", "official"], "sectors", "build years", "year", "unresearched", 3),
    ("C sector", "capacity", "What is the combined hourly capacity of the lifts in {s}?", "factual", ["osm", "skiresort"], "sectors", "capacity", "people per hour", "researching", 3),
    ("C sector", "aspect", "Which way do the main slopes of {s} face?", "analytical", ["osm"], "sectors", "aspect", "compass direction", "unresearched", 1),
    ("C sector", "sun", "Does {s} get morning or afternoon sun in midwinter?", "analytical", ["osm"], "sectors", "sun hours", "hours", "unresearched", 2),
    ("C sector", "tree cover", "How much of {s} lies below the tree line?", "analytical", ["osm"], "sectors", "share", "% of piste", "unresearched", 2),
    ("C sector", "wind", "Which lifts in {s} are exposed to wind closures?", "analytical", ["reports", "osm"], "sectors", "lift list", "", "unresearched", 1),
    ("C sector", "snowmaking", "What share of the pistes in {s} has snowmaking?", "factual", ["official"], "snow", "share", "% of piste", "unresearched", 1),
    ("C sector", "snow band", "Which elevation band best represents the snow history of {s}?", "analytical", ["era5", "osm"], "snow", "band", "m", "researching", 1),
    ("C sector", "spring snow", "When does snow on the lower runs of {s} usually turn soft or thin in spring?", "temporal", ["era5", "reports"], "snow", "date", "", "unresearched", 2),
    ("C sector", "beginner terrain", "Where is the beginner terrain in {s}, and which lifts serve it?", "factual", ["official", "osm"], "who", "zone list", "", "unresearched", 1),
    ("C sector", "intermediate", "How much blue and red cruising does {s} offer?", "analytical", ["osm"], "terrain", "km", "km", "researching", 1),
    ("C sector", "expert", "Which black runs or itineraries does {s} contain?", "factual", ["osm", "map"], "terrain", "run list", "", "researching", 1),
    ("C sector", "off piste", "What off piste terrain is accessible from the lifts of {s}?", "factual", ["reviews", "official"], "terrain", "terrain description", "", "unresearched", 2),
    ("C sector", "park", "Does {s} have a snowpark, and what features does it have?", "factual", ["official"], "terrain", "park features", "", "unresearched", 2),
    ("C sector", "snowboard", "Are there flat sections or drag lifts in {s} that hinder snowboarders?", "analytical", ["osm", "reviews"], "who", "obstacle list", "", "unresearched", 1),
    ("C sector", "crowding", "When and where does {s} get crowded or queue?", "analytical", ["reviews", "reports"], "sectors", "queue evidence", "", "unresearched", 2),
    ("C sector", "restaurants", "Which mountain restaurants are in {s}?", "factual", ["tourism"], "food", "restaurant list", "", "unresearched", 2),
    ("C sector", "facilities", "Where are toilets, first aid and lockers in {s}?", "factual", ["official"], "sectors", "facility list", "", "unresearched", 3),
    ("C sector", "connections out", "Which neighbouring sectors can be reached from {s}, and by which lifts?", "analytical", ["osm", "map"], "network", "links", "", "evidenced", 1),
    ("C sector", "return", "Can a skier return to the base of {s} on a piste, and of which colour?", "analytical", ["osm", "skiresort"], "network", "return run", "", "researching", 1),
    ("C sector", "critical lift", "Which single lift closure would cut {s} off from the rest of the network?", "analytical", ["osm"], "network", "lift", "", "researching", 1),
    ("C sector", "night", "Is there night skiing in {s}?", "factual", ["official"], "sectors", "schedule", "", "unresearched", 3),
    ("C sector", "opening", "What are the 2026/27 opening and closing dates for {s}?", "factual", ["official"], "sectors", "dates", "", "researching", 1),
    ("C sector", "pass", "Which passes cover {s}, besides the full domain pass?", "factual", ["prices"], "pass", "pass list", "", "researching", 2),
    ("C sector", "atmosphere", "What is the character of {s}: car free station, village, forest or open bowls?", "analytical", ["tourism", "reviews"], "sectors", "description", "", "unresearched", 2),
]
for sname, sid in SECTORS.items():
    for cat, sub, q, t, src, dest, var, units, status, pr in SECTOR_Q:
        ev = "E016" if sub in ("base elevation", "top elevation") else ("E049" if sub == "connections out" else "")
        add(cat, f"{sub} ({sid})", q.format(s=sname), t, "sector", src, dest, var, units, status=status, evidence=ev,
            priority=pr, deps=f"sector:{sid}", limits="OpenStreetMap based until checked against the official map" if "osm" in src else "")

# ---------------------------------------------------------------- 3. Connections
CONNECTIONS = [
    ("Les Gets to Morzine (Chavannes and Pléney side)", "les-gets", "pleney"),
    ("Les Gets village crossing (Mont Chéry to Chavannes)", "mont-chery", "les-gets"),
    ("Morzine town crossing (Pléney to Super-Morzine)", "pleney", "super-morzine"),
    ("Super-Morzine to Avoriaz (Zore and Proclou)", "super-morzine", "avoriaz"),
    ("Avoriaz back to Super-Morzine (Séraussaix)", "avoriaz", "super-morzine"),
    ("Avoriaz to Les Lindarets", "avoriaz", "lindarets-brochaux"),
    ("Les Lindarets to Châtel (Chaux Fleurie towards Linga)", "lindarets-brochaux", "linga-pre-la-joux"),
    ("Châtel Linga to Super-Châtel (Gabelou)", "linga-pre-la-joux", "super-chatel"),
    ("Super-Châtel to Morgins (Corbeau link)", "super-chatel", "morgins-corbeau"),
    ("Super-Châtel to Torgon", "super-chatel", "torgon"),
    ("Torgon to La Chapelle d'Abondance (Braitaz and Panthiaz)", "torgon", "panthiaz-braitaz"),
    ("Morgins village crossing (Corbeau to Foilleuse)", "morgins-corbeau", "morgins-foilleuse"),
    ("Morgins to Champoussin", "morgins-foilleuse", "champoussin"),
    ("Champoussin to Les Crosets (Pointe de l'Au)", "champoussin", "les-crosets"),
    ("Les Crosets to Champéry (Planachaux)", "les-crosets", "champery-planachaux"),
    ("Champéry village up to Planachaux (cable car, Grand Paradis)", "champery-planachaux", "les-crosets"),
    ("Les Crosets to Avoriaz (Chavanette)", "les-crosets", "avoriaz"),
    ("Avoriaz to Les Crosets (Mossettes or Chavanette)", "avoriaz", "les-crosets"),
    ("Les Lindarets to Les Crosets (Mossettes)", "lindarets-brochaux", "les-crosets"),
    ("Swiss Wall descent (Chavanette) and the lift alternative", "les-crosets", "les-crosets"),
    ("Montriond and Ardent up to Les Lindarets", "lindarets-brochaux", "lindarets-brochaux"),
    ("Morzine (Prodains) up to Avoriaz", "avoriaz", "avoriaz"),
]
CONN_Q = [
    ("what connects", "What lifts, pistes or transfers make up the {c} link?", "factual", "evidenced"),
    ("direction", "Can the {c} link be used in both directions?", "analytical", "researching"),
    ("users", "Is the {c} link open to skiers, snowboarders and pedestrians alike?", "factual", "unresearched"),
    ("time", "How long does the {c} link take in normal conditions?", "analytical", "unresearched"),
    ("difficulty", "What is the easiest piste colour that completes the {c} link?", "analytical", "researching"),
    ("terrain issues", "Does the {c} link involve a flat traverse, drag lift, long chair or walk?", "analytical", "researching"),
    ("dependency", "Which lift must be running for the {c} link to work?", "analytical", "researching"),
    ("exposure", "Is the {c} link exposed to wind, poor visibility or avalanche closures?", "analytical", "unresearched"),
    ("alternative", "What is the alternative route if the {c} link closes, and how much longer is it?", "analytical", "researching"),
    ("last time", "What is the last time to start the {c} link and still get back?", "operational", "unresearched"),
    ("beginners", "Is the {c} link suitable for beginners and less confident snowboarders?", "traveller-specific", "unresearched"),
    ("map vs practice", "Does the official map show the {c} link accurately?", "comparative", "unresearched"),
]
for cname, a, b in CONNECTIONS:
    for sub, q, t, status in CONN_Q:
        add("B connection", f"{sub} ({a} to {b})", q.format(c=cname), t, "route", ["osm", "map", "official"], "network",
            "route attributes", "minutes, piste colour", status=status, evidence="E048;E049" if status == "evidenced" else "",
            priority=1 if sub in ("what connects", "dependency", "alternative", "difficulty", "last time") else 2,
            deps=f"connection:{a}>{b}", limits="Graph model from OpenStreetMap; to verify on site and on the official map")

# ---------------------------------------------------------------- 4. Bases and travellers
BASES = ["Les Gets", "Morzine", "Avoriaz", "Montriond and Ardent", "Les Lindarets", "Châtel", "Pré la Joux and Plaine Dranse",
         "La Chapelle d'Abondance", "Abondance", "Saint-Jean-d'Aulps", "Torgon", "Morgins", "Champoussin", "Les Crosets", "Champéry",
         "Val-d'Illiez"]
BASE_Q = [
    ("direct access", "Which lifts leave from {b}, and how far are they from the main lodging areas?", "factual", "stay", 1),
    ("beginner access", "Is there a beginner area within walking distance in {b}?", "factual", "stay", 1),
    ("high terrain", "How many lift rides does it take to reach terrain above 2,000 m from {b}?", "analytical", "stay", 1),
    ("reach Avoriaz", "How many lift rides does it take to reach Avoriaz from {b}?", "analytical", "stay", 1),
    ("reach Switzerland", "How many lift rides does it take to reach Les Crosets from {b}?", "analytical", "stay", 1),
    ("reach Châtel", "How many lift rides does it take to reach Super-Châtel from {b}?", "analytical", "stay", 1),
    ("return home", "Can skiers ski back into {b} at the end of the day, and on which colour?", "analytical", "stay", 1),
    ("last lift", "What is the latest time to leave the far side of the domain and still get back to {b}?", "operational", "stay", 1),
    ("transport", "Which buses and trains serve {b}, and how often?", "factual", "travel", 2),
    ("car", "Is a car needed when staying in {b}?", "analytical", "travel", 2),
    ("families", "What childcare, ski school and nursery slopes does {b} offer?", "factual", "who", 2),
    ("evenings", "What is the evening atmosphere in {b}: bars, restaurants or quiet?", "analytical", "food", 2),
    ("non skiers", "What can non skiers do in {b} during the day?", "factual", "food", 3),
    ("snow at base", "How reliable is snow at the base of {b} in December and March?", "analytical", "snow", 1),
]
for b in BASES:
    for sub, q, t, dest, pr in BASE_Q:
        status = "researching" if sub in ("reach Avoriaz", "reach Switzerland", "reach Châtel", "high terrain") else "unresearched"
        add("E base", f"{sub} ({b})", q.format(b=b), t, "village", ["osm", "official", "tourism", "transport"], dest,
            "base attributes", "lift rides, minutes", status=status, priority=pr, deps=f"base:{b}")

SEGMENTS = ["first time skiers", "progressing beginners", "intermediate skiers", "advanced and expert skiers", "snowboarders",
            "freeriders and ski tourers", "freestyle riders", "families with young children", "families with teenagers",
            "mixed ability groups", "couples", "groups of friends", "solo travellers", "people seeking quiet slopes",
            "people seeking nightlife", "people who value mountain food", "non skiers", "visitors with accessibility needs"]
SEG_Q = [
    ("best sectors", "Which sectors of the domain suit {g} best, and why?", 1),
    ("best base", "Which base village suits {g} best?", 1),
    ("constraints", "Which links or sectors should {g} avoid or plan around?", 1),
    ("pass choice", "Which pass gives {g} the best value?", 2),
    ("week plan", "What does a realistic six day itinerary across the domain look like for {g}?", 2),
    ("evidence", "What evidence from reviews supports or contradicts the domain's suitability for {g}?", 3),
]
for g in SEGMENTS:
    for sub, q, pr in SEG_Q:
        add("D traveller", f"{sub} ({g})", q.format(g=g), "traveller-specific", "domain",
            ["osm", "official", "reviews", "prices"], "who", "assessment", "", segments=g, priority=pr,
            status="researching" if sub in ("constraints", "pass choice") else "unresearched")

# ---------------------------------------------------------------- write
seen = set()
for i, r in enumerate(ROWS, 1):
    assert r["question"] not in seen, r["question"]
    seen.add(r["question"])
    r["question_id"] = f"PDS-{i:04d}"
os.makedirs(os.path.join(HERE, "..", "data"), exist_ok=True)
with open(os.path.join(HERE, "..", "data", "question_bank.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    for r in ROWS:
        w.writerow({k: r.get(k, "") for k in FIELDS})
json.dump([{k: r.get(k, "") for k in FIELDS} for r in ROWS], open(os.path.join(HERE, "..", "data", "question_bank.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
from collections import Counter
print(len(ROWS), "questions")
print(Counter(r["status"] for r in ROWS))
print(Counter(r["category"] for r in ROWS))
print(Counter(r["priority"] for r in ROWS))
