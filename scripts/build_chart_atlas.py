#!/usr/bin/env python3
"""Build Paramaribo Letter's free-data Bitcoin cycle and on-chain atlas."""

from __future__ import annotations

import json
import math
import statistics
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "charts" / "atlas.json"
GENESIS = date(2009, 1, 3)
CYCLE_EPOCH = datetime(2000, 1, 1, tzinfo=timezone.utc)
HALVINGS = [date(2012, 11, 28), date(2016, 7, 9), date(2020, 5, 11), date(2024, 4, 20)]


def get_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "ParamariboLetter/1.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.load(response)


def utc_ms(day: date) -> int:
    return int(datetime(day.year, day.month, day.day, tzinfo=timezone.utc).timestamp() * 1000)


def parse_day(value: str) -> date:
    return date.fromisoformat(value[:10])


def pct_change(current: float, previous: float) -> float:
    return (current / previous - 1.0) * 100.0


def compact_money(value: float) -> str:
    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:,.0f}"


def coinmetrics_rows() -> list[dict]:
    params = urllib.parse.urlencode({
        "assets": "btc",
        "metrics": "PriceUSD,CapMVRVCur,AdrActCnt",
        "frequency": "1d",
        "start_time": "2010-07-18",
        "end_time": datetime.now(timezone.utc).date().isoformat(),
        "page_size": 10000,
    })
    payload = get_json(f"https://community-api.coinmetrics.io/v4/timeseries/asset-metrics?{params}")
    rows = []
    for item in payload.get("data", []):
        try:
            rows.append({
                "date": parse_day(item["time"]),
                "price": float(item["PriceUSD"]),
                "mvrv": float(item["CapMVRVCur"]),
                "active": int(item["AdrActCnt"]),
            })
        except (KeyError, TypeError, ValueError):
            continue
    if len(rows) < 1000:
        raise RuntimeError("Coin Metrics returned too little BTC history")
    return rows


def rainbow_brief(rows: list[dict]) -> dict:
    fit_rows = [row for row in rows if row["date"] >= date(2011, 1, 1) and row["price"] > 0]
    xs = [math.log10((row["date"] - GENESIS).days + 1) for row in fit_rows]
    ys = [math.log10(row["price"]) for row in fit_rows]
    x_mean = statistics.mean(xs)
    y_mean = statistics.mean(ys)
    slope = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys)) / sum((x - x_mean) ** 2 for x in xs)
    intercept = y_mean - slope * x_mean
    residuals = [y - (intercept + slope * x) for x, y in zip(xs, ys)]
    sigma = statistics.pstdev(residuals)
    sampled = fit_rows[::7]
    z_steps = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0]
    colors = ["#2563eb", "#0891b2", "#059669", "#65a30d", "#ca8a04", "#ea580c", "#dc2626", "#be123c", "#7e22ce"]
    labels = ["−2σ", "−1.5σ", "−1σ", "−0.5σ", "Trend", "+0.5σ", "+1σ", "+1.5σ", "+2σ"]
    series = [{
        "label": "BTC price [USD]",
        "useThemeText": True,
        "lineWidth": 3,
        "data": [[utc_ms(row["date"]), round(row["price"], 2)] for row in sampled],
    }]
    for z, color, label in zip(z_steps, colors, labels):
        data = []
        for row in sampled:
            x = math.log10((row["date"] - GENESIS).days + 1)
            value = 10 ** (intercept + slope * x + z * sigma)
            data.append([utc_ms(row["date"]), round(value, 2)])
        series.append({"label": label, "color": color, "lineWidth": 1, "lastValueVisible": False, "data": data})
    latest = fit_rows[-1]
    latest_x = math.log10((latest["date"] - GENESIS).days + 1)
    latest_z = (math.log10(latest["price"]) - (intercept + slope * latest_x)) / sigma
    return {
        "id": "atlas-rainbow",
        "asset": "BTC · RAINBOW REGRESSION",
        "headline": "A dynamic rainbow, with the assumptions left visible",
        "lede": f"BTC finished {latest['date'].isoformat()} at {compact_money(latest['price'])}, {latest_z:+.2f} standard deviations from the fitted long-run log trend.",
        "bodyHtml": (
            "<p><strong>Method.</strong> Paramaribo fits log10(BTC price) against log10(days since genesis) using daily Coin Metrics data from 2011 onward. "
            "The nine colored lines are half-standard-deviation residual steps around that fitted trend.</p>"
            "<p><strong>Use.</strong> This is a long-horizon valuation map, not a timing signal or a law of nature. The regression refits as new data arrive, so historical band placement can move.</p>"
        ),
        "charts": [{
            "title": "BTC price and dynamic log-regression rainbow bands",
            "logScale": True,
            "legend": "Log scale · weekly observations · move across for band values",
            "series": series,
        }],
    }


