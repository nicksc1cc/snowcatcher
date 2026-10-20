"""Shared helpers for the Snow Catchers database: SQL quoting, figure formatting and
page layout resolution. The seed builder and the page exporter both import this, so a
figure is formatted the same way when it is checked on the way in and printed on the way out.
"""
import json
import re
from decimal import Decimal, ROUND_HALF_UP

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
         "nine", "ten", "eleven", "twelve"]


def q(v):
    """SQL literal."""
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float, Decimal)):
        return str(v)
    if isinstance(v, (dict, list)):
        return q(json.dumps(v, ensure_ascii=False)) + "::jsonb"
    return "'" + str(v).replace("'", "''") + "'"


def qarr(items):
    if not items:
        return "'{}'::text[]"
    return "array[" + ",".join(q(i) for i in items) + "]::text[]"


def _num(d, unit):
    d = Decimal(str(d))
    if unit == "cm":
        d = d.quantize(Decimal(1), rounding=ROUND_HALF_UP)
    if d == d.to_integral_value():
        i = int(d)
        return str(i) if unit == "year" else f"{i:,}"
    return f"{d:,.2f}" if unit == "eur" else f"{d:,}"


def fmt_fact(f, mode=None):
    """Format a fact row (dict with value_num/value_text/unit) for print."""
    unit = f.get("unit")
    if f.get("value_text") is not None and f.get("value_num") is None:
        t = f["value_text"]
        if unit == "date":
            y, m, d = (int(x) for x in t.split("-"))
            if mode == "dm":
                return f"{d} {MONTHS[m - 1]}"
            return f"{d} {MONTHS[m - 1]} {y}"
        return t
    v = f["value_num"]
    if mode in ("w", "W"):
        w = WORDS[int(v)]
        return w.capitalize() if mode == "W" else w
    n = _num(v, unit)
    if mode == "n":
        return ("€" + n) if unit == "eur" else n
    if unit == "eur":
        return "€" + n
    if unit in ("km", "m", "cm"):
        return f"{n} {unit}"
    if unit == "pct":
        return f"{n}%"
    return n


def fmt_diff(a, b, mode=None):
    d = abs(Decimal(str(a["value_num"])) - Decimal(str(b["value_num"])))
    return fmt_fact({"value_num": d, "unit": a.get("unit")}, mode)


TOKEN = re.compile(r"\{\{(f|diff|m):([^}|]+)(?:\|([a-zA-Z]+))?\}\}")


def resolve_text(body, facts, matrices=None):
    """Replace {{f:ID|mode}}, {{diff:A,B|mode}} and {{m:matrix.from.to|mode}} tokens."""
    def rep(mt):
        kind, ref, mode = mt.group(1), mt.group(2), mt.group(3)
        if kind == "f":
            return fmt_fact(facts[ref], mode)
        if kind == "diff":
            a, b = ref.split(",")
            return fmt_diff(facts[a], facts[b], mode)
        name, fr, to = ref.split(".")
        return fmt_fact({"value_num": matrices[name][fr][to], "unit": "count"}, mode)
    return TOKEN.sub(rep, body)


def token_refs(body):
    out = []
    for kind, ref, _ in TOKEN.findall(body):
        if kind == "f":
            out.append(ref)
        elif kind == "diff":
            out.extend(ref.split(","))
    return out


def num_out(v):
    d = Decimal(str(v))
    return int(d) if d == d.to_integral_value() else float(d)


def resolve_layout(node, ctx):
    """Walk a page layout and replace references with values.
    ctx: blocks{field:body}, facts{id:row}, places{id:row}, lists{id:[items]},
         media{id:row}, links{dataset:[rows]}, matrices{name:matrix}."""
    if isinstance(node, list):
        return [resolve_layout(x, ctx) for x in node]
    if not isinstance(node, dict):
        return node
    if "$b" in node:
        return resolve_text(ctx["blocks"][node["$b"]], ctx["facts"], ctx["matrices"])
    if "$f" in node:
        return num_out(ctx["facts"][node["$f"]]["value_num"])
    if "$m" in node:
        name, fr, to = node["$m"]
        return ctx["matrices"][name][fr][to]
    if "$p" in node:
        return ctx["places"][node["$p"]]["name"]
    if "$media" in node:
        m = ctx["media"][node["$media"]]
        return [m["file_name"], m["author"], m["licence"], m["alt"]]
    if "$list" in node:
        out = []
        for it in ctx["lists"][node["$list"]]:
            a = it.get("attrs") or {}
            name = a.get("name") or ctx["places"][it["item_place_id"]]["name"]
            out.append({"name": name, "where": a.get("where"),
                        "text": resolve_text(it["blurb"], ctx["facts"], ctx["matrices"])})
        return out
    if "$links" in node:
        return ctx["links"][node["$links"]]
    return {k: resolve_layout(v, ctx) for k, v in node.items()}
