#!/usr/bin/env python3
"""Build the publication charts for Paramaribo Letter Issue 32.

Reads the frozen Coinbase and Farside tables in research/. Does not fetch.
"""

from __future__ import annotations

import csv
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOW = ROOT / "research" / "btc-door-printed-2026-10-30.csv"
HOURLY = ROOT / "research" / "btc-oct29-2026-hourly.csv"
OUT = ROOT / "public" / "images"
PACK = ROOT / "public" / "charts" / "packs" / "2026-10-30-the-door-printed.json"
RETRIEVED = "30 Oct 2026 · 8:13 a.m. CT / 13:13 UTC"

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
                if key in {"time", "date"}:
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


def chart_hourly(rows: list[dict]) -> str:
    width, height = 1200, 720
    left, top, plot_w, plot_h = 94, 108, 1015, 490
    y_min, y_max = 76_800, 83_200
    lines = start(
        width,
        height,
        "The 20:00 hour lost $80k. The close stayed under it.",
        "Hourly Coinbase BTC-USD candles on 29 October 2026. The session highs $81,890 at 16:00 UTC, breaks $80,000 in the 20:00 hour, and the UTC day closes $77,780.",
        "Coinbase hourly UTC candles · 29 Oct 2026 · low $77,699 · daily close $77,780",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [77_699, 80_000, 81_890], y_min, y_max, lambda v: f"${v / 1000:.1f}k")
    for level, label, color, dash in [(80_000, "$80k", YELLOW, "6 5"), (77_000, "$77k", RED, "6 5")]:
        yy = y_pos(level, y_min, y_max, top, plot_h)
        lines.append(f'<line x1="{left:.1f}" y1="{yy:.1f}" x2="{left + plot_w:.1f}" y2="{yy:.1f}" stroke="{color}" stroke-width="1.4" stroke-dasharray="{dash}"/>')
        lines.append(f'<text x="{left + plot_w + 8:.1f}" y="{yy + 4:.1f}" class="label" fill="{color}">{label}</text>')
    candle_w = 26
    for i, row in enumerate(rows):
        xx = x_pos(i, len(rows), left, plot_w)
        op, hi, lo, cl = float(row["open"]), float(row["high"]), float(row["low"]), float(row["close"])
        color = GREEN if cl >= op else RED
        yl, yh = y_pos(lo, y_min, y_max, top, plot_h), y_pos(hi, y_min, y_max, top, plot_h)
        yo, yc = y_pos(op, y_min, y_max, top, plot_h), y_pos(cl, y_min, y_max, top, plot_h)
        lines.append(f'<line x1="{xx:.1f}" y1="{yh:.1f}" x2="{xx:.1f}" y2="{yl:.1f}" stroke="{color}" stroke-width="1.8"/>')
        lines.append(
            f'<rect x="{xx - candle_w / 2:.1f}" y="{min(yo, yc):.1f}" width="{candle_w}" height="{max(abs(yc - yo), 2.5):.1f}" fill="{color}" opacity="0.92" stroke="{color}"/>'
        )
        hour = str(row["time"])[11:13]
        if hour in {"00", "04", "08", "12", "16", "20", "23"}:
            lines.append(f'<text x="{xx:.1f}" y="{top + plot_h + 24:.1f}" class="axis" text-anchor="middle">{hour}:00</text>')
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">16:00 UTC hour high $81,890. 20:00 UTC hour low $78,177, close $78,744. UTC daily close: $77,780 on 9,934 BTC. $80,000 did not come back.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Source: Coinbase Exchange BTC-USD · retrieved {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def chart_path(rows: list[dict]) -> str:
    width, height = 1200, 740
    left, top, plot_w, plot_h = 94, 108, 1015, 510
    y_min, y_max = 75_000, 89_000
    lines = start(
        width,
        height,
        "$80k held on closes until 29 October.",
        "Daily Coinbase BTC-USD candles from 1 October through 29 October 2026. 29 October low $77,699 and close $77,780. 30 October is not plotted.",
        "Coinbase daily UTC candles · 1–29 Oct 2026 · last completed day is 29 Oct · 30 Oct is partial",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [77_780, 80_000, 84_856, 86_507], y_min, y_max, lambda v: f"${v / 1000:.1f}k")
    for level, label, color, dash in [(86_000, "$86k", CYAN, "7 5"), (82_000, "$82k", YELLOW, "7 5"), (80_000, "$80k", RED, "5 5")]:
        yy = y_pos(level, y_min, y_max, top, plot_h)
        lines.append(f'<line x1="{left:.1f}" y1="{yy:.1f}" x2="{left + plot_w:.1f}" y2="{yy:.1f}" stroke="{color}" stroke-width="1.4" stroke-dasharray="{dash}"/>')
        lines.append(f'<text x="{left + plot_w + 8:.1f}" y="{yy + 4:.1f}" class="label" fill="{color}">{label}</text>')
    candle_w = 18
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
        if day in {"10-01", "10-04", "10-15", "10-22", "10-26", "10-29"}:
            lines.append(f'<text x="{xx:.1f}" y="{top + plot_h + 24:.1f}" class="axis" text-anchor="middle">{day}</text>')
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">4 Oct close $86,507 was not followed by a second. 29 Oct close $77,780. The 15 Oct wick at $79,676 is no longer the low of this window.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Source: Coinbase Exchange BTC-USD · retrieved {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def chart_flows(rows: list[dict]) -> str:
    width, height = 1200, 740
    left, top, plot_w, price_h = 94, 108, 1015, 240
    flow_top, flow_h = 405, 220
    p_min, p_max = 76_000, 88_500
    f_min, f_max = -750, 700
    lines = start(
        width,
        height,
        "Four inflow days. Then a close through $80k.",
        "Coinbase Bitcoin closing price compared with Farside US spot Bitcoin ETF net flows from 12 October through 29 October. 26–29 October net +$440.8M. 29 October printed +$17.2M and closed $77,780.",
        "Coinbase daily closes + Farside US-session ETF flows · weekend blanks are not zeroes · 30 Oct is incomplete",
    )
    panel(lines, left, top, plot_w, price_h)
    panel(lines, left, flow_top, plot_w, flow_h)
    grid(lines, left, top, plot_w, price_h, [77_780, 80_000, 86_000], p_min, p_max, lambda v: f"${v / 1000:.0f}k")
    grid(lines, left, flow_top, plot_w, flow_h, [-636, 0, 527], f_min, f_max, lambda v: f"${v:.0f}M")
    price_points = []
    for i, row in enumerate(rows):
        xx = x_pos(i, len(rows), left, plot_w)
        price_points.append((xx, y_pos(float(row["btc_close"]), p_min, p_max, top, price_h)))
        flow = row["etf_flow_usd_m"]
        if flow is not None:
            zero_y = y_pos(0, f_min, f_max, flow_top, flow_h)
            bar_y = y_pos(float(flow), f_min, f_max, flow_top, flow_h)
            color = GREEN if float(flow) >= 0 else RED
            bar_w = min(28, plot_w / len(rows) * 0.55)
            lines.append(
                f'<rect x="{xx - bar_w / 2:.1f}" y="{min(zero_y, bar_y):.1f}" width="{bar_w:.1f}" height="{max(abs(zero_y - bar_y), 2):.1f}" fill="{color}" opacity="0.86" rx="3"/>'
            )
            if abs(float(flow)) >= 170:
                lines.append(
                    f'<text x="{xx:.1f}" y="{bar_y - 8 if float(flow) >= 0 else bar_y + 16:.1f}" class="note" text-anchor="middle">{float(flow):+.0f}</text>'
                )
        day = str(row["date"])[5:]
        if day in {"10-12", "10-16", "10-22", "10-26", "10-29"}:
            lines.append(f'<text x="{xx:.1f}" y="{flow_top + flow_h + 24:.1f}" class="axis" text-anchor="middle">{day}</text>')
    coords = " ".join(f"{x:.1f},{y:.1f}" for x, y in price_points)
    lines.append(f'<polyline points="{coords}" fill="none" stroke="{CYAN}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>')
    for xx, yy in price_points:
        lines.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="3.2" fill="{CYAN}"/>')
    zero_y = y_pos(0, f_min, f_max, flow_top, flow_h)
    lines.append(f'<line x1="{left:.1f}" y1="{zero_y:.1f}" x2="{left + plot_w:.1f}" y2="{zero_y:.1f}" stroke="{MUTE}"/>')
    lines.append(f'<text x="{left + 12}" y="{top + 24}" class="label">BTC-USD close</text>')
    lines.append(f'<text x="{left + 12}" y="{flow_top + 24}" class="label">Farside US spot BTC ETF net flow · US$ millions</text>')
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">22 Oct −$635.6M. 23 Oct −$137.9M. 26–29 Oct net +$440.8M, of which 29 Oct is +$17.2M. 17–18 and 24–25 Oct are weekend blanks, not zeroes. 30 Oct is not a zero.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Sources: Coinbase Exchange + Farside Investors · {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def ms(iso: str) -> int:
    from datetime import datetime, timezone

    return int(datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp() * 1000)


