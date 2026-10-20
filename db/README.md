# Snow Catchers database

Supabase project `snow-catchers` (ref `xycfsimxicybvmwxbdfx`, London). The schema lives in the project's migration history; the one change made by hand in the SQL editor on 20 October 2026 widened four allowed value lists (place types, place links, fact status, network edge kinds).

## Layout

- `snowdb.py` formats figures and resolves page layouts. The seed builder checks every figure through it.
- `canon.py` prints JSON the way Postgres prints jsonb, so a page file can be compared with the database by hash.
- `pilot_l3v/build_seed.py` turns the live Les 3 Vallées page data and its evidence register into seed SQL and a coverage report. It stops if any figure taken from the database would read differently from the live page.

## How a page is built from the database

`public.render_page(page_id)` returns the JSON a template reads. Every leaf of the page layout is either a structural value or a reference: a block of words (`$b`), a fact (`$f`), a network matrix cell (`$m`), a place name (`$p`), a list (`$list`), a photo (`$media`) or the network links (`$links`). Inside blocks, figures are tokens such as `{{f:F000042}}` or `{{diff:F000042,F000059}}`, formatted when the page is rendered.

The function runs with the caller's rights, so with the publishable key it only sees published pages, live places and text, and accepted facts.

## Pilot result, 20 October 2026

Loaded: 81 places, 32 sources, 33 properties, 218 facts, 385 blocks, 26 list items, 8 photos, 228 snowfall rows, 14 sector links.

Rendered as the public role, the page, the network matrices and the snowfall series hash identically to the live files (`dda01fa8…`, `f0eb1198…`, `48d8c5c3…`).

Open items:
- Raw lift and piste nodes are not loaded; the browser code that built the network graph is not committed.
- Two conflicts wait in the review queue: lifts 169 or 159, lowest point 1,300 or 1,100 m.
- The page gives Lyon as 170 to 200 km and Chambéry as 90 to 120 km; the router gave 163 to 199 and 85 to 121.
- Les Sybelles' operator figure of 310 km has no source in the register.
