# BTC, Altcoin, Meme-Coin, and AI Research Council

Paste the prompt below into a new Codex/Conductor chat in this project.

```text
Run a seven-agent crypto research council for the following question:

QUESTION: [Replace this with the market question, asset, and decision horizon.]
AS-OF TIME: Use the current time and state the timezone.
PRIMARY HORIZON: [Choose one: 1 week or 1 month.]
SECONDARY HORIZON: [Optional adjacent horizon.]
OPTIONAL WATCHLIST: [Maximum 8 assets or sectors.]

Use these project-scoped agents:
- killa_quant
- bang_technician
- macro_liquidity
- glassnode_onchain
- bitwise_fundamentals
- leopold_ai_scaling
- cowen_cycle_risk

You are the moderator, not a sixth market forecaster. Coordinate the council through the following rounds. Do not let agents claim to be, speak for, or impersonate the named people or firms that inspired their analytical lenses.

Round 0 — evidence packet
1. Establish the as-of timestamp and timezone.
2. Gather one current, citable evidence packet from primary or authoritative sources where possible: BTC price/volume, major market indexes, BTC dominance, ETH/BTC, derivatives, relevant macro releases, on-chain metrics, ETF/fund flows, and token-specific fundamentals.
3. Mark delayed, paywalled, unavailable, or conflicting data. Never substitute memory for live data.
4. Give every agent the same timestamped packet and question. Agents should verify only critical gaps, not independently rebuild the packet.

Round 1 — independent work
Spawn all seven agents in parallel. Require independent memos before any agent sees another memo. Wait for all seven. Each memo must separate facts, inference, and speculation; cite sources; give bull/base/bear probabilities in 10-point increments totaling 100%; and identify invalidation conditions. Enforce the memo-length limits in the agent definitions. Permit leopold_ai_scaling to report "no material connection" rather than forcing an AI explanation for an unrelated crypto move.

Round 2 — cross-examination
Build a compact disagreement matrix from the seven memos. Do not send every full memo to every agent. Select at most three disputes that could materially change the final conclusion, and send each dispute only to the relevant agents:
- killa_quant handles weak statistics, derivative interpretation, and untested assumptions.
- bang_technician handles theses not confirmed by price structure or offering poor risk/reward.
- macro_liquidity handles causal stories that ignore rates, USD, liquidity, policy, or release lags.
- glassnode_onchain handles claims inconsistent with holder behavior and on-chain measurement limits.
- bitwise_fundamentals handles token quality, liquidity, unlocks, concentration, investability, and meme exit risk.
- leopold_ai_scaling handles unsupported AI scaling, compute, power, infrastructure, miner-conversion, or AI-token narratives.
- cowen_cycle_risk handles unsupported four-year-cycle analogies, BTC-dominance interpretation, ETH/BTC and ALT/BTC relative performance, breadth, and time-based capitulation.

Skip Round 2 entirely if the differences are immaterial. Otherwise allow one concise challenge and one concise response per selected dispute. Ask participating agents whether they changed their conclusion and for revised probabilities. Preserve unresolved disagreement.

Round 3 — synthesis
Wait for all revisions, then produce one council report with:
1. Executive summary in plain English.
2. Data timestamp, freshness, sources, and gaps.
3. BTC regime for the primary horizon, plus a short note on the secondary horizon when supplied.
4. Council bull/base/bear table in 5-point increments. Probabilities must sum to 100%. Do not calculate a simple average: discount stale evidence, unsupported claims, and correlated signals. Include triggers, invalidation, and price zones only when supported by current evidence.
5. Market transmission map: BTC -> BTC dominance -> ETH/BTC -> large-cap alts -> smaller alts -> meme coins. State when the expected sequence may fail.
6. Cross-market check: equities, rates, USD, gold, credit, stablecoins, derivatives, on-chain behavior, and any material AI/compute/power transmission.
7. Watchlist table scored 0-5 on liquidity, relative strength, catalyst quality, tokenomics/unlocks, holder concentration, fundamental/on-chain evidence, and downside/exit risk. Use N/A when a criterion does not fit.
8. Council disagreements: show each agent's final probabilities and why they differ.
9. Risk plan: invalidation signals, no-trade conditions, data to monitor next, and the date/time for reassessment.
10. A forecast record containing a unique forecast ID, creation time, expiry time, base scenario, probabilities, and invalidation so the result can later be scored in `research/forecast-ledger.csv`.
11. A short educational-use disclaimer.

Hard rules:
- This is scenario analysis, not certainty or personalized financial advice.
- Never fabricate live prices, metrics, chart levels, sources, quotes, or social posts.
- Use exact dates instead of "today" or "recently."
- Label facts, inferences, and speculation.
- Prefer primary data and dated research; link every material time-sensitive claim.
- Do not execute trades, connect an exchange, recommend leverage, or size positions.
- Treat meme coins as an extreme-risk category and explicitly assess liquidity, concentration, contract, manipulation, and exit risk.
- If evidence is insufficient, say "insufficient evidence" and specify what is missing.
- A unanimous answer is not required. Preserve important dissent.
- Keep the final report under 1,800 words unless the user asks for more detail.
```

## Why these five lenses

- `killa_quant`: systematic evidence, derivatives, probabilities, and falsification.
- `bang_technician`: chart structure, timing, risk/reward, and invalidation.
- `macro_liquidity`: rates, USD, policy, fiscal conditions, and cross-asset transmission.
- `glassnode_onchain`: holder behavior, cost basis, realized activity, and cycle diagnostics.
- `bitwise_fundamentals`: institutional investability, tokenomics, liquidity, and alt/meme due diligence.
- `leopold_ai_scaling`: AI capability scaling, compute and power buildout, national-security policy, miner infrastructure, and AI-token narrative testing.
- `cowen_cycle_risk`: market-cycle regime, BTC dominance, ETH/BTC and ALT/BTC relative strength, breadth, and time-based capitulation.

The parent chat mediates the discussion. This is more reliable than asking five agents to hold an unstructured group conversation: independent first-round work reduces anchoring, assigned challenges create useful disagreement, and the final synthesis preserves dissent rather than forcing consensus.

## Public research basis

These are analytical lenses, not endorsements or simulated identities.

- Killa: the user-provided profile identifies a quantitative-trader orientation; the prompt intentionally assumes nothing about private methods.
- BANG: the user-provided post demonstrates a chart-led thesis with targets, invalidation, and explicit risk/reward; the prompt uses only that visible style.
- Lyn Alden Research: [Bitcoin: A Global Liquidity Barometer](https://www.lynalden.com/bitcoin-a-global-liquidity-barometer/).
- Glassnode: [digital-asset market and on-chain intelligence](https://glassnode.com/).
- Bitwise: [rules-based crypto asset index methodology](https://bitwiseinvestments.com/indexes/methodologies/bitwise-crypto-asset-index-methodology) and [crypto research](https://bitwiseinvestments.com/crypto-market-insights).
- Leopold Aschenbrenner: [Situational Awareness: The Decade Ahead](https://situational-awareness.ai/), including published theses on AI scaling, compute clusters, power, industrial buildout, and national security.
- Benjamin Cowen: [Into The Cryptoverse quantitative market analysis](https://intothecryptoverse.com/) and his dated [Q2 2026 Crypto Risk Memo](https://www.benjamincowen.com/reports/crypto-risk-memo-q2-2026), covering public risk, cycle, dominance, breadth, and macro-regime concepts.
