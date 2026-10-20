"""Evidence register for Portes du Soleil. Run to write data/evidence_register.csv."""
import csv, os
HERE = os.path.dirname(__file__)
R = "2026-10-20"
OFF = "https://en.portesdusoleil.com"
PDF = "https://www.portesdusoleil.com/app/uploads/lesportesdusoleil/2026/06/TARIFS-2026-2027-1.pdf"
SR = "https://www.skiresort.com/en/ski-resort/les-portes-du-soleil-morzine-avoriaz-les-gets-chatel-morgins-champery/"
LG = "https://pass.lesgets.com/en/"
CH = "https://skipass-pds-ch.ch/en/pricing"
OM = "https://open-meteo.com/en/docs/historical-weather-api"
# id, claim, value, unit, scope, period, source_title, url, source_type, data_type, confidence, conflict_group, note
E = [
 ("E001","Resorts in the domain","12","resorts","domain","2026/27","Portes du Soleil official site",OFF+"/portes-du-soleil-lift-passes/","official","reported","high","",""),
 ("E002","Piste length (official)","600","km","domain","2026/27","Portes du Soleil official site",OFF+"/in-winter/skiing-in-les-portes-du-soleil/","official","reported","medium","piste_length","Operator figure; method not stated."),
 ("E003","Piste length (measured)","580","km","domain","checked 2026-10-20","skiresort.com",SR,"independent","measured","medium","piste_length","Measured along centre line by skiresort.com."),
 ("E004","Piste length (Les Gets lift company page)","650","km","domain","2026/27","Les Gets lift company",LG+"ski-area/","official","reported","low","piste_length","Also appears in skiresort.com body text."),
 ("E005","Piste length in OpenStreetMap","427.6","km","domain incl. pass only areas","snapshot 2026-10-20","OpenStreetMap via Overpass","https://www.openstreetmap.org","open data","derived","low","piste_length","Incomplete piste geometry; useful for topology, not totals."),
 ("E006","Number of runs","307","runs","domain","2026/27","Portes du Soleil official site (figures page)",OFF+"/in-winter/skiing-in-les-portes-du-soleil/","official","reported","medium","run_count","39 green, 130 blue, 105 red, 33 black."),
 ("E007","Number of runs","308","runs","domain","2026/27","Portes du Soleil official site (winter pass page)",OFF+"/portes-du-soleil-lift-passes/book-my-winter-pass/","official","reported","low","run_count",""),
 ("E008","Number of runs","296","runs","domain","undated","Portes du Soleil official site (cross border page)",OFF+"/les-portes-du-soleil/europes-largest-cross-border-ski-bike-domain/","official","reported","low","run_count","Probably older."),
 ("E009","Number of lifts","208","lifts","domain","2026/27","Portes du Soleil official site (figures page)",OFF+"/in-winter/skiing-in-les-portes-du-soleil/","official","reported","medium","lift_count",""),
 ("E010","Number of lifts","209","lifts","domain","2026/27","Portes du Soleil official site (winter pass page)",OFF+"/portes-du-soleil-lift-passes/book-my-winter-pass/","official","reported","low","lift_count",""),
 ("E011","Number of lifts","202","lifts","domain","undated","Portes du Soleil official site (cross border page)",OFF+"/les-portes-du-soleil/europes-largest-cross-border-ski-bike-domain/","official","reported","low","lift_count",""),
 ("E012","Number of lifts","163","lifts","linked area excl. Abondance and Roc d'Enfer","checked 2026-10-20","skiresort.com",SR,"independent","measured","medium","lift_count","Total capacity 250,876 p/h; total lift length 145.3 km."),
 ("E013","Snowparks and similar areas","30 / 10","areas","domain","2026/27","Portes du Soleil official site",OFF+"/in-winter/skiing-in-les-portes-du-soleil/","official","reported","low","park_count","30 snowparks, boarder cross and ski cross areas on one page; 10 snowparks on another."),
 ("E014","Altitude range (official)","900 to 2460","m","domain","2026/27","Portes du Soleil official site",OFF+"/in-winter/skiing-in-les-portes-du-soleil/","official","reported","medium","altitude",""),
 ("E015","Altitude range (measured)","985 to 2254","m","linked area","checked 2026-10-20","skiresort.com",SR,"independent","measured","medium","altitude",""),
 ("E016","Highest lift top in OpenStreetMap and DEM","2243","m","Mossettes chair, Les Lindarets side","snapshot 2026-10-20","OpenStreetMap + Copernicus DEM via Open-Meteo","https://open-meteo.com/en/docs/elevation-api","open data","derived","medium","altitude","DEM at the mapped end point of the lift."),
 ("E017","Season dates 2026/27","11 Dec 2026 to 18 Apr 2027","dates","domain pass","2026/27","Portes du Soleil winter pass page",OFF+"/portes-du-soleil-lift-passes/book-my-winter-pass/","official","reported","medium","season_dates","Price validity period."),
 ("E018","Season dates 2026/27","19 Dec 2026 to 18 Apr 2027","dates","domain","2026/27","Portes du Soleil openings page",OFF+"/in-winter/openings-slopes-and-lifts/","official","reported","medium","season_dates",""),
 ("E019","Season dates 2026/27","28 Nov 2026 to 18 Apr 2027","dates","linked area","2026/27","skiresort.com",SR,"independent","reported","low","season_dates","May reflect the earliest resort opening."),
 ("E020","Les Gets-Morzine season","partial 12 Dec, full 19 Dec 2026, close 11 Apr 2027","dates","Les Gets-Morzine","2026/27","Les Gets lift company",LG+"winter-opening-dates-hours/","official","reported","high","",""),
 ("E021","Day pass, adult, ticket office until 19 Mar 2027","73","EUR","domain pass","2026/27","Portes du Soleil price list (PDF)",PDF,"official","reported","high","day_pass",""),
 ("E022","Day pass, adult, online until 19 Mar 2027","69","EUR","domain pass","2026/27","Portes du Soleil price list (PDF)",PDF,"official","reported","high","day_pass",""),
 ("E023","Six day pass, adult, ticket office until 19 Mar 2027","373","EUR","domain pass","2026/27","Portes du Soleil price list (PDF)",PDF,"official","reported","high","",""),
 ("E024","Six day pass, adult, online until 19 Mar 2027","352","EUR","domain pass","2026/27","Portes du Soleil price list (PDF)",PDF,"official","reported","high","",""),
 ("E025","Six day pass, adult, from 20 Mar 2027","317 office / 299 online","EUR","domain pass","2026/27","Portes du Soleil price list (PDF)",PDF,"official","reported","high","",""),
 ("E026","Day pass, adult, main season","72","EUR","domain pass","2026/27","skiresort.com",SR,"independent","reported","low","day_pass","Differs from the official 73 at the ticket office."),
 ("E027","Six day pass, adult, Les Gets-Morzine only","276 online / 312 office","EUR","Les Gets-Morzine","2026/27","Les Gets lift company",LG+"skipass-prices/","official","reported","high","",""),
 ("E028","Day pass, adult, Les Gets-Morzine only","50 online / 56 office","EUR","Les Gets-Morzine","2026/27","Les Gets lift company",LG+"skipass-prices/","official","reported","high","",""),
 ("E029","Day pass, adult 26 to 64, full domain, Swiss online fare","75","CHF","domain pass sold in Switzerland","2026/27","Portes du Soleil Suisse SA",CH,"official","reported","high","",""),
 ("E030","Day pass, adult 26 to 64, Swiss 3CM area only, online","68","CHF","Champéry, Les Crosets, Champoussin, Morgins","2026/27","Portes du Soleil Suisse SA",CH,"official","reported","high","",""),
 ("E031","Six day pass, adult 26 to 64, full domain, Swiss online fare","383","CHF","domain pass sold in Switzerland","2026/27","Portes du Soleil Suisse SA",CH,"official","reported","high","",""),
 ("E032","Season pass, adult, 1 Oct to 30 Nov 2026","1108","EUR","domain","2026/27","Les Gets lift company",LG+"portes-du-soleil-ski-pass/","official","reported","high","",""),
 ("E033","Hands free card","3 EUR / 4 CHF","fee","domain","2026/27","Portes du Soleil winter pass page",OFF+"/portes-du-soleil-lift-passes/book-my-winter-pass/","official","reported","high","","Compulsory for passes of 3 days or more."),
 ("E034","Les Gets-Morzine size","120 km, 50 lifts, 74 runs","","Les Gets-Morzine","2026/27","Les Gets lift company",LG+"ski-area/","official","reported","medium","",""),
 ("E035","Pass only resorts","Abondance, La Chapelle d'Abondance, Saint-Jean-d'Aulps","","domain","checked 2026-10-20","skiresort.com",SR,"independent","reported","medium","pass_only","OSM graph agrees for Abondance, Roc d'Enfer and the Crêt Béni side of La Chapelle; the Panthiaz gondola links La Chapelle to Torgon."),
 ("E036","No piste back to Super-Morzine or Panthiaz","valley run exceptions","","Morzine, La Chapelle","checked 2026-10-20","skiresort.com",SR,"independent","reported","medium","","OSM graph agrees."),
 ("E037","Longest run","Chamossière to Morzine, 11 km, 1,002 m drop","","Morzine","checked 2026-10-20","skiresort.com",SR,"independent","reported","medium","",""),
 ("E038","Steepest run","Chavanette (Swiss Wall), 1 km, 330 m drop, up to 100% gradient","","Champéry side","checked 2026-10-20","skiresort.com",SR,"independent","reported","medium","",""),
 ("E039","Lifts to cross the domain end to end","15 one way, 14 the other","lifts","linked area","checked 2026-10-20","skiresort.com",SR,"independent","reported","low","","Route not stated."),
 ("E040","Famille Plus resorts","Châtel, Les Gets, Morzine","","domain","2026/27","Portes du Soleil family page",OFF+"/in-winter/a-territory-adapted-to-families/","official","reported","high","",""),
 ("E041","Nordic areas","8","areas","domain","2026/27","Portes du Soleil family page",OFF+"/in-winter/a-territory-adapted-to-families/","official","reported","medium","",""),
 ("E042","First international lift link","1956, Super-Châtel to Morgins","","Châtel, Morgins","historical","Portes du Soleil history page",OFF+"/les-portes-du-soleil/a-human-story/","official","reported","high","",""),
 ("E043","Champéry to Avoriaz link via Chavanette","1968","","Champéry, Avoriaz","historical","Portes du Soleil history page",OFF+"/les-portes-du-soleil/a-human-story/","official","reported","high","",""),
 ("E044","First international ski pass","1976","","domain","historical","Portes du Soleil figures page",OFF+"/in-winter/skiing-in-les-portes-du-soleil/","official","reported","medium","",""),
 ("E045","New lift 2026/27","Pointe du Chéry, 6 seat detachable chair","","Les Gets, Mont Chéry","2026/27","skiresort.com",SR,"independent","reported","medium","",""),
 ("E046","Only covered (bubble) lift","one lift in Champéry","","domain","checked 2026-10-20","skiresort.com",SR,"independent","reported","low","",""),
 ("E047","Snowmaking on connections","all important connecting slopes covered","","linked area","checked 2026-10-20","skiresort.com",SR,"independent","reported","low","","Not stated by the operator in sources read so far."),
 ("E048","Domain splits into two networks joined at Morzine","no lift or piste link between Les Gets-Morzine (Pléney, Nyon, Chavannes, Mont Chéry) and the Avoriaz side","","domain","snapshot 2026-10-20","OpenStreetMap graph analysis","research/portes-du-soleil/04_network_graph.md","open data","derived","medium","","To verify on the official map."),
 ("E049","Critical lifts","Super-Morzine gondola, Séraussaix, Proclou, Zore, Pointe de l'Au, Bochasses, Aiguille des Champeys, Morgins-Foilleuse, Morclan, Chaux Fleurie","","domain","snapshot 2026-10-20","OpenStreetMap graph analysis","research/portes-du-soleil/data/network_graph.json","open data","derived","low","","Single lift removal test."),
 ("E050","Seasonal snowfall median 1991-2020 at 1,600 m","285","cm","ERA5 cell 46.25N 6.75E, elevation adjusted","Nov to Apr, 1991/92 to 2020/21","Open-Meteo historical weather API, ERA5",OM,"documented API","modelled reanalysis","medium","","One grid cell covers the whole domain."),
 ("E051","Seasonal snowfall median at 1,100 m: 1961-1990 vs 1991-2020","173 vs 116","cm","ERA5 cell, elevation adjusted","Nov to Apr","Open-Meteo historical weather API, ERA5",OM,"documented API","modelled reanalysis","medium","",""),
 ("E052","Winter (Dec to Feb) temperature trend","+0.34","C per decade","ERA5 cell","1950/51 to 2025/26","Open-Meteo historical weather API, ERA5",OM,"documented API","modelled reanalysis","medium","",""),
 ("E053","Open-Meteo free API is non-commercial only","terms","","","2026-10-20","Open-Meteo terms","https://open-meteo.com/en/terms","provider terms","","high","","Commercial use requires a paid plan; historical API needs Professional plan per FAQ (page inconsistent)."),
 ("E054","IMIS network measures snow depth every 30 minutes at nearly 200 stations","","","Switzerland","2026-10-20","EnviDat (SLF)","https://envidat.ch/dataset/imis-measuring-network","provider page","measured","high","","Terms of use to be checked."),
 ("E055","Meteostat daily data includes snow depth, model filled by default","","","","2026-10-20","Meteostat docs","https://dev.meteostat.net/api/point/daily","provider page","measured + modelled","high","",""),
]
with open(os.path.join(HERE,"..","data","evidence_register.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["evidence_id","claim","value","unit","applies_to","period","source","url","source_type","data_type","confidence","conflict_group","note","retrieved"])
    for e in E: w.writerow(list(e)+[R])
print(len(E),"records")
