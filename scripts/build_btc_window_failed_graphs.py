#!/usr/bin/env python3
"""Build the publication charts for Paramaribo Letter Issue 35.

Reads the frozen Coinbase, Yahoo, and Farside tables in research/. Does not fetch.
"""

from __future__ import annotations

import csv
import html
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAILY = ROOT / "research" / "btc-window-failed-2026-11-20.csv"
HOURLY = ROOT / "research" / "btc-nov19-20-2026-hourly.csv"
CROSS = ROOT / "research" / "cross-asset-nov12-to-nov19-2026.csv"
FLOWS = ROOT / "research" / "farside-btc-nov20-2026.csv"
OUT = ROOT / "public" / "images"
PACK = ROOT / "public" / "charts" / "packs" / "2026-11-20-the-window-failed.json"
CATALOG = ROOT / "public" / "charts" / "catalog.json"
RETRIEVED = "20 Nov 2026 · 8:05 a.m. CT / 14:05 UTC"

BG = "#0e1721"
PANEL = "#122131"
GRID = "#2a3b4d"
TEXT = "#e6edf3"
MUTE = "#9eb0c1"
ACCENT = "#f1b56f"
CYAN = "#7ac7d4"
GREEN = "#79d3a3"
RED = "#ef8d8d"
YELLOW = "#e8d36c"


def read_csv(path: Path) -> list[dict[str, float | str | None]]:
    rows: list[dict[str, float | str | None]] = []
    with path.open(newline="") as fh:
        for raw in csv.DictReader(fh):
            row: dict[str, float | str | None] = {}
            for key, value in raw.items():
                if key in {"time", "date", "name"}:
                    row[key] = value
                    continue
                row[key] = None if value == "" else float(value)
            rows.append(row)
    return rows


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def start(width: int, height: int, title: str, desc: str, subtitle: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{esc(title)}</title>',
        f'<desc id="desc">{esc(desc)}</desc>',
        f'<rect width="{width}" height="{height}" fill="{BG}"/>',
        '<style>text{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.title{font-size:28px;font-weight:700;fill:%s}.sub{font-size:15px;fill:%s}.axis{font-size:13px;fill:%s}.note{font-size:12px;fill:%s}.label{font-size:13px;font-weight:600;fill:%s}</style>'
        % (TEXT, MUTE, MUTE, MUTE, TEXT),
        f'<text x="56" y="48" class="title">{esc(title)}</text>',
        f'<text x="56" y="76" class="sub">{esc(subtitle)}</text>',
    ]


def panel(lines: list[str], x: float, y: float, width: float, height: float) -> None:
    lines.append(
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" rx="8" fill="{PANEL}" stroke="{GRID}"/>'
    )


def y_pos(value: float, y_min: float, y_max: float, top: float, height: float) -> float:
    return top + (y_max - value) / (y_max - y_min) * height


def x_pos(index: int, count: int, left: float, width: float) -> float:
    return left + (index / (count - 1)) * width if count > 1 else left


def grid(lines, left, top, width, height, ticks, y_min, y_max, fmt) -> None:
    for tick in ticks:
        yy = y_pos(tick, y_min, y_max, top, height)
        lines.append(f'<line x1="{left:.1f}" y1="{yy:.1f}" x2="{left + width:.1f}" y2="{yy:.1f}" stroke="{GRID}"/>')
        lines.append(f'<text x="{left - 12:.1f}" y="{yy + 4:.1f}" class="axis" text-anchor="end">{esc(fmt(tick))}</text>')


