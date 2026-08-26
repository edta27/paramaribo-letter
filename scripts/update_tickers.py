#!/usr/bin/env python3
"""Refresh every watchlist ticker: last quote + recent SEC filings. No trades, no email."""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
WATCHLIST = ROOT / "vault" / "watchlist.md"
TICKER_DIR = ROOT / "vault" / "tickers"
LIVE_DIR = ROOT / "vault" / "live"
CIK_CACHE = ROOT / "vault" / "cik-map.json"
DESK_JS_PATHS = (
    ROOT / "desk" / "live.js",
    ROOT / "public" / "desk" / "live.js",
)
YAHOO_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
SEC_UA = "Investment Research educational AdminContact@example.com"
YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=5d"
NASDAQ = "https://api.nasdaq.com/api/quote/{ticker}/info?assetclass={asset}"
SEC_TICKERS = "https://www.sec.gov/files/company_tickers.json"
SEC_SUBS = "https://data.sec.gov/submissions/CIK{cik}.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


TICKER_RE = re.compile(r"^[A-Z]{1,5}(?:[.-][A-Z]{1,3})?$")


def load_watchlist() -> list[str]:
    names: list[str] = []
    for line in WATCHLIST.read_text().splitlines():
        line = line.strip().split("#")[0].strip()
        if not line:
            continue
        token = line.upper()
        if not TICKER_RE.match(token):
            continue
        if token not in names:
            names.append(token)
    return names


def get_json(url: str, timeout: float = 20.0, user_agent: str = YAHOO_UA) -> dict:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": user_agent, "Accept": "application/json"},
    )
    last_err: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            last_err = exc
            if exc.code == 429:
                time.sleep(8 * (attempt + 1))
            elif exc.code in {401, 403, 404}:
                raise
            else:
                time.sleep(0.6 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_err = exc
            time.sleep(0.6 * (attempt + 1))
    raise last_err  # type: ignore[misc]


def parse_number(text) -> float | None:
    if text is None:
        return None
    s = str(text).replace("$", "").replace(",", "").replace("%", "").replace("+", "").strip()
    if not s or s in {"N/A", "UNCH", "--"}:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def recent_filing(date_str: str | None, days: int = 21) -> bool:
    if not date_str:
        return False
    try:
        filed = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return False
    return datetime.now(timezone.utc) - filed <= timedelta(days=days)


def quote_from_chart(ticker: str) -> dict:
    data = get_json(YAHOO.format(ticker=ticker), user_agent=YAHOO_UA)
    result = (data.get("chart") or {}).get("result") or [None]
    row = result[0] or {}
    meta = row.get("meta") or {}
    return normalize_quote(
        ticker,
        meta.get("regularMarketPrice"),
        meta.get("chartPreviousClose") or meta.get("previousClose"),
        meta.get("currency"),
        meta.get("exchangeName"),
        meta.get("regularMarketVolume"),
        "yahoo-v8",
    )


def normalize_quote(
    ticker: str,
    price,
    prev,
    currency,
    exchange,
    volume,
    source: str,
) -> dict:
    change = None
    change_pct = None
    if price is not None and prev:
        change = round(price - prev, 4)
        change_pct = round(100.0 * (price - prev) / prev, 3)
    return {
        "ticker": ticker,
        "price": price,
        "prev_close": prev,
        "change": change,
        "change_pct": change_pct,
        "currency": currency,
        "exchange": exchange,
        "volume": volume,
        "quote_source": source,
    }


def quote_nasdaq(ticker: str) -> dict:
    last_err: Exception | None = None
    for asset in ("stocks", "etf"):
        try:
            data = get_json(NASDAQ.format(ticker=ticker, asset=asset), user_agent=YAHOO_UA)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError) as exc:
            last_err = exc
            continue
        payload = data.get("data") or {}
        primary = payload.get("primaryData") or {}
        price = parse_number(primary.get("lastSalePrice"))
        if price is None:
            continue
        change = parse_number(primary.get("netChange"))
        change_pct = parse_number(primary.get("percentageChange"))
        prev = None
        if change is not None:
            prev = round(price - change, 4)
        return normalize_quote(
            ticker,
            price,
            prev,
            "USD",
            payload.get("exchange"),
            parse_number(primary.get("volume")),
            f"nasdaq-{asset}",
        )
    if last_err:
        raise last_err
    raise KeyError(f"no nasdaq quote for {ticker}")


