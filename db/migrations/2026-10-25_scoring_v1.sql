-- Scoring v1: data model for resort and domain scores.
-- Method: Snow Catchers resort scoring method (Claude Docs, 25 Oct 2026).
-- Adds only: one column, new properties, a new score schema. No UPDATE, DROP or DELETE.

-- 1. Bases: villages and resorts where people stay. A base links to the sectors it
--    starts from with the existing 'serves' relation (base serves sector).
alter table core.place add column if not exists is_base boolean not null default false;

-- 2. New properties. Existing ones are reused where they fit:
--    facility_count (kind = snow_park, halfpipe, boardercross, airbag, sledge_run,
--    ice_rink, spa, thermal_baths, cinema, museum, famille_plus_label ...),
--    pass_price_eur (product = pedestrian), michelin_stars_count, road_km.
insert into core.property (key,label,value_type,unit,allowed_methods,applies_to,qualifier_keys,description,requires_scope) values
('snowmaking_share_pct','Share of pistes with snowmaking','number','pct',array['operator','measured','estimated'],array['area','resort'],array[]::text[],'Share of piste km covered by snow cannons',false),
('snowmaking_km','Piste km with snowmaking','number','km',array['operator','measured'],array['area','resort'],array[]::text[],'Piste km covered by snow cannons',false),
('snowfall_cv_pct','Snowfall variation between seasons','number','pct',array['reanalysis'],array['cell'],array['elevation_m','period'],'Coefficient of variation of seasonal snowfall',false),
('terrain_above_share_pct','Share of terrain above a height','number','pct',array['modelled'],array['area','resort','village','sector'],array['elevation_m'],'Share of mapped piste length above the stated height',false),
('north_facing_share_pct','Share of terrain facing north','number','pct',array['modelled'],array['area','resort','village','sector'],array[]::text[],'Share of mapped piste length facing north west to north east',false),
('reachable_km','Piste km reachable at a level','number','km',array['modelled'],array['village','resort','sector','area'],array['level'],'Mapped piste km reachable from the base using only the grades of that level: beginner green and blue, intermediate blue and red, advanced red and black',false),
('park_feature_count','Snow park features','number','count',array['operator','measured','editorial'],array['poi','area','resort'],array['level'],'Features in a park, by level',false),
('offpiste_area_ha','Lift served off piste area','number','ha',array['modelled'],array['area','resort','village'],array['steepness','cover'],'Lift served area off piste by slope band (25-35 or 35-45 degrees) and cover (open or trees)',false),
('vertical_above_treeline_m','Lift served vertical above the treeline','number','m',array['modelled'],array['area','resort','village'],array[]::text[],'Lift served vertical above the treeline',false),
('lift_capacity_ph','Uphill capacity','number','count',array['operator','measured','modelled'],array['lift','area','resort'],array[]::text[],'Skiers per hour',false),
('tourist_beds_count','Tourist beds','number','count',array['operator','measured'],array['area','resort','village'],array[]::text[],'Tourist beds',false),
('road_minutes','Road time','number','min',array['modelled'],array['area','resort','village'],array['from','bound'],'Road time by OSRM',false),
('venue_count','Venues','number','count',array['measured','modelled','operator'],array['area','resort','village'],array['kind','zone'],'Count of venues by kind (bar, late_bar, restaurant) and zone (mountain or village)',false),
('item_price_eur','Price of an item','number','eur',array['operator','measured','modelled'],array['poi','resort','village'],array['item','zone','stat'],'Price of an item (pint_50cl, main_course, espresso, ski_hire_week, group_lessons_week) at a venue, or the median for a zone',false),
('accommodation_night_eur','Accommodation price per night','number','eur',array['measured','modelled'],array['resort','village'],array['type','month','stat'],'Price per night by type (apartment or hotel) and month, usually the median',false),
('trail_km','Winter trails','number','km',array['operator','measured'],array['area','resort','village'],array['kind'],'Kilometres of winter walking, snowshoe or cross country trails',false),
('kids_club_min_age_years','Youngest age at a kids club','number','year',array['operator'],array['poi','resort','village'],array[]::text[],'Youngest age taken',false),
('free_pass_under_age_years','Free lift pass under this age','number','year',array['operator'],array['pass'],array[]::text[],'Children under this age ski free',false),
('bed_to_lift_m','Distance from beds to the nearest lift','number','m',array['modelled'],array['resort','village'],array['stat'],'Walking distance from accommodation to the nearest lift station, usually the median',false),
('ski_in_out_share_pct','Share of beds ski in, ski out','number','pct',array['modelled','operator'],array['resort','village'],array[]::text[],'Share of accommodation within 100 m of a piste or lift',false),
('flat_piste_km','Flat piste','number','km',array['modelled'],array['area','resort','village','sector'],array['level'],'Mapped piste with a gradient under 3 percent, the stretches where snowboarders unstrap',false),
('below_treeline_share_pct','Share of terrain below the treeline','number','pct',array['modelled'],array['area','resort','village','sector'],array[]::text[],'Share of mapped piste length in or beside forest, skiable in flat light',false),
('enclosed_lift_share_pct','Share of enclosed lifts','number','pct',array['modelled','operator'],array['area','resort','sector'],array[]::text[],'Share of main lifts that are gondolas, cable cars, funiculars or covered chairs',false),
('season_days','Season length','number','count',array['operator'],array['area','resort','pass'],array[]::text[],'Days from opening to closing',false),
('vertical_drop_m','Largest vertical descent','number','m',array['modelled','operator'],array['area','resort','village'],array[]::text[],'Largest lift served descent on pistes',false),
('longest_run_km','Longest run','number','km',array['modelled','operator'],array['area','resort'],array[]::text[],'Longest continuous descent on pistes',false),
('resort_character','Resort character','enum','none',array['editorial','operator'],array['resort','village'],array['aspect'],'Labels by aspect: style (traditional, purpose_built, town), traffic (car_free, partly_car_free, cars), walk_to_lifts (short, medium, long)',false)
on conflict (key) do nothing;

