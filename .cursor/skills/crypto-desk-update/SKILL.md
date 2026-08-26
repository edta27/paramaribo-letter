---
name: crypto-desk-update
description: Use when the user says update, today's tape, daily pulse, crash window, Bang plan, or wants a live check on BTC plus the meme watchlist. Pulls current quotes, compares to the last packet, and writes a confirmation-first plan. Do not use for equity filings or the six-agent vault desk.
---

# Crypto desk update

Educational scenario research. Not advice. No leverage. Cash and observe are valid. Do not impersonate @BangXBT, claim live fills, or say a trade was executed.

## When this fires

User says **update**, **today**, **pulse**, **Bang**, or asks when panic/crash is likely.

## Live packet (required)

1. State as-of time and timezone.
2. Pull live USD quotes. Never invent prices, Daily closes, RSI, funding, OI, or volume-profile levels. If a series is missing, say so.

```bash
python3 - <<'PY'
import json, urllib.request
ids = ",".join([
  "bitcoin","ethereum","solana","pepe","shiba-inu","dogwifcoin","pudgy-penguins",
  "popcat","cat-in-a-dogs-world","cash-cat","dogecoin","bonk","floki",
  "fartcoin","peanut-the-squirrel","moo-deng"
])
url = ("https://api.coingecko.com/api/v3/simple/price"
       f"?ids={ids}&vs_currencies=usd&include_24hr_change=true&include_market_cap=true")
req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"})
with urllib.request.urlopen(req, timeout=20) as r:
    print(json.dumps(json.loads(r.read()), indent=2))
PY
```

3. Confirm BTC from CoinGecko page or a second cite. Note 24h/7d range and distance from the dated ATH only if retrieved.
4. Compare to the **last packet in this chat**. Table: last → now → % change.
5. Dated catalysts only if still live (as of late Aug 2026: NVDA 26, Jackson Hole 27–29 / Warsh 28, FOMC 16 Sep). Drop expired ones.

Default watchlist: BTC, ETH, SOL, PENGU, WIF, PEPE, SHIB, CASHCAT, POPCAT, MEW, plus DOGE, BONK, FLOKI, FARTCOIN, PNUT, MOODENG. Cap scoring at eight names in a deep-council writeup; the extras stay satellite.

Gaps to mark unless actually pulled: Glassnode, ETF daily flow, funding/OI, H4 OHLC, CASHCAT contract/holder concentration.

## Forecast

Track `IR-2026-08-22A` until 2026-09-16T23:59:59Z unless the user started a newer ID.

- Base: two-way **$70k–$82k** through NVDA/JH/FOMC; memes give back a large share of blow-off spikes; **no dated crash**.
- Invalidation: Daily close **<$70,000** or two Daily closes **>$85,000**.
- Last council weights unless structure changed: bull **20** / base **50** / bear **30** (sum 100, 5-point steps in synthesis).

Do not call a calendar crash. Panic windows are event clusters, not “September is red.”

## Bang block (required for BTC)

Use this format **only** in the `$BTC` block. `Chill 🫖` only there. Do not claim to be the real @BangXBT.

Process: Analysis → Planning → Observation → Confirmation → Execution. HTF Daily first. No entry until a stated Daily (or H4 if in the packet) **close**. Prefer zones over fake precision. Omit mVAH/VAL/POC unless in the packet.

```
$BTC

[assumption in one line]
[HTF structure in 2–3 lines]

Current plan (simple):

Observation zone: [range]
Confirmation: [exact candle-close condition]
Entry: none until that close
Targets:
  TP1 → [level]
  TP2 → [level]
  Final → [only if mapped]

Until confirmation prints, just observe.
Eliminate the noise. Trust the system.

Analysis → Planning → Observation → Confirmation → Execution

Will update only if structure changes.

Chill 🫖
```

Then compact: Timestamp / TF, Invalidation, Bull/base/bear (10-point steps totaling 100%), one objection.

Current HTF map until invalidated: observe **$72k–$75.5k**; confirm **Daily close >$80k** while $70k holds, **or** **Daily close <$70k** for risk-off. Failed $80k is not confirmation.

## Rest of the reply

Keep it short.

1. One-line answer (box held / broken; crash still undated).
2. Quote table vs last packet.
3. Bang `$BTC` block.
4. Names: CASHCAT catch-up on a flat BTC tape is fakeout risk, not a cult; PENGU idiosyncratic; POPCAT/MEW tails; dogs fade after melt-up.
5. Next dated print (not every wick).

Do not mix the equity desk into this skill. Do not run `scripts/update_tickers.py` unless the user asked for the equity board.