def quotes_batch(tickers: list[str]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for ticker in tickers:
        try:
            out[ticker] = quote_nasdaq(ticker)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError, TypeError):
            try:
                out[ticker] = quote_from_chart(ticker)
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError, TypeError):
                continue
        time.sleep(0.25)
    return out


def load_cik_cache() -> dict[str, str]:
    if not CIK_CACHE.exists():
        return {}
    try:
        raw = json.loads(CIK_CACHE.read_text())
    except json.JSONDecodeError:
        return {}
    out: dict[str, str] = {}
    for ticker, cik in raw.items():
        token = str(ticker).upper()
        padded = str(cik).zfill(10)
        if TICKER_RE.match(token) and padded != "0000000000":
            out[token] = padded
    return out


def save_cik_cache(ciks: dict[str, str]) -> None:
    merged = load_cik_cache()
    merged.update(ciks)
    CIK_CACHE.write_text(json.dumps(dict(sorted(merged.items())), indent=2) + "\n")


def cik_map(needed: list[str]) -> dict[str, str]:
    out = load_cik_cache()
    missing = [t for t in needed if t not in out]
    if not missing:
        print(f"using cached CIKs for {len(needed)} tickers", flush=True)
        return out
    print(
        f"SEC company list needed for {', '.join(missing)} (can take ~20s)…",
        flush=True,
    )
    raw = get_json(SEC_TICKERS, user_agent=SEC_UA, timeout=12.0)
    for rec in raw.values():
        ticker = str(rec.get("ticker") or "").upper()
        cik = str(rec.get("cik_str") or "").zfill(10)
        if ticker and cik != "0000000000":
            out[ticker] = cik
    save_cik_cache({t: out[t] for t in needed if t in out})
    still = [t for t in needed if t not in out]
    if still:
        print(f"no CIK for {', '.join(still)}; those names skip EDGAR", flush=True)
    return out


def filings(ticker: str, cik: str | None) -> list[dict]:
    if not cik:
        return []
    data = get_json(SEC_SUBS.format(cik=cik), user_agent=SEC_UA)
    recent = (data.get("filings") or {}).get("recent") or {}
    forms = recent.get("form") or []
    dates = recent.get("filingDate") or []
    acc = recent.get("accessionNumber") or []
    docs = recent.get("primaryDocument") or []
    keep = {"8-K", "8-K/A", "10-K", "10-Q", "10-K/A", "10-Q/A", "6-K", "20-F", "4", "4/A", "13F-HR"}
    rows: list[dict] = []
    for i, form in enumerate(forms):
        if form not in keep:
            continue
        accession = acc[i].replace("-", "") if i < len(acc) else ""
        doc = docs[i] if i < len(docs) else ""
        url = ""
        if accession and doc:
            url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession}/{doc}"
        rows.append(
            {
                "form": form,
                "filing_date": dates[i] if i < len(dates) else None,
                "accession": acc[i] if i < len(acc) else None,
                "url": url,
            }
        )
        if len(rows) >= 5:
            break
    return rows


