-- Render bus and walk links between sectors as "village" (dotted on the map), as the site template draws them.
-- Needed for the Grand Massif page (Sixt to Samoëns by free skibus). Leaves every existing page unchanged:
-- no other dataset has a bus or walk link.
CREATE OR REPLACE FUNCTION content.resolve_layout(node jsonb, p_place text, matrices jsonb)
 RETURNS jsonb
 LANGUAGE plpgsql
 STABLE
 SET search_path TO ''
AS $function$
declare k text; v jsonb; res jsonb; body text;
begin
  if jsonb_typeof(node) = 'array' then
    select coalesce(jsonb_agg(content.resolve_layout(e, p_place, matrices) order by o), '[]'::jsonb) into res
      from jsonb_array_elements(node) with ordinality t(e, o);
    return res;
  end if;
  if jsonb_typeof(node) <> 'object' then return node; end if;
  if node ? '$b' then
    select c.body into body from public.api_content c where c.place_id = p_place and c.field = node ->> '$b';
    if body is null then raise exception 'block % is not live', node ->> '$b'; end if;
    return to_jsonb(content.resolve_text(body, matrices));
  elsif node ? '$f' then
    select to_jsonb(f.value_num) into res from public.api_fact f where f.id = node ->> '$f';
    if res is null then raise exception 'fact % is not available', node ->> '$f'; end if;
    return res;
  elsif node ? '$m' then
    return matrices -> (node -> '$m' ->> 0) -> (node -> '$m' ->> 1) -> (node -> '$m' ->> 2);
  elsif node ? '$p' then
    select to_jsonb(p.name) into res from public.api_place p where p.id = node ->> '$p';
    if res is null then raise exception 'place % is not live', node ->> '$p'; end if;
    return res;
  elsif node ? '$media' then
    select jsonb_build_array(m.file_name, m.author, m.licence, m.alt) into res
      from content.media m where m.id = node ->> '$media' and m.status = 'live';
    return res;
  elsif node ? '$list' then
    select coalesce(jsonb_agg(jsonb_build_object(
        'name', coalesce(l.attrs ->> 'name', p.name),
        'where', l.attrs ->> 'where',
        'text', content.resolve_text(l.blurb, matrices)) order by l.ord), '[]'::jsonb) into res
      from public.api_list l left join public.api_place p on p.id = l.item_place_id
      where l.list_id = node ->> '$list';
    return res;
  elsif node ? '$links' then
    select coalesce(jsonb_agg(jsonb_build_array(
        split_part(s.from_sector, '.', 2), split_part(s.to_sector, '.', 2),
        case when s.by = 'lift_down' then 'ride' when s.by in ('bus', 'walk') then 'village' else 'lift' end,
        coalesce((s.conditions ->> 'critical')::boolean, false), coalesce(s.note, ''))
        order by (s.conditions ->> 'ord')::int), '[]'::jsonb) into res
      from public.api_sector_link s where s.dataset_id = node ->> '$links';
    return res;
  end if;
  res := '{}'::jsonb;
  for k, v in select * from jsonb_each(node) loop
    res := res || jsonb_build_object(k, content.resolve_layout(v, p_place, matrices));
  end loop;
  return res;
end $function$;
