# Research Desk Operating Guide

## Recommended setup

Use a strong parent model for orchestration and Luna workers for bounded research. When the controls are available, choose **Sol High** for the parent chat. The project agents already specify their worker settings.

**Core seven** (default deep council):

| Agent | Effort | Purpose |
|---|---:|---|
| `killa_quant` | Max | Quantitative regime and derivatives |
| `macro_liquidity` | Extra High | Macro causality and cross-asset effects |
| `bang_technician` | High | @BangXBT HTF plan: structure, sweeps, confirmation, targets |
| `glassnode_onchain` | High | On-chain confirmation and cycle risk |
| `bitwise_fundamentals` | High | Alt/meme investability and token risk |
| `leopold_ai_scaling` | Extra High | AI scaling, compute, power, miner infrastructure, and AI-token transmission |
| `cowen_cycle_risk` | High | BTC dominance, ETH/BTC, breadth, market cycles, and time-based capitulation |

**Bench specialists** (spawn only when the question needs them):

| Agent | Effort | Spawn when |
|---|---:|---|
| `eth_platform` | High | ETH, staking, L2s, rollup security, or L2-native tokens |
| `hayes_crypto_credit` | Extra High | Stablecoins, Tether, funding, basis, JPY/carry, crypto credit |
| `policy_regulation` | High | ETFs, listings, bills, enforcement, brokers, jurisdiction |
| `carter_monetary` | High | BTC as money vs casino, energy, stablecoin reserves, ETF plumbing |
| `murad_meme` | High | Meme coins or attention/cult-coin claims on the watchlist |
| `hasu_incentives` | High | MEV, staking agency, restaking, sequencer rents, protocol incentives |
| `cryptoquant_flows` | High | Exchange netflow, miner-to-exchange, or Asia-session premium |
| `options_vol` | High | Barrier events, listed options, skew, or implied-touch math |
| `capriole_systematic` | High | BTC timing vs buy-and-hold, long/short/cash, Hash Ribbons/Energy Value, institutional absorption vs issuance, leveraged BTC treasuries, or gold/equity/cash rotation |
| `risk_red_team` | High | Always in deep-council Round 2; not a Round 1 forecaster |

**Letter editor** (parent role for public issues):

| Agent | Effort | Purpose |
|---|---:|---|
| `research_director` | High | Managing Editor of The Paramaribo Letter: packet → question, levels, scenarios, red-team, synthesis, headline |

**Publisher desk** (promote the site; not a market lens):

| Agent | Effort | Purpose |
|---|---:|---|
| `letter_marketing` | High | Ethical growth copy, LinkedIn/X/email CTAs, funnel check; dry-run unless `APPROVE_SEND` |

**Equity desk** (separate session; do not mix with the crypto council):

| Agent | Effort | Purpose |
|---|---:|---|
| `filings` | High | EDGAR 10-K / 10-Q / 8-K flags |
| `earnings` | High | Transcript tone and guidance vs prior quarter |
| `sector` | High | Rule changes, competitors, supply-chain noise |
| `insider` | High | Form 4 buys and lagged 13F appearances/exits |
| `chatter` | High | Public mention spikes; 3σ only if a baseline exists |
| `chief_of_staff` | High | Drops single-source flags; one-page morning brief; no email without `APPROVE_SEND` |

All agents remain on `gpt-5.6-luna`. Sessions allow up to 16 concurrent workers so a full crypto bench or the five equity specialists can run in parallel. Default crypto deep runs stay at the core seven plus Round-2 red team. Say **full bench** in the crypto parent prompt to spawn every crypto Round-1 specialist — not the equity desk.

## Which prompt to use

| Need | Prompt | Agents | Normal cadence |
|---|---|---:|---|
| Quick BTC regime check | `daily-btc-pulse.md` | 3 + specialists if needed | Daily or around major events |
| Confirmation-first buy-low / sell-high plan | `buy-low-sell-high.md` | bang + capriole + glassnode | When deciding whether to add, hold cash, or reduce |
| BTC plus alt/meme/AI conviction review | `run-crypto-council.md` | 7 + specialists if needed | Weekly, or before a material decision |
| Newsletter issue (headline, scenarios, stands) | `run-paramaribo-letter.md` | `research_director` (+ council as needed) | When publishing to The Paramaribo Letter |
| Promote the site or a new issue | `run-letter-marketing.md` | `letter_marketing` | After each publish, or weekly growth pass |
| Overnight equity filings / earnings / insider desk | `run-equity-desk.md` | 5 + chief_of_staff | Nightly or pre-market; dry-run first |
| Auto-update each watchlist ticker (quotes + EDGAR index) | `scripts/update_tickers.py` | none | Once, `--loop 300`, or GitHub Action weekdays |
| Visual night-run board (open in a browser) | `desk/index.html` | UI + `desk/live.js` | Refreshes after each ticker update |
| Cursor skill: live BTC + meme tape / Bang plan | `.cursor/skills/crypto-desk-update/SKILL.md` | parent chat | Say **update** or **Bang**; pulls CoinGecko, no invented prices |
| Newsletter archive (issues are never deleted) | `public/index.html` | none | `python3 -m http.server 8766 --directory public` |

The daily pulse normally stays at three agents. It activates `leopold_ai_scaling` only for a material AI, technology-equity, compute/power, miner-HPC, or AI-token catalyst.
It activates `cowen_cycle_risk` when dominance, ETH/BTC, alt breadth, or a multi-week cycle thesis is central.
It activates `eth_platform`, `hayes_crypto_credit`, `policy_regulation`, `carter_monetary`, `murad_meme`, `hasu_incentives`, `cryptoquant_flows`, `options_vol`, or `capriole_systematic` by the same specialist rules as the deep council.

Do not run the deep council repeatedly on the same unchanged evidence. A new run is useful when price invalidates a level, a macro release lands, derivatives positioning changes materially, fresh on-chain data arrives, or a token catalyst/unlock changes.

## Practices that improve results

1. Ask one concrete question with one main horizon. More horizons produce more words, not necessarily more signal.
2. Keep the watchlist to eight assets or fewer in crypto deep mode, five or fewer in daily pulse, and 20 or fewer on the equity desk.
3. Use one timestamped evidence packet so every agent analyzes the same market state.
4. Keep first-round work independent to reduce anchoring.
5. Debate only material disagreements; do not circulate every full memo to every agent.
6. Preserve `no trade` and `insufficient evidence` as valid conclusions.
7. Record forecasts before the outcome, then score them after expiry. Favor agents and indicators that demonstrate calibration over time.
8. Do not add every specialist to every run. Extra voices help only when they own a mechanism the core seven cannot cover.
9. Run the equity desk in its own session. Specialists must not see each other; the chief drops single-source flags. Dry-run until you set `APPROVE_SEND`.

## Forecast review

Use `review-forecast.md` after a forecast horizon expires. Record the outcome in `research/forecast-ledger.csv`. After at least 20 comparable forecasts, review calibration by agent and horizon before changing weights.