def chart_path(rows: list[dict]) -> str:
    width, height = 1200, 740
    left, top, plot_w, plot_h = 94, 108, 980, 510
    y_min, y_max = 58_000, 76_000
    lines = start(
        width,
        height,
        "The $72k window failed. The July close did not.",
        "Daily Coinbase BTC-USD candles from 12 November through 19 November 2026. 13 and 14 November close under $72,000. 19 November closes at $61,913, still above the 2 July close.",
        "Coinbase daily UTC candles · 12–19 Nov 2026 · 20 Nov is partial and is not plotted",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [60_000, 64_000, 68_000, 72_000], y_min, y_max, lambda v: f"${v / 1000:.0f}k")
    for level, label, color in [
        (72_000, "$72k", YELLOW),
        (61_946, "15 Nov low", ACCENT),
        (61_484, "2 Jul close", CYAN),
    ]:
        yy = y_pos(level, y_min, y_max, top, plot_h)
        lines.append(
            f'<line x1="{left:.1f}" y1="{yy:.1f}" x2="{left + plot_w:.1f}" y2="{yy:.1f}" stroke="{color}" stroke-width="1.4" stroke-dasharray="7 5"/>'
        )
        lines.append(f'<text x="{left + plot_w + 8:.1f}" y="{yy + 4:.1f}" class="label" fill="{color}">{label}</text>')
    candle_w = 36
    for i, row in enumerate(rows):
        xx = x_pos(i, len(rows), left + 40, plot_w - 80)
        op, hi, lo, cl = float(row["btc_open"]), float(row["btc_high"]), float(row["btc_low"]), float(row["btc_close"])
        color = GREEN if cl >= op else RED
        yl, yh = y_pos(lo, y_min, y_max, top, plot_h), y_pos(hi, y_min, y_max, top, plot_h)
        yo, yc = y_pos(op, y_min, y_max, top, plot_h), y_pos(cl, y_min, y_max, top, plot_h)
        lines.append(f'<line x1="{xx:.1f}" y1="{yh:.1f}" x2="{xx:.1f}" y2="{yl:.1f}" stroke="{color}" stroke-width="1.6"/>')
        lines.append(
            f'<rect x="{xx - candle_w / 2:.1f}" y="{min(yo, yc):.1f}" width="{candle_w}" height="{max(abs(yc - yo), 2.5):.1f}" fill="{color}" opacity="0.92" stroke="{color}"/>'
        )
        day = str(row["date"])[5:]
        lines.append(f'<text x="{xx:.1f}" y="{top + plot_h + 28:.1f}" class="axis" text-anchor="middle">{esc(day)}</text>')
        if day in {"11-13", "11-14", "11-19"}:
            lines.append(
                f'<text x="{xx:.1f}" y="{yc - 12:.1f}" class="label" text-anchor="middle">{cl / 1000:.1f}k</text>'
            )
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">13 Nov close $68,237. 14 Nov close $64,119. Neither day traded $72,000. 19 Nov close $61,913, $429 above the 2 July close of $61,484.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Source: Coinbase Exchange · retrieved {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def chart_hourly(rows: list[dict]) -> str:
    width, height = 1200, 740
    left, top, plot_w, plot_h = 94, 108, 980, 510
    y_min, y_max = 60_000, 65_000
    lines = start(
        width,
        height,
        "$60k has not traded. The day has not closed.",
        "Hourly Coinbase BTC-USD candles from 19 November 00:00 UTC through the 20 November 13:00 UTC hour. The low is $61,161. Price does not trade $60,000.",
        "Coinbase hourly UTC candles · 19 Nov 00:00 through 20 Nov 13:00 · the 14:00 UTC hour is not plotted",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [60_000, 61_000, 62_000, 63_000, 64_000], y_min, y_max, lambda v: f"${v / 1000:.0f}k")
    yy = y_pos(61_946, y_min, y_max, top, plot_h)
    lines.append(
        f'<line x1="{left:.1f}" y1="{yy:.1f}" x2="{left + plot_w:.1f}" y2="{yy:.1f}" stroke="{ACCENT}" stroke-width="1.4" stroke-dasharray="7 5"/>'
    )
    lines.append(f'<text x="{left + plot_w + 8:.1f}" y="{yy + 4:.1f}" class="label" fill="{ACCENT}">15 Nov low</text>')
    for i, row in enumerate(rows):
        xx = x_pos(i, len(rows), left + 16, plot_w - 24)
        op, hi, lo, cl = float(row["open"]), float(row["high"]), float(row["low"]), float(row["close"])
        color = GREEN if cl >= op else RED
        yl, yh = y_pos(lo, y_min, y_max, top, plot_h), y_pos(hi, y_min, y_max, top, plot_h)
        yo, yc = y_pos(op, y_min, y_max, top, plot_h), y_pos(cl, y_min, y_max, top, plot_h)
        lines.append(f'<line x1="{xx:.1f}" y1="{yh:.1f}" x2="{xx:.1f}" y2="{yl:.1f}" stroke="{color}" stroke-width="1.4"/>')
        lines.append(
            f'<rect x="{xx - 8:.1f}" y="{min(yo, yc):.1f}" width="16" height="{max(abs(yc - yo), 2):.1f}" fill="{color}"/>'
        )
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">19 Nov close $61,913. 20 Nov 12:00 UTC low $61,161. The unfinished day has not traded $60,000 and has not closed.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Source: Coinbase Exchange · retrieved {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def chart_cross(rows: list[dict]) -> str:
    width, height = 1200, 740
    left, top, plot_w, plot_h = 94, 108, 1040, 500
    y_min, y_max = -16, 2
    lines = start(
        width,
        height,
        "Bitcoin fell further than the indexes. Credit barely moved.",
        "Percent change from the 12 November close to the 19 November close. Bitcoin, equities, gold, HYG, and January Brent.",
        "Coinbase and Yahoo Finance · completed closes · 12 Nov to 19 Nov 2026",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [-15, -10, -5, 0], y_min, y_max, lambda v: f"{v:.0f}%")
    zero = y_pos(0, y_min, y_max, top, plot_h)
    lines.append(f'<line x1="{left:.1f}" y1="{zero:.1f}" x2="{left + plot_w:.1f}" y2="{zero:.1f}" stroke="{TEXT}" stroke-width="1.2"/>')
    bar_w = 64
    for i, row in enumerate(rows):
        pct = float(row["change_pct"])
        xx = x_pos(i, len(rows), left + 50, plot_w - 80)
        yy = y_pos(pct, y_min, y_max, top, plot_h)
        color = GREEN if pct >= 0 else RED
        lines.append(
            f'<rect x="{xx - bar_w / 2:.1f}" y="{min(zero, yy):.1f}" width="{bar_w:.1f}" height="{max(abs(zero - yy), 2):.1f}" fill="{color}" opacity="0.9" rx="4"/>'
        )
        lines.append(
            f'<text x="{xx:.1f}" y="{yy - 10 if pct >= 0 else yy + 18:.1f}" class="label" text-anchor="middle" fill="{color}">{pct:+.1f}</text>'
        )
        lines.append(
            f'<text x="{xx:.1f}" y="{top + plot_h + 28:.1f}" class="axis" text-anchor="middle">{esc(row["name"])}</text>'
        )
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">Bitcoin −13.3%. Nasdaq −5.9%. HYG −0.6%. The VIX cash close went from 18.70 to 28.44 and is not plotted as a return.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Source: Coinbase and Yahoo Finance · retrieved {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def chart_flows(rows: list[dict]) -> str:
    width, height = 1200, 740
    left, top, plot_w, plot_h = 100, 108, 1020, 500
    y_min, y_max = -700, 150
    lines = start(
        width,
        height,
        "19 November is an outflow. It is not a zero.",
        "US spot Bitcoin ETF net flows, 2 November through 19 November 2026. 20 November is dashes on the table and is not plotted.",
        "Farside Investors · US$ millions · completed sessions only",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [-600, -400, -200, 0], y_min, y_max, lambda v: f"{v:.0f}")
    zero = y_pos(0, y_min, y_max, top, plot_h)
    lines.append(f'<line x1="{left:.1f}" y1="{zero:.1f}" x2="{left + plot_w:.1f}" y2="{zero:.1f}" stroke="{TEXT}" stroke-width="1.2"/>')
    bar_w = 36
    for i, row in enumerate(rows):
        pct = float(row["total_usd_m"])
        xx = x_pos(i, len(rows), left + 28, plot_w - 40)
        yy = y_pos(pct, y_min, y_max, top, plot_h)
        color = GREEN if pct >= 0 else RED
        lines.append(
            f'<rect x="{xx - bar_w / 2:.1f}" y="{min(zero, yy):.1f}" width="{bar_w:.1f}" height="{max(abs(zero - yy), 2):.1f}" fill="{color}" opacity="0.9" rx="3"/>'
        )
        if str(row["date"]).endswith(("11-04", "11-16", "11-19")):
            lines.append(
                f'<text x="{xx:.1f}" y="{yy + (16 if pct < 0 else -8):.1f}" class="label" text-anchor="middle" fill="{color}">{pct:+.0f}</text>'
            )
        lines.append(
            f'<text x="{xx:.1f}" y="{top + plot_h + 28:.1f}" class="axis" text-anchor="middle">{esc(str(row["date"])[5:])}</text>'
        )
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">Completed November total −$3,467.8M. 19 Nov −$582.3M, of which IBIT was −$541.1M. 20 Nov is dashes and is not plotted.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Source: Farside Investors · retrieved {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def ms(iso: str) -> int:
    return int(datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp() * 1000)


