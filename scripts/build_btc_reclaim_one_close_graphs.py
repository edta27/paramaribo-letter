#!/usr/bin/env python3
"""Build the publication charts for Paramaribo Letter Issue 33.

Reads the frozen Coinbase and cross-asset tables in research/. Does not fetch.
"""

from __future__ import annotations

import csv
import html
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAILY = ROOT / "research" / "btc-reclaim-one-close-2026-11-06.csv"
HOURLY = ROOT / "research" / "btc-nov4-5-2026-hourly.csv"
CROSS = ROOT / "research" / "cross-asset-nov5-2026.csv"
OUT = ROOT / "public" / "images"
PACK = ROOT / "public" / "charts" / "packs" / "2026-11-06-the-reclaim-lasted-one-close.json"
CATALOG = ROOT / "public" / "charts" / "catalog.json"
RETRIEVED = "6 Nov 2026 · 8:27 a.m. CT / 14:27 UTC"

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


def chart_hourly(rows: list[dict]) -> str:
    width, height = 1200, 720
    left, top, plot_w, plot_h = 94, 108, 1015, 490
    y_min, y_max = 74_200, 82_400
    lines = start(
        width,
        height,
        "One close above $80k. The next day gave it back.",
        "Hourly Coinbase BTC-USD candles for 4 and 5 November 2026. The 4 November low is $75,600.64 at 03:00 UTC. The 15:00 UTC hour reclaims $80,000. The 5 November 15:00 UTC hour loses it.",
        "Coinbase hourly UTC candles · 4–5 Nov 2026 · 4 Nov close $80,428 · 5 Nov close $75,969",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [75_035, 77_000, 80_000], y_min, y_max, lambda v: f"${v / 1000:.1f}k")
    for level, label, color in [(80_000, "$80k", YELLOW), (77_000, "$77k", RED)]:
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
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">4 Nov 03:00 UTC low $75,600.64. 4 Nov 15:00 UTC high $81,130.79, close $80,214. 5 Nov 15:00 UTC low $75,431. Daily close $75,969. $74,000 was not tagged.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Source: Coinbase Exchange BTC-USD · retrieved {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def chart_path(rows: list[dict]) -> str:
    width, height = 1200, 740
    left, top, plot_w, plot_h = 94, 108, 1015, 510
    y_min, y_max = 73_500, 88_000
    lines = start(
        width,
        height,
        "The window closed. One later close did not reopen it.",
        "Daily Coinbase BTC-USD candles from 15 October through 5 November 2026. 30 and 31 October close under $80,000. 4 November closes $80,428. 5 November closes $75,969.",
        "Coinbase daily UTC candles · 15 Oct–5 Nov 2026 · 6 Nov is partial and is not plotted",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [75_969, 80_000, 84_856], y_min, y_max, lambda v: f"${v / 1000:.1f}k")
    for level, label, color in [(86_000, "$86k", CYAN), (80_000, "$80k", YELLOW), (77_000, "$77k", RED)]:
        yy = y_pos(level, y_min, y_max, top, plot_h)
        lines.append(
            f'<line x1="{left:.1f}" y1="{yy:.1f}" x2="{left + plot_w:.1f}" y2="{yy:.1f}" stroke="{color}" stroke-width="1.4" stroke-dasharray="7 5"/>'
        )
        lines.append(f'<text x="{left + plot_w + 8:.1f}" y="{yy + 4:.1f}" class="label" fill="{color}">{label}</text>')
    shown = [row for row in rows if str(row["date"]) >= "2026-10-15"]
    candle_w = 22
    for i, row in enumerate(shown):
        xx = x_pos(i, len(shown), left, plot_w)
        op, hi, lo, cl = float(row["btc_open"]), float(row["btc_high"]), float(row["btc_low"]), float(row["btc_close"])
        color = GREEN if cl >= op else RED
        yl, yh = y_pos(lo, y_min, y_max, top, plot_h), y_pos(hi, y_min, y_max, top, plot_h)
        yo, yc = y_pos(op, y_min, y_max, top, plot_h), y_pos(cl, y_min, y_max, top, plot_h)
        lines.append(f'<line x1="{xx:.1f}" y1="{yh:.1f}" x2="{xx:.1f}" y2="{yl:.1f}" stroke="{color}" stroke-width="1.6"/>')
        lines.append(
            f'<rect x="{xx - candle_w / 2:.1f}" y="{min(yo, yc):.1f}" width="{candle_w}" height="{max(abs(yc - yo), 2.5):.1f}" fill="{color}" opacity="0.92" stroke="{color}"/>'
        )
        day = str(row["date"])[5:]
        if day in {"10-15", "10-22", "10-29", "10-31", "11-02", "11-04", "11-05"}:
            lines.append(f'<text x="{xx:.1f}" y="{top + plot_h + 24:.1f}" class="axis" text-anchor="middle">{day}</text>')
    lines.append(
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">30 Oct close $77,180. 31 Oct close $77,424. 2 Nov close $76,674. 4 Nov close $80,428. 5 Nov close $75,969, low $75,035. No close above $86k since 4 Oct.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Source: Coinbase Exchange BTC-USD · retrieved {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def chart_cross(rows: list[dict]) -> str:
    width, height = 1200, 720
    left, top, plot_w, plot_h = 168, 118, 900, 470
    y_min, y_max = -14.0, 6.0
    lines = start(
        width,
        height,
        "5 November: equities traveled. Oil did not.",
        "Percent change from the 4 November close to the 5 November close. Bitcoin is Coinbase. The others are Yahoo cash or futures closes. VIX is not plotted as a return.",
        "Completed 5 Nov 2026 closes versus 4 Nov · VIX cash close 16.61 to 28.18, not shown as a percent",
    )
    panel(lines, left, top, plot_w, plot_h)
    grid(lines, left, top, plot_w, plot_h, [-12, -6, 0, 4], y_min, y_max, lambda v: f"{v:.0f}%")
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
        f'<text x="{left + 10:.1f}" y="{height - 47}" class="note">SOXX is Yahoo’s split-adjusted series. A 3-for-1 split took effect at the 5 November open, so the raw level is not Issue 32’s $513.86. January Brent is BZF27, the same contract.</text>'
    )
    lines.append(
        f'<text x="{left + plot_w:.1f}" y="{height - 22}" class="note" text-anchor="end">Sources: Coinbase Exchange and Yahoo Finance · {esc(RETRIEVED)}</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def ms(iso: str) -> int:
    return int(datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp() * 1000)


def write_pack(daily: list[dict], hourly: list[dict], cross: list[dict]) -> None:
    shown = [row for row in daily if str(row["date"]) >= "2026-10-15"]

    def series(rows, time_key, value_key):
        out = []
        for row in rows:
            value = row[value_key]
            out.append([ms(str(row[time_key])), None if value is None else round(float(value), 2)])
        return out

    pack = {
        "id": "2026-11-06-the-reclaim-lasted-one-close",
        "date": "2026-11-06",
        "kicker": "Chart Desk · Issue 33",
        "title": "The reclaim lasted one close.",
        "dek": "The 48-hour test of $80,000 failed. 4 November closed at $80,428. 5 November closed at $75,969, and equities traveled with it.",
        "asOf": "2026-11-06T14:27:47Z",
        "cadence": "follow-up",
        "thesis": "The reclaim lasted one close.",
        "stakes": "BTC ~$75.6k. 4 Nov close $80,428 did not hold. 5 Nov close $75,969. VIX cash close 28.18. The new 48-hour test of $77k is open. WAIT.",
        "levels": ["$86k", "$80k", "$77k", "$74–76k", "$72k", "~$57.7k"],
        "letterId": "2026-11-06-the-reclaim-lasted-one-close",
        "letterUrl": "/issue?id=2026-11-06-the-reclaim-lasted-one-close",
        "letterLabel": "Vol. 1 · Issue 33",
        "subscribeHook": "A UTC close back above $77k on 6 or 7 November, or a completed close through $74k, updates the sequence. Charts stay free here; the call moves by email.",
        "sourceNote": "Issue 33 charts use Coinbase Exchange UTC candles (hourly 4–5 Nov 2026; daily 15 Oct–5 Nov) and completed 4–5 November closes from Yahoo Finance for the S&P 500, Nasdaq, Dow, Invesco RSP, SOXX, HYG, January Brent BZF27, and gold futures. 6 November is a partial UTC day and is not plotted. Farside ETF flows were not retrieved. Educational scenario research; no leverage.",
        "briefs": [
            {
                "id": "btc-reclaim-hours",
                "asset": "BTC · 4–5 NOV 2026",
                "headline": "One close above $80k. The next day gave it back.",
                "lede": "The 4 November low was $75,600.64 at 03:00 UTC. The 15:00 UTC hour reclaimed $80k. The 5 November close was $75,969.",
                "bodyHtml": "<p><strong>Fact.</strong> $80,000 was reclaimed on the 4 November UTC close and lost on the 5 November UTC close.</p><p><strong>Read.</strong> One close is not acceptance. The new 48-hour test of $77,000 was still open at the freeze.</p>",
                "charts": [
                    {
                        "title": "BTC hourly range [USD] vs close · 4–5 Nov 2026",
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
                "id": "btc-reclaim-path",
                "asset": "BTC",
                "headline": "The window closed. One later close did not reopen it.",
                "lede": "30 and 31 October both closed under $80,000. 4 November closed at $80,428. 5 November closed at $75,969.",
                "bodyHtml": "<p><strong>Fact.</strong> The 48-hour reclaim Issue 32 was watching did not print. A later one-day close above $80,000 did not hold.</p><p><strong>Read.</strong> $77,000 has a new close through it. That window runs through the 7 November UTC close.</p>",
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
                                for row in shown
                            ],
                        },
                        "line": {
                            "label": "BTC-USD close [USD]",
                            "data": series(
                                [{**row, "time": str(row["date"]) + "T00:00:00+00:00"} for row in shown],
                                "time",
                                "btc_close",
                            ),
                        },
                    }
                ],
            },
            {
                "id": "btc-reclaim-cross",
                "asset": "CROSS-ASSET · 5 NOV",
                "headline": "Equities traveled. Oil did not.",
                "lede": "From the 4 November close to the 5 November close, the S&P 500 fell 4.4% and Bitcoin fell 5.5%. January Brent rose 3.9%.",
                "bodyHtml": "<p><strong>Fact.</strong> The S&amp;P 500, the Nasdaq, the Dow, and equal-weight equities all closed lower. January Brent and gold closed higher.</p><p><strong>Read.</strong> That is transmission in equities and volatility. It is not yet a full panic cluster. Credit spreads were not retrieved.</p>",
                "charts": [
                    {
                        "title": "4 Nov close to 5 Nov close [%]",
                        "bars": {
                            "label": "Change from the 4 Nov close to the 5 Nov close [%]",
                            "data": [
                                [ms("2026-11-05T00:00:00+00:00") + i, round(float(row["change_pct"]), 2)]
                                for i, row in enumerate(cross)
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
    public["packUrl"] = "/charts/packs/2026-11-06-the-reclaim-lasted-one-close.json"
    catalog.insert(0, public)
    CATALOG.write_text(json.dumps(catalog, indent=2) + "\n")
    print(f"wrote {PACK.relative_to(ROOT)}")


def main() -> None:
    daily = read_csv(DAILY)
    hourly = read_csv(HOURLY)
    cross = read_csv(CROSS)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "chart-btc-reclaim-hours.svg").write_text(chart_hourly(hourly))
    (OUT / "chart-btc-reclaim-path.svg").write_text(chart_path(daily))
    (OUT / "chart-btc-reclaim-cross.svg").write_text(chart_cross(cross))
    write_pack(daily, hourly, cross)
    print("wrote three svgs")


if __name__ == "__main__":
    main()
