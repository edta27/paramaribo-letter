# Crypto Council Operating Guide

## Recommended setup

Use a strong parent model for orchestration and Luna workers for bounded research. When the controls are available, choose **Sol High** for the parent chat. The project agents already specify their worker settings:

| Agent | Effort | Purpose |
|---|---:|---|
| `killa_quant` | Max | Quantitative regime and derivatives |
| `macro_liquidity` | Extra High | Macro causality and cross-asset effects |
| `bang_technician` | High | @BangXBT HTF plan: structure, sweeps, confirmation, targets |
| `glassnode_onchain` | High | On-chain confirmation and cycle risk |
| `bitwise_fundamentals` | High | Alt/meme investability and token risk |
| `leopold_ai_scaling` | Extra High | AI scaling, compute, power, miner infrastructure, and AI-token transmission |
| `cowen_cycle_risk` | High | BTC dominance, ETH/BTC, breadth, market cycles, and time-based capitulation |

Higher effort is reserved for the work most likely to benefit from it. All five agents remain on `gpt-5.6-luna`.

## Which prompt to use

| Need | Prompt | Agents | Normal cadence |
|---|---|---:|---|
| Quick BTC regime check | `daily-btc-pulse.md` | 3 | Daily or around major events |
| BTC plus alt/meme/AI conviction review | `run-crypto-council.md` | 7 | Weekly, or before a material decision |

The daily pulse normally stays at three agents. It activates `leopold_ai_scaling` only for a material AI, technology-equity, compute/power, miner-HPC, or AI-token catalyst.
It activates `cowen_cycle_risk` when dominance, ETH/BTC, alt breadth, or a multi-week cycle thesis is central.

Do not run the deep council repeatedly on the same unchanged evidence. A new run is useful when price invalidates a level, a macro release lands, derivatives positioning changes materially, fresh on-chain data arrives, or a token catalyst/unlock changes.

## Practices that improve results

1. Ask one concrete question with one main horizon. More horizons produce more words, not necessarily more signal.
2. Keep the watchlist to eight assets or fewer in deep mode and five or fewer in daily mode.
3. Use one timestamped evidence packet so every agent analyzes the same market state.
4. Keep first-round work independent to reduce anchoring.
5. Debate only material disagreements; do not circulate every full memo to every agent.
6. Preserve `no trade` and `insufficient evidence` as valid conclusions.
7. Record forecasts before the outcome, then score them after expiry. Favor agents and indicators that demonstrate calibration over time.

## Forecast review

Use `review-forecast.md` after a forecast horizon expires. Record the outcome in `research/forecast-ledger.csv`. After at least 20 comparable forecasts, review calibration by agent and horizon before changing weights.
