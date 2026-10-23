#!/usr/bin/env python3
"""Build the publication charts for Paramaribo Letter Issue 31."""

from __future__ import annotations

import csv
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOW = ROOT / "research" / "btc-outflow-door-2026-10-23.csv"
HOURLY = ROOT / "research" / "btc-oct22-2026-hourly.csv"
OUT = ROOT / "public" / "images"
RETRIEVED = "23 Oct 2026 · 8:13 a.m. CT / 13:13 UTC"

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
    y_min, y_max = 80_000, 85_200
    lines = start(
        width,
        height,
        "The low found $80.8k. The close stayed above $80k.",
        "Hourly Coinbase BTC-USD candles on 22 October 2026. The session opens at $84,025, lows $80,790 at 16:00 UTC, and the UTC day closes $81,307.",
        "Coinbase hourly UTC candles · 22 Oct 2026 · low $80,790 · daily close $81,307",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [80_790, 82_000, 84_000, 84_856], y_min, y_max, lambda v: f"${v / 1000:.1f}k")
    for level, label, color, dash in [(80_000, "$80k", YELLOW, "6 5"), (82_000, "$82k", CYAN, "6 5")]:
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
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">16:00 UTC hour low $80,790. The hour closed $81,175. UTC daily close: $81,307 on 7,277 BTC. $80,000 was not traded.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Source: Coinbase Exchange BTC-USD · retrieved {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def chart_path(rows: list[dict]) -> str:
    width, height = 1200, 740
    left, top, plot_w, plot_h = 94, 108, 1015, 510
    y_min, y_max = 78_000, 89_000
    lines = start(
        width,
        height,
        "A lower high at $84.9k. Then another close through $82k.",
        "Daily Coinbase BTC-USD candles from 1 October through 22 October 2026. 21 October high $84,856 and close $84,025. 22 October low $80,790 and close $81,307. 23 October is not plotted.",
        "Coinbase daily UTC candles · 1–22 Oct 2026 · last completed day is 22 Oct · 23 Oct is partial",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [80_000, 82_000, 84_856, 86_507], y_min, y_max, lambda v: f"${v / 1000:.1f}k")
    for level, label, color, dash in [(86_000, "$86k", CYAN, "7 5"), (82_000, "$82k", YELLOW, "7 5"), (80_000, "$80k", RED, "5 5")]:
        yy = y_pos(level, y_min, y_max, top, plot_h)
        lines.append(f'<line x1="{left:.1f}" y1="{yy:.1f}" x2="{left + plot_w:.1f}" y2="{yy:.1f}" stroke="{color}" stroke-width="1.4" stroke-dasharray="{dash}"/>')
        lines.append(f'<text x="{left + plot_w + 8:.1f}" y="{yy + 4:.1f}" class="label" fill="{color}">{label}</text>')
    candle_w = 22
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
        if day in {"10-01", "10-04", "10-08", "10-15", "10-21", "10-22"}:
            lines.append(f'<text x="{xx:.1f}" y="{top + plot_h + 24:.1f}" class="axis" text-anchor="middle">{day}</text>')
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">4 Oct close $86,507 was not followed by a second. 21 Oct high $84,856. 22 Oct close $81,307. The 15 Oct wick at $79,676 is still the low.</text>'
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
    p_min, p_max = 78_000, 88_500
    f_min, f_max = -750, 700
    lines = start(
        width,
        height,
        "Three sessions of creations. Then October's largest outflow.",
        "Coinbase Bitcoin closing price compared with Farside US spot Bitcoin ETF net flows. 19–21 October net +$1,074.7M. 22 October printed −$635.6M. October weekdays net −$175.6M.",
        "Coinbase daily closes + Farside US-session ETF flows · weekend blanks are not zeroes · 23 Oct is incomplete",
    )
    panel(lines, left, top, plot_w, price_h)
    panel(lines, left, flow_top, plot_w, flow_h)
    grid(lines, left, top, plot_w, price_h, [80_000, 82_000, 86_000], p_min, p_max, lambda v: f"${v / 1000:.0f}k")
    grid(lines, left, flow_top, plot_w, flow_h, [-636, -485, 0, 527], f_min, f_max, lambda v: f"${v:.0f}M")
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
        if day in {"10-01", "10-07", "10-15", "10-19", "10-22"}:
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
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">19 Oct +$526.7M. 21 Oct +$524.8M. 22 Oct −$635.6M. 3–4, 10–11 and 17–18 Oct are weekend blanks, not zeroes. 23 Oct is not a zero.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Sources: Coinbase Exchange + Farside Investors · {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    daily = read_csv(NOW)
    outputs = {
        "chart-btc-outflow-hours.svg": chart_hourly(read_csv(HOURLY)),
        "chart-btc-outflow-path.svg": chart_path(daily),
        "chart-btc-outflow-flows.svg": chart_flows(daily),
    }
    for name, content in outputs.items():
        path = OUT / name
        path.write_text(content + "\n")
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
