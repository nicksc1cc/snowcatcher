// Snow Catchers bulk scoring inputs: automatic measures for many resorts at once.
//
// Runs in a browser page like network.js (the research workspace cannot reach Overpass, Open-Meteo
// or OSRM). Load it, then:
//   await SCBulk.fetch(bbox, tiles)   OpenStreetMap lifts, pistes, venues and accommodation, lift end heights
//   SCBulk.measure(resorts)           one record per resort: [slug, lat, lon, ...]
//   await SCBulk.access(resorts, from) road minutes and km by OSRM from each origin
//
// Model, method v1 (25 October 2026):
//  - one graph for the whole region, built as in network.js: piste vertices shared by OSM node and
//    snapped within 20 m, lifts bottom to top by DEM height, walk edges of 80 m at lift ends
//  - starts for a resort: main lift bottoms within 1,500 m of the resort point, or the nearest main lift
//    bottom within 5 km if there is none
//  - levels, by grades usable / grades counted:
//      beginner      novice, easy / novice, easy
//      intermediate  novice, easy, intermediate / easy, intermediate
//      advanced      all / intermediate, advanced, expert, freeride
//    a piste way counts when its first vertex is reached using only usable grades
//  - lift quality: main lifts reachable at advanced level; drag share and enclosed share (funicular, cable
//    car, gondola, mixed lift, or a chair tagged aerialway:bubble=yes)
//  - vertical: highest reachable lift top less the lowest start bottom
//  - resilience: for each main lift within two rides of the starts, the share of reachable advanced km
//    lost when it closes; the measure is the largest share (lower is better)
//  - venues: bars and pubs, nightclubs, restaurants. Village = within 1,500 m of the resort point; mountain =
//    beyond that and within 150 m of a reachable piste or lift. Late bars = nightclubs plus bars whose
//    opening_hours run past 01:00
//  - ski in, ski out: accommodation within 1,500 m of the resort point; share within 100 m of a reachable
//    piste vertex or lift bottom, and the median distance to the nearest start lift bottom
(() => {
  const R = 6371000, rad = Math.PI / 180;
  const dist = (a, b) => { const x = (b[1] - a[1]) * rad * Math.cos((a[0] + b[0]) / 2 * rad), y = (b[0] - a[0]) * rad; return R * Math.hypot(x, y); };
  const MAIN = new Set(["funicular", "cable_car", "gondola", "mixed_lift", "chair_lift", "drag_lift", "t-bar", "j-bar", "platter"]);
  const DOWN = new Set(["funicular", "cable_car", "gondola", "mixed_lift"]);
  const DRAG = new Set(["drag_lift", "t-bar", "j-bar", "platter"]);
  const ENCL = new Set(["funicular", "cable_car", "gondola", "mixed_lift"]);
  const SKIP = new Set(["goods", "station", "pylon", "zip_line", "construction", "proposed", "disused", "magic_carpet", "rope_tow"]);
  const LEVEL = {
    beginner: { use: new Set(["novice", "easy"]), count: new Set(["novice", "easy"]) },
    intermediate: { use: new Set(["novice", "easy", "intermediate"]), count: new Set(["easy", "intermediate"]) },
    advanced: { use: null, count: new Set(["intermediate", "advanced", "expert", "freeride"]) },
  };
  const S = (window.SCBulk = { raw: null, elev: {}, log: [] });
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const OVERPASS = ["https://overpass-api.de/api/interpreter", "https://overpass.private.coffee/api/interpreter"];
  async function overpass(q) {
    for (let k = 0; k < 10; k++) {
      const u = OVERPASS[k % OVERPASS.length];
      try { const r = await fetch(u, { method: "POST", body: "data=" + encodeURIComponent(q), signal: AbortSignal.timeout(240000) }); const t = await r.text(); if (r.ok && t.startsWith("{")) return JSON.parse(t); S.log.push("overpass " + r.status + " " + u); }
      catch (e) { S.log.push("overpass " + e); }
      await sleep(30000 + 15000 * k);
    }
    throw new Error("overpass failed");
  }

  S.fetch = async (bbox, tiles = 4) => {
    const [s, w, n, e] = bbox, dl = (n - s) / tiles, dw = (e - w) / tiles;
    S.tiles = S.tiles || {}; const ways = new Map(), nodes = new Map(); let osm = null;
    for (let i = 0; i < tiles; i++) for (let j = 0; j < tiles; j++) {
      const b = [s + i * dl, w + j * dw, s + (i + 1) * dl, w + (j + 1) * dw].map((x) => x.toFixed(4)).join(",");
      const q = `[out:json][timeout:180];(way["aerialway"](${b});way["piste:type"="downhill"](${b});way["railway"="funicular"](${b}););out body geom;
        (nwr["amenity"~"^(bar|pub|nightclub|restaurant)$"](${b});nwr["tourism"~"^(hotel|apartment|chalet|guest_house|hostel)$"](${b}););out tags center;`;
      const tk = b; const j2 = S.tiles[tk] || (S.tiles[tk] = await overpass(q)); osm = osm || (j2.osm3s && j2.osm3s.timestamp_osm_base);
      for (const x of j2.elements) { if (x.type === "way" && x.geometry) ways.set(x.id, x); else nodes.set(x.type + x.id, x); }
      S.log.push(`tile ${i},${j}: ${j2.elements.length}`); await sleep(5000);
    }
    const lifts = [], pistes = [], venues = [], beds = [];
    for (const wy of ways.values()) {
      const g = wy.geometry.map((p) => [p.lat, p.lon]), t = wy.tags || {};
      if (t.railway === "funicular") { lifts.push({ id: wy.id, name: t.name || `funicular ${wy.id}`, type: "funicular", g, bubble: true }); continue; }
      if (t.aerialway && !SKIP.has(t.aerialway)) { lifts.push({ id: wy.id, name: t.name || `${t.aerialway} ${wy.id}`, type: t.aerialway, g, bubble: t["aerialway:bubble"] === "yes" }); continue; }
      if (t["piste:type"] === "downhill" && wy.nodes && g.length > 1 && !(t.area === "yes")) {
        if (t["piste:grooming"] === "backcountry" || t.disused === "yes") continue;
        let km = 0; for (let k = 1; k < g.length; k++) km += dist(g[k - 1], g[k]) / 1000;
        pistes.push({ id: wy.id, name: t["piste:name"] || t.name || "", diff: t["piste:difficulty"] || "", oneway: t.oneway !== "no", g, nodes: wy.nodes, km });
      }
    }
    for (const x of nodes.values()) {
      const t = x.tags || {}, p = x.type === "node" ? [x.lat, x.lon] : x.center ? [x.center.lat, x.center.lon] : null; if (!p) continue;
      if (t.amenity) venues.push({ kind: t.amenity, p, name: t.name || "", late: lateHours(t.opening_hours) });
      else if (t.tourism) beds.push({ kind: t.tourism, p });
    }
    const pts = []; lifts.forEach((l) => { pts.push(l.g[0], l.g[l.g.length - 1]); });
    for (let i = 0; i < pts.length; i += 100) {
      const chunk = pts.slice(i, i + 100).filter((p) => !(p.join() in S.elev)); if (!chunk.length) continue;
      const u = `https://api.open-meteo.com/v1/elevation?latitude=${chunk.map((p) => p[0].toFixed(5)).join(",")}&longitude=${chunk.map((p) => p[1].toFixed(5)).join(",")}`;
      let ej = null; for (let k = 0; k < 5 && !ej; k++) { const r = await fetch(u); if (r.ok) ej = await r.json(); else await sleep(61000); }
      chunk.forEach((p, k) => (S.elev[p.join()] = ej.elevation[k])); await sleep(500);
    }
    for (const l of lifts) {
      let a = l.g[0], b = l.g[l.g.length - 1], ea = S.elev[a.join()], eb = S.elev[b.join()];
      if (ea > eb) { [a, b] = [b, a]; [ea, eb] = [eb, ea]; }
      Object.assign(l, { bot: a, top: b, eBot: Math.round(ea), eTop: Math.round(eb), len: Math.round(l.g.reduce((s2, p, i) => s2 + (i ? dist(l.g[i - 1], p) : 0), 0)) });
    }
    S.raw = { lifts, pistes, venues, beds, osm };
    S.G = graph();
    return { snapshot: osm, lifts: lifts.length, pistes: pistes.length, venues: venues.length, beds: beds.length, nodes: S.G.nodes.length };
  };

  // true when an opening_hours string has a span ending after 01:00 (or running past midnight)
  function lateHours(oh) {
    if (!oh) return false; if (/24\/7/.test(oh)) return true;
    for (const m of oh.matchAll(/(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})/g)) {
      const a = +m[1] * 60 + +m[2], b = +m[3] * 60 + +m[4];
      if (b < a ? b > 60 : b > 25 * 60) return true;
    }
    return false;
  }

  function graph() {
    const { lifts, pistes } = S.raw;
    const nodes = [], key = new Map(), grid = new Map(), cell = 0.0003;
    const gk = (p) => Math.floor(p[0] / cell) + ":" + Math.floor(p[1] / cell);
    const near = (p, m) => { const out = [], [a, b] = gk(p).split(":").map(Number), r = Math.ceil(m / 25); for (let i = -r; i <= r; i++) for (let j = -r; j <= r; j++) for (const id of grid.get(a + i + ":" + (b + j)) || []) if (dist(nodes[id], p) <= m) out.push(id); return out; };
    const add = (p, osm) => {
      if (osm != null && key.has("o" + osm)) return key.get("o" + osm);
      const hit = near(p, 20)[0]; if (hit != null) { if (osm != null) key.set("o" + osm, hit); return hit; }
      const id = nodes.length; nodes.push(p); const k = gk(p); if (!grid.has(k)) grid.set(k, []); grid.get(k).push(id);
      if (osm != null) key.set("o" + osm, id); return id;
    };
    const adj = [], edge = (a, b, w, kind, ref) => { (adj[a] = adj[a] || []).push([b, w, kind, ref]); };
    const P = [];
    pistes.forEach((p, pi) => {
      const ids = p.g.map((pt, i) => add(pt, p.nodes[i])); P[pi] = ids;
      for (let i = 1; i < ids.length; i++) { edge(ids[i - 1], ids[i], 0, "p", p.diff); if (!p.oneway) edge(ids[i], ids[i - 1], 0, "p", p.diff); }
    });
    const L = [];
    lifts.forEach((l, i) => {
      const a = add(l.bot, null), b = add(l.top, null); edge(a, b, 1, "l", i);
      if (DOWN.has(l.type) || (l.type === "chair_lift" && l.eTop - l.eBot < 30)) edge(b, a, 1, "l", i);
      L[i] = [a, b];
    });
    for (const i in L) for (const end of L[i]) for (const nb of near(nodes[end], 80)) if (nb !== end) { edge(end, nb, 0, "w"); edge(nb, end, 0, "w"); }
    return { nodes, adj, L, P, near };
  }

  function bfs(G, starts, use, skipLift = -1) {
    const d = new Float64Array(G.nodes.length).fill(Infinity), via = new Int32Array(G.nodes.length).fill(-1);
    let cur = [], next = [];
    for (const s of starts) { d[s] = 0; cur.push(s); }
    while (cur.length) {
      for (let h = 0; h < cur.length; h++) {
        const u = cur[h];
        for (const [v, w, kind, ref] of G.adj[u] || []) {
          if (kind === "p" && use && !use.has(ref)) continue;
          if (kind === "l" && ref === skipLift) continue;
          const nd = d[u] + w;
          if (nd < d[v]) { d[v] = nd; via[v] = kind === "l" ? ref : via[u]; (w ? next : cur).push(v); }
        }
      }
      cur = next; next = [];
    }
    return d;
  }

  const kmReached = (G, d, count) => { let km = 0; S.raw.pistes.forEach((p, pi) => { if (count.has(p.diff) && isFinite(d[G.P[pi][0]])) km += p.km; }); return km; };
  const median = (a) => { if (!a.length) return null; const s = [...a].sort((x, y) => x - y), m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };

  S.measure = (resorts, opts = {}) => {
    const G = S.G, { lifts, pistes, venues, beds } = S.raw, out = [];
    for (const [slug, lat, lon] of resorts) {
      const pt = [lat, lon];
      let st = lifts.map((l, i) => i).filter((i) => MAIN.has(lifts[i].type) && dist(lifts[i].bot, pt) <= 1500);
      let note = "";
      if (!st.length) { const cand = lifts.map((l, i) => [dist(l.bot, pt), i]).filter(([dd, i]) => MAIN.has(lifts[i].type) && dd <= 5000).sort((a, b) => a[0] - b[0]); if (cand.length) { st = [cand[0][1]]; note = "nearest lift " + Math.round(cand[0][0]) + " m"; } }
      if (!st.length) { out.push({ slug, note: "no lift within 5 km" }); continue; }
      const starts = st.map((i) => G.L[i][0]);
      const rec = { slug, startLifts: st.length, note };
      const dAdv = bfs(G, starts, null);
      for (const [lv, cfg] of Object.entries(LEVEL)) rec["km_" + lv] = Math.round(kmReached(G, lv === "advanced" ? dAdv : bfs(G, starts, cfg.use), cfg.count) * 10) / 10;
      // lifts reachable
      const reach = lifts.map((l, i) => i).filter((i) => MAIN.has(lifts[i].type) && isFinite(dAdv[G.L[i][0]]));
      rec.lifts = reach.length; rec.drag_pct = reach.length ? Math.round(100 * reach.filter((i) => DRAG.has(lifts[i].type)).length / reach.length) : null;
      rec.enclosed_pct = reach.length ? Math.round(100 * reach.filter((i) => ENCL.has(lifts[i].type) || lifts[i].bubble).length / reach.length) : null;
      rec.top_m = reach.length ? Math.max(...reach.map((i) => lifts[i].eTop)) : null;
      rec.bottom_m = Math.min(...st.map((i) => lifts[i].eBot)); rec.vertical_m = rec.top_m != null ? rec.top_m - rec.bottom_m : null;
      rec.km_all = Math.round(pistes.reduce((a, p, pi) => a + (isFinite(dAdv[G.P[pi][0]]) ? p.km : 0), 0) * 10) / 10;
      // resilience
      if (opts.resilience !== false && rec.km_advanced > 0) {
        const near2 = reach.filter((i) => dAdv[G.L[i][0]] <= 1 && lifts[i].len >= 300);
        let worst = 0, worstLift = "";
        for (const i of near2) { const d2 = bfs(G, starts.filter((s, k) => st[k] !== i).length ? starts.filter((s, k) => st[k] !== i) : starts, null, i); const lost = 1 - kmReached(G, d2, LEVEL.advanced.count) / rec.km_advanced; if (lost > worst) { worst = lost; worstLift = lifts[i].name; } }
        rec.resilience_lost_pct = Math.round(worst * 100); rec.critical_lift = worstLift;
      }
      // mountain zone: reachable piste vertices and lifts
      const reachPts = []; pistes.forEach((p, pi) => { if (isFinite(dAdv[G.P[pi][0]])) p.g.forEach((q, k) => { if (k % 3 === 0) reachPts.push(q); }); }); reach.forEach((i) => { reachPts.push(lifts[i].bot, lifts[i].top); });
      const zgrid = new Map(), zc = 0.002, zk = (q) => Math.floor(q[0] / zc) + ":" + Math.floor(q[1] / zc);
      reachPts.forEach((q) => { const k = zk(q); if (!zgrid.has(k)) zgrid.set(k, []); zgrid.get(k).push(q); });
      const nearZone = (q, m) => { const [a, b] = zk(q).split(":").map(Number); for (let i = -1; i <= 1; i++) for (let j = -1; j <= 1; j++) for (const r of zgrid.get(a + i + ":" + (b + j)) || []) if (dist(q, r) <= m) return true; return false; };
      const c = { bar_village: 0, bar_mountain: 0, late: 0, restaurant_village: 0, restaurant_mountain: 0 };
      for (const v of venues) {
        const dv = dist(v.p, pt), zone = dv <= 1500 ? "village" : (dv <= 25000 && nearZone(v.p, 150) ? "mountain" : null); if (!zone) continue;
        if (v.kind === "restaurant") c["restaurant_" + zone]++; else { if (v.kind !== "nightclub") c["bar_" + zone]++; if (zone === "village" && (v.kind === "nightclub" || v.late)) c.late++; }
      }
      Object.assign(rec, c);
      const startBots = st.map((i) => lifts[i].bot), bd = [], near100 = [];
      for (const b of beds) { if (dist(b.p, pt) > 1500) continue; bd.push(Math.min(...startBots.map((q) => dist(b.p, q)))); near100.push(nearZone(b.p, 100)); }
      rec.beds_mapped = bd.length; rec.bed_to_lift_m = bd.length ? Math.round(median(bd)) : null; rec.ski_in_out_pct = bd.length ? Math.round(100 * near100.filter(Boolean).length / bd.length) : null;
      out.push(rec);
    }
    return out;
  };

  S.access = async (resorts, from) => {
    // from: {key: [lat, lon]}; OSRM table, all resorts per origin
    const res = {};
    for (const [k, o] of Object.entries(from)) {
      const coords = [o, ...resorts.map((r) => [r[1], r[2]])].map((p) => p[1].toFixed(5) + "," + p[0].toFixed(5)).join(";");
      const u = `https://router.project-osrm.org/table/v1/driving/${coords}?sources=0&annotations=duration,distance`;
      let j = null; for (let t = 0; t < 4 && !j; t++) { const r = await fetch(u); if (r.ok) j = await r.json(); else await sleep(15000); }
      resorts.forEach((r, i) => { (res[r[0]] = res[r[0]] || {})[k] = j && j.durations[0][i + 1] != null ? { min: Math.round(j.durations[0][i + 1] / 60), km: Math.round(j.distances[0][i + 1] / 1000) } : null; });
      await sleep(2000);
    }
    return res;
  };
})();