-- 3. Score schema.
create schema if not exists score;

create table score.method (
  version text primary key,
  title text not null,
  status text not null default 'draft' check (status in ('draft','accepted','superseded')),
  anchors jsonb not null default '{}',        -- per measure: floor, ceiling, direction, part weights
  doc_url text,
  note text,
  created_at timestamptz not null default now()
);

create table score.theme (
  key text primary key,
  label text not null,
  ord integer not null
);

create table score.measure (
  key text primary key,
  theme_key text not null references score.theme(key),
  label text not null,
  levels text[] not null default '{}',        -- e.g. beginner, intermediate, advanced
  automatic boolean not null default false,   -- computed from open data for every area
  ord integer not null
);

create table score.persona (
  key text primary key,
  label text not null,
  method_version text not null references score.method(version),
  weights jsonb not null                      -- measure key -> weight 0 to 3
);

create table score.value (
  id bigint generated always as identity primary key,
  method_version text not null references score.method(version),
  place_id text not null references core.place(id) on delete cascade,
  measure_key text not null references score.measure(key),
  level text,
  raw_num numeric,
  score numeric check (score between 0 and 100),
  rank_in_set integer,
  set_size integer,
  set_key text,                               -- e.g. range:northern-alps
  confidence text not null check (confidence in ('high','medium','low')),
  fact_refs text[] not null default '{}',
  dataset_id text references model.dataset(id),
  computed_at timestamptz not null default now()
);
create unique index value_one_per_measure on score.value (method_version, place_id, measure_key, coalesce(level,''));
create index value_place on score.value (place_id);
create index value_measure on score.value (measure_key);
create index value_dataset on score.value (dataset_id);

create table score.theme_value (
  method_version text not null references score.method(version),
  place_id text not null references core.place(id) on delete cascade,
  theme_key text not null references score.theme(key),
  level text,
  score numeric check (score between 0 and 100),
  confidence text not null check (confidence in ('high','medium','low')),
  measures_scored integer not null,
  measures_total integer not null,
  computed_at timestamptz not null default now()
);
create unique index theme_value_one on score.theme_value (method_version, place_id, theme_key, coalesce(level,''));
create index theme_value_place on score.theme_value (place_id);
create index theme_value_theme on score.theme_value (theme_key);
create index measure_theme on score.measure (theme_key);
create index persona_method on score.persona (method_version);

