#!/usr/bin/env python3
"""Build Emily's free, daily, evidence-based market snapshot.

The updater intentionally uses public endpoints that do not require API keys.
Required crypto inputs fail closed; optional cross-market inputs are reported as
missing and reduce the published data-quality grade instead of being scored as
benign.
"""

from __future__ import annotations

import csv
import html
import io
import json
import math
import os
import statistics
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
LIVE_PATH = PUBLIC / "emily-live.js"
HISTORY_PATH = PUBLIC / "emily-history.json"
USER_AGENT = "Paramaribo-Letter-Emily/1.0 (+https://www.paramariboletter.com/emily)"

STABLES = {
    "BUSD", "DAI", "FDUSD", "FRAX", "GUSD", "LUSD", "PYUSD", "RLUSD",
    "TUSD", "USD0", "USD1", "USDC", "USDD", "USDE", "USDG", "USDJ",
    "USDP", "USDS", "USDT", "USDY", "SUSDS",
}
DERIVATIVES = {
    "CBETH", "EZETH", "RETH", "SDAI", "STETH", "WBTC", "WEETH", "WETH",
    "WSTETH",
}


def fetch(
    url: str,
    *,
    timeout: int = 25,
    attempts: int = 3,
    headers: dict[str, str] | None = None,
) -> bytes:
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            request_headers = {
                "Accept": "application/json,text/csv,*/*",
                "User-Agent": USER_AGENT,
            }
            if headers:
                request_headers.update(headers)
            req = Request(url, headers=request_headers)
            with urlopen(req, timeout=timeout) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status} from {url}")
                return response.read()
        except (HTTPError, URLError, TimeoutError, OSError, RuntimeError) as exc:
            last = exc
            if attempt + 1 < attempts:
                time.sleep(1.25 * (attempt + 1))
    raise RuntimeError(f"Could not fetch {url}: {last}")