def flags_for(row: dict) -> list[dict]:
    out: list[dict] = []
    ticker = row["ticker"]
    pct = row.get("change_pct")
    if pct is None:
        out.append(
            {
                "ticker": ticker,
                "lane": "quotes",
                "tag": "BIN",
                "text": "quote missing",
                "severity": 2,
            }
        )
    else:
        tag = "BEAT" if pct >= 0 else "FLAG"
        if abs(pct) >= 5:
            tag = "ALPHA" if pct > 0 else "FLAG"
        out.append(
            {
                "ticker": ticker,
                "lane": "quotes",
                "tag": tag,
                "text": f"{row['price']} ({pct:+.2f}%)",
                "severity": 4 if abs(pct) >= 5 else 2,
            }
        )
    for item in row.get("filings") or []:
        if not recent_filing(item.get("filing_date")):
            continue
        form = item.get("form") or ""
        tag = "FLAG"
        if form.startswith("4"):
            tag = "ALPHA"
        elif form.startswith("13F"):
            tag = "13F"
        out.append(
            {
                "ticker": ticker,
                "lane": "filings",
                "tag": tag,
                "text": f"{form} {item.get('filing_date') or ''}".strip(),
                "severity": 3,
                "url": item.get("url"),
            }
        )
    return out


def refresh_once(ciks: dict[str, str]) -> dict:
    tickers = load_watchlist()
    rows: list[dict] = []
    errors = 0
    filing_count = 0
    TICKER_DIR.mkdir(parents=True, exist_ok=True)
    LIVE_DIR.mkdir(parents=True, exist_ok=True)
    quotes = quotes_batch(tickers)
    for i, ticker in enumerate(tickers):
        rec: dict = {
            "ticker": ticker,
            "updated_at": utc_now(),
            "price": None,
            "filings": [],
            "error": None,
        }
        q = quotes.get(ticker)
        if q and q.get("price") is not None:
            rec.update(q)
        else:
            rec["error"] = "quote missing"
            errors += 1
        try:
            got = filings(ticker, ciks.get(ticker))
            rec["filings"] = got
            filing_count += len(got)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError) as exc:
            rec["error"] = ((rec.get("error") or "") + f" filings: {exc}").strip()
            errors += 1
        time.sleep(0.2)
        (TICKER_DIR / f"{ticker}.json").write_text(json.dumps(rec, indent=2) + "\n")
        rows.append(rec)
        print(
            f"[{i + 1}/{len(tickers)}] {ticker} {rec.get('price')} {rec.get('change_pct')}",
            flush=True,
        )

    flag_rows: list[dict] = []
    for rec in rows:
        flag_rows.extend(flags_for(rec))

    snapshot = {
        "updated_at": utc_now(),
        "mode": "auto-refresh",
        "disclaimer": "Educational quotes and EDGAR indexes only. Not advice. No trades. No email.",
        "watchlist": tickers,
        "tickers": rows,
        "flags": flag_rows,
        "stats": {
            "tickers": len(tickers),
            "ok_quotes": sum(1 for r in rows if r.get("price") is not None),
            "filings_read": filing_count,
            "errors": errors,
        },
    }
    (LIVE_DIR / "snapshot.json").write_text(json.dumps(snapshot, indent=2) + "\n")
    live_js = "window.DESK_LIVE = " + json.dumps(snapshot) + ";\n"
    for path in DESK_JS_PATHS:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(live_js)
    return snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description="Update each equity-desk ticker")
    parser.add_argument("--loop", type=int, default=0, help="Repeat every N seconds (0 = once)")
    args = parser.parse_args()
    tickers = load_watchlist()
    if not tickers:
        print("no tickers in vault/watchlist.md", flush=True)
        return 1
    print(f"watchlist {len(tickers)} names", flush=True)
    try:
        ciks = cik_map(tickers)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"SEC ticker map unavailable ({exc}); quotes only this run", flush=True)
        ciks = load_cik_cache()
    while True:
        snap = refresh_once(ciks)
        stats = snap["stats"]
        print(
            f"done {snap['updated_at']} quotes={stats['ok_quotes']}/{stats['tickers']} "
            f"filings={stats['filings_read']} errors={stats['errors']}",
            flush=True,
        )
        if not args.loop:
            return 0 if stats["ok_quotes"] or stats["filings_read"] else 1
        print(f"next refresh in {args.loop}s — leave this terminal open, Ctrl+C to stop", flush=True)
        time.sleep(args.loop)


if __name__ == "__main__":
    raise SystemExit(main())
