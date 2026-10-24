# Snow Catchers: working context

Read this before starting work on a Snow Catchers page. Last updated 24 October 2026.

## Repositories and services

| What | Where |
|---|---|
| Site | nicksc1cc/projectsnow. Eleventy builds `src` into `docs`; GitHub Pages serves main `/docs`. Work branch france-redesign is kept level with main. |
| Live site | https://nicksc1cc.github.io/projectsnow/ |
| Research and loader | nicksc1cc/snowcatcher (this repo): `research/<domain>/`, `db/load_package.py`, `db/model/network.js`, `db/canon.py` |
| Database | Supabase project xycfsimxicybvmwxbdfx (core facts, content blocks, pages) |

## How a linked domain page is made

1. Research to the depth of the Portes du Soleil page: operator and measured figures, the OpenStreetMap network model, ERA5 snowfall, OSRM roads, pass prices, and four chapters (snowboarding with parks and off piste, families, food, après) plus getting there, parking and winter driving rules.
2. Build the package in `research/<domain>/` (evidence register, places, facts, model run, `page/draft.json`), then run `db/load_package.py` to write `out/load.sql` and a local preview.
3. Load everything into Supabase as drafts. Check the block hash against the files, then dry run `content.approve_page` inside a rolled back transaction and compare the render hash with `db/canon.py` on the preview.
4. Render a PDF of the preview and send it to Nick for review. Compare chapter depth with Portes du Soleil before sending.
5. Publish only when Nick says so: copy the preview files into `projectsnow/src/data/l3/`, build, commit, push main, and push main to france-redesign. Approve the page in the database so the site and the database match.

## Standing rules

- Writing: concise, like a veteran travel writer. No em dashes, no hyphenated compounds, no fragmented sentences, no stock or slogan lines. Never address the reader by name or role.
- Every figure is a sourced fact token. No invented figures, no averaging of conflicting figures, and no "honest drawbacks" field.
- Ask Nick before building anything new, and push live only when he says so.
- Supabase sometimes cancels UPDATE and DROP statements. Do not work around a cancellation; write the SQL to a file in `research/<domain>/out/` and list it below for Nick to run.
- Secrets (such as SUPABASE_PUBLISHABLE_KEY) are added by Nick himself.

## Waiting on Nick

| Item | What to do | Then |
|---|---|---|
| Tignes Val d'Isère text | Run `research/tignes-val-disere/out/revisions_2026-10-24.sql` in the Supabase SQL editor. It should end with 374 rows and hash c4c82a7d52f3a50957222ff4b4eca36d. | Claude approves page:area:tignes-val-disere so the database matches the live page. |
| Family pass property | Run: `update core.property set definition = 'Discount when a family buys the stated number of passes together; the fact note says whether it is per pass or off the total' where key = 'family_pack_discount_eur';` | Nothing further. |
| Paradiski snowfall | Decide whether F000361 (288 cm) supersedes F000104 (290 cm), both snowfall at 1,600 m for the Paradiski cell. | Claude writes the SQL. |
| GitHub secret | Add SUPABASE_PUBLISHABLE_KEY to the projectsnow repository secrets if not already done. | Needed for the publish from database workflow. |

## Checks still open

- Network models for Les 3 Vallées, Paradiski and Tignes Val d'Isère are to be checked against the official 2026/27 piste maps (critical lifts, black run shortcuts, base tables).
- 2026/27 bus timetables from Bourg-Saint-Maurice, Aime and Moûtiers are not checked.

## Linked domain queue, by size

Published: Les 3 Vallées (600 km), Portes du Soleil (600 km), Paradiski (425 km), Tignes Val d'Isère (300 km). Les Sybelles (310 km) has an earlier page.

Next, from `projectsnow/src/data/linked_domains.json`: Évasion Mont Blanc (445 km), Via Lattea (400 km), Grand Massif (265 km), Alpe d'Huez Grand Domaine (250 km), Serre Chevalier (250 km), Espace Diamant (192 km), then the smaller areas.
