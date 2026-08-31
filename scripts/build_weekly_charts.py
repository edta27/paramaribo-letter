#!/usr/bin/env python3
"""Build a weekly Chart Desk pack from CoinGecko (public price/volume).

Does not scrape Glassnode or Farside. ETF issuer-flow series stay out of the
pack unless you paste sourced numbers into the JSON by hand.
"""

from __future__ import annotations

import argparse
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKS = ROOT / "public" / "charts" / "packs"
CATALOG = ROOT / "public" / "charts" / "catalog.json"
UA = {"User-Agent": "ParamariboLetter/1.0", "Accept": "application/json"}


def fetch(url: str) -> dict:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45) as res:
        return json.loads(res.read())


def dailyize(pairs: list[list[float]]) -> list[list[float]]:
    """Collapse intraday points to one last-print per UTC day."""
    by_day: dict[str, list[float]] = {}
    for ts_ms, val in pairs:
        day = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
        by_day[day] = [ts_ms, float(val)]
    return [by_day[k] for k in sorted(by_day)]


def volume_deltas(vols: list[list[float]]) -> list[list[float]]:
    out = []
    for i, (ts, v) in enumerate(vols):
        if i == 0:
            out.append([ts, 0.0])
        else:
            out.append([ts, float(v) - float(vols[i - 1][1])])
    return out


def series_payload(coin_id: str, days: int = 90) -> dict:
    url = (
        f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        f"?vs_currency=usd&days={days}"
    )
    raw = fetch(url)
    prices = dailyize(raw.get("prices") or [])
    vols = dailyize(raw.get("total_volumes") or [])
    # Align lengths on shared days
    pmap = {datetime.fromtimestamp(t / 1000, tz=timezone.utc).strftime("%Y-%m-%d"): [t, v] for t, v in prices}
    vmap = {datetime.fromtimestamp(t / 1000, tz=timezone.utc).strftime("%Y-%m-%d"): [t, v] for t, v in vols}
    days_keys = sorted(set(pmap) & set(vmap))
    prices = [pmap[d] for d in days_keys]
    vols = [vmap[d] for d in days_keys]
    return {
        "prices": prices,
        "volumes": vols,
        "volume_deltas": volume_deltas(vols),
        "last_price": prices[-1][1] if prices else None,
        "first_price": prices[0][1] if prices else None,
    }


def pct(a: float | None, b: float | None) -> str:
    if not a or not b:
        return "n/a"
    return f"{((b / a) - 1) * 100:+.1f}%"


