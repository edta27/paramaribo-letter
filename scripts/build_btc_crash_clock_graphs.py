#!/usr/bin/env python3
"""Build the publication charts for Paramaribo Letter Issue 28."""

from __future__ import annotations

import csv
import html
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WICK = ROOT / "research" / "btc-oct10-2025-5m.csv"
MONTH = ROOT / "research" / "btc-oct2025-daily.csv"
NOW = ROOT / "research" / "btc-crash-clock-freeze-2026-09-30.csv"
OUT = ROOT / "public" / "images"
RETRIEVED = "30 Sep 2026 · 1:45 a.m. CDT / 06:45 UTC"

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


def grid(
    lines: list[str],
    left: float,
    top: float,
    width: float,
    height: float,
    ticks: list[float],
    y_min: float,
    y_max: float,
    fmt,
) -> None:
    for tick in ticks:
        yy = y_pos(tick, y_min, y_max, top, height)
        lines.append(
            f'<line x1="{left:.1f}" y1="{yy:.1f}" x2="{left + width:.1f}" y2="{yy:.1f}" stroke="{GRID}"/>'
        )
        lines.append(
            f'<text x="{left - 12:.1f}" y="{yy + 4:.1f}" class="axis" text-anchor="end">{esc(fmt(tick))}</text>'
        )


def line(points: list[tuple[float, float]], color: str, width: float = 2.5, dash: str = "") -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    coords = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return (
        f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{width}" '
        f'stroke-linejoin="round" stroke-linecap="round"{dash_attr}/>'
    )


