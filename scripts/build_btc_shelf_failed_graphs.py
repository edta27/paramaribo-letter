#!/usr/bin/env python3
"""Build the publication charts for Paramaribo Letter Issue 36.

Reads the frozen Coinbase, Yahoo, and Farside tables in research/. Does not fetch.
"""

from __future__ import annotations

import csv
import html
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAILY = ROOT / "research" / "btc-shelf-failed-2026-11-27.csv"
HOURLY = ROOT / "research" / "btc-nov21-2026-hourly.csv"
CROSS = ROOT / "research" / "cross-asset-nov19-to-nov25-2026.csv"
FLOWS = ROOT / "research" / "farside-btc-nov27-2026.csv"
OUT = ROOT / "public" / "images"
PACK = ROOT / "public" / "charts" / "packs" / "2026-11-27-the-shelf-failed.json"
CATALOG = ROOT / "public" / "charts" / "catalog.json"
RETRIEVED = "27 Nov 2026 · 8:11 a.m. CT / 14:11 UTC"

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
    y_min, y_max = 54_000, 66_000
    lines = start(
        width,
        height,
        "The shelf failed. June's close held.",
        "Daily Coinbase BTC-USD candles from 19 November through 26 November 2026. 20 and 21 November close under $61,946. Every close holds above the 30 June close.",
        "Coinbase daily UTC candles · 19–26 Nov 2026 · 27 Nov is partial and is not plotted",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [56_000, 58_000, 60_000, 62_000, 64_000], y_min, y_max, lambda v: f"${v / 1000:.0f}k")
    for level, label, color in [
        (61_946, "15 Nov low", YELLOW),
        (61_484, "2 Jul close", ACCENT),
        (58_524, "30 Jun close", CYAN),
        (57_718, "1 Jul low", RED),
    ]:
        yy = y_pos(level, y_min, y_max, top, plot_h)
        lines.append(
            f'<line x1="{left:.1f}" y1="{yy:.1f}" x2="{left + plot_w:.1f}" y2="{yy:.1f}" stroke="{color}" stroke-width="1.4" stroke-dasharray="7 5"/>'
        )
        lines.append(f'<text x="{left + plot_w + 8:.1f}" y="{yy + 4:.1f}" class="label" fill="{color}">{label}</text>')
    candle_w = 36
    for i, row in enumerate(rows):
        xx = x_pos(i, len(rows), left + 50, plot_w - 100)
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
        if day in {"11-20", "11-21", "11-26"}:
            lines.append(
                f'<text x="{xx:.1f}" y="{yc - 12:.1f}" class="label" text-anchor="middle">{cl / 1000:.1f}k</text>'
            )
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">20 Nov close $58,815, $291 above the 30 June close. 21 Nov low $55,106. 26 Nov close $60,496. No completed close is under $58,524.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Source: Coinbase Exchange · retrieved {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def chart_hourly(rows: list[dict]) -> str:
    width, height = 1200, 740
    left, top, plot_w, plot_h = 94, 108, 980, 510
    y_min, y_max = 54_000, 62_000
    lines = start(
        width,
        height,
        "The low was $55,106. The close was $60,086.",
        "Hourly Coinbase BTC-USD candles for 21 November 2026. The low prints in the 06:00 UTC hour. The day closes above the 30 June close.",
        "Coinbase hourly UTC candles · 21 Nov 00:00 through 23:00 · 27 Nov is not plotted",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [55_000, 57_000, 59_000, 61_000], y_min, y_max, lambda v: f"${v / 1000:.0f}k")
    for level, label, color in [
        (58_524, "30 Jun close", CYAN),
        (57_718, "1 Jul low", RED),
    ]:
        yy = y_pos(level, y_min, y_max, top, plot_h)
        lines.append(
            f'<line x1="{left:.1f}" y1="{yy:.1f}" x2="{left + plot_w:.1f}" y2="{yy:.1f}" stroke="{color}" stroke-width="1.4" stroke-dasharray="7 5"/>'
        )
        lines.append(f'<text x="{left + plot_w + 8:.1f}" y="{yy + 4:.1f}" class="label" fill="{color}">{label}</text>')
    candle_w = 18
    for i, row in enumerate(rows):
        xx = x_pos(i, len(rows), left + 28, plot_w - 56)
        op, hi, lo, cl = float(row["open"]), float(row["high"]), float(row["low"]), float(row["close"])
        color = GREEN if cl >= op else RED
        yl, yh = y_pos(lo, y_min, y_max, top, plot_h), y_pos(hi, y_min, y_max, top, plot_h)
        yo, yc = y_pos(op, y_min, y_max, top, plot_h), y_pos(cl, y_min, y_max, top, plot_h)
        lines.append(f'<line x1="{xx:.1f}" y1="{yh:.1f}" x2="{xx:.1f}" y2="{yl:.1f}" stroke="{color}" stroke-width="1.4"/>')
        lines.append(
            f'<rect x="{xx - candle_w / 2:.1f}" y="{min(yo, yc):.1f}" width="{candle_w}" height="{max(abs(yc - yo), 2.2):.1f}" fill="{color}" opacity="0.92" stroke="{color}"/>'
        )
        hour = str(row["time"])[11:13]
        if hour in {"00", "06", "12", "18", "23"}:
            lines.append(f'<text x="{xx:.1f}" y="{top + plot_h + 28:.1f}" class="axis" text-anchor="middle">{esc(hour)}</text>')
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">06:00 UTC low $55,106, which is 12:17 a.m. Central on the 1-minute print. 23:00 UTC close $60,086, above the 30 June close of $58,524.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Source: Coinbase Exchange · retrieved {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def chart_cross(rows: list[dict]) -> str:
    width, height = 1200, 740
    left, top, plot_w, plot_h = 180, 120, 900, 500
    lines = start(
        width,
        height,
        "From 19 November to 25 November.",
        "Percent change from the 19 November close to the 25 November close. 25 November is the last completed US cash session before this freeze.",
        "Coinbase BTC close · Yahoo Finance cash and futures closes · 26 Nov had no US cash session",
    )
    y_min, y_max = -6, 4
    panel(lines, left, top, plot_w, plot_h)
    zero = y_pos(0, y_min, y_max, top, plot_h)
    lines.append(f'<line x1="{left:.1f}" y1="{zero:.1f}" x2="{left + plot_w:.1f}" y2="{zero:.1f}" stroke="{GRID}"/>')
    for tick in [-4, -2, 0, 2]:
        yy = y_pos(tick, y_min, y_max, top, plot_h)
        lines.append(f'<line x1="{left:.1f}" y1="{yy:.1f}" x2="{left + plot_w:.1f}" y2="{yy:.1f}" stroke="{GRID}"/>')
        lines.append(f'<text x="{left - 12:.1f}" y="{yy + 4:.1f}" class="axis" text-anchor="end">{tick:+.0f}%</text>')
    n = len(rows)
    gap = plot_h / n
    for i, row in enumerate(rows):
        value = float(row["change_pct"])
        yy = top + gap * i + gap * 0.22
        bh = gap * 0.56
        x0 = left + (0 - y_min) / (y_max - y_min) * plot_w
        x1 = left + (value - y_min) / (y_max - y_min) * plot_w
        color = GREEN if value >= 0 else RED
        lines.append(
            f'<rect x="{min(x0, x1):.1f}" y="{yy:.1f}" width="{abs(x1 - x0):.1f}" height="{bh:.1f}" fill="{color}" opacity="0.9"/>'
        )
        lines.append(f'<text x="{left - 16:.1f}" y="{yy + bh * 0.7:.1f}" class="label" text-anchor="end">{esc(row["name"])}</text>')
        lines.append(
            f'<text x="{max(x0, x1) + 8:.1f}" y="{yy + bh * 0.7:.1f}" class="label" fill="{color}">{value:+.2f}%</text>'
        )
    lines.append(
        f'<text x="{left:.1f}" y="{height - 47}" class="note">Bitcoin −2.47%. S&amp;P 500 +0.10%. Nasdaq −1.23%. HYG −0.01%. On 20 November alone, Bitcoin −5.00% and the S&amp;P 500 −3.70%.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Source: Coinbase, Yahoo Finance · retrieved {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def chart_flows(rows: list[dict]) -> str:
    width, height = 1200, 740
    left, top, plot_w, plot_h = 94, 108, 1040, 500
    lines = start(
        width,
        height,
        "November is an outflow. 27 November is not a zero.",
        "US spot Bitcoin ETF net flow, completed sessions 2–25 November 2026. 26 November is absent. 27 November is dashes and is not plotted.",
        "Farside Investors · US$ millions · weekend blanks are not zeroes",
    )
    y_min, y_max = -800, 200
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [-600, -400, -200, 0], y_min, y_max, lambda v: f"{v:.0f}")
    n = len(rows)
    slot = plot_w / n
    bar_w = slot * 0.62
    for i, row in enumerate(rows):
        value = float(row["total_usd_m"])
        xx = left + slot * i + (slot - bar_w) / 2
        y0 = y_pos(0, y_min, y_max, top, plot_h)
        y1 = y_pos(value, y_min, y_max, top, plot_h)
        color = GREEN if value >= 0 else RED
        lines.append(
            f'<rect x="{xx:.1f}" y="{min(y0, y1):.1f}" width="{bar_w:.1f}" height="{max(abs(y1 - y0), 1.5):.1f}" fill="{color}" opacity="0.9"/>'
        )
        day = str(row["date"])[8:]
        if day in {"02", "16", "19", "20", "25"}:
            lines.append(f'<text x="{xx + bar_w / 2:.1f}" y="{top + plot_h + 24:.1f}" class="axis" text-anchor="middle">{esc(day)}</text>')
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">Completed November total −$5,391.1 million. 20 Nov −$669.2 million. IBIT’s table minimum is now −$544.7 million, on 20 Nov. 26 Nov is absent.</text>'
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
        "id": "2026-11-27-the-shelf-failed",
        "date": "2026-11-27",
        "kicker": "Chart Desk · Issue 36",
        "title": "The shelf failed. Credit went through.",
        "dek": "20 and 21 November both closed under $61,946. 20 November closed at $58,815, $291 above the 30 June close. High-yield OAS printed 3.76% on 20 November.",
        "asOf": "2026-11-27T14:11:51Z",
        "cadence": "follow-up",
        "thesis": "The shelf failed. Credit went through. June's close held.",
        "stakes": "BTC ~$61.3k. 20 and 21 Nov closed under $61,946. 20 Nov close $58,815, $291 above 30 June. Low $55,106. HY OAS 3.76% on 20 Nov, 3.72% on 24 Nov. WAIT.",
        "levels": ["$61.9k", "$61.5k", "$58.5k", "~$57.7k"],
        "letterId": "2026-11-27-the-shelf-failed",
        "letterUrl": "/issue?id=2026-11-27-the-shelf-failed",
        "letterLabel": "Vol. 1 · Issue 36",
        "subscribeHook": "A UTC close under the 30 June close, or a UTC close back above the 2 July close, updates the sequence. Charts stay free here; the call moves by email.",
        "sourceNote": "Issue 36 charts use Coinbase Exchange UTC candles (daily 19–26 Nov 2026; hourly 21 Nov), completed 19 and 25 November closes from Yahoo Finance, and Farside Investors US-session ETF flows for 2–25 November. 2–6 November totals are the figures Issue 35 retrieved; 9–19 November on this pull match that letter. 26 November is absent. 27 November is a partial UTC day and an incomplete Farside row. Weekend blanks are not zeroes. Educational scenario research; no leverage.",
        "briefs": [
            {
                "id": "btc-shelf-path",
                "asset": "BTC",
                "headline": "The shelf failed. June's close held.",
                "lede": "20 and 21 November both closed under $61,946. Every completed close from 20 November through 26 November held above $58,524.",
                "bodyHtml": "<p><strong>Fact.</strong> The 48-hour test Issue 35 wrote down failed. The 30 June close was traded through and was not lost on a close.</p><p><strong>Read.</strong> The tail door is a close under the 1 July low. That close is not in.</p>",
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
                "id": "btc-shelf-hours",
                "asset": "BTC · 21 NOV 2026",
                "headline": "The low was $55,106. The close was $60,086.",
                "lede": "21 November's low printed in the 06:00 UTC hour. The UTC close held above the 30 June close.",
                "bodyHtml": "<p><strong>Fact.</strong> The 1 July low was traded. It was not a close.</p><p><strong>Read.</strong> Acceptance, in the rule this letter inherited, is a UTC close.</p>",
                "charts": [
                    {
                        "title": "BTC hourly range [USD] vs close · 21 Nov 2026",
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
                "id": "btc-shelf-cross",
                "asset": "CROSS-ASSET · 19–25 NOV",
                "headline": "Bitcoin stayed down. The S&P 500 did not.",
                "lede": "From the 19 November close to the 25 November close, Bitcoin fell 2.47% and the S&P 500 rose 0.10%. HYG was unchanged.",
                "bodyHtml": "<p><strong>Fact.</strong> On 20 November alone, Bitcoin fell 5.00% and the S&P 500 fell 3.70%.</p><p><strong>Read.</strong> The spread went through 3.48%. The high-yield fund did not stay down.</p>",
                "charts": [
                    {
                        "title": "19 Nov close to 25 Nov close [%]",
                        "bars": {
                            "label": "Change from the 19 Nov close to the 25 Nov close [%]",
                            "data": [
                                [ms("2026-11-25T00:00:00+00:00") + i, round(float(row["change_pct"]), 2)]
                                for i, row in enumerate(cross)
                            ],
                        },
                    }
                ],
            },
            {
                "id": "btc-shelf-flows",
                "asset": "US SPOT BTC ETF",
                "headline": "20 November is the new IBIT minimum on the table.",
                "lede": "The completed November total is −$5,391.1 million. 20 November is −$669.2 million, of which IBIT is −$544.7 million.",
                "bodyHtml": "<p><strong>Fact.</strong> The Minimum row for IBIT on the retrieved table is (544.7). The Total column’s minimum is still a larger outflow on another day.</p><p><strong>Read.</strong> 26 November is absent. 27 November is dashes. Neither is a zero.</p>",
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
    public["packUrl"] = "/charts/packs/2026-11-27-the-shelf-failed.json"
    catalog.insert(0, public)
    CATALOG.write_text(json.dumps(catalog, indent=2) + "\n")
    print(f"wrote {PACK.relative_to(ROOT)}")


def main() -> None:
    daily = read_csv(DAILY)
    hourly = read_csv(HOURLY)
    cross = read_csv(CROSS)
    flows = read_csv(FLOWS)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "chart-btc-shelf-path.svg").write_text(chart_path(daily))
    (OUT / "chart-btc-shelf-hours.svg").write_text(chart_hourly(hourly))
    (OUT / "chart-btc-shelf-cross.svg").write_text(chart_cross(cross))
    (OUT / "chart-btc-shelf-flows.svg").write_text(chart_flows(flows))
    write_pack(daily, hourly, cross, flows)
    print("wrote four svgs")


if __name__ == "__main__":
    main()
