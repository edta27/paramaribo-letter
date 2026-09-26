#!/usr/bin/env python3
"""Build the publication charts for Paramaribo Letter Issue 27."""

from __future__ import annotations

import csv
import html
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "research" / "btc-87k-rejection-2026-09-26.csv"
OUT = ROOT / "public" / "images"
RETRIEVED = "26 Sep 2026 · 12:01 a.m. CDT / 05:01 UTC"
LIVE_PRICE = 83_975.53

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


def read_rows() -> list[dict[str, float | str | None]]:
    rows: list[dict[str, float | str | None]] = []
    with DATA.open(newline="") as fh:
        for raw in csv.DictReader(fh):
            row: dict[str, float | str | None] = {"date": raw["date"]}
            for key, value in raw.items():
                if key == "date":
                    continue
                row[key] = None if value == "" else float(value)
            rows.append(row)
    return rows


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def start(width: int, height: int, title: str, desc: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{esc(title)}</title>',
        f'<desc id="desc">{esc(desc)}</desc>',
        f'<rect width="{width}" height="{height}" fill="{BG}"/>',
        '<style>text{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.title{font-size:28px;font-weight:700;fill:%s}.sub{font-size:15px;fill:%s}.axis{font-size:13px;fill:%s}.note{font-size:12px;fill:%s}.label{font-size:13px;font-weight:600;fill:%s}</style>' % (TEXT, MUTE, MUTE, MUTE, TEXT),
        f'<text x="56" y="48" class="title">{esc(title)}</text>',
        f'<text x="56" y="76" class="sub">Daily UTC candles · {esc(RETRIEVED)} · last completed day is 25 Sep</text>',
    ]


def panel(lines: list[str], x: float, y: float, width: float, height: float) -> None:
    lines.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" rx="8" fill="{PANEL}" stroke="{GRID}"/>')


def y_pos(value: float, y_min: float, y_max: float, top: float, height: float) -> float:
    return top + (y_max - value) / (y_max - y_min) * height


def x_pos(index: int, count: int, left: float, width: float) -> float:
    return left + (index / (count - 1)) * width if count > 1 else left


def grid(lines: list[str], left: float, top: float, width: float, height: float, ticks: list[float], y_min: float, y_max: float, fmt) -> None:
    for tick in ticks:
        yy = y_pos(tick, y_min, y_max, top, height)
        lines.append(f'<line x1="{left:.1f}" y1="{yy:.1f}" x2="{left + width:.1f}" y2="{yy:.1f}" stroke="{GRID}"/>')
        lines.append(f'<text x="{left - 12:.1f}" y="{yy + 4:.1f}" class="axis" text-anchor="end">{esc(fmt(tick))}</text>')


def x_ticks(lines: list[str], rows: list[dict], left: float, top: float, width: float, height: float) -> None:
    for i, row in enumerate(rows):
        xx = x_pos(i, len(rows), left, width)
        label = str(row["date"])[5:].replace("-", "/")
        lines.append(f'<line x1="{xx:.1f}" y1="{top:.1f}" x2="{xx:.1f}" y2="{top + height:.1f}" stroke="{GRID}" opacity="0.42"/>')
        lines.append(f'<text x="{xx:.1f}" y="{top + height + 25:.1f}" class="axis" text-anchor="middle">{label}</text>')


def line(points: list[tuple[float, float]], color: str, width: float = 2.5, dash: str = "") -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    coords = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"{dash_attr}/>'