def write_pack(daily: list[dict], hourly: list[dict], cross: list[dict], flows: list[dict]) -> None:
    def series(rows, time_key, value_key):
        out = []
        for row in rows:
            value = row[value_key]
            out.append([ms(str(row[time_key])), None if value is None else round(float(value), 2)])
        return out

    pack = {
        "id": "2026-11-20-the-window-failed",
        "date": "2026-11-20",
        "kicker": "Chart Desk · Issue 35",
        "title": "The window failed. Credit did not.",
        "dek": "13 and 14 November both closed under $72,000. 19 November closed at $61,913. The VIX cash close was 28.44. High-yield OAS did not go through 3.48%.",
        "asOf": "2026-11-20T14:05:46Z",
        "cadence": "follow-up",
        "thesis": "The window failed. Credit did not.",
        "stakes": "BTC ~$61.8k. 13 and 14 Nov closed under $72k. 19 Nov close $61,913. The 48-hour test of the 15 Nov low is open. VIX cash close 28.44. HY OAS 3.47% on 18 Nov. WAIT.",
        "levels": ["$72k", "$61.9k", "$61.5k", "~$57.7k"],
        "letterId": "2026-11-20-the-window-failed",
        "letterUrl": "/issue?id=2026-11-20-the-window-failed",
        "letterLabel": "Vol. 1 · Issue 35",
        "subscribeHook": "A UTC close back above the 15 November low on 20 or 21 November, or a second close under it, updates the sequence. Charts stay free here; the call moves by email.",
        "sourceNote": "Issue 35 charts use Coinbase Exchange UTC candles (daily 12–19 Nov 2026; hourly 19 Nov 00:00 through 20 Nov 13:00 UTC), completed 12 and 19 November closes from Yahoo Finance, and Farside Investors US-session ETF flows for 2–19 November. 20 November is a partial UTC day and an incomplete Farside row. Weekend blanks are not zeroes. Educational scenario research; no leverage.",
        "briefs": [
            {
                "id": "btc-failed-path",
                "asset": "BTC",
                "headline": "The $72k window failed. The July close did not.",
                "lede": "13 and 14 November both closed under $72,000. 19 November closed at $61,913.",
                "bodyHtml": "<p><strong>Fact.</strong> The 48-hour test Issue 34 wrote down failed. Neither day traded $72,000.</p><p><strong>Read.</strong> The close is the lowest since 2 July. It is still $429 above that July close.</p>",
                "charts": [
                    {
                        "title": "BTC daily range [USD] vs close",
                        "bars": {
                            "label": "Daily high–low range [USD]",
                            "unsigned": True,
                            "data": [
                                [
                                    ms(str(row["date"]) + "T00:00:00+00:00"),
                                    round(float(row["btc_high"]) - float(row["btc_low"]), 2),
                                ]
                                for row in daily
                            ],
                        },
                        "line": {
                            "label": "BTC-USD close [USD]",
                            "data": series(
                                [{**row, "time": str(row["date"]) + "T00:00:00+00:00"} for row in daily],
                                "time",
                                "btc_close",
                            ),
                        },
                    }
                ],
            },
            {
                "id": "btc-failed-hours",
                "asset": "BTC · 19–20 NOV 2026",
                "headline": "One close under the 15 November low. $60,000 has not traded.",
                "lede": "19 November closed at $61,913. The 20 November 12:00 UTC hour low was $61,161.",
                "bodyHtml": "<p><strong>Fact.</strong> The low is on an unfinished UTC day.</p><p><strong>Read.</strong> A wick is not acceptance. The 48-hour test of the local shelf runs through the 21 November close.</p>",
                "charts": [
                    {
                        "title": "BTC hourly range [USD] vs close · 19–20 Nov 2026",
                        "bars": {
                            "label": "Hourly high–low range [USD]",
                            "unsigned": True,
                            "data": [
                                [ms(str(row["time"])), round(float(row["high"]) - float(row["low"]), 2)]
                                for row in hourly
                            ],
                        },
                        "line": {
                            "label": "BTC-USD hourly close [USD]",
                            "data": series(hourly, "time", "close"),
                        },
                    }
                ],
            },
            {
                "id": "btc-failed-cross",
                "asset": "CROSS-ASSET · 12–19 NOV",
                "headline": "Bitcoin fell further than the indexes. Credit barely moved.",
                "lede": "From the 12 November close to the 19 November close, Bitcoin fell 13.3% and the Nasdaq fell 5.9%. HYG fell 0.6%.",
                "bodyHtml": "<p><strong>Fact.</strong> Equities, gold, and January Brent closed lower. HYG was nearly unchanged on the week.</p><p><strong>Read.</strong> Volatility traveled. The high-yield spread did not go through the 5 November print.</p>",
                "charts": [
                    {
                        "title": "12 Nov close to 19 Nov close [%]",
                        "bars": {
                            "label": "Change from the 12 Nov close to the 19 Nov close [%]",
                            "data": [
                                [ms("2026-11-19T00:00:00+00:00") + i, round(float(row["change_pct"]), 2)]
                                for i, row in enumerate(cross)
                            ],
                        },
                    }
                ],
            },
            {
                "id": "btc-failed-flows",
                "asset": "US SPOT BTC ETF",
                "headline": "Nineteen November is the IBIT minimum on the table.",
                "lede": "Farside’s completed November total is −$3,467.8 million. 19 November is −$582.3 million, of which IBIT is −$541.1 million.",
                "bodyHtml": "<p><strong>Fact.</strong> The Minimum row for IBIT on the retrieved table is (541.1). The Total column’s minimum is a larger outflow on another day.</p><p><strong>Read.</strong> 20 November is dashes. That is not a zero.</p>",
                "charts": [
                    {
                        "title": "US spot Bitcoin ETF net flow [US$ millions]",
                        "bars": {
                            "label": "Net flow [US$ millions]",
                            "data": [
                                [ms(str(row["date"]) + "T00:00:00+00:00"), round(float(row["total_usd_m"]), 1)]
                                for row in flows
                            ],
                        },
                    }
                ],
            },
        ],
    }
    PACK.parent.mkdir(parents=True, exist_ok=True)
    PACK.write_text(json.dumps(pack, indent=2) + "\n")
    catalog = json.loads(CATALOG.read_text())
    catalog = [row for row in catalog if row.get("id") != pack["id"]]
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
            "letterId",
            "letterUrl",
            "letterLabel",
            "subscribeHook",
            "sourceNote",
        )
    }
    public["packUrl"] = "/charts/packs/2026-11-20-the-window-failed.json"
    catalog.insert(0, public)
    CATALOG.write_text(json.dumps(catalog, indent=2) + "\n")
    print(f"wrote {PACK.relative_to(ROOT)}")


def main() -> None:
    daily = read_csv(DAILY)
    hourly = read_csv(HOURLY)
    cross = read_csv(CROSS)
    flows = read_csv(FLOWS)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "chart-btc-failed-path.svg").write_text(chart_path(daily))
    (OUT / "chart-btc-failed-hours.svg").write_text(chart_hourly(hourly))
    (OUT / "chart-btc-failed-cross.svg").write_text(chart_cross(cross))
    (OUT / "chart-btc-failed-flows.svg").write_text(chart_flows(flows))
    write_pack(daily, hourly, cross, flows)
    print("wrote four svgs")


if __name__ == "__main__":
    main()
