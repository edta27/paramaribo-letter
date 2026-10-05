#!/usr/bin/env python3
"""Build the publication charts for Paramaribo Letter Issue 29."""

from __future__ import annotations

import csv
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOW = ROOT / "research" / "btc-shock-ran-2026-10-05.csv"
HOURLY = ROOT / "research" / "btc-oct2-2026-hourly.csv"
OUT = ROOT / "public" / "images"
RETRIEVED = "5 Oct 2026 · 8:20 a.m. CDT / 13:20 UTC"

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
    y_min, y_max = 82_000, 88_500
    lines = start(
        width,
        height,
        "Six hours is not ten minutes",
        "Hourly Coinbase BTC-USD candles on 2 October 2026. Price reaches $87,249 at 12:30 UTC, then falls to $83,850 by 18:45 UTC. The $82,000 door is not tagged.",
        "Coinbase hourly UTC candles · 2 Oct 2026 · jobs-day high $87,249 to afternoon low $83,850",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [82_000, 83_850, 86_000, 87_249], y_min, y_max, lambda v: f"${v / 1000:.1f}k")
    for level, label, color, dash in [(82_000, "$82k", YELLOW, "6 5"), (86_000, "$86k", CYAN, "6 5")]:
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
        if hour in {"00", "04", "08", "12", "16", "18", "23"}:
            lines.append(f'<text x="{xx:.1f}" y="{top + plot_h + 24:.1f}" class="axis" text-anchor="middle">{hour}:00</text>')
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">5-minute high $87,249 at 12:30 UTC. 5-minute low $83,850 at 18:45 UTC. Elapsed: 375 minutes. Daily close: $84,505.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Source: Coinbase Exchange BTC-USD · retrieved {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def chart_path(rows: list[dict]) -> str:
    width, height = 1200, 740
    left, top, plot_w, plot_h = 94, 108, 1015, 510
    y_min, y_max = 80_000, 89_000
    lines = start(
        width,
        height,
        "One close above $86k. Not two. Thin volume.",
        "Daily Coinbase BTC-USD candles from 22 September through 4 October 2026. The $82,510 low held. 2 October swept $87,249 and closed $84,505. 4 October closed $86,507 on 2,623 BTC.",
        "Coinbase daily UTC candles · 22 Sep–4 Oct 2026 · last completed day is 4 Oct · 5 Oct is partial",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [82_000, 83_850, 86_000, 87_400], y_min, y_max, lambda v: f"${v / 1000:.0f}k")
    for level, label, color, dash in [(87_397, "$87.4k", MUTE, "5 5"), (86_000, "$86k", CYAN, "7 5"), (82_000, "$82k", YELLOW, "7 5")]:
        yy = y_pos(level, y_min, y_max, top, plot_h)
        lines.append(f'<line x1="{left:.1f}" y1="{yy:.1f}" x2="{left + plot_w:.1f}" y2="{yy:.1f}" stroke="{color}" stroke-width="1.4" stroke-dasharray="{dash}"/>')
        lines.append(f'<text x="{left + plot_w + 8:.1f}" y="{yy + 4:.1f}" class="label" fill="{color}">{label}</text>')
    candle_w = 32
    for i, row in enumerate(rows):
        xx = x_pos(i, len(rows), left, plot_w)
        op, hi, lo, cl = float(row["btc_open"]), float(row["btc_high"]), float(row["btc_low"]), float(row["btc_close"])
        color = GREEN if cl >= op else RED
        yl, yh = y_pos(lo, y_min, y_max, top, plot_h), y_pos(hi, y_min, y_max, top, plot_h)
        yo, yc = y_pos(op, y_min, y_max, top, plot_h), y_pos(cl, y_min, y_max, top, plot_h)
        lines.append(f'<line x1="{xx:.1f}" y1="{yh:.1f}" x2="{xx:.1f}" y2="{yl:.1f}" stroke="{color}" stroke-width="1.8"/>')
        lines.append(
            f'<rect x="{xx - candle_w / 2:.1f}" y="{min(yo, yc):.1f}" width="{candle_w}" height="{max(abs(yc - yo), 2.5):.1f}" fill="{color}" opacity="0.92" stroke="{color}"/>'
        )
        day = str(row["date"])[5:]
        if day in {"09-22", "09-28", "09-30", "10-02", "10-04"}:
            lines.append(f'<text x="{xx:.1f}" y="{top + plot_h + 24:.1f}" class="axis" text-anchor="middle">{day}</text>')
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">28 Sep low $82,510. 2 Oct high $87,249, close $84,505, volume 8,762 BTC. 4 Oct close $86,507, volume 2,623 BTC (Sunday).</text>'
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
    p_min, p_max = 81_000, 88_500
    f_min, f_max = -250, 250
    lines = start(
        width,
        height,
        "The bid went red for one session, then returned",
        "Coinbase Bitcoin closing price compared with Farside US spot Bitcoin ETF net flows. 30 September printed −$148.7M. 1–2 October printed +$102.7M and +$189.9M.",
        "Coinbase daily closes + Farside US-session ETF flows · weekend blanks are not zeroes · 5 Oct Farside row is incomplete",
    )
    panel(lines, left, top, plot_w, price_h)
    panel(lines, left, flow_top, plot_w, flow_h)
    grid(lines, left, top, plot_w, price_h, [82_000, 84_000, 86_000, 88_000], p_min, p_max, lambda v: f"${v / 1000:.0f}k")
    grid(lines, left, flow_top, plot_w, flow_h, [-150, 0, 100, 200], f_min, f_max, lambda v: f"${v:.0f}M")
    price_points = []
    for i, row in enumerate(rows):
        xx = x_pos(i, len(rows), left, plot_w)
        price_points.append((xx, y_pos(float(row["btc_close"]), p_min, p_max, top, price_h)))
        flow = row["etf_flow_usd_m"]
        if flow is not None:
            zero_y = y_pos(0, f_min, f_max, flow_top, flow_h)
            bar_y = y_pos(float(flow), f_min, f_max, flow_top, flow_h)
            color = GREEN if float(flow) >= 0 else RED
            bar_w = min(48, plot_w / len(rows) * 0.52)
            lines.append(
                f'<rect x="{xx - bar_w / 2:.1f}" y="{min(zero_y, bar_y):.1f}" width="{bar_w:.1f}" height="{max(abs(zero_y - bar_y), 2):.1f}" fill="{color}" opacity="0.86" rx="3"/>'
            )
            lines.append(
                f'<text x="{xx:.1f}" y="{bar_y - 8 if float(flow) >= 0 else bar_y + 16:.1f}" class="note" text-anchor="middle">{float(flow):+.0f}</text>'
            )
        day = str(row["date"])[5:]
        if day in {"09-22", "09-25", "09-30", "10-02", "10-04"}:
            lines.append(f'<text x="{xx:.1f}" y="{flow_top + flow_h + 24:.1f}" class="axis" text-anchor="middle">{day}</text>')
    coords = " ".join(f"{x:.1f},{y:.1f}" for x, y in price_points)
    lines.append(f'<polyline points="{coords}" fill="none" stroke="{CYAN}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>')
    for xx, yy in price_points:
        lines.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="3.5" fill="{CYAN}"/>')
    zero_y = y_pos(0, f_min, f_max, flow_top, flow_h)
    lines.append(f'<line x1="{left:.1f}" y1="{zero_y:.1f}" x2="{left + plot_w:.1f}" y2="{zero_y:.1f}" stroke="{MUTE}"/>')
    lines.append(f'<text x="{left + 12}" y="{top + 24}" class="label">BTC-USD close</text>')
    lines.append(f'<text x="{left + 12}" y="{flow_top + 24}" class="label">Farside US spot BTC ETF net flow · US$ millions</text>')
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">30 Sep −$148.7M ended a nine-session green streak. 1 Oct IBIT +$195.6M against FBTC −$60.7M. 2 Oct completed +$189.9M, not the provisional +$31.7M in some secondary trackers.</text>'
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
        "chart-btc-shock-ran-hours.svg": chart_hourly(read_csv(HOURLY)),
        "chart-btc-shock-ran-path.svg": chart_path(daily),
        "chart-btc-shock-ran-flows.svg": chart_flows(daily),
    }
    for name, content in outputs.items():
        path = OUT / name
        path.write_text(content + "\n")
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