-- 4. Access, matching the other schemas.
do $$ declare r record; begin
  for r in select tablename from pg_tables where schemaname = 'score' loop
    execute format('alter table score.%I enable row level security', r.tablename);
    execute format('alter table score.%I force row level security', r.tablename);
  end loop;
end $$;
grant usage on schema score to anon, authenticated;
grant select on all tables in schema score to anon, authenticated;
grant insert, update, delete on all tables in schema score to authenticated;

create policy method_read on score.method for select using (true);
create policy method_write on score.method for all to authenticated using (core.is_editor()) with check (core.is_editor());
create policy theme_read on score.theme for select using (true);
create policy theme_write on score.theme for all to authenticated using (core.is_editor()) with check (core.is_editor());
create policy measure_read on score.measure for select using (true);
create policy measure_write on score.measure for all to authenticated using (core.is_editor()) with check (core.is_editor());
create policy persona_read on score.persona for select using (true);
create policy persona_write on score.persona for all to authenticated using (core.is_editor()) with check (core.is_editor());
create policy value_read on score.value for select using (
  core.is_agent() or exists (select 1 from core.place p join score.method m on m.version = method_version
                             where p.id = place_id and p.status = 'live' and m.status = 'accepted'));
create policy value_write on score.value for all to authenticated using (core.is_agent()) with check (core.is_agent());
create policy theme_value_read on score.theme_value for select using (
  core.is_agent() or exists (select 1 from core.place p join score.method m on m.version = method_version
                             where p.id = place_id and p.status = 'live' and m.status = 'accepted'));
create policy theme_value_write on score.theme_value for all to authenticated using (core.is_agent()) with check (core.is_agent());

-- 5. Method v1, seven themes and twenty three measures. Resort character is
--    stored as labels (resort_character facts), not scored.
insert into score.method (version,title,doc_url,note) values
('v1','Snow Catchers resort scoring v1','https://claude.ai/artifact/B8XnrWevNNicpnQucZbmVF','Anchors to be set during the Northern Alps pilot');

insert into score.theme (key,label,ord) values
('snow','Snow',1),('skiing','Skiing',2),('getting-there','Getting there',3),
('value','Value',4),('apres-food','Après and food',5),('beyond-skiing','Families and beyond skiing',6),
('the-resort','The resort',7);

insert into score.measure (key,theme_key,label,levels,automatic,ord) values
('snow_reliability','snow','Snow reliability','{beginner,intermediate,advanced}',true,1),
('bad_weather','snow','Bad weather days','{}',true,2),
('season_length','snow','Season length and spring snow','{}',false,3),
('snowmaking','snow','Snowmaking','{}',false,4),
('reachable_km','skiing','Kilometres by ability','{beginner,intermediate,advanced}',true,5),
('ski_in_out','skiing','Ski in, ski out','{}',true,6),
('flat_sections','skiing','Flat sections','{beginner,intermediate,advanced}',true,7),
('vertical_long_runs','skiing','Vertical and long runs','{}',true,8),
('network_resilience','skiing','Network resilience','{}',true,9),
('lift_quality','skiing','Lift quality','{}',true,10),
('snow_parks','skiing','Snow parks','{}',false,11),
('off_piste','skiing','Off piste','{intermediate,advanced}',true,12),
('crowding','skiing','Crowding','{}',true,13),
('access','getting-there','Access','{}',true,14),
('value','value','Value','{}',false,15),
('bars','apres-food','Bars','{}',true,16),
('late_bars','apres-food','Late bars','{}',true,17),
('restaurants','apres-food','Restaurants','{}',true,18),
('michelin','apres-food','Michelin','{}',true,19),
('families','beyond-skiing','Families','{}',false,20),
('resort_activities','beyond-skiing','Resort activities','{}',false,21),
('non_skiers','beyond-skiing','Non skiers','{}',false,22),
('solo','the-resort','Solo travellers','{}',false,23);
-- Applied to Supabase as migration scoring_v1 on 25 October 2026.