def build_pack(as_of: datetime) -> dict:
    btc = series_payload("bitcoin", 90)
    sol = series_payload("solana", 90)
    day = as_of.strftime("%Y-%m-%d")
    pack_id = f"{day}-weekly"

    btc_chg = pct(btc["first_price"], btc["last_price"])
    sol_chg = pct(sol["first_price"], sol["last_price"])
    btc_last = btc["last_price"]
    sol_last = sol["last_price"]

    return {
        "id": pack_id,
        "date": day,
        "kicker": "Chart Desk · Weekly",
        "title": "Weekly charts: BTC stall tape and SOL volume",
        "dek": (
            f"As-of {as_of.strftime('%d %b %Y %H:%M UTC')}. Dual charts from public CoinGecko "
            "price/volume — not Glassnode issuer ETF flows. Educational only."
        ),
        "asOf": as_of.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "cadence": "weekly",
        "thesis": "Bitcoin is still in a $77–80k stall. AI equities can bid without making that one trade.",
        "stakes": (
            f"Spot ~${btc_last:,.0f}. Until a Daily close reclaims $80k or loses $77k, "
            "the desk stays cash / observe — charts below are the tape under that call."
        ),
        "levels": ["$77k", "$78.8k", "$80k", "$81–81.5k"],
        "letterId": "2026-08-31-two-tapes",
        "letterUrl": "/issue?id=2026-08-31-two-tapes",
        "letterLabel": "Issue 14 · Two tapes",
        "subscribeHook": (
            "When the Daily close breaks the stall — or fails it — the letter hits your inbox "
            "the same day. Charts stay free here; the call moves by email."
        ),
        "sourceNote": (
            "Charts built from CoinGecko market_chart (USD). Green/red bars are day-over-day "
            "spot volume change, a tape proxy — not US spot ETF net creations. Issuer ETF flow "
            "tables (Farside / Glassnode / SoSoValue) were not available to this builder; paste "
            "sourced ETF numbers into a future pack when you have them."
        ),
        "briefs": [
            {
                "id": "btc-stall",
                "asset": "BTC",
                "headline": f"Bitcoin ~${btc_last:,.0f}: still a two-way stall on the 90-day tape",
                "lede": (
                    f"90-day change about {btc_chg}. Issue 14’s working map remains the "
                    "$77–80k observation box until a Daily close decides."
                ),
                "bodyHtml": (
                    f"<p><strong>Fact (CoinGecko).</strong> Last ~${btc_last:,.0f}. "
                    f"Ninety-day path {btc_chg} from the start of this window. "
                    "Bars below are day-over-day changes in reported spot volume (USD), "
                    "overlaid with price — a Glassnode-style dual panel, not an ETF creation print.</p>"
                    "<p><strong>Analysis.</strong> Volume spikes that do not reclaim the failed "
                    "high zone are still digestion inside the stall. Quiet green bars under "
                    "$80k are not confirmation of a floor.</p>"
                    "<p><strong>Scenarios.</strong> A — Daily acceptance back above $80k toward "
                    "$81–81.5k. B — Daily acceptance below $77k opens the deeper process map "
                    "(75.6k / 71.7–72.3k). Invalidation is the Daily close, not an intraday wick.</p>"
                    "<p>Educational scenario research. Not advice. No leverage.</p>"
                ),
                "charts": [
                    {
                        "title": "BTC: daily volume Δ [USD] vs price",
                        "bars": {
                            "label": "BTC volume day-over-day Δ [USD]",
                            "data": btc["volume_deltas"],
                        },
                        "line": {
                            "label": "BTC price [USD]",
                            "data": btc["prices"],
                        },
                    },
                    {
                        "title": "BTC: daily spot volume [USD] vs price",
                        "bars": {
                            "label": "BTC spot volume [USD]",
                            "data": btc["volumes"],
                            "unsigned": True,
                        },
                        "line": {
                            "label": "BTC price [USD]",
                            "data": btc["prices"],
                        },
                    },
                ],
            },
            {
                "id": "sol-tape",
                "asset": "SOL",
                "headline": f"Solana ~${sol_last:,.2f}: 90-day volume and price, not ETF AUM",
                "lede": (
                    f"90-day change about {sol_chg}. Public issuer ETF flow / BSOL AUM prints "
                    "are not in this pack — cite Farside or Glassnode when you add them next week."
                ),
                "bodyHtml": (
                    f"<p><strong>Fact (CoinGecko).</strong> Last ~${sol_last:,.2f}. "
                    f"Ninety-day path {sol_chg}. Same dual layout as Bitcoin: volume Δ and "
                    "absolute volume versus price.</p>"
                    "<p><strong>Analysis.</strong> Spot volume expansion with a soft price tape "
                    "is not the same as documented US spot SOL ETF net creations. Do not read "
                    "these bars as Bitwise BSOL AUM.</p>"
                    "<p><strong>Next pack.</strong> When a sourced ETF flow table is available, "
                    "replace or append a third brief with net-flow bars and cumulative balances "
                    "— attributed to that source, not reverse-engineered from this screenshot.</p>"
                    "<p>Educational scenario research. Not advice.</p>"
                ),
                "charts": [
                    {
                        "title": "SOL: daily volume Δ [USD] vs price",
                        "bars": {
                            "label": "SOL volume day-over-day Δ [USD]",
                            "data": sol["volume_deltas"],
                        },
                        "line": {
                            "label": "SOL price [USD]",
                            "data": sol["prices"],
                        },
                    },
                    {
                        "title": "SOL: daily spot volume [USD] vs price",
                        "bars": {
                            "label": "SOL spot volume [USD]",
                            "data": sol["volumes"],
                            "unsigned": True,
                        },
                        "line": {
                            "label": "SOL price [USD]",
                            "data": sol["prices"],
                        },
                    },
                ],
            },
        ],
    }


def write_catalog(pack: dict) -> None:
    rows = []
    if CATALOG.exists():
        try:
            rows = json.loads(CATALOG.read_text())
        except Exception:
            rows = []
    if not isinstance(rows, list):
        rows = []
    public = {
        k: pack[k]
        for k in (
            "id",
            "date",
            "kicker",
            "title",
            "dek",
            "asOf",
            "cadence",
            "thesis",
            "stakes",
            "levels",
            "subscribeHook",
            "letterId",
            "letterUrl",
            "letterLabel",
        )
        if k in pack
    }
    rows = [r for r in rows if r.get("id") != pack["id"]]
    rows.insert(0, public)
    rows.sort(key=lambda r: (r.get("date") or "", r.get("id") or ""), reverse=True)
    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    CATALOG.write_text(json.dumps(rows, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default="")
    args = parser.parse_args()
    as_of = (
        datetime.fromisoformat(args.date.replace("Z", "+00:00"))
        if args.date
        else datetime.now(timezone.utc)
    )
    if as_of.tzinfo is None:
        as_of = as_of.replace(tzinfo=timezone.utc)
    pack = build_pack(as_of)
    PACKS.mkdir(parents=True, exist_ok=True)
    path = PACKS / f"{pack['id']}.json"
    path.write_text(json.dumps(pack, indent=2) + "\n")
    write_catalog(pack)
    print(f"wrote {path.relative_to(ROOT)}")
    print(f"catalog {CATALOG.relative_to(ROOT)} ({pack['id']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