def chart_wick(rows: list[dict]) -> str:
    width, height = 1200, 720
    left, top, plot_w, plot_h = 94, 108, 1015, 490
    y_min, y_max = 105_000, 118_000
    lines = start(
        width,
        height,
        "The daily candle hid a ten-minute hole",
        "Coinbase BTC-USD five-minute candles from 20:50 to 21:55 UTC on 10 October 2025. Price drops from about $116,900 to a $107,000 print, then recovers toward $114,000 inside the same hour.",
        "Coinbase 5-minute UTC candles · 10 Oct 2025 · 20:50–21:55 · the $107,000 print is one one-minute tick",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [107_000, 110_000, 113_000, 116_000], y_min, y_max, lambda v: f"${v / 1000:.0f}k")
    labels = ["20:50", "20:55", "21:00", "21:05", "21:10", "21:15", "21:20", "21:25", "21:30", "21:35", "21:40", "21:45", "21:50", "21:55"]
    candle_w = 42
    close_pts = []
    for i, row in enumerate(rows):
        xx = x_pos(i, len(rows), left, plot_w)
        op, hi, lo, cl = float(row["open"]), float(row["high"]), float(row["low"]), float(row["close"])
        color = GREEN if cl >= op else RED
        yl, yh = y_pos(lo, y_min, y_max, top, plot_h), y_pos(hi, y_min, y_max, top, plot_h)
        yo, yc = y_pos(op, y_min, y_max, top, plot_h), y_pos(cl, y_min, y_max, top, plot_h)
        lines.append(f'<line x1="{xx:.1f}" y1="{yh:.1f}" x2="{xx:.1f}" y2="{yl:.1f}" stroke="{color}" stroke-width="2"/>')
        lines.append(
            f'<rect x="{xx - candle_w / 2:.1f}" y="{min(yo, yc):.1f}" width="{candle_w}" height="{max(abs(yc - yo), 3):.1f}" fill="{color}" opacity="0.92" stroke="{color}"/>'
        )
        close_pts.append((xx, yc))
        lines.append(f'<text x="{xx:.1f}" y="{top + plot_h + 24:.1f}" class="axis" text-anchor="middle">{labels[i]}</text>')
    yy107 = y_pos(107_000, y_min, y_max, top, plot_h)
    lines.append(
        f'<line x1="{left:.1f}" y1="{yy107:.1f}" x2="{left + plot_w:.1f}" y2="{yy107:.1f}" stroke="{RED}" stroke-width="1.5" stroke-dasharray="6 5"/>'
    )
    i_low = 7  # 21:25 bar contains 21:26 $107,000
    xx = x_pos(i_low, len(rows), left, plot_w)
    lines.append(f'<circle cx="{xx:.1f}" cy="{yy107:.1f}" r="6" fill="{BG}" stroke="{RED}" stroke-width="3"/>')
    lines.append(f'<text x="{xx + 12:.1f}" y="{yy107 - 12:.1f}" class="label" fill="{RED}">21:26 UTC · $107,000</text>')
    i_back = 8
    xxb = x_pos(i_back, len(rows), left, plot_w)
    yb = y_pos(114_480, y_min, y_max, top, plot_h)
    lines.append(f'<text x="{xxb + 8:.1f}" y="{yb - 8:.1f}" class="label" fill="{GREEN}">21:30 already ~$114k</text>')
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">Hour 21:00 UTC opened $114,324 and closed $113,875. The $107,000 Coinbase print lived inside that hour. Daily close: $112,980.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Source: Coinbase Exchange BTC-USD · retrieved {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def chart_month(rows: list[dict]) -> str:
    oct_rows = [r for r in rows if str(r["time"]).startswith("2025-10")]
    width, height = 1200, 740
    left, top, plot_w, plot_h = 94, 108, 1015, 500
    y_min, y_max = 100_000, 128_000
    lines = start(
        width,
        height,
        "October 2025 closed −4%. The month was not calm.",
        "Daily Coinbase BTC-USD candles for October 2025. The month opened near $114,000, peaked at $126,296 on 6 October, wicked to $107,000 on 10 October, printed a $103,517 low on 17 October, and closed 31 October at $109,555.",
        "Coinbase daily UTC candles · October 2025 · monthly close versus intra-month low",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [103_500, 110_000, 114_000, 120_000, 126_000], y_min, y_max, lambda v: f"${v / 1000:.0f}k")
    for level, label, color in [(114_068, "Sep 30 close", MUTE), (109_555, "Oct 31 close", CYAN), (103_517, "Oct 17 low", RED)]:
        yy = y_pos(level, y_min, y_max, top, plot_h)
        lines.append(
            f'<line x1="{left:.1f}" y1="{yy:.1f}" x2="{left + plot_w:.1f}" y2="{yy:.1f}" stroke="{color}" stroke-width="1.4" stroke-dasharray="6 5"/>'
        )
        lines.append(f'<text x="{left + plot_w + 8:.1f}" y="{yy + 4:.1f}" class="label" fill="{color}">{label}</text>')
    candle_w = 22
    for i, row in enumerate(oct_rows):
        xx = x_pos(i, len(oct_rows), left, plot_w)
        op, hi, lo, cl = float(row["open"]), float(row["high"]), float(row["low"]), float(row["close"])
        color = GREEN if cl >= op else RED
        yl, yh = y_pos(lo, y_min, y_max, top, plot_h), y_pos(hi, y_min, y_max, top, plot_h)
        yo, yc = y_pos(op, y_min, y_max, top, plot_h), y_pos(cl, y_min, y_max, top, plot_h)
        lines.append(f'<line x1="{xx:.1f}" y1="{yh:.1f}" x2="{xx:.1f}" y2="{yl:.1f}" stroke="{color}" stroke-width="1.6"/>')
        lines.append(
            f'<rect x="{xx - candle_w / 2:.1f}" y="{min(yo, yc):.1f}" width="{candle_w}" height="{max(abs(yc - yo), 2.5):.1f}" fill="{color}" opacity="0.92" stroke="{color}"/>'
        )
        day = int(str(row["time"])[-2:])
        if day in {1, 6, 10, 17, 31}:
            lines.append(f'<text x="{xx:.1f}" y="{top + plot_h + 24:.1f}" class="axis" text-anchor="middle">{day}</text>')
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">Monthly return from the 30 Sep close ($114,068) to the 31 Oct close ($109,555): −4.0%. Peak-to-intramonth-low ($126,296 → $103,517): −18.0%.</text>'
    )
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 25}" class="note">10 Oct daily: O $121,715 · H $122,600 · L $107,000 · C $112,980. Volume 22,432 BTC, the month’s largest session.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Source: Coinbase Exchange BTC-USD · retrieved {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def chart_now(rows: list[dict]) -> str:
    width, height = 1200, 820
    left, plot_w = 94, 1015
    p_top, p_h = 108, 300
    f_top, f_h = 448, 250
    p_min, p_max = 72_000, 90_000
    f_min, f_max = -550, 1_100
    lines = start(
        width,
        height,
        "$82–83k was probed again. The ETF impulse faded.",
        "Daily Coinbase BTC-USD candles from 15 through 29 September 2026, with Farside US spot Bitcoin ETF net flows. The $87,397 high rejected; $82,510 printed on 28 September; ETF prints decelerated from +$999M to +$31M then +$66M.",
        "Coinbase daily UTC candles + Farside US-session ETF flows · last completed day is 29 Sep · 30 Sep is partial",
    )
    panel(lines, left, p_top, plot_w, p_h)
    panel(lines, left, f_top, plot_w, f_h)
    grid(lines, left, p_top, plot_w, p_h, [74_000, 77_000, 82_000, 86_000, 87_400], p_min, p_max, lambda v: f"${v / 1000:.0f}k")
    grid(lines, left, f_top, plot_w, f_h, [-500, 0, 500, 1_000], f_min, f_max, lambda v: f"${v / 1000:.1f}B" if abs(v) >= 1000 else f"${v:.0f}M")
    for level, label, color, dash in [
        (86_000, "$86k", CYAN, "7 5"),
        (82_000, "$82k", YELLOW, "7 5"),
        (77_000, "$77k", MUTE, "5 5"),
    ]:
        yy = y_pos(level, p_min, p_max, p_top, p_h)
        lines.append(
            f'<line x1="{left:.1f}" y1="{yy:.1f}" x2="{left + plot_w:.1f}" y2="{yy:.1f}" stroke="{color}" stroke-width="1.4" stroke-dasharray="{dash}"/>'
        )
        lines.append(f'<text x="{left + plot_w + 8:.1f}" y="{yy + 4:.1f}" class="label" fill="{color}">{label}</text>')
    candle_w = 28
    price_pts = []
    for i, row in enumerate(rows):
        xx = x_pos(i, len(rows), left, plot_w)
        op, hi, lo, cl = float(row["btc_open"]), float(row["btc_high"]), float(row["btc_low"]), float(row["btc_close"])
        color = GREEN if cl >= op else RED
        yl, yh = y_pos(lo, p_min, p_max, p_top, p_h), y_pos(hi, p_min, p_max, p_top, p_h)
        yo, yc = y_pos(op, p_min, p_max, p_top, p_h), y_pos(cl, p_min, p_max, p_top, p_h)
        lines.append(f'<line x1="{xx:.1f}" y1="{yh:.1f}" x2="{xx:.1f}" y2="{yl:.1f}" stroke="{color}" stroke-width="1.8"/>')
        lines.append(
            f'<rect x="{xx - candle_w / 2:.1f}" y="{min(yo, yc):.1f}" width="{candle_w}" height="{max(abs(yc - yo), 2.5):.1f}" fill="{color}" opacity="0.92" stroke="{color}"/>'
        )
        price_pts.append((xx, yc))
        flow = row["etf_flow_usd_m"]
        if flow is not None:
            zero_y = y_pos(0, f_min, f_max, f_top, f_h)
            bar_y = y_pos(float(flow), f_min, f_max, f_top, f_h)
            fcolor = GREEN if float(flow) >= 0 else RED
            bar_w = min(48, plot_w / len(rows) * 0.52)
            lines.append(
                f'<rect x="{xx - bar_w / 2:.1f}" y="{min(zero_y, bar_y):.1f}" width="{bar_w:.1f}" height="{max(abs(zero_y - bar_y), 2):.1f}" fill="{fcolor}" opacity="0.86" rx="3"/>'
            )
            lines.append(
                f'<text x="{xx:.1f}" y="{bar_y - 8 if float(flow) >= 0 else bar_y + 16:.1f}" class="note" text-anchor="middle">{float(flow):+.0f}</text>'
            )
        day = str(row["date"])[8:]
        if day in {"15", "21", "24", "28", "29"}:
            lines.append(f'<text x="{xx:.1f}" y="{f_top + f_h + 24:.1f}" class="axis" text-anchor="middle">{str(row["date"])[5:]}</text>')
    zero_y = y_pos(0, f_min, f_max, f_top, f_h)
    lines.append(f'<line x1="{left:.1f}" y1="{zero_y:.1f}" x2="{left + plot_w:.1f}" y2="{zero_y:.1f}" stroke="{MUTE}"/>')
    lines.append(f'<text x="{left + 12}" y="{p_top + 24}" class="label">BTC-USD daily range</text>')
    lines.append(f'<text x="{left + 12}" y="{f_top + 24}" class="label">Farside US spot BTC ETF net flow · US$ millions · weekend blanks are not zeroes</text>')
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">28 Sep low $82,510, close $83,457. 29 Sep low $82,736, close $83,638. No completed close above $86k since 22 Sep. No completed close below $82k.</text>'
    )
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 25}" class="note">ETF slope after 21 Sep: +$999M → +$715M → +$347M → +$191M → +$135M → +$31M → +$66M. Sign still green. Impulse gone.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Sources: Coinbase Exchange + Farside Investors · {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    outputs = {
        "chart-btc-crash-clock-wick.svg": chart_wick(read_csv(WICK)),
        "chart-btc-crash-clock-october.svg": chart_month(read_csv(MONTH)),
        "chart-btc-crash-clock-now.svg": chart_now(read_csv(NOW)),
    }
    for name, content in outputs.items():
        path = OUT / name
        path.write_text(content + "\n")
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