def cycle_brief(rows: list[dict]) -> dict:
    by_day = {row["date"]: row["price"] for row in rows}
    palette = ["#a855f7", "#f97316", "#22c55e", "#2e90fa"]
    series = []
    current_day = (rows[-1]["date"] - HALVINGS[-1]).days
    current_index = None
    for halving, color in zip(HALVINGS, palette):
        base = by_day.get(halving)
        if not base:
            continue
        points = []
        max_day = min(1100, (rows[-1]["date"] - halving).days)
        for relative in range(-180, max_day + 1, 7):
            day = halving + timedelta(days=relative)
            price = by_day.get(day)
            if price is None:
                continue
            synthetic = CYCLE_EPOCH + timedelta(days=relative + 365)
            index = price / base * 100.0
            points.append([int(synthetic.timestamp() * 1000), round(index, 2)])
            if halving == HALVINGS[-1] and abs(relative - current_day) < 7:
                current_index = index
        series.append({
            "label": f"{halving.year} cycle",
            "color": color,
            "lineWidth": 2 if halving == HALVINGS[-1] else 1,
            "data": points,
        })
    index_text = f"{current_index:.0f}" if current_index is not None else "unavailable"
    return {
        "id": "atlas-four-year-cycle",
        "asset": "BTC · FOUR-YEAR CYCLES",
        "headline": "Compare the current cycle without pretending the calendar must repeat",
        "lede": f"The 2024 halving cycle is at day +{current_day}; its sampled price index is about {index_text}, with halving day set to 100.",
        "bodyHtml": (
            "<p><strong>Method.</strong> Each cycle is aligned to its halving date and normalized to 100 on that date. Weekly observations run from 180 days before to 1,100 days after each halving.</p>"
            "<p><strong>Use.</strong> This reveals similarities and breaks in path, speed, and drawdown. Four completed or partial cycles are too few to treat repetition as a statistical certainty.</p>"
        ),
        "charts": [{
            "title": "BTC halving-cycle price index · halving day = 100",
            "xMode": "cycleDays",
            "logScale": True,
            "legend": "Cycle day · logarithmic price index",
            "series": series,
        }],
    }


def onchain_brief(rows: list[dict]) -> dict:
    cutoff = rows[-1]["date"] - timedelta(days=730)
    window = [row for row in rows if row["date"] >= cutoff][::7]
    latest = rows[-1]
    nupl = 1.0 - 1.0 / latest["mvrv"]
    realized = latest["price"] / latest["mvrv"]
    price_data = [[utc_ms(row["date"]), round(row["price"], 2)] for row in window]
    realized_data = [[utc_ms(row["date"]), round(row["price"] / row["mvrv"], 2)] for row in window]
    nupl_data = [[utc_ms(row["date"]), round(1.0 - 1.0 / row["mvrv"], 4)] for row in window]
    return {
        "id": "atlas-onchain-value",
        "asset": "BTC · ON-CHAIN VALUE",
        "headline": "Network cost basis is profitable, but not euphoric",
        "lede": f"The community-data proxy puts network realized price near {compact_money(realized)} and NUPL near {nupl:.2f} on {latest['date'].isoformat()}.",
        "bodyHtml": (
            "<p><strong>Method.</strong> Realized price proxy = PriceUSD ÷ MVRV. NUPL proxy = 1 − 1/MVRV, using Coin Metrics community MVRV.</p>"
            "<p><strong>Boundary.</strong> This is a network-wide proxy. It does not reproduce Glassnode's proprietary whale, shark, or shrimp cost-basis cohorts; those remain an explicit paid-data gap.</p>"
        ),
        "charts": [
            {
                "title": "BTC price vs network realized-price proxy [USD]",
                "logScale": True,
                "legend": "Weekly observations · Coin Metrics community data",
                "series": [
                    {"label": "BTC price [USD]", "useThemeText": True, "lineWidth": 2, "data": price_data},
                    {"label": "Realized price proxy [USD]", "color": "#f59e0b", "lineWidth": 2, "data": realized_data},
                ],
            },
            {
                "title": "NUPL proxy vs BTC price · weekly",
                "bars": {"label": "NUPL proxy", "data": nupl_data},
                "line": {"label": "BTC price [USD]", "data": price_data},
            },
        ],
    }


