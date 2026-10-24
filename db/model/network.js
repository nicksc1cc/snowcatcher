// Snow Catchers lift and piste network model.
//
// Runs in a browser page (the research workspace cannot reach Overpass or Open-Meteo), for example
// on https://example.com through the built-in browser. Paste this file, then:
//   await SCNet.fetch(cfg)      OpenStreetMap lifts and pistes in cfg.bbox, lift end heights from Open-Meteo
//   SCNet.lifts(cfg)            one line per lift (to choose sector centres and check assignments)
//   SCNet.analyse(cfg)          matrices, base table, critical lifts, heights, mapped piste by sector
//   SCNet.route(cfg, from, to, ability)   the lifts on one fewest-rides route
//
// Model (as used for the Portes du Soleil and Les 3 Vallées, 20 October 2026):
//  - piste vertices shared by OSM node id, then snapped within 20 m; piste edges follow way order
//    (downhill by OSM convention), oneway=no adds the reverse
//  - lifts run bottom to top by DEM height; gondolas, cable cars and mixed lifts can also be ridden
//    down; chairs with under 30 m of rise run both ways
//  - walk edges both ways between a lift end and any node within 80 m; hand transfers from cfg.transfers
//  - cost is lift rides (0/1 breadth first search); targets are main lift bases in the target sector
//  - ability: easy = novice and easy runs, red = up to intermediate, all = every piste way
//  - matrix starts: every main lift base in the sector; base table starts: main lift bases within
//    200 m of the sector's lowest main lift (the village lifts)
//
// cfg = { bbox:[s,w,n,e], exclude:[[s,w,n,e],...], sectors:{id:[lat,lon]}, liftSector:{"lift name":id},
//         transfers:[[label,[lat,lon],[lat,lon]]], topAbove: 2800, dropLifts:["second cabin of a double lift"],
//         dropWays:[OSM way ids to ignore, such as the passing loops of a funicular] }
// Funiculars (railway=funicular) count as lifts that can be ridden both ways.
// A lift given a sector id that is not in cfg.sectors (for example "x-outlying") is kept in the graph but
// left out of every sector's starts, targets and counts.
(() => {
  const R = 6371000, rad = Math.PI / 180;
  const dist = (a, b) => { const x = (b[1] - a[1]) * rad * Math.cos((a[0] + b[0]) / 2 * rad), y = (b[0] - a[0]) * rad; return R * Math.hypot(x, y); };
  const MAIN = new Set(["funicular", "cable_car", "gondola", "mixed_lift", "chair_lift", "drag_lift", "t-bar", "j-bar", "platter"]);
  const DOWN = new Set(["funicular", "cable_car", "gondola", "mixed_lift"]);
  const DRAG = new Set(["drag_lift", "t-bar", "j-bar", "platter"]);
  const SKIP = new Set(["goods", "station", "pylon", "zip_line", "construction", "proposed", "disused"]);
  const EASY = new Set(["novice", "easy"]), RED = new Set(["novice", "easy", "intermediate"]);
  const S = (window.SCNet = { raw: null, elev: {} });

  S.fetch = async (cfg) => {
    const [s, w, n, e] = cfg.bbox;
    const q = `[out:json][timeout:180];(way["aerialway"](${s},${w},${n},${e});way["piste:type"="downhill"](${s},${w},${n},${e});way["railway"="funicular"](${s},${w},${n},${e}););out body geom;`;
    const r = await fetch("https://overpass-api.de/api/interpreter", { method: "POST", body: "data=" + encodeURIComponent(q) });
    const j = await r.json();
    const out = (p) => (cfg.exclude || []).some(([a, b, c, d]) => p[0] >= a && p[0] <= c && p[1] >= b && p[1] <= d);
    const ways = j.elements.filter((x) => x.type === "way" && x.geometry);
    const lifts = [], pistes = [];
    for (const wy of ways) {
      const g = wy.geometry.map((p) => [p.lat, p.lon]), t = wy.tags || {};
      if ((cfg.dropWays || []).includes(wy.id)) continue;
      if (t.railway === "funicular") {
        // funiculars mapped in several ways (bridge, tunnel) are joined end to end under one name
        const prev = lifts.find((l) => l.type === "funicular" && l.name === (t.name || "") && [l.g[0], l.g[l.g.length - 1]].some((p) => (p[0] === g[0][0] && p[1] === g[0][1]) || (p[0] === g[g.length - 1][0] && p[1] === g[g.length - 1][1])));
        if (prev) { const pe = prev.g[prev.g.length - 1]; prev.g = (pe[0] === g[0][0] && pe[1] === g[0][1]) ? prev.g.concat(g.slice(1)) : g.concat(prev.g.slice(1)); }
        else if (!out(g[0])) lifts.push({ id: wy.id, name: t.name || `funicular ${wy.id}`, type: "funicular", g });
        continue;
      }
      if (t.aerialway && !SKIP.has(t.aerialway)) { if (!out(g[0]) && !(cfg.dropLifts || []).includes(t.name)) lifts.push({ id: wy.id, name: t.name || `${t.aerialway} ${wy.id}`, type: t.aerialway, g }); }
      else if (t["piste:type"] === "downhill" && wy.nodes && !out(g[Math.floor(g.length / 2)])) {
        if (g.length > 1 && !(g[0][0] === g[g.length - 1][0] && g[0][1] === g[g.length - 1][1] && t.area === "yes"))
          pistes.push({ id: wy.id, name: t["piste:name"] || t.name || "", diff: t["piste:difficulty"] || "", oneway: t.oneway === "no" ? false : true, g, nodes: wy.nodes, closed: t["piste:grooming"] === "backcountry" || t.disused === "yes" });
      }
    }
    // lift end heights, 100 points a request
    const pts = []; lifts.forEach((l) => { pts.push(l.g[0], l.g[l.g.length - 1]); });
    for (let i = 0; i < pts.length; i += 100) {
      const chunk = pts.slice(i, i + 100).filter((p) => !(p.join() in S.elev));
      if (!chunk.length) continue;
      const u = `https://api.open-meteo.com/v1/elevation?latitude=${chunk.map((p) => p[0].toFixed(5)).join(",")}&longitude=${chunk.map((p) => p[1].toFixed(5)).join(",")}`;
      const ej = await (await fetch(u)).json();
      chunk.forEach((p, k) => (S.elev[p.join()] = ej.elevation[k]));
      await new Promise((res) => setTimeout(res, 400));
    }
    for (const l of lifts) {
      let a = l.g[0], b = l.g[l.g.length - 1], ea = S.elev[a.join()], eb = S.elev[b.join()];
      if (ea > eb) { [a, b] = [b, a]; [ea, eb] = [eb, ea]; }
      Object.assign(l, { bot: a, top: b, eBot: Math.round(ea), eTop: Math.round(eb), len: Math.round(l.g.reduce((s2, p, i) => s2 + (i ? dist(l.g[i - 1], p) : 0), 0)) });
    }
    S.raw = { lifts, pistes, osm: j.osm3s && j.osm3s.timestamp_osm_base };
    return { snapshot: S.raw.osm, lifts: lifts.length, mainLifts: lifts.filter((l) => MAIN.has(l.type)).length, pistes: pistes.length,
             pisteKm: Math.round(pistes.reduce((s2, p) => s2 + p.g.reduce((a, q2, i) => a + (i ? dist(p.g[i - 1], q2) : 0), 0), 0) / 1000) };
  };

  const nearest = (cfg, p) => { let best = null, bd = 1e12; for (const [k, c] of Object.entries(cfg.sectors)) { const d = dist(p, c); if (d < bd) { bd = d; best = k; } } return best; };
  const sectorOf = (cfg, l) => (cfg.liftSector && cfg.liftSector[l.name]) || nearest(cfg, l.bot);

  S.lifts = (cfg) => S.raw.lifts.map((l) => [l.name, l.type, l.bot.map((x) => +x.toFixed(4)).join(","), l.eBot, l.eTop, l.len, cfg && cfg.sectors ? sectorOf(cfg, l) : ""].join("|"));

  function graph(cfg, skipLift) {
    const { lifts, pistes } = S.raw;
    const nodes = [], key = new Map(), grid = new Map(), cell = 0.0003;
    const gk = (p) => Math.floor(p[0] / cell) + ":" + Math.floor(p[1] / cell);
    const near = (p, m) => { const out = [], [a, b] = gk(p).split(":").map(Number), r = Math.ceil(m / 25); for (let i = -r; i <= r; i++) for (let j = -r; j <= r; j++) for (const id of grid.get(a + i + ":" + (b + j)) || []) if (dist(nodes[id], p) <= m) out.push(id); return out; };
    const add = (p, osm) => {
      if (osm != null && key.has("o" + osm)) return key.get("o" + osm);
      const hit = near(p, 20)[0];
      if (hit != null) { if (osm != null) key.set("o" + osm, hit); return hit; }
      const id = nodes.length; nodes.push(p); const k = gk(p); if (!grid.has(k)) grid.set(k, []); grid.get(k).push(id);
      if (osm != null) key.set("o" + osm, id); return id;
    };
    const adj = [], edge = (a, b, w, kind, ref) => { (adj[a] = adj[a] || []).push([b, w, kind, ref]); };
    for (const p of pistes) {
      if (p.closed) continue;
      const ids = p.g.map((pt, i) => add(pt, p.nodes[i]));
      for (let i = 1; i < ids.length; i++) { edge(ids[i - 1], ids[i], 0, "p", p.diff); if (!p.oneway) edge(ids[i], ids[i - 1], 0, "p", p.diff); }
    }
    const L = [];
    lifts.forEach((l, i) => {
      if (i === skipLift) return;
      const a = add(l.bot, null), b = add(l.top, null);
      edge(a, b, 1, "l", i);
      if (DOWN.has(l.type) || (l.type === "chair_lift" && l.eTop - l.eBot < 30)) edge(b, a, 1, "l", i);
      L[i] = [a, b];
    });
    for (const i in L) for (const end of L[i]) for (const nb of near(nodes[end], 80)) if (nb !== end) { edge(end, nb, 0, "w"); edge(nb, end, 0, "w"); }
    for (const [, x, y] of cfg.transfers || []) { const a = add(x, null), b = add(y, null); for (const u of near(nodes[a], 80)) { edge(a, u, 0, "w"); edge(u, a, 0, "w"); } for (const u of near(nodes[b], 80)) { edge(b, u, 0, "w"); edge(u, b, 0, "w"); } edge(a, b, 0, "t"); edge(b, a, 0, "t"); }
    return { nodes, adj, L };
  }

  function bfs(G, starts, ability) {
    const d = new Float64Array(G.nodes.length).fill(Infinity), prev = new Int32Array(G.nodes.length).fill(-1), via = [];
    const dq = []; let h = 0;
    for (const s of starts) { d[s] = 0; dq.push(s); }
    // 0/1 BFS with a simple two queue scheme
    let cur = dq, next = [];
    while (cur.length) {
      for (h = 0; h < cur.length; h++) {
        const u = cur[h];
        for (const [v, w, kind, ref] of G.adj[u] || []) {
          if (kind === "p" && ability === "easy" && !EASY.has(ref)) continue;
          if (kind === "p" && ability === "red" && !RED.has(ref)) continue;
          const nd = d[u] + w;
          if (nd < d[v]) { d[v] = nd; prev[v] = u; via[v] = kind === "l" ? ref : null; (w ? next : cur).push(v); }
        }
      }
      cur = next; next = [];
    }
    return { d, prev, via };
  }

  S.analyse = (cfg, opts = {}) => {
    const { lifts, pistes } = S.raw, ids = Object.keys(cfg.sectors);
    const sec = lifts.map((l) => sectorOf(cfg, l));
    const main = lifts.map((l) => MAIN.has(l.type));
    const G = graph(cfg, -1);
    const bases = (s) => lifts.map((l, i) => i).filter((i) => sec[i] === s && main[i] && G.L[i]).map((i) => G.L[i][0]);
    const village = (s) => { const ix = lifts.map((l, i) => i).filter((i) => sec[i] === s && main[i]); if (!ix.length) return []; const lo = ix.reduce((a, i) => (lifts[i].eBot < lifts[a].eBot ? i : a), ix[0]); return ix.filter((i) => dist(lifts[i].bot, lifts[lo].bot) <= 200).map((i) => G.L[i][0]); };
    const matrix = (g, ability, startOf) => { const m = {}; for (const a of ids) { const r = bfs(g, startOf(a), ability); m[a] = {}; for (const b of ids) if (b !== a) { const t = lifts.map((l, i) => i).filter((i) => sec[i] === b && main[i] && g.L[i]); const v = Math.min(...t.map((i) => r.d[g.L[i][0]])); m[a][b] = isFinite(v) ? v : null; } } return m; };
    const res = { snapshot: S.raw.osm, ids };
    res.all = matrix(G, "all", bases); res.easy = matrix(G, "easy", bases); res.red = matrix(G, "red", bases);
    // base table from the village lifts, with a "top above" column
    const top = cfg.topAbove || 2800;
    res.base = {};
    for (const a of ids) {
      const r = bfs(G, village(a), "all"); res.base[a] = {};
      for (const b of cfg.baseTargets || ids) { const t = lifts.map((l, i) => i).filter((i) => sec[i] === b && main[i] && G.L[i]); const v = Math.min(...t.map((i) => r.d[G.L[i][0]])); res.base[a][b] = a === b ? 0 : (isFinite(v) ? v : null); }
      const hi = lifts.map((l, i) => i).filter((i) => main[i] && lifts[i].eTop >= top && G.L[i]); const v = Math.min(...hi.map((i) => r.d[G.L[i][0]] + 1)); res.base[a]["top" + top] = isFinite(v) ? v : null;
      for (const extra of cfg.baseExtra || []) { const t = lifts.map((l, i) => i).filter((i) => sec[i] === extra && main[i] && G.L[i]); const v2 = Math.min(...t.map((i) => r.d[G.L[i][0]])); res.base[a][extra] = isFinite(v2) ? v2 : null; }
    }
    // sectors: heights, lifts, mapped piste
    res.sectors = {};
    for (const s of ids) {
      const ix = lifts.map((l, i) => i).filter((i) => sec[i] === s && main[i]);
      res.sectors[s] = { lifts: lifts.filter((l, i) => sec[i] === s).length, main: ix.length, drags: ix.filter((i) => DRAG.has(lifts[i].type)).length,
        lo: ix.length ? Math.min(...ix.map((i) => lifts[i].eBot)) : null, hi: ix.length ? Math.max(...ix.map((i) => lifts[i].eTop)) : null, km: 0, easyKm: 0, redKm: 0, blackKm: 0 };
    }
    for (const p of pistes) {
      if (p.closed) continue;
      const s = nearest(cfg, p.g[Math.floor(p.g.length / 2)]), km = p.g.reduce((a, q2, i) => a + (i ? dist(p.g[i - 1], q2) : 0), 0) / 1000;
      res.sectors[s].km += km; if (EASY.has(p.diff)) res.sectors[s].easyKm += km; else if (p.diff === "intermediate") res.sectors[s].redKm += km; else if (p.diff) res.sectors[s].blackKm += km;
    }
    for (const s of ids) for (const k of ["km", "easyKm", "redKm", "blackKm"]) res.sectors[s][k] = Math.round(res.sectors[s][k] * 10) / 10;
    res.totals = { lifts: lifts.length, main: main.filter(Boolean).length, drags: lifts.filter((l) => DRAG.has(l.type)).length, pisteWays: pistes.length,
      pisteKm: Math.round(Object.values(res.sectors).reduce((a, x) => a + x.km, 0)) };
    // critical lifts: closing one main lift over 300 m
    if (opts.critical !== false) {
      res.critical = [];
      lifts.forEach((l, i) => {
        if (!main[i] || l.len < 300) return;
        const g = graph(cfg, i), m = matrix(g, "all", (s) => lifts.map((x, j) => j).filter((j) => sec[j] === s && main[j] && g.L[j]).map((j) => g.L[j][0]));
        let lost = 0, extra = 0;
        for (const a of ids) for (const b of ids) if (a !== b && res.all[a][b] != null) { if (m[a][b] == null) lost++; else extra += m[a][b] - res.all[a][b]; }
        if (lost || extra) res.critical.push([l.name, sec[i], lost, extra]);
      });
      res.critical.sort((x, y) => y[2] - x[2] || y[3] - x[3]);
    }
    S.last = { cfg, G, sec, main };
    return res;
  };

  S.route = (cfg, from, to, ability = "all") => {
    const { G, sec, main } = S.last, lifts = S.raw.lifts;
    const starts = lifts.map((l, i) => i).filter((i) => sec[i] === from && main[i] && G.L[i]).map((i) => G.L[i][0]);
    const r = bfs(G, starts, ability);
    const t = lifts.map((l, i) => i).filter((i) => sec[i] === to && main[i] && G.L[i]);
    let best = t.reduce((a, i) => (r.d[G.L[i][0]] < r.d[G.L[a][0]] ? i : a), t[0]), v = G.L[best][0], out = [];
    while (v !== -1 && r.prev[v] !== -1) { if (r.via[v] != null) out.push(lifts[r.via[v]].name); v = r.prev[v]; }
    return { rides: r.d[G.L[best][0]], lifts: out.reverse() };
  };
})();