def get_json(url: str, *, headers: dict[str, str] | None = None) -> Any:
    try:
        return json.loads(fetch(url, headers=headers).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Invalid JSON from {url}: {exc}") from exc


def finite(value: Any) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("non-finite number")
    return number


def pct_change(current: float, previous: float) -> float | None:
    if previous == 0:
        return None
    return (current / previous - 1) * 100


def clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def threshold(value: float, levels: tuple[tuple[float, int], ...]) -> int:
    for minimum, points in levels:
        if value >= minimum:
            return points
    return 0


def last_history() -> dict[str, Any] | None:
    if not HISTORY_PATH.exists():
        return None
    try:
        rows = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
        return rows[-1] if isinstance(rows, list) and rows else None
    except (OSError, json.JSONDecodeError):
        return None


def save_history(row: dict[str, Any]) -> None:
    rows: list[dict[str, Any]] = []
    if HISTORY_PATH.exists():
        try:
            loaded = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
            if isinstance(loaded, list):
                rows = [item for item in loaded if isinstance(item, dict)]
        except (OSError, json.JSONDecodeError):
            rows = []
    # Manual verification runs should not create several observations for the
    # same day. Keep the latest successfully validated snapshot per UTC date.
    by_day: dict[str, dict[str, Any]] = {}
    for item in [*rows, row]:
        stamp = str(item.get("updated_at", ""))
        key = stamp[:10] if len(stamp) >= 10 else stamp
        if key:
            by_day[key] = item
    rows = sorted(by_day.values(), key=lambda item: str(item.get("updated_at", "")))[-180:]
    HISTORY_PATH.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def coinpaprika() -> dict[str, Any]:
    base = "https://api.coinpaprika.com/v1"
    global_data = get_json(f"{base}/global")
    tickers = get_json(f"{base}/tickers?quotes=USD")
    if not isinstance(global_data, dict) or not isinstance(tickers, list):
        raise RuntimeError("CoinPaprika returned an unexpected response")

    by_id = {row.get("id"): row for row in tickers if isinstance(row, dict)}
    btc = by_id.get("btc-bitcoin")
    eth = by_id.get("eth-ethereum")
    if not isinstance(btc, dict) or not isinstance(eth, dict):
        raise RuntimeError("Required BTC or ETH ticker is missing")

    def quote(row: dict[str, Any]) -> dict[str, float]:
        usd = row.get("quotes", {}).get("USD", {})
        return {
            "price": finite(usd["price"]),
            "change_24h": finite(usd["percent_change_24h"]),
            "change_7d": finite(usd["percent_change_7d"]),
            "market_cap": finite(usd["market_cap"]),
            "volume_24h": finite(usd["volume_24h"]),
        }

    btc_q = quote(btc)
    eth_q = quote(eth)
    eligible: list[dict[str, Any]] = []
    for row in tickers:
        if not isinstance(row, dict):
            continue
        try:
            rank = int(row.get("rank", 0))
            symbol = str(row.get("symbol", "")).upper()
            name = str(row.get("name", "")).lower()
            if not 1 <= rank <= 50 or row.get("id") == "btc-bitcoin":
                continue
            if symbol in STABLES or symbol in DERIVATIVES:
                continue
            if any(term in name for term in ("wrapped", "bridged", "staked ether", "liquid staking")):
                continue
            q = quote(row)
            if q["market_cap"] <= 0 or q["price"] <= 0:
                continue
            eligible.append({"symbol": symbol, "rank": rank, **q})
        except (KeyError, TypeError, ValueError):
            continue
    if len(eligible) < 10:
        raise RuntimeError("Too few valid large-cap altcoins for a breadth reading")

    excess = [row["change_7d"] - btc_q["change_7d"] for row in eligible]
    breadth = sum(item > 0 for item in excess) / len(excess) * 100
    median_excess = statistics.median(excess)
    eth_excess = eth_q["change_7d"] - btc_q["change_7d"]
    market_change = finite(global_data["market_cap_change_24h"])
    tone = (market_change + btc_q["change_24h"]) / 2
    dominance = finite(global_data["bitcoin_dominance_percentage"])
    market_cap = finite(global_data["market_cap_usd"])
    volume = finite(global_data["volume_24h_usd"])
    source_time = datetime.fromtimestamp(finite(global_data["last_updated"]), tz=timezone.utc)
    if datetime.now(timezone.utc) - source_time > timedelta(hours=3):
        raise RuntimeError("CoinPaprika global data is stale by more than three hours")

    return {
        "btc": btc_q,
        "eth": eth_q,
        "dominance": dominance,
        "market_cap": market_cap,
        "market_change_24h": market_change,
        "volume_24h": volume,
        "volume_to_cap": volume / market_cap * 100,
        "breadth": breadth,
        "median_excess": median_excess,
        "eth_excess": eth_excess,
        "tone": tone,
        "eligible_count": len(eligible),
        "source_updated_at": source_time.isoformat(),
    }


def fear_greed() -> dict[str, Any]:
    payload = get_json("https://api.alternative.me/fng/?limit=2&format=json")
    rows = payload.get("data", []) if isinstance(payload, dict) else []
    if not rows:
        raise RuntimeError("Fear and Greed history is empty")
    latest = rows[0]
    return {
        "value": int(latest["value"]),
        "classification": str(latest["value_classification"]),
        "timestamp": datetime.fromtimestamp(int(latest["timestamp"]), tz=timezone.utc).isoformat(),
    }


def okx_derivatives() -> dict[str, Any]:
    funding = get_json(
        "https://www.okx.com/api/v5/public/funding-rate-history?instId=BTC-USDT-SWAP&limit=6"
    )
    oi = get_json(
        "https://www.okx.com/api/v5/rubik/stat/contracts/open-interest-volume?ccy=BTC&period=1D"
    )
    funding_rows = funding.get("data", []) if isinstance(funding, dict) else []
    oi_rows = oi.get("data", []) if isinstance(oi, dict) else []
    if not funding_rows:
        raise RuntimeError("OKX funding history is empty")
    rates = [finite(row["fundingRate"]) * 100 for row in funding_rows[:3]]
    valid_oi = []
    for row in oi_rows:
        try:
            value = finite(row[1])
            if value > 0:
                valid_oi.append((int(row[0]), value))
        except (IndexError, TypeError, ValueError):
            continue
    oi_change = None
    oi_value = None
    oi_time = None
    if valid_oi:
        oi_time, oi_value = valid_oi[0]
        if len(valid_oi) >= 8:
            oi_change = pct_change(oi_value, valid_oi[7][1])
    return {
        "funding_8h_pct": statistics.mean(rates),
        "funding_timestamp": datetime.fromtimestamp(
            int(funding_rows[0]["fundingTime"]) / 1000, tz=timezone.utc
        ).isoformat(),
        "oi_usd": oi_value,
        "oi_change_7d_pct": oi_change,
        "oi_timestamp": (
            datetime.fromtimestamp(oi_time / 1000, tz=timezone.utc).isoformat()
            if oi_time else None
        ),
        "venue": "OKX BTC-USDT perpetual and OKX BTC aggregate",
    }


def cmc_json(path: str, api_key: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    query = f"?{urlencode(params)}" if params else ""
    payload = get_json(
        f"https://pro-api.coinmarketcap.com{path}{query}",
        headers={"X-CMC_PRO_API_KEY": api_key},
    )
    if not isinstance(payload, dict):
        raise RuntimeError("CoinMarketCap returned an unexpected response")
    status = payload.get("status", {})
    if isinstance(status, dict) and status.get("error_code") not in (None, 0, "0"):
        raise RuntimeError(f"CoinMarketCap error {status.get('error_code')}: {status.get('error_message')}")
    return payload


def coinmarketcap_derivatives(api_key: str) -> dict[str, Any]:
    """Fetch free, cross-venue derivatives and BTC liquidation observations.

    CoinMarketCap's exchange feed publishes market-wide USD open interest. Its
    BTC pair feed is still useful for funding and basis, but some Basic-plan
    responses omit converted pair-level open interest. Treat those as two
    different observations instead of manufacturing a BTC aggregate.
    """
    exchanges_payload = cmc_json(
        "/v5/exchange/derivatives/list",
        api_key,
        {"limit": 250, "convert": "USD"},
    )
    exchanges_data = exchanges_payload.get("data", {})
    exchanges = (
        exchanges_data.get("exchanges", [])
        if isinstance(exchanges_data, dict)
        else exchanges_data
    )
    if not isinstance(exchanges, list) or not exchanges:
        raise RuntimeError("CoinMarketCap returned no derivative exchanges")

    global_open_interest = 0.0
    exchange_count = 0
    latest_updates: list[str] = []
    for exchange in exchanges:
        if not isinstance(exchange, dict):
            continue
        quotes = exchange.get("quotes", [])
        if isinstance(quotes, dict):
            quotes = [quotes]
        usd_quote = next(
            (
                row for row in quotes
                if isinstance(row, dict)
                and (row.get("convert_symbol") == "USD" or row.get("symbol") == "USD")
            ),
            None,
        )
        if not usd_quote:
            continue
        raw_oi = usd_quote.get("open_interest_usd", usd_quote.get("open_interest"))
        try:
            oi = finite(raw_oi)
        except (TypeError, ValueError):
            continue
        if oi <= 0:
            continue
        global_open_interest += oi
        exchange_count += 1
        latest = usd_quote.get("last_updated") or exchange.get("last_updated")
        if latest:
            latest_updates.append(str(latest))

    if global_open_interest <= 0 or exchange_count == 0:
        raise RuntimeError("CoinMarketCap aggregate derivative open interest is unavailable")

    pairs_payload = cmc_json(
        "/v5/cryptocurrency/derivatives/market-pairs/list/latest",
        api_key,
        {"crypto_id": 1, "limit": 250, "category": "all", "convert": "USD"},
    )
    pairs_data = pairs_payload.get("data", {})
    pairs = pairs_data.get("market_pairs", []) if isinstance(pairs_data, dict) else []
    if not isinstance(pairs, list) or not pairs:
        raise RuntimeError("CoinMarketCap returned no BTC derivative market pairs")

    btc_open_interest = 0.0
    btc_oi_pairs = 0
    funding_weighted = 0.0
    funding_weight = 0.0
    basis_weighted = 0.0
    basis_weight = 0.0
    venues: set[str] = set()
    accepted_pairs = 0

    for pair in pairs:
        if not isinstance(pair, dict) or pair.get("outlier_detected") is True:
            continue
        quotes = pair.get("quotes", [])
        reported = pair.get("exchange_reported_quotes", [])
        usd_quote = next(
            (row for row in quotes if isinstance(row, dict) and row.get("symbol") == "USD"),
            None,
        )
        usd_reported = next(
            (row for row in reported if isinstance(row, dict) and row.get("symbol") == "USD"),
            None,
        )
        accepted_pairs += 1
        exchange = pair.get("exchange", {})
        if isinstance(exchange, dict) and exchange.get("exchange_name"):
            venues.add(str(exchange["exchange_name"]))
        latest = usd_quote.get("last_updated") if usd_quote else None
        if latest:
            latest_updates.append(str(latest))

        oi = None
        if usd_quote:
            try:
                candidate = finite(usd_quote.get("open_interest"))
                if candidate > 0:
                    oi = candidate
                    btc_open_interest += candidate
                    btc_oi_pairs += 1
            except (TypeError, ValueError):
                pass

        weight = oi
        if not isinstance(weight, (int, float)) and usd_quote:
            try:
                candidate = finite(usd_quote.get("volume_24h"))
                if candidate > 0:
                    weight = candidate
            except (TypeError, ValueError):
                pass
        if not isinstance(weight, (int, float)) or weight <= 0:
            weight = 1.0

        if usd_reported:
            try:
                funding = finite(usd_reported["funding_rate"])
                funding_weighted += funding * weight
                funding_weight += weight
            except (KeyError, TypeError, ValueError):
                pass
            try:
                basis = finite(usd_reported["index_basis"])
                basis_weighted += basis * weight
                basis_weight += weight
            except (KeyError, TypeError, ValueError):
                pass

    if accepted_pairs == 0:
        raise RuntimeError("CoinMarketCap BTC derivative market pairs are unavailable")

    global_liq_payload = cmc_json(
        "/v5/derivatives/liquidations/quotes/latest", api_key, {"convert": "USD"}
    )
    global_quotes = global_liq_payload.get("data", {}).get("quotes", [])
    global_liq = next(
        (row for row in global_quotes if isinstance(row, dict) and row.get("symbol") == "USD"),
        None,
    )
    if not global_liq:
        raise RuntimeError("CoinMarketCap global liquidations are unavailable")

    btc_liq_payload = cmc_json(
        "/v5/derivatives/liquidations/cryptocurrency/list/latest",
        api_key,
        {"crypto_id": 1, "limit": 1, "convert": "USD"},
    )
    cryptocurrencies = btc_liq_payload.get("data", {}).get("cryptocurrencies", [])
    btc_row = cryptocurrencies[0] if cryptocurrencies and isinstance(cryptocurrencies[0], dict) else None
    btc_quotes = btc_row.get("quotes", []) if btc_row else []
    btc_liq = next(
        (row for row in btc_quotes if isinstance(row, dict) and row.get("symbol") == "USD"),
        None,
    )
    if not btc_liq:
        raise RuntimeError("CoinMarketCap BTC liquidations are unavailable")

    return {
        "global_open_interest_usd": global_open_interest,
        "global_derivatives_venues": exchange_count,
        "btc_open_interest_usd": btc_open_interest if btc_oi_pairs else None,
        "btc_weighted_funding_pct": funding_weighted / funding_weight * 100 if funding_weight else None,
        "btc_weighted_basis_pct": basis_weighted / basis_weight * 100 if basis_weight else None,
        "btc_market_pairs": accepted_pairs,
        "btc_venues": len(venues),
        "global_liquidations_1h_usd": finite(global_liq["total_liquidations_1h"]),
        "global_liquidations_24h_usd": finite(global_liq["total_liquidations_24h"]),
        "global_long_liquidations_24h_usd": finite(global_liq["long_liquidations_24h"]),
        "global_short_liquidations_24h_usd": finite(global_liq["short_liquidations_24h"]),
        "btc_liquidations_1h_usd": finite(btc_liq["total_liquidations_1h"]),
        "btc_liquidations_24h_usd": finite(btc_liq["total_liquidations_24h"]),
        "btc_long_liquidations_24h_usd": finite(btc_liq["long_liquidations_24h"]),
        "btc_short_liquidations_24h_usd": finite(btc_liq["short_liquidations_24h"]),
        "updated_at": max(
            [*latest_updates, str(global_liq.get("last_updated", "")), str(btc_liq.get("last_updated", ""))]
        ),
        "source": "CoinMarketCap aggregated derivatives and liquidations",
    }


def stablecoins() -> dict[str, Any]:
    payload = get_json("https://stablecoins.llama.fi/stablecoins?includePrices=true")
    assets = payload.get("peggedAssets", []) if isinstance(payload, dict) else []
    current = 0.0
    prior = 0.0
    for asset in assets:
        if not isinstance(asset, dict) or asset.get("pegType") != "peggedUSD":
            continue
        try:
            current += finite(asset["circulating"]["peggedUSD"])
            prior += finite(asset["circulatingPrevWeek"]["peggedUSD"])
        except (KeyError, TypeError, ValueError):
            continue
    if current <= 0 or prior <= 0:
        raise RuntimeError("Stablecoin supply totals are unavailable")
    return {"supply_usd": current, "change_7d_pct": pct_change(current, prior)}


def fred_series(series_id: str) -> dict[str, Any]:
    start = (datetime.now(timezone.utc).date() - timedelta(days=45)).isoformat()
    query = urlencode({"id": series_id, "cosd": start})
    text = fetch(f"https://fred.stlouisfed.org/graph/fredgraph.csv?{query}").decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    values: list[tuple[str, float]] = []
    for row in reader:
        raw = row.get(series_id)
        if raw in (None, "", "."):
            continue
        try:
            values.append((str(row.get("observation_date") or row["DATE"]), finite(raw)))
        except (KeyError, ValueError):
            continue
    if not values:
        raise RuntimeError(f"FRED {series_id} has no recent values")
    previous = values[-6][1] if len(values) >= 6 else values[0][1]
    previous_three = values[-4][1] if len(values) >= 4 else values[0][1]
    window_high = max(value for _, value in values)
    window_low = min(value for _, value in values)
    return {
        "date": values[-1][0],
        "value": values[-1][1],
        "change_3obs_pct": pct_change(values[-1][1], previous_three),
        "change_3obs": values[-1][1] - previous_three,
        "change_5obs_pct": pct_change(values[-1][1], previous),
        "change_5obs": values[-1][1] - previous,
        "window_high": window_high,
        "window_low": window_low,
        "distance_from_window_high_pct": pct_change(values[-1][1], window_high),
        "observations": len(values),
    }


def rotation_score(market: dict[str, Any], previous: dict[str, Any] | None) -> tuple[int, str, str]:
    breadth_points = threshold(market["breadth"], ((70, 35), (55, 27), (40, 18), (25, 9)))
    median_points = threshold(market["median_excess"], ((8, 20), (4, 15), (0, 10), (-4, 5)))
    eth_points = threshold(market["eth_excess"], ((8, 20), (4, 15), (0, 10), (-4, 5)))
    tone_points = threshold(market["tone"], ((3, 10), (0, 7), (-3, 3)))

    dominance_change = None
    if previous and isinstance(previous.get("btc_dominance"), (int, float)):
        try:
            prior_time = datetime.fromisoformat(str(previous["updated_at"]).replace("Z", "+00:00"))
            age = datetime.now(timezone.utc) - prior_time.astimezone(timezone.utc)
            if timedelta(hours=18) <= age <= timedelta(hours=36):
                dominance_change = market["dominance"] - finite(previous["btc_dominance"])
        except (KeyError, TypeError, ValueError):
            dominance_change = None
    if dominance_change is not None:
        dominance_points = threshold(-dominance_change, ((2, 15), (1, 12), (0.5, 8), (-0.5, 4)))
        dominance_read = f"{dominance_change:+.2f} pp day over day"
    else:
        d = market["dominance"]
        dominance_points = 15 if d <= 45 else 12 if d <= 50 else 8 if d <= 55 else 4 if d <= 60 else 0
        dominance_read = "level proxy; daily direction is not yet available"
    score = breadth_points + median_points + eth_points + tone_points + dominance_points
    regime = (
        "Broad alt rotation" if score >= 80 else
        "Alt rotation building" if score >= 65 else
        "Rotation watch" if score >= 50 else
        "Bitcoin leadership" if score >= 30 else
        "Defensive / Bitcoin shelter"
    )
    return score, regime, dominance_read


def weighted_score(components: list[tuple[str, float, float]]) -> tuple[int, list[dict[str, Any]]]:
    usable = [(name, clamp(risk, 0, 1), weight) for name, risk, weight in components if risk is not None]
    total_weight = sum(weight for _, _, weight in usable)
    if total_weight < 60:
        raise RuntimeError(f"Only {total_weight:.0f}% of the panic model has usable evidence")
    score = round(sum(risk * weight for _, risk, weight in usable) / total_weight * 100)
    detail = [
        {"name": name, "risk": round(risk * 100), "weight": weight}
        for name, risk, weight in usable
    ]
    return score, detail


def equity_rates_divergence(macro: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    """Measure latent fragility when strong growth equities defy expensive money.

    This is not a sell signal and not evidence of active panic. It measures an
    unstable combination: a Nasdaq near its recent high, high or rising long
    yields, growth-stock leadership, and calm volatility or credit markets.
    """
    nasdaq = macro.get("nasdaq")
    ten_year = macro.get("ten_year")
    if not nasdaq or not ten_year:
        return None

    distance = nasdaq.get("distance_from_window_high_pct")
    proximity_risk = None
    if isinstance(distance, (int, float)):
        below_high = abs(min(0.0, distance))
        proximity_risk = (
            0.85 if below_high <= 0.25 else
            0.75 if below_high <= 1 else
            0.58 if below_high <= 3 else
            0.4 if below_high <= 6 else
            0.22
        )
    nasdaq_move = nasdaq.get("change_5obs_pct")
    momentum_risk = None
    if isinstance(nasdaq_move, (int, float)):
        momentum_risk = 0.8 if nasdaq_move >= 2 else 0.68 if nasdaq_move >= 0 else 0.45 if nasdaq_move >= -2 else 0.24
    equity_parts = [value for value in (proximity_risk, momentum_risk) if value is not None]
    equity_strength = statistics.mean(equity_parts) if equity_parts else None

    yield_level = ten_year["value"]
    level_risk = 0.85 if yield_level >= 5.25 else 0.75 if yield_level >= 5 else 0.6 if yield_level >= 4.5 else 0.42 if yield_level >= 4 else 0.24
    yield_change = ten_year.get("change_5obs")
    change_risk = None
    if isinstance(yield_change, (int, float)):
        change_risk = 0.85 if yield_change >= 0.25 else 0.7 if yield_change >= 0.15 else 0.5 if yield_change >= 0.05 else 0.32 if yield_change >= 0 else 0.18
    rate_pressure = statistics.mean([level_risk, change_risk]) if change_risk is not None else level_risk

    sp500 = macro.get("sp500")
    leadership_gap = None
    leadership_risk = None
    if sp500:
        nasdaq_change = nasdaq.get("change_5obs_pct")
        sp500_change = sp500.get("change_5obs_pct")
        if isinstance(nasdaq_change, (int, float)) and isinstance(sp500_change, (int, float)):
            leadership_gap = nasdaq_change - sp500_change
            leadership_risk = 0.8 if leadership_gap >= 2 else 0.65 if leadership_gap >= 1 else 0.5 if leadership_gap >= 0 else 0.34 if leadership_gap >= -1 else 0.2

    calm_bits: list[float] = []
    if "vix" in macro:
        vix = macro["vix"]["value"]
        calm_bits.append(0.8 if vix < 14 else 0.65 if vix < 17 else 0.5 if vix < 20 else 0.32 if vix < 25 else 0.18)
    if "hy" in macro:
        spread = macro["hy"]["value"]
        calm_bits.append(0.75 if spread < 3 else 0.6 if spread < 3.5 else 0.45 if spread < 4 else 0.28 if spread < 5 else 0.15)
    complacency = statistics.mean(calm_bits) if calm_bits else None

    score, components = weighted_score([
        ("Nasdaq strength", equity_strength, 30),
        ("Long-rate pressure", rate_pressure, 35),
        ("Growth leadership proxy", leadership_risk, 15),
        ("Volatility and credit calm", complacency, 20),
    ])
    score_band, score_slug = band(score)
    dates = [
        row.get("date") for row in (nasdaq, ten_year, sp500, macro.get("vix"), macro.get("hy"))
        if row and row.get("date")
    ]
    return {
        "score": score,
        "band": score_band,
        "slug": score_slug,
        "nasdaq_value": nasdaq["value"],
        "nasdaq_change_5obs_pct": nasdaq.get("change_5obs_pct"),
        "nasdaq_distance_from_45d_high_pct": distance,
        "ten_year_yield_pct": yield_level,
        "ten_year_change_5obs_bp": yield_change * 100 if isinstance(yield_change, (int, float)) else None,
        "nasdaq_vs_sp500_5obs_pp": leadership_gap,
        "vix": macro.get("vix", {}).get("value"),
        "hy_spread_pct": macro.get("hy", {}).get("value"),
        "latest_date": max(dates) if dates else None,
        "components": components,
        "interpretation": "Latent valuation and concentration vulnerability; not evidence of active panic.",
    }


def vulnerability_and_active(
    market: dict[str, Any],
    fgi: dict[str, Any] | None,
    deriv: dict[str, Any] | None,
    stable: dict[str, Any] | None,
    macro: dict[str, dict[str, Any]],
    consumer: dict[str, Any] | None,
    equity_rates: dict[str, Any] | None,
    cmc_deriv: dict[str, Any] | None,
) -> tuple[int, int, list[dict[str, Any]], list[dict[str, Any]]]:
    # Vulnerability measures how quickly a future shock could propagate. It is
    # deliberately separate from evidence that a panic is already underway.
    okx_leverage = None
    if deriv:
        funding = deriv["funding_8h_pct"]
        funding_risk = 0.95 if funding >= 0.05 else 0.78 if funding >= 0.03 else 0.58 if funding >= 0.015 else 0.35 if funding >= 0.005 else 0.5 if funding <= -0.03 else 0.2
        oi_change = deriv.get("oi_change_7d_pct")
        oi_risk = 0.45
        if isinstance(oi_change, (int, float)):
            oi_risk = 1.0 if oi_change >= 15 else 0.82 if oi_change >= 8 else 0.62 if oi_change >= 3 else 0.42 if oi_change >= 0 else 0.28
        okx_leverage = clamp((funding_risk * 0.45 + oi_risk * 0.55), 0, 1)

    cmc_leverage = None
    if cmc_deriv:
        cmc_bits: list[float] = []
        funding = cmc_deriv.get("btc_weighted_funding_pct")
        if isinstance(funding, (int, float)):
            magnitude = abs(funding)
            cmc_bits.append(0.95 if magnitude >= 0.05 else 0.78 if magnitude >= 0.03 else 0.58 if magnitude >= 0.015 else 0.35 if magnitude >= 0.005 else 0.2)
        basis = cmc_deriv.get("btc_weighted_basis_pct")
        if isinstance(basis, (int, float)):
            magnitude = abs(basis)
            cmc_bits.append(0.9 if magnitude >= 0.5 else 0.72 if magnitude >= 0.25 else 0.52 if magnitude >= 0.1 else 0.3)
        aggregate_oi = cmc_deriv.get("global_open_interest_usd")
        total_market_cap = market.get("market_cap")
        if isinstance(aggregate_oi, (int, float)) and isinstance(total_market_cap, (int, float)) and total_market_cap > 0:
            oi_ratio = aggregate_oi / total_market_cap * 100
            cmc_bits.append(0.9 if oi_ratio >= 18 else 0.75 if oi_ratio >= 14 else 0.58 if oi_ratio >= 10 else 0.4 if oi_ratio >= 7 else 0.22)
        if cmc_bits:
            cmc_leverage = statistics.mean(cmc_bits)

    if okx_leverage is not None and cmc_leverage is not None:
        leverage = okx_leverage * 0.45 + cmc_leverage * 0.55
    else:
        leverage = cmc_leverage if cmc_leverage is not None else okx_leverage

    sentiment = None
    if fgi:
        value = fgi["value"]
        fgi_risk = 0.9 if value >= 80 else 0.7 if value >= 70 else 0.5 if value >= 60 else 0.35 if value >= 40 else 0.55 if value >= 20 else 0.75
        move = abs(market["btc"]["change_7d"])
        move_risk = 0.9 if move >= 15 else 0.68 if move >= 8 else 0.45 if move >= 4 else 0.22
        sentiment = fgi_risk * 0.6 + move_risk * 0.4

    breadth_risk = 0.82 if market["breadth"] < 25 else 0.65 if market["breadth"] < 40 else 0.45 if market["breadth"] < 55 else 0.22
    dominance_risk = 0.78 if market["dominance"] >= 60 else 0.6 if market["dominance"] >= 55 else 0.4 if market["dominance"] >= 50 else 0.25
    concentration = breadth_risk * 0.6 + dominance_risk * 0.4

    macro_bits: list[float] = []
    if "vix" in macro:
        v = macro["vix"]["value"]
        macro_bits.append(1.0 if v >= 40 else 0.82 if v >= 30 else 0.62 if v >= 25 else 0.42 if v >= 20 else 0.22 if v >= 15 else 0.12)
    if "hy" in macro:
        v = macro["hy"]["value"]
        macro_bits.append(1.0 if v >= 6 else 0.78 if v >= 5 else 0.58 if v >= 4 else 0.35 if v >= 3 else 0.18)
    if "ten_year" in macro:
        v = macro["ten_year"]["value"]
        macro_bits.append(0.9 if v >= 5.25 else 0.72 if v >= 5 else 0.55 if v >= 4.5 else 0.38 if v >= 4 else 0.2)
    if "oil" in macro:
        v = macro["oil"]["value"]
        change = abs(macro["oil"].get("change_5obs_pct") or 0)
        level = 0.78 if v >= 110 else 0.62 if v >= 95 else 0.48 if v >= 80 else 0.3 if v >= 65 else 0.18
        shock = 0.8 if change >= 12 else 0.6 if change >= 8 else 0.4 if change >= 4 else 0.2
        macro_bits.append(level * 0.65 + shock * 0.35)
    if "dollar" in macro:
        change = macro["dollar"].get("change_5obs_pct") or 0
        macro_bits.append(0.75 if change >= 2 else 0.55 if change >= 1 else 0.35 if change >= 0 else 0.2)
    macro_risk = statistics.mean(macro_bits) if macro_bits else None

    liquidity_bits: list[float] = []
    if stable and isinstance(stable.get("change_7d_pct"), (int, float)):
        change = stable["change_7d_pct"]
        liquidity_bits.append(0.9 if change <= -2 else 0.7 if change <= -1 else 0.48 if change < 0 else 0.2 if change < 1 else 0.12)
    ratio = market["volume_to_cap"]
    liquidity_bits.append(0.72 if ratio < 2 else 0.52 if ratio < 3 else 0.32 if ratio < 5 else 0.2)
    liquidity_risk = statistics.mean(liquidity_bits)

    consumer_risk = None
    if consumer:
        consumer_bits: list[float] = []
        gap = consumer.get("spending_income_gap_3obs_pp")
        if isinstance(gap, (int, float)):
            consumer_bits.append(0.92 if gap >= 1.5 else 0.75 if gap >= 0.75 else 0.55 if gap >= 0.25 else 0.3 if gap >= 0 else 0.18)
        saving_rate = consumer.get("saving_rate_pct")
        if isinstance(saving_rate, (int, float)):
            consumer_bits.append(0.92 if saving_rate < 3 else 0.76 if saving_rate < 4 else 0.58 if saving_rate < 5 else 0.38 if saving_rate < 6 else 0.2)
        sentiment_value = consumer.get("sentiment_index")
        if isinstance(sentiment_value, (int, float)):
            consumer_bits.append(0.88 if sentiment_value < 60 else 0.72 if sentiment_value < 70 else 0.56 if sentiment_value < 80 else 0.4 if sentiment_value < 90 else 0.22)
        if consumer_bits:
            consumer_risk = statistics.mean(consumer_bits)

    vulnerability, vulnerability_detail = weighted_score([
        ("Leverage and crowding", leverage, 23),
        ("Momentum and sentiment", sentiment, 14),
        ("Crypto concentration", concentration, 13),
        ("Cross-market transmission", macro_risk, 22),
        ("Liquidity and absorption", liquidity_risk, 10),
        ("Consumer exhaustion", consumer_risk, 10),
        ("Equity-rates divergence", equity_rates["score"] / 100 if equity_rates else None, 8),
    ])

    price_damage = 0.05
    c24 = market["btc"]["change_24h"]
    c7 = market["btc"]["change_7d"]
    if c24 <= -12 or c7 <= -20:
        price_damage = 1.0
    elif c24 <= -8 or c7 <= -15:
        price_damage = 0.82
    elif c24 <= -5 or c7 <= -10:
        price_damage = 0.62
    elif c24 <= -2.5 or c7 <= -6:
        price_damage = 0.38
    elif c24 < 0:
        price_damage = 0.18

    vol_stress = None
    if "vix" in macro:
        v = macro["vix"]["value"]
        vol_stress = 1.0 if v >= 40 else 0.78 if v >= 30 else 0.55 if v >= 25 else 0.32 if v >= 20 else 0.12
    credit_stress = None
    if "hy" in macro:
        level = macro["hy"]["value"]
        delta = macro["hy"].get("change_5obs") or 0
        credit_stress = 1.0 if level >= 6 or delta >= 1 else 0.72 if level >= 5 or delta >= 0.6 else 0.45 if level >= 4 or delta >= 0.3 else 0.12
    cross_asset = None
    if "sp500" in macro:
        change = macro["sp500"].get("change_5obs_pct") or 0
        cross_asset = 1.0 if change <= -8 else 0.75 if change <= -5 else 0.5 if change <= -3 else 0.28 if change <= -1 else 0.08
    deleveraging = None
    if deriv:
        oi_change = deriv.get("oi_change_7d_pct")
        funding = deriv["funding_8h_pct"]
        if isinstance(oi_change, (int, float)):
            deleveraging = 0.9 if oi_change <= -20 and c7 < 0 else 0.65 if oi_change <= -10 and c7 < 0 else 0.42 if funding <= -0.03 else 0.1
        else:
            deleveraging = 0.42 if funding <= -0.03 else 0.1
    if cmc_deriv:
        global_24h = cmc_deriv.get("global_liquidations_24h_usd")
        btc_24h = cmc_deriv.get("btc_liquidations_24h_usd")
        liquidation_bits: list[float] = []
        if isinstance(global_24h, (int, float)):
            liquidation_bits.append(1.0 if global_24h >= 3_000_000_000 else 0.82 if global_24h >= 1_500_000_000 else 0.62 if global_24h >= 750_000_000 else 0.38 if global_24h >= 300_000_000 else 0.12)
        if isinstance(btc_24h, (int, float)):
            liquidation_bits.append(1.0 if btc_24h >= 1_000_000_000 else 0.82 if btc_24h >= 500_000_000 else 0.62 if btc_24h >= 250_000_000 else 0.38 if btc_24h >= 100_000_000 else 0.12)
        if liquidation_bits:
            liquidation_risk = statistics.mean(liquidation_bits)
            deleveraging = max(deleveraging or 0, liquidation_risk)
    stable_stress = None
    if stable and isinstance(stable.get("change_7d_pct"), (int, float)):
        change = stable["change_7d_pct"]
        stable_stress = 0.9 if change <= -3 else 0.65 if change <= -2 else 0.4 if change <= -1 else 0.08

    active, active_detail = weighted_score([
        ("BTC price damage", price_damage, 30),
        ("Equity volatility", vol_stress, 20),
        ("Credit synchronization", credit_stress, 20),
        ("Cross-asset selling", cross_asset, 15),
        ("Forced deleveraging", deleveraging, 10),
        ("Stablecoin contraction", stable_stress, 5),
    ])
    return vulnerability, active, vulnerability_detail, active_detail


def band(score: int) -> tuple[str, str]:
    if score >= 75:
        return "Red", "red"
    if score >= 60:
        return "Orange", "orange"
    if score >= 45:
        return "Amber", "amber"
    if score >= 25:
        return "Yellow", "yellow"
    return "Green", "green"


def money(value: float) -> str:
    absolute = abs(value)
    if absolute >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.2f}T"
    if absolute >= 1_000_000_000:
        return f"${value / 1_000_000_000:.1f}B"
    if absolute >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    return f"${value:,.0f}"


def optional(label: str, fn: Any, gaps: list[str]) -> Any:
    try:
        return fn()
    except Exception as exc:  # A missing optional feed is evidence, not a green signal.
        gaps.append(f"{label}: {exc}")
        print(f"warning: {label}: {exc}", file=sys.stderr)
        return None


def main() -> None:
    now = datetime.now(timezone.utc)
    previous = last_history()
    market = coinpaprika()  # Required: failure preserves yesterday's published file.
    gaps: list[str] = []
    fgi = optional("Fear & Greed", fear_greed, gaps)
    deriv = optional("OKX derivatives", okx_derivatives, gaps)
    stable = optional("Stablecoin supply", stablecoins, gaps)
    cmc_api_key = os.environ.get("CMC_API_KEY", "").strip()
    cmc_deriv = (
        optional("CoinMarketCap derivatives", lambda: coinmarketcap_derivatives(cmc_api_key), gaps)
        if cmc_api_key else None
    )
    if not cmc_api_key:
        gaps.append("CoinMarketCap derivatives: CMC_API_KEY is not configured")

    macro: dict[str, dict[str, Any]] = {}
    for key, series_id, label in (
        ("vix", "VIXCLS", "VIX"),
        ("ten_year", "DGS10", "US 10-year yield"),
        ("hy", "BAMLH0A0HYM2", "US high-yield spread"),
        ("oil", "DCOILWTICO", "WTI oil"),
        ("dollar", "DTWEXBGS", "Broad dollar index"),
        ("sp500", "SP500", "S&P 500"),
        ("nasdaq", "NASDAQCOM", "Nasdaq Composite"),
    ):
        result = optional(label, lambda sid=series_id: fred_series(sid), gaps)
        if result:
            macro[key] = result

    consumer_series: dict[str, dict[str, Any]] = {}
    for key, series_id, label in (
        ("real_spending", "PCEC96", "Real consumer spending"),
        ("real_income", "DSPIC96", "Real disposable personal income"),
        ("saving_rate", "PSAVERT", "Personal saving rate"),
        ("sentiment", "UMCSENT", "University of Michigan consumer sentiment"),
    ):
        result = optional(label, lambda sid=series_id: fred_series(sid), gaps)
        if result:
            consumer_series[key] = result

    consumer = None
    if {"real_spending", "real_income", "saving_rate", "sentiment"}.issubset(consumer_series):
        spending_change = consumer_series["real_spending"].get("change_3obs_pct")
        income_change = consumer_series["real_income"].get("change_3obs_pct")
        if isinstance(spending_change, (int, float)) and isinstance(income_change, (int, float)):
            gap = spending_change - income_change
            saving_rate = consumer_series["saving_rate"]["value"]
            sentiment_index = consumer_series["sentiment"]["value"]
            raw_risk = statistics.mean([
                92 if gap >= 1.5 else 75 if gap >= 0.75 else 55 if gap >= 0.25 else 30 if gap >= 0 else 18,
                92 if saving_rate < 3 else 76 if saving_rate < 4 else 58 if saving_rate < 5 else 38 if saving_rate < 6 else 20,
                88 if sentiment_index < 60 else 72 if sentiment_index < 70 else 56 if sentiment_index < 80 else 40 if sentiment_index < 90 else 22,
            ])
            consumer = {
                "score": round(raw_risk),
                "band": band(round(raw_risk))[0],
                "real_spending_change_3obs_pct": spending_change,
                "real_income_change_3obs_pct": income_change,
                "spending_income_gap_3obs_pp": gap,
                "saving_rate_pct": saving_rate,
                "sentiment_index": sentiment_index,
                "date": min(row["date"] for row in consumer_series.values()),
                "source_note": "FRED series sourced from BEA and the University of Michigan",
            }

    equity_rates = equity_rates_divergence(macro)
    if cmc_deriv:
        cmc_deriv["global_open_interest_to_market_cap_pct"] = (
            cmc_deriv["global_open_interest_usd"] / market["market_cap"] * 100
        )
    rotation, rotation_regime, dominance_read = rotation_score(market, previous)
    vulnerability, active, vulnerability_detail, active_detail = vulnerability_and_active(
        market, fgi, deriv, stable, macro, consumer, equity_rates, cmc_deriv
    )
    vulnerability_band, vulnerability_slug = band(vulnerability)
    active_band, active_slug = band(active)

    if active >= 60:
        decision = "ACTION WATCH"
        headline = "Panic signals are synchronizing."
    elif active >= 25:
        decision = "DEFENSIVE"
        headline = "Stress is spreading beyond one market."
    elif vulnerability >= 60:
        decision = "WATCH"
        headline = "Calm surface, fragile structure."
    elif vulnerability >= 45:
        decision = "WAIT"
        headline = "Stable, but still vulnerable."
    else:
        decision = "WAIT"
        headline = "No active panic. Keep watching the structure."

    source_dates = [row["date"] for row in macro.values() if row.get("date")]
    quality = "DQ-A" if not gaps else "DQ-B" if len(gaps) <= 2 else "DQ-C"
    notes = [
        "The automated score uses only free, public data and does not place trades.",
        "ETF flows and order-book depth are not treated as favorable when unavailable; they remain explicit gaps.",
        "A daily automated snapshot cannot replace Emily's event-driven review when a shock is moving quickly.",
    ]
    if gaps:
        notes.append(f"Missing optional feeds today: {len(gaps)}. The model published only because more than 60% of each panic score remained observable.")

    snapshot = {
        "schema_version": 2,
        "updated_at": now.isoformat().replace("+00:00", "Z"),
        "source_updated_at": market["source_updated_at"],
        "quality": quality,
        "decision": decision,
        "headline": headline,
        "summary": (
            f"BTC is {market['btc']['change_7d']:+.1f}% over seven days. "
            f"{market['breadth']:.0f}% of {market['eligible_count']} eligible large alts beat BTC. "
            f"Panic vulnerability is {vulnerability_band.lower()}, while active-panic evidence remains {active_band.lower()}."
        ),
        "scores": {
            "rotation": rotation,
            "rotation_regime": rotation_regime,
            "vulnerability": vulnerability,
            "vulnerability_band": vulnerability_band,
            "vulnerability_slug": vulnerability_slug,
            "active": active,
            "active_band": active_band,
            "active_slug": active_slug,
        },
        "crypto": {
            "btc_price_usd": market["btc"]["price"],
            "btc_change_24h_pct": market["btc"]["change_24h"],
            "btc_change_7d_pct": market["btc"]["change_7d"],
            "eth_change_7d_pct": market["eth"]["change_7d"],
            "eth_excess_7d_pp": market["eth_excess"],
            "btc_dominance_pct": market["dominance"],
            "dominance_read": dominance_read,
            "alt_breadth_pct": market["breadth"],
            "median_alt_excess_pp": market["median_excess"],
            "eligible_alts": market["eligible_count"],
            "market_cap_usd": market["market_cap"],
            "market_change_24h_pct": market["market_change_24h"],
            "volume_24h_usd": market["volume_24h"],
        },
        "sentiment": fgi,
        "derivatives": deriv,
        "aggregated_derivatives": cmc_deriv,
        "stablecoins": stable,
        "macro": macro,
        "consumer": consumer,
        "equity_rates": equity_rates,
        "model": {
            "vulnerability_components": vulnerability_detail,
            "active_components": active_detail,
            "missing": gaps,
            "notes": notes,
            "latest_macro_date": max(source_dates) if source_dates else None,
        },
        "sources": [
            {"label": "CoinPaprika", "url": "https://api.coinpaprika.com/"},
            {"label": "Alternative.me Fear & Greed", "url": "https://alternative.me/crypto/fear-and-greed-index/"},
            {"label": "OKX public market data", "url": "https://www.okx.com/docs-v5/en/"},
            {"label": "CoinMarketCap derivatives", "url": "https://coinmarketcap.com/charts/derivatives/"},
            {"label": "Federal Reserve Economic Data", "url": "https://fred.stlouisfed.org/"},
            {"label": "Nasdaq Composite via FRED", "url": "https://fred.stlouisfed.org/series/NASDAQCOM"},
            {"label": "BEA consumer spending and income", "url": "https://www.bea.gov/data/consumer-spending/main"},
            {"label": "DefiLlama stablecoins", "url": "https://defillama.com/stablecoins"},
        ],
    }

    payload = json.dumps(snapshot, separators=(",", ":"), ensure_ascii=False)
    LIVE_PATH.write_text(
        "// Generated by scripts/update_emily.py; do not edit by hand.\n"
        f"window.EMILY_LIVE={payload};\n",
        encoding="utf-8",
    )
    save_history({
        "updated_at": snapshot["updated_at"],
        "btc_dominance": market["dominance"],
        "rotation": rotation,
        "vulnerability": vulnerability,
        "active": active,
        "equity_rates_divergence": equity_rates["score"] if equity_rates else None,
        "btc_price_usd": market["btc"]["price"],
    })
    print(
        f"Emily updated {snapshot['updated_at']} {quality} "
        f"rotation={rotation} vulnerability={vulnerability} active={active}"
    )


if __name__ == "__main__":
    main()