def active_address_brief(rows: list[dict]) -> dict:
    window = rows[-187:]
    smoothed = []
    for index, row in enumerate(window):
        if index < 6:
            continue
        mean = statistics.mean(item["active"] for item in window[index - 6:index + 1])
        smoothed.append([utc_ms(row["date"]), round(mean)])
    price = [[utc_ms(row["date"]), round(row["price"], 2)] for row in window[6:]]
    latest = smoothed[-1][1]
    prior = smoothed[-31][1]
    change = pct_change(latest, prior)
    return {
        "id": "atlas-active-addresses",
        "asset": "BTC · NETWORK USE",
        "headline": "Active addresses add adoption context, not a price target",
        "lede": f"Bitcoin's seven-day average active-address count is about {latest:,.0f}, {change:+.1f}% versus 30 observations earlier.",
        "bodyHtml": (
            "<p><strong>Method.</strong> Seven-day average of distinct active Bitcoin addresses from Coin Metrics. One user can control many addresses, and exchange batching can change the count.</p>"
            "<p><strong>Use.</strong> Look for persistent participation changes and price divergences; do not interpret a single-day spike as unique-user growth.</p>"
        ),
        "charts": [{
            "title": "BTC active addresses · 7-day average vs price",
            "bars": {"label": "Active addresses · 7d average", "unsigned": True, "data": smoothed},
            "line": {"label": "BTC price [USD]", "data": price},
        }],
    }


def leverage_brief(rows: list[dict]) -> dict:
    payload = get_json("https://www.okx.com/api/v5/rubik/stat/contracts/open-interest-volume?ccy=BTC&period=1D")
    oi_by_day = {}
    for item in payload.get("data", []):
        try:
            day = datetime.fromtimestamp(int(item[0]) / 1000, tz=timezone.utc).date()
            oi_by_day[day] = float(item[1])
        except (IndexError, TypeError, ValueError):
            continue
    price_by_day = {row["date"]: row["price"] for row in rows}
    common = sorted(set(oi_by_day).intersection(price_by_day))
    raw_rows = []
    for index, day in enumerate(common):
        if index < 7:
            continue
        earlier = common[index - 7]
        oi_change = pct_change(oi_by_day[day], oi_by_day[earlier])
        price_change = pct_change(price_by_day[day], price_by_day[earlier])
        raw_rows.append((day, oi_change - min(price_change, 0.0), price_by_day[day]))
    scored = []
    for index, (day, raw, price) in enumerate(raw_rows):
        history = [item[1] for item in raw_rows[max(0, index - 89):index + 1]]
        percentile = 100.0 * sum(value <= raw for value in history) / len(history)
        color = "#ef4444" if percentile >= 80 else "#22c55e" if percentile <= 20 else "#2e90fa"
        scored.append((day, percentile, price, color))
    scored = scored[-120:]
    latest = scored[-1]
    return {
        "id": "atlas-leverage-stress",
        "asset": "BTC · LEVERAGE STRESS",
        "headline": "A transparent leverage-stress percentile",
        "lede": f"The Paramaribo 90-observation leverage-stress percentile is {latest[1]:.0f}/100 through {latest[0].isoformat()}.",
        "bodyHtml": (
            "<p><strong>Method.</strong> The score ranks seven-day OKX BTC open-interest growth plus the magnitude of any simultaneous seven-day BTC price decline against the prior 90 observations.</p>"
            "<p><strong>Boundary.</strong> This is Paramaribo's reproducible proxy, not the proprietary Alphractal indicator. Red means unusually fast leverage rebuilding during weak price; green means relatively cleared positioning.</p>"
        ),
        "charts": [{
            "title": "Paramaribo leverage-stress percentile [90 observations] vs BTC price",
            "bars": {"label": "Leverage-stress percentile", "data": [[utc_ms(day), round(score, 1), color] for day, score, _, color in scored]},
            "line": {"label": "BTC price [USD]", "data": [[utc_ms(day), round(price, 2)] for day, _, price, _ in scored]},
        }],
    }


