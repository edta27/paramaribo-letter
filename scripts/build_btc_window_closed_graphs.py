#!/usr/bin/env python3
"""Build the publication charts for Paramaribo Letter Issue 34.

Reads the frozen Coinbase, Yahoo, and Farside tables in research/. Does not fetch.
"""

from __future__ import annotations

import csv
import html
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAILY = ROOT / "research" / "btc-window-closed-2026-11-13.csv"
HOURLY = ROOT / "research" / "btc-nov12-13-2026-hourly.csv"
CROSS = ROOT / "research" / "cross-asset-nov5-to-nov12-2026.csv"
FLOWS = ROOT / "research" / "farside-btc-nov-2026.csv"
OUT = ROOT / "public" / "images"
PACK = ROOT / "public" / "charts" / "packs" / "2026-11-13-the-window-closed.json"
CATALOG = ROOT / "public" / "charts" / "catalog.json"
RETRIEVED = "13 Nov 2026 · 8:08 a.m. CT / 14:08 UTC"

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
    left, top, plot_w, plot_h = 94, 108, 1015, 510
    y_min, y_max = 70_000, 82_000
    lines = start(
        width,
        height,
        "The $77k window closed. $72k has one close through it.",
        "Daily Coinbase BTC-USD candles from 29 October through 12 November 2026. 6 and 7 November close under $77,000. 10 November is the first close under $74,000. 12 November closes at $71,370.",
        "Coinbase daily UTC candles · 29 Oct–12 Nov 2026 · 13 Nov is partial and is not plotted",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [72_000, 74_000, 77_000, 80_000], y_min, y_max, lambda v: f"${v / 1000:.0f}k")
    for level, label, color in [(80_000, "$80k", CYAN), (77_000, "$77k", YELLOW), (74_000, "$74k", ACCENT), (72_000, "$72k", RED)]:
        yy = y_pos(level, y_min, y_max, top, plot_h)
        lines.append(
            f'<line x1="{left:.1f}" y1="{yy:.1f}" x2="{left + plot_w:.1f}" y2="{yy:.1f}" stroke="{color}" stroke-width="1.4" stroke-dasharray="7 5"/>'
        )
        lines.append(f'<text x="{left + plot_w + 8:.1f}" y="{yy + 4:.1f}" class="label" fill="{color}">{label}</text>')
    candle_w = 28
    for i, row in enumerate(rows):
        xx = x_pos(i, len(rows), left, plot_w)
        op, hi, lo, cl = float(row["btc_open"]), float(row["btc_high"]), float(row["btc_low"]), float(row["btc_close"])
        color = GREEN if cl >= op else RED
        yl, yh = y_pos(lo, y_min, y_max, top, plot_h), y_pos(hi, y_min, y_max, top, plot_h)
        yo, yc = y_pos(op, y_min, y_max, top, plot_h), y_pos(cl, y_min, y_max, top, plot_h)
        lines.append(f'<line x1="{xx:.1f}" y1="{yh:.1f}" x2="{xx:.1f}" y2="{yl:.1f}" stroke="{color}" stroke-width="1.6"/>')
        lines.append(
            f'<rect x="{xx - candle_w / 2:.1f}" y="{min(yo, yc):.1f}" width="{candle_w}" height="{max(abs(yc - yo), 2.5):.1f}" fill="{color}" opacity="0.92" stroke="{color}"/>'
        )
        day = str(row["date"])[5:]
        if day in {"10-29", "11-04", "11-06", "11-07", "11-10", "11-12"}:
            lines.append(f'<text x="{xx:.1f}" y="{top + plot_h + 24:.1f}" class="axis" text-anchor="middle">{day}</text>')
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">6 Nov close $75,731. 7 Nov close $75,754. Neither day traded $77,000. 10 Nov close $73,698. 12 Nov close $71,370, low $71,008.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Source: Coinbase Exchange BTC-USD · retrieved {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def chart_hourly(rows: list[dict]) -> str:
    width, height = 1200, 720
    left, top, plot_w, plot_h = 94, 108, 1015, 490
    y_min, y_max = 66_500, 75_000
    lines = start(
        width,
        height,
        "One close under $72k. The next day has not traded it back.",
        "Hourly Coinbase BTC-USD candles from 12 November 00:00 UTC through the completed 13 November 13:00 UTC hour. The 05:00 UTC hour low is $67,555. $72,000 is not traded on 13 November.",
        "Coinbase hourly UTC candles · 12 Nov 00:00 through 13 Nov 13:00 · the 14:00 hour is unfinished and is not plotted",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [67_555, 72_000, 74_000], y_min, y_max, lambda v: f"${v / 1000:.1f}k")
    for level, label, color in [(74_000, "$74k", ACCENT), (72_000, "$72k", RED)]:
        yy = y_pos(level, y_min, y_max, top, plot_h)
        lines.append(
            f'<line x1="{left:.1f}" y1="{yy:.1f}" x2="{left + plot_w:.1f}" y2="{yy:.1f}" stroke="{color}" stroke-width="1.4" stroke-dasharray="6 5"/>'
        )
        lines.append(f'<text x="{left + plot_w + 8:.1f}" y="{yy + 4:.1f}" class="label" fill="{color}">{label}</text>')
    candle_w = 12
    for i, row in enumerate(rows):
        xx = x_pos(i, len(rows), left, plot_w)
        op, hi, lo, cl = float(row["open"]), float(row["high"]), float(row["low"]), float(row["close"])
        color = GREEN if cl >= op else RED
        yl, yh = y_pos(lo, y_min, y_max, top, plot_h), y_pos(hi, y_min, y_max, top, plot_h)
        yo, yc = y_pos(op, y_min, y_max, top, plot_h), y_pos(cl, y_min, y_max, top, plot_h)
        lines.append(f'<line x1="{xx:.1f}" y1="{yh:.1f}" x2="{xx:.1f}" y2="{yl:.1f}" stroke="{color}" stroke-width="1.5"/>')
        lines.append(
            f'<rect x="{xx - candle_w / 2:.1f}" y="{min(yo, yc):.1f}" width="{candle_w}" height="{max(abs(yc - yo), 2.2):.1f}" fill="{color}" opacity="0.92" stroke="{color}"/>'
        )
        stamp = str(row["time"])
        if stamp.endswith("T00:00:00Z") or stamp.endswith("T12:00:00Z"):
            label = stamp[5:10] + " " + stamp[11:13] + "h"
            lines.append(f'<text x="{xx:.1f}" y="{top + plot_h + 24:.1f}" class="axis" text-anchor="middle">{label}</text>')
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">12 Nov close $71,370. 13 Nov 05:00 UTC low $67,555, which is 11:00 p.m. Central on 12 Nov. 13 Nov high through 13:00 UTC is $71,429. $72,000 was not traded.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Source: Coinbase Exchange BTC-USD · retrieved {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def chart_cross(rows: list[dict]) -> str:
    width, height = 1200, 720
    left, top, plot_w, plot_h = 168, 118, 900, 470
    y_min, y_max = -10.0, 20.0
    lines = start(
        width,
        height,
        "Since 5 November, equities repaired. Bitcoin did not.",
        "Percent change from the 5 November close to the 12 November close. Bitcoin is Coinbase. The others are Yahoo cash or futures closes. VIX is not plotted as a return.",
        "Completed 12 Nov 2026 closes versus 5 Nov · VIX cash close 28.18 to 18.70, not shown as a percent",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [-6, 0, 6, 12, 18], y_min, y_max, lambda v: f"{v:.0f}%")
    zero = y_pos(0, y_min, y_max, top, plot_h)
    lines.append(f'<line x1="{left:.1f}" y1="{zero:.1f}" x2="{left + plot_w:.1f}" y2="{zero:.1f}" stroke="{MUTE}"/>')
    short = {
        "Bitcoin": "Bitcoin",
        "S&P 500": "S&P",
        "Nasdaq": "Nasdaq",
        "Dow": "Dow",
        "Equal-weight": "RSP",
        "SOXX": "SOXX",
        "HYG": "HYG",
        "January Brent": "Brent",
        "Gold": "Gold",
    }
    n = len(rows)
    gap = plot_w / n
    bar_w = gap * 0.62
    for i, row in enumerate(rows):
        xx = left + gap * i + gap / 2
        pct = float(row["change_pct"])
        yy = y_pos(pct, y_min, y_max, top, plot_h)
        color = GREEN if pct >= 0 else RED
        lines.append(
            f'<rect x="{xx - bar_w / 2:.1f}" y="{min(zero, yy):.1f}" width="{bar_w:.1f}" height="{max(abs(zero - yy), 2):.1f}" fill="{color}" opacity="0.9" rx="4"/>'
        )
        lines.append(
            f'<text x="{xx:.1f}" y="{yy - 10 if pct >= 0 else yy + 18:.1f}" class="label" text-anchor="middle" fill="{color}">{pct:+.1f}%</text>'
        )
        lines.append(
            f'<text x="{xx:.1f}" y="{top + plot_h + 28:.1f}" class="axis" text-anchor="middle">{esc(short.get(str(row["name"]), row["name"]))}</text>'
        )
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">SOXX is Yahoo’s split-adjusted series, the same one Issue 33 used. January Brent is BZF27. Gold and Brent are futures settles, not the unfinished 13 Nov session.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Sources: Coinbase Exchange and Yahoo Finance · {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def chart_flows(rows: list[dict]) -> str:
    width, height = 1200, 720
    left, top, plot_w, plot_h = 110, 118, 980, 470
    y_min, y_max = -500.0, 160.0
    lines = start(
        width,
        height,
        "Six completed sessions of ETF outflows.",
        "US spot Bitcoin ETF net flow, US$ millions, from Farside. 4 November is the only completed November inflow. 13 November is an unfinished row of dashes and is not plotted.",
        "Farside Investors · completed US sessions 2–12 Nov 2026 · weekend blanks are not zeroes",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [-400, -200, 0, 100], y_min, y_max, lambda v: f"{v:.0f}")
    zero = y_pos(0, y_min, y_max, top, plot_h)
    lines.append(f'<line x1="{left:.1f}" y1="{zero:.1f}" x2="{left + plot_w:.1f}" y2="{zero:.1f}" stroke="{MUTE}"/>')
    n = len(rows)
    gap = plot_w / n
    bar_w = gap * 0.62
    for i, row in enumerate(rows):
        xx = left + gap * i + gap / 2
        pct = float(row["total_usd_m"])
        yy = y_pos(pct, y_min, y_max, top, plot_h)
        color = GREEN if pct >= 0 else RED
        lines.append(
            f'<rect x="{xx - bar_w / 2:.1f}" y="{min(zero, yy):.1f}" width="{bar_w:.1f}" height="{max(abs(zero - yy), 2):.1f}" fill="{color}" opacity="0.9" rx="4"/>'
        )
        lines.append(
            f'<text x="{xx:.1f}" y="{yy - 10 if pct >= 0 else yy + 18:.1f}" class="label" text-anchor="middle" fill="{color}">{pct:+.0f}</text>'
        )
        lines.append(
            f'<text x="{xx:.1f}" y="{top + plot_h + 28:.1f}" class="axis" text-anchor="middle">{esc(str(row["date"])[5:])}</text>'
        )
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">Completed November total −$2,161.6M. 5–12 Nov −$1,722.0M across six sessions. IBIT was −$201.2M on the only inflow day, 4 Nov, when the total was +$74.6M.</text>'
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
        "id": "2026-11-13-the-window-closed",
        "date": "2026-11-13",
        "kicker": "Chart Desk · Issue 34",
        "title": "The window closed. Panic did not.",
        "dek": "6 and 7 November both closed under $77,000. 12 November closed at $71,370. Equities and the VIX repaired. Credit tightened.",
        "asOf": "2026-11-13T14:08:59Z",
        "cadence": "follow-up",
        "thesis": "The window closed. Panic did not.",
        "stakes": "BTC ~$69.2k. 6 and 7 Nov closed under $77k. 12 Nov close $71,370. The 48-hour test of $72k is open. VIX cash close 18.70. WAIT.",
        "levels": ["$86k", "$80k", "$77k", "$74k", "$72k", "~$57.7k"],
        "letterId": "2026-11-13-the-window-closed",
        "letterUrl": "/issue?id=2026-11-13-the-window-closed",
        "letterLabel": "Vol. 1 · Issue 34",
        "subscribeHook": "A UTC close back above $72k on 13 or 14 November, or a second close under it, updates the sequence. Charts stay free here; the call moves by email.",
        "sourceNote": "Issue 34 charts use Coinbase Exchange UTC candles (daily 29 Oct–12 Nov 2026; hourly 12 Nov 00:00 through 13 Nov 13:00 UTC), completed 5 and 12 November closes from Yahoo Finance, and Farside Investors US-session ETF flows for 2–12 November. 13 November is a partial UTC day and an incomplete Farside row. Weekend blanks are not zeroes. Educational scenario research; no leverage.",
        "briefs": [
            {
                "id": "btc-window-path",
                "asset": "BTC",
                "headline": "The $77k window closed. $72k has one close through it.",
                "lede": "6 and 7 November both closed under $77,000. 12 November closed at $71,370.",
                "bodyHtml": "<p><strong>Fact.</strong> The 48-hour test Issue 33 wrote down failed. A later close under $74,000 was not reclaimed inside 48 hours either.</p><p><strong>Read.</strong> $72,000 has one completed close through it. That window was still open at the freeze.</p>",
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
                "id": "btc-window-hours",
                "asset": "BTC · 12–13 NOV 2026",
                "headline": "One close under $72k. The next day has not traded it back.",
                "lede": "12 November closed at $71,370. The 13 November 05:00 UTC hour low was $67,555. $72,000 was not traded.",
                "bodyHtml": "<p><strong>Fact.</strong> The low is on an unfinished UTC day.</p><p><strong>Read.</strong> A wick is not acceptance. The 48-hour test runs through the 14 November close.</p>",
                "charts": [
                    {
                        "title": "BTC hourly range [USD] vs close · 12–13 Nov 2026",
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
                "id": "btc-window-cross",
                "asset": "CROSS-ASSET · 5–12 NOV",
                "headline": "Equities repaired. Bitcoin did not.",
                "lede": "From the 5 November close to the 12 November close, the S&P 500 rose 3.2% and Bitcoin fell 6.1%. The VIX cash close went from 28.18 to 18.70.",
                "bodyHtml": "<p><strong>Fact.</strong> The equity indexes and equal-weight stocks closed higher. January Brent and gold closed lower. HYG was nearly unchanged.</p><p><strong>Read.</strong> That is not the panic cluster. Credit spreads tightened over the same week.</p>",
                "charts": [
                    {
                        "title": "5 Nov close to 12 Nov close [%]",
                        "bars": {
                            "label": "Change from the 5 Nov close to the 12 Nov close [%]",
                            "data": [
                                [ms("2026-11-12T00:00:00+00:00") + i, round(float(row["change_pct"]), 2)]
                                for i, row in enumerate(cross)
                            ],
                        },
                    }
                ],
            },
            {
                "id": "btc-window-flows",
                "asset": "US SPOT BTC ETF",
                "headline": "Six completed sessions of outflows.",
                "lede": "Farside’s completed November total is −$2,161.6 million. 5 through 12 November are six outflow sessions, −$1,722.0 million.",
                "bodyHtml": "<p><strong>Fact.</strong> 4 November, the one-day reclaim of $80,000, is the only completed November inflow, and IBIT was negative that day.</p><p><strong>Read.</strong> 13 November is dashes on the table. That is not a zero.</p>",
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
    public = {k: pack[k] for k in (
        "id", "date", "kicker", "title", "dek", "asOf", "cadence", "thesis", "stakes",
        "levels", "letterId", "letterUrl", "letterLabel", "subscribeHook", "sourceNote",
    )}
    public["packUrl"] = "/charts/packs/2026-11-13-the-window-closed.json"
    catalog.insert(0, public)
    CATALOG.write_text(json.dumps(catalog, indent=2) + "\n")
    print(f"wrote {PACK.relative_to(ROOT)}")


def main() -> None:
    daily = read_csv(DAILY)
    hourly = read_csv(HOURLY)
    cross = read_csv(CROSS)
    flows = read_csv(FLOWS)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "chart-btc-window-path.svg").write_text(chart_path(daily))
    (OUT / "chart-btc-window-hours.svg").write_text(chart_hourly(hourly))
    (OUT / "chart-btc-window-cross.svg").write_text(chart_cross(cross))
    (OUT / "chart-btc-window-flows.svg").write_text(chart_flows(flows))
    write_pack(daily, hourly, cross, flows)
    print("wrote four svgs")


if __name__ == "__main__":
    main()