def write_pack(daily: list[dict], hourly: list[dict]) -> None:
    def series(rows, time_key, value_key):
        out = []
        for row in rows:
            value = row[value_key]
            out.append([ms(str(row[time_key])), None if value is None else round(float(value), 2)])
        return out

    path_rows = daily
    flow_rows = [row for row in daily if str(row["date"]) >= "2026-10-12"]
    pack = {
        "id": "2026-10-30-the-door-printed",
        "date": "2026-10-30",
        "kicker": "Chart Desk · Issue 32",
        "title": "The door printed. Panic did not.",
        "dek": "29 October 2026 hourly break through $80,000, the daily box since 1 October, and Farside ETF flows through the +$17.2M session.",
        "asOf": "2026-10-30T13:13:51Z",
        "cadence": "follow-up",
        "thesis": "The door printed. Panic did not.",
        "stakes": "BTC ~$77.2k. 29 Oct close $77,780, the first daily close under $80k since 17 Sep. The 48-hour reclaim is not in. WAIT.",
        "levels": ["$86k", "$82k", "$80k", "$77k", "$72k", "~$57.7k"],
        "letterId": "2026-10-30-the-door-printed",
        "letterUrl": "/issue?id=2026-10-30-the-door-printed",
        "letterLabel": "Vol. 1 · Issue 32",
        "subscribeHook": "A UTC close back above $80k on 30 or 31 October, or a completed close through $77k, updates the sequence. Charts stay free here; the call moves by email.",
        "sourceNote": "Issue 32 charts use Coinbase Exchange UTC candles (hourly 29 Oct 2026; daily 1–29 Oct) and Farside Investors US-session ETF flows from 12 October. 30 October is a partial UTC day and an incomplete Farside row. Weekend blanks are not zeroes. Educational scenario research; no leverage.",
        "briefs": [
            {
                "id": "btc-door-hours",
                "asset": "BTC · 29 OCT 2026",
                "headline": "The 20:00 hour lost $80k. The close stayed under it.",
                "lede": "The 16:00 UTC hour high was $81,890. The 20:00 hour closed $78,744. The UTC day closed $77,780.",
                "bodyHtml": "<p><strong>Fact.</strong> $80k broke during the 20:00 UTC hour and was not reclaimed by the daily close.</p><p><strong>Read.</strong> A close is not the same thing as a finished 48-hour test. One session is not a panic.</p>",
                "charts": [
                    {
                        "title": "BTC hourly range [USD] vs close · 29 Oct 2026",
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
                "id": "btc-door-path",
                "asset": "BTC",
                "headline": "$80k held on closes until 29 October.",
                "lede": "29 October low $77,699 and close $77,780. 4 October's $86,507 is still the only close above $86k.",
                "bodyHtml": "<p><strong>Fact.</strong> The first completed close under $80k since 17 September printed on 29 October.</p><p><strong>Read.</strong> The door the last letter was watching has a close through it. The reclaim window was still open at the freeze.</p>",
                "charts": [
                    {
                        "title": "BTC daily range [USD] vs close",
                        "bars": {
                            "label": "Daily high–low range [USD]",
                            "unsigned": True,
                            "data": [
                                [ms(str(row["date"]) + "T00:00:00+00:00"), round(float(row["btc_high"]) - float(row["btc_low"]), 2)]
                                for row in path_rows
                            ],
                        },
                        "line": {
                            "label": "BTC-USD close [USD]",
                            "data": series(
                                [{**row, "time": str(row["date"]) + "T00:00:00+00:00"} for row in path_rows],
                                "time",
                                "btc_close",
                            ),
                        },
                    }
                ],
            },
            {
                "id": "btc-door-flows",
                "asset": "BTC · ETF",
                "headline": "Four inflow days. Then a close through $80k.",
                "lede": "26–29 October net +$440.8 million. 29 October was +$17.2 million. The close was $77,780.",
                "bodyHtml": "<p><strong>Fact.</strong> The US-session creations did not stop the UTC close through $80k.</p><p><strong>Read.</strong> A small positive flow is not absorption, and it is not a structural bleed. 30 October is not a zero.</p>",
                "charts": [
                    {
                        "title": "Farside net flow [US$ millions] vs BTC close",
                        "bars": {
                            "label": "Farside US spot BTC ETF net flow [US$ millions]",
                            "data": series(
                                [{**row, "time": str(row["date"]) + "T00:00:00+00:00"} for row in flow_rows],
                                "time",
                                "etf_flow_usd_m",
                            ),
                        },
                        "line": {
                            "label": "BTC-USD close [USD]",
                            "data": series(
                                [{**row, "time": str(row["date"]) + "T00:00:00+00:00"} for row in flow_rows],
                                "time",
                                "btc_close",
                            ),
                        },
                    }
                ],
            },
        ],
    }
    PACK.write_text(json.dumps(pack, indent=2) + "\n")
    print(f"wrote {PACK.relative_to(ROOT)}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    daily = read_csv(NOW)
    hourly = read_csv(HOURLY)
    outputs = {
        "chart-btc-door-hours.svg": chart_hourly(hourly),
        "chart-btc-door-path.svg": chart_path(daily),
        "chart-btc-door-flows.svg": chart_flows([row for row in daily if str(row["date"]) >= "2026-10-12"]),
    }
    for name, content in outputs.items():
        path = OUT / name
        path.write_text(content + "\n")
        print(f"wrote {path.relative_to(ROOT)}")
    write_pack(daily, hourly)


if __name__ == "__main__":
    main()