def options_brief() -> dict:
    payload = get_json("https://www.deribit.com/api/v2/public/get_book_summary_by_currency?currency=BTC&kind=option")
    grouped = defaultdict(lambda: {"call": 0.0, "put": 0.0})
    underlyings = []
    snapshot_ms = 0
    for item in payload.get("result", []):
        try:
            name = item["instrument_name"].split("-")
            expiry = datetime.strptime(name[1], "%d%b%y").replace(tzinfo=timezone.utc).date()
            kind = "call" if name[-1] == "C" else "put"
            grouped[expiry][kind] += float(item.get("open_interest") or 0.0)
            if item.get("underlying_price"):
                underlyings.append(float(item["underlying_price"]))
            snapshot_ms = max(snapshot_ms, int(item.get("creation_timestamp") or 0))
        except (KeyError, IndexError, TypeError, ValueError):
            continue
    today = datetime.now(timezone.utc).date()
    expiries = [day for day in sorted(grouped) if today <= day <= today + timedelta(days=365) and sum(grouped[day].values()) > 0][:18]
    call_total = sum(grouped[day]["call"] for day in expiries)
    put_total = sum(grouped[day]["put"] for day in expiries)
    ratio = put_total / call_total if call_total else 0.0
    spot = statistics.median(underlyings) if underlyings else 0.0
    snapshot = datetime.fromtimestamp(snapshot_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC") if snapshot_ms else "current"
    return {
        "id": "atlas-options-positioning",
        "asset": "BTC · OPTIONS",
        "headline": "Options open interest by expiry, not a one-number signal",
        "lede": f"Across the next {len(expiries)} listed expiries, Deribit put/call open interest is {ratio:.2f}; reference BTC underlying is about {compact_money(spot)}.",
        "bodyHtml": (
            f"<p><strong>Snapshot.</strong> Public Deribit book summaries at {snapshot}. Open interest is aggregated in BTC by listed expiry for calls and puts.</p>"
            "<p><strong>Use.</strong> Concentrated expiry interest identifies dates where hedging and dealer positioning may matter. It does not reveal direction by itself and is not a historical options-OI series.</p>"
        ),
        "charts": [{
            "title": "Deribit BTC options open interest by expiry [BTC]",
            "legend": "Snapshot by expiry · calls and puts",
            "series": [
                {"label": "Call OI [BTC]", "color": "#22c55e", "lineWidth": 2, "data": [[utc_ms(day), round(grouped[day]["call"], 1)] for day in expiries]},
                {"label": "Put OI [BTC]", "color": "#ef4444", "lineWidth": 2, "data": [[utc_ms(day), round(grouped[day]["put"], 1)] for day in expiries]},
            ],
        }],
    }


def build() -> dict:
    rows = coinmetrics_rows()
    briefs = [
        rainbow_brief(rows),
        cycle_brief(rows),
        onchain_brief(rows),
        active_address_brief(rows),
        leverage_brief(rows),
        options_brief(),
    ]
    now = datetime.now(timezone.utc)
    return {
        "schemaVersion": 1,
        "date": now.date().isoformat(),
        "asOf": now.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "dek": "Free-data long-horizon context: dynamic rainbow bands, halving-cycle comparison, on-chain valuation and activity, leverage stress, and options positioning.",
        "sourceNote": "Coin Metrics Community API, OKX public market data, and Deribit public book summaries. Derived formulas are disclosed in each panel. No paid Glassnode cohort data is reproduced.",
        "briefs": briefs,
    }


def main() -> None:
    atlas = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(atlas, separators=(",", ":")) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)} with {len(atlas['briefs'])} briefs")


if __name__ == "__main__":
    main()