def chart_price(rows: list[dict]) -> str:
    width, height = 1200, 750
    left, top, plot_w, plot_h = 94, 108, 1015, 510
    y_min, y_max = 55_000, 90_000
    lines = start(width, height, "The $87k door failed; $82–83k held", "Daily Coinbase BTC-USD candles from September 15 through September 25, 2026. The chart shows the rally to 87.4 thousand, the September 23 rejection, and the September 24 test of 82.7 thousand.")
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [58_000, 65_000, 72_000, 77_000, 82_000, 87_000], y_min, y_max, lambda v: f"${v / 1000:.0f}k")
    x_ticks(lines, rows, left, top, plot_w, plot_h)
    for level, label, color, dash in [(58_000, "$57.7k low", MUTE, "5 5"), (72_000, "$71.7–72.3k", YELLOW, "7 5"), (77_000, "$77k", ACCENT, "7 5"), (82_000, "$82k", CYAN, "7 5")]:
        yy = y_pos(level, y_min, y_max, top, plot_h)
        lines.append(f'<line x1="{left:.1f}" y1="{yy:.1f}" x2="{left + plot_w:.1f}" y2="{yy:.1f}" stroke="{color}" stroke-width="1.5" stroke-dasharray="{dash}"/>')
        lines.append(f'<text x="{left + plot_w + 10:.1f}" y="{yy + 4:.1f}" class="label">{label}</text>')
    band_top = y_pos(76_000, y_min, y_max, top, plot_h)
    band_bottom = y_pos(74_000, y_min, y_max, top, plot_h)
    lines.append(f'<rect x="{left:.1f}" y="{band_top:.1f}" width="{plot_w:.1f}" height="{band_bottom - band_top:.1f}" fill="{YELLOW}" opacity="0.10"/>')
    lines.append(f'<text x="{left + 8:.1f}" y="{band_top - 7:.1f}" class="label" fill="{YELLOW}">$74–76k process band</text>')
    candle_w = 38
    for i, row in enumerate(rows):
        xx = x_pos(i, len(rows), left, plot_w)
        low, high = float(row["btc_low"]), float(row["btc_high"])
        op, close = float(row["btc_open"]), float(row["btc_close"])
        color = GREEN if close >= op else RED
        yl, yh = y_pos(low, y_min, y_max, top, plot_h), y_pos(high, y_min, y_max, top, plot_h)
        yo, yc = y_pos(op, y_min, y_max, top, plot_h), y_pos(close, y_min, y_max, top, plot_h)
        lines.append(f'<line x1="{xx:.1f}" y1="{yh:.1f}" x2="{xx:.1f}" y2="{yl:.1f}" stroke="{color}" stroke-width="2"/>')
        lines.append(f'<rect x="{xx - candle_w / 2:.1f}" y="{min(yo, yc):.1f}" width="{candle_w}" height="{max(abs(yc - yo), 3):.1f}" fill="{color}" opacity="0.92" stroke="{color}"/>')
    for date, label, value, color in [("2026-09-21", "87.4k high", 87_397, CYAN), ("2026-09-24", "82.7k test", 82_709, RED)]:
        i = next(j for j, row in enumerate(rows) if row["date"] == date)
        xx = x_pos(i, len(rows), left, plot_w)
        yy = y_pos(value, y_min, y_max, top, plot_h)
        lines.append(f'<line x1="{xx:.1f}" y1="{top:.1f}" x2="{xx:.1f}" y2="{top + plot_h:.1f}" stroke="{color}" stroke-width="1.5" stroke-dasharray="4 5"/>')
        lines.append(f'<text x="{xx + 10:.1f}" y="{max(top + 25, yy - 16):.1f}" class="label" fill="{color}">{label}</text>')
    live_x = x_pos(len(rows) - 1, len(rows), left, plot_w)
    live_y = y_pos(LIVE_PRICE, y_min, y_max, top, plot_h)
    lines.append(f'<circle cx="{live_x:.1f}" cy="{live_y:.1f}" r="6" fill="{BG}" stroke="{ACCENT}" stroke-width="3"/>')
    lines.append(f'<text x="{live_x - 12:.1f}" y="{live_y - 13:.1f}" class="label" text-anchor="end">live $84.0k</text>')
    lines.append(f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">25 Sep completed close: $84,093 · 24 Sep low: $82,709 · 21 Sep high: $87,397 · the 26 Sep UTC candle is partial.</text>')
    lines.append(f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Source: Coinbase Exchange BTC-USD candles · retrieved {esc(RETRIEVED)}</text>')
    lines.append("</svg>")
    return "\n".join(lines)


def chart_flows(rows: list[dict]) -> str:
    width, height = 1200, 740
    left, top, plot_w, price_h = 94, 108, 1015, 240
    flow_top, flow_h = 405, 220
    p_min, p_max = 74_000, 89_000
    f_min, f_max = -550, 1_100
    lines = start(width, height, "ETF demand stayed positive as price stalled", "Coinbase Bitcoin closing price is compared with Farside US spot Bitcoin ETF flows from September 15 through September 25, 2026. Inflows decelerated after the $999 million session.")
    panel(lines, left, top, plot_w, price_h)
    panel(lines, left, flow_top, plot_w, flow_h)
    grid(lines, left, top, plot_w, price_h, [75_000, 80_000, 85_000, 89_000], p_min, p_max, lambda v: f"${v / 1000:.0f}k")
    grid(lines, left, flow_top, plot_w, flow_h, [-500, 0, 500, 1_000], f_min, f_max, lambda v: f"${v / 1000:.1f}B" if abs(v) >= 1000 else f"${v:.0f}M")
    x_ticks(lines, rows, left, flow_top, plot_w, flow_h)
    price_points = []
    for i, row in enumerate(rows):
        xx = x_pos(i, len(rows), left, plot_w)
        price_points.append((xx, y_pos(float(row["btc_close"]), p_min, p_max, top, price_h)))
        flow = row["etf_flow_usd_m"]
        if flow is not None:
            zero_y = y_pos(0, f_min, f_max, flow_top, flow_h)
            bar_y = y_pos(float(flow), f_min, f_max, flow_top, flow_h)
            color = GREEN if float(flow) >= 0 else RED
            bar_w = min(58, plot_w / len(rows) * 0.56)
            lines.append(f'<rect x="{xx - bar_w / 2:.1f}" y="{min(zero_y, bar_y):.1f}" width="{bar_w:.1f}" height="{max(abs(zero_y - bar_y), 2):.1f}" fill="{color}" opacity="0.86" rx="3"/>')
            lines.append(f'<text x="{xx:.1f}" y="{bar_y - 8 if float(flow) >= 0 else bar_y + 17:.1f}" class="note" text-anchor="middle">{float(flow):+.0f}</text>')
    lines.append(line(price_points, CYAN, 3))
    for xx, yy in price_points:
        lines.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="3.5" fill="{CYAN}"/>')
    zero_y = y_pos(0, f_min, f_max, flow_top, flow_h)
    lines.append(f'<line x1="{left:.1f}" y1="{zero_y:.1f}" x2="{left + plot_w:.1f}" y2="{zero_y:.1f}" stroke="{MUTE}"/>')
    lines.append(f'<text x="{left + 12}" y="{top + 24}" class="label">BTC-USD close</text>')
    lines.append(f'<text x="{left + 12}" y="{flow_top + 24}" class="label">Farside US spot BTC ETF net flow · US$ millions</text>')
    lines.append(f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">17–25 Sep reported-session sum: +$2.978B. Daily prints after 21 Sep: +$999M → +$715M → +$347M → +$191M → +$135M.</text>')
    lines.append(f'<text x="{left + 10:.1f}" y="{height - 25}" class="note">Issue 26 froze 23 Sep at a preliminary +$32.4M. The completed Farside row is +$346.9M. Weekend blanks are not zeroes.</text>')
    lines.append(f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Sources: Coinbase Exchange + Farside Investors · {esc(RETRIEVED)}</text>')
    lines.append("</svg>")
    return "\n".join(lines)


def chart_leverage(rows: list[dict]) -> str:
    width, height = 1200, 840
    left, plot_w = 94, 1015
    p_top, p_h = 105, 185
    oi_top, oi_h = 330, 175
    fund_top, fund_h = 545, 180
    p_min, p_max = 74_000, 89_000
    oi_min, oi_max = 1.9, 2.9
    fund_min, fund_max = -0.002, 0.012
    lines = start(width, height, "Leverage kept coming out after the flush", "Coinbase Bitcoin closing price is shown with OKX BTC-USDT perpetual open interest and average realized funding per eight hours through 25 September 2026.")
    for y, h in [(p_top, p_h), (oi_top, oi_h), (fund_top, fund_h)]:
        panel(lines, left, y, plot_w, h)
    grid(lines, left, p_top, plot_w, p_h, [75_000, 80_000, 85_000, 89_000], p_min, p_max, lambda v: f"${v / 1000:.0f}k")
    grid(lines, left, oi_top, plot_w, oi_h, [2.0, 2.4, 2.8], oi_min, oi_max, lambda v: f"${v:.1f}B")
    grid(lines, left, fund_top, plot_w, fund_h, [0, 0.004, 0.008, 0.012], fund_min, fund_max, lambda v: f"{v:.3f}%")
    x_ticks(lines, rows, left, fund_top, plot_w, fund_h)
    lines.append(f'<text x="{left + 12}" y="{p_top + 24}" class="label">BTC-USD close</text>')
    lines.append(f'<text x="{left + 12}" y="{oi_top + 24}" class="label">OKX BTC-USDT-SWAP open interest · US$ billions</text>')
    lines.append(f'<text x="{left + 12}" y="{fund_top + 24}" class="label">OKX realized funding · average per 8 hours</text>')
    price_points, oi_points = [], []
    zero = y_pos(0, fund_min, fund_max, fund_top, fund_h)
    for i, row in enumerate(rows):
        xx = x_pos(i, len(rows), left, plot_w)
        price_points.append((xx, y_pos(float(row["btc_close"]), p_min, p_max, p_top, p_h)))
        oi_points.append((xx, y_pos(float(row["okx_oi_usd_b"]), oi_min, oi_max, oi_top, oi_h)))
        fund = float(row["okx_funding_avg_pct_8h"])
        fy = y_pos(fund, fund_min, fund_max, fund_top, fund_h)
        bar_w = min(58, plot_w / len(rows) * 0.56)
        color = ACCENT if fund >= 0 else RED
        lines.append(f'<rect x="{xx - bar_w / 2:.1f}" y="{min(fy, zero):.1f}" width="{bar_w:.1f}" height="{max(abs(zero - fy), 2):.1f}" fill="{color}" opacity="0.88" rx="3"/>')
        lines.append(f'<text x="{xx:.1f}" y="{fy - 8 if fund >= 0 else fy + 16:.1f}" class="note" text-anchor="middle">{fund:.3f}%</text>')
    lines.append(line(price_points, CYAN, 3))
    lines.append(line(oi_points, GREEN, 3))
    for xx, yy in price_points:
        lines.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="3.5" fill="{CYAN}"/>')
    for xx, yy in oi_points:
        lines.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="3.5" fill="{GREEN}"/>')
    i = next(j for j, row in enumerate(rows) if row["date"] == "2026-09-24")
    xx = x_pos(i, len(rows), left, plot_w)
    lines.append(f'<line x1="{xx:.1f}" y1="{p_top:.1f}" x2="{xx:.1f}" y2="{fund_top + fund_h:.1f}" stroke="{RED}" stroke-width="1.5" stroke-dasharray="4 5"/>')
    lines.append(f'<text x="{xx - 10:.1f}" y="{p_top + 42:.1f}" class="label" text-anchor="end" fill="{RED}">24 Sep $82.7k test</text>')
    lines.append(f'<text x="{left + 10:.1f}" y="{height - 49}" class="note">OKX OI: $2.66B on 20 Sep → $2.40B on 25 Sep; still above $2.14B on 15 Sep.</text>')
    lines.append(f'<text x="{left + 10:.1f}" y="{height - 28}" class="note">Funding cooled to 0.0010% average on 24 Sep, with brief negative 8-hour prints; this is not a market-wide total.</text>')
    lines.append(f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Sources: Coinbase Exchange + OKX public APIs · {esc(RETRIEVED)}</text>')
    lines.append("</svg>")
    return "\n".join(lines)


def main() -> None:
    rows = read_rows()
    OUT.mkdir(parents=True, exist_ok=True)
    outputs = {
        "chart-btc-87k-rejection-price.svg": chart_price(rows),
        "chart-btc-87k-rejection-flows.svg": chart_flows(rows),
        "chart-btc-87k-rejection-leverage.svg": chart_leverage(rows),
    }
    for name, content in outputs.items():
        path = OUT / name
        path.write_text(content + "\n")
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
