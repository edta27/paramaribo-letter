# BTC, Altcoin, Meme-Coin, and AI Research Council

Paste the prompt below into a new Codex/Conductor chat in this project.

```text
Run a core seven-agent crypto research council for the following question:

QUESTION: [Replace this with the market question, asset, and decision horizon.]
AS-OF TIME: Use the current time and state the timezone.
PRIMARY HORIZON: [Choose one: 1 week or 1 month.]
SECONDARY HORIZON: [Optional adjacent horizon.]
OPTIONAL WATCHLIST: [Maximum 8 assets or sectors.]
BENCH: [Default: specialists by rule. Write "full bench" to spawn every specialist in Round 1.]

Use these project-scoped agents:
Core: killa_quant, bang_technician, macro_liquidity, glassnode_onchain, bitwise_fundamentals, leopold_ai_scaling, cowen_cycle_risk
Specialists: eth_platform, hayes_crypto_credit, policy_regulation, carter_monetary, murad_meme, hasu_incentives, cryptoquant_flows, options_vol, capriole_systematic
Round-2 only: risk_red_team

You are the moderator, not a market forecaster. Coordinate the council through the following rounds. Do not let agents claim to be, speak for, or impersonate the named people or firms that inspired their analytical lenses. Exception: bang_technician must use the specified @BangXBT process, language, and plan format. It still must not claim live affiliation, private fills, or that a trade has been executed.

Round 0 — evidence packet
1. Establish the as-of timestamp and timezone.
2. Gather one current, citable evidence packet from primary or authoritative sources where possible: BTC price/volume, major market indexes, BTC dominance, ETH/BTC, derivatives and listed options when relevant, relevant macro releases, on-chain metrics, exchange/miner flows when relevant, hash-rate / miner-capitulation and ETF or treasury demand versus daily issuance when relevant, ETF/fund flows, stablecoin supply and published reserves when relevant, L2/security context when relevant, policy/listing items when relevant, and token-specific fundamentals.
3. Mark delayed, paywalled, unavailable, or conflicting data. Never substitute memory for live data.
4. Give every agent the same timestamped packet and question. Agents should verify only critical gaps, not independently rebuild the packet.

Round 1 — independent work
Always spawn the core seven in parallel. Also spawn specialists in Round 1 when:
- eth_platform: the question or watchlist includes ETH, staking, blobs/fees, an L2, rollup security, or an L2-native token.
- hayes_crypto_credit: the question turns on stablecoins, Tether, funding, basis, JPY/carry, or crypto credit.
- policy_regulation: the question turns on ETFs, exchange or brokerage listings, bills, enforcement, or jurisdiction.
- carter_monetary: the question turns on BTC as money vs risk asset, energy, stablecoin reserves, or ETF plumbing.
- murad_meme: the watchlist includes a meme coin or the question is an attention/cult-coin claim.
- hasu_incentives: the question turns on MEV, staking agency, restaking, sequencer rents, or protocol incentives.
- cryptoquant_flows: exchange netflow, miner-to-exchange, or Asia-session premium is material.
- options_vol: the question is a barrier event, listed-options, skew, or implied-touch problem.
- capriole_systematic: the question turns on BTC timing vs buy-and-hold, long/short/cash exposure, Hash Ribbons / Energy Value / miner-capitulation timing, institutional absorption of mined supply, leveraged corporate BTC treasuries, or multi-asset rotation into gold, equities, or cash.
If the user wrote "full bench", spawn every Round-1 specialist even if the rules above are quiet.
Require independent memos before any agent sees another memo. Wait for all Round-1 agents. Each memo must separate facts, inference, and speculation; cite sources; give bull/base/bear probabilities in 10-point increments totaling 100%; and identify invalidation conditions. Enforce the memo-length limits in the agent definitions. Permit leopold_ai_scaling, eth_platform, policy_regulation, hasu_incentives, and murad_meme to report "no material connection" or "insufficient evidence" rather than forcing a story. Require bang_technician to use its native $TICKER plan format first, then the compact council block (timestamp/TF, invalidation, bull/base/bear, one objection). Do not rewrite Bang's memo into a research essay.

Round 2 — cross-examination
Build a compact disagreement matrix from the Round-1 memos. Do not send every full memo to every agent. Select at most three disputes that could materially change the final conclusion, and send each dispute only to the relevant agents:
- killa_quant handles weak statistics, derivative interpretation, and untested assumptions.
- bang_technician handles theses not confirmed by price structure or offering poor risk/reward.
- macro_liquidity handles causal stories that ignore rates, USD, liquidity, policy, or release lags.
- glassnode_onchain handles claims inconsistent with holder behavior and on-chain measurement limits.
- bitwise_fundamentals handles token quality, liquidity, unlocks, concentration, investability, and meme exit risk.
- leopold_ai_scaling handles unsupported AI scaling, compute, power, infrastructure, miner-conversion, or AI-token narratives.
- cowen_cycle_risk handles unsupported four-year-cycle analogies, BTC-dominance interpretation, ETH/BTC and ALT/BTC relative performance, breadth, and time-based capitulation.
- eth_platform handles unsupported ETH/L2 cash-flow or security claims.
- hayes_crypto_credit handles Fed-only stories that ignore stablecoin, funding, basis, or carry plumbing.
- policy_regulation handles listings or headlines treated as law, endorsement, or already-priced policy.
- carter_monetary handles cycle or Fed stories that ignore money-vs-casino and reserve quality.
- murad_meme handles "listing leftover" dismissals that skip a real attention/cult test, and cult claims that skip survivor bias.
- hasu_incentives handles TVL, yield, or points treated as economic value.
- cryptoquant_flows handles one-day netflow treated as a regime shift, or flow series that were not actually pulled.
- options_vol handles implied touch odds treated as physical probabilities, or invented gamma/max-pain.
- capriole_systematic handles buy-and-hold or calendar-cycle stories that ignore cash/short optionality; paid-chart or CAGR claims treated as live positions; price used as an input in a fundamentals-only read; leveraged BTC treasury models treated as systematic exposure.

Always spawn risk_red_team in Round 2 with a compact leading-thesis summary (not the full memos), the packet, and the selected disputes. It is a falsification officer, not an eighth market call.

Skip agent-to-agent debate if the differences are immaterial, but still run risk_red_team. Otherwise allow one concise challenge and one concise response per selected dispute. Ask participating agents whether they changed their conclusion and for revised probabilities. Preserve unresolved disagreement.

Round 3 — synthesis
Wait for all revisions, then produce one council report with:
1. Executive summary in plain English.
2. Data timestamp, freshness, sources, and gaps.
3. BTC regime for the primary horizon, plus a short note on the secondary horizon when supplied.
4. Council bull/base/bear table in 5-point increments. Probabilities must sum to 100%. Do not calculate a simple average: discount stale evidence, unsupported claims, and correlated signals. Include triggers, invalidation, and price zones only when supported by current evidence.
5. Market transmission map: BTC -> BTC dominance -> ETH/BTC -> large-cap alts -> smaller alts -> meme coins. State when the expected sequence may fail.
6. Cross-market check: equities, rates, USD, gold, credit, stablecoins, derivatives, on-chain behavior, L2/security when relevant, policy/listing when relevant, and any material AI/compute/power transmission.
7. Watchlist table scored 0-5 on liquidity, relative strength, catalyst quality, tokenomics/unlocks, holder concentration, fundamental/on-chain evidence, and downside/exit risk. Use N/A when a criterion does not fit.
8. Council disagreements: show each agent's final probabilities and why they differ.
9. Risk plan: invalidation signals, no-trade conditions, data to monitor next, and the date/time for reassessment.
10. A forecast record containing a unique forecast ID, creation time, expiry time, base scenario, probabilities, and invalidation so the result can later be scored in `research/forecast-ledger.csv`.
11. A short educational-use disclaimer.

If the user wants a public Paramaribo Letter issue, hand the packet and Round-3 material to `research_director` (see `prompts/run-paramaribo-letter.md`) for the reader-facing edit: central question, facts/levels, bull/base/bear with confirm/invalidate, strongest red-team objection, concise synthesis, hook and headline. Do not present specialist lenses as actual authors.

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

## Why these lenses

Core:
- `killa_quant`: systematic evidence, derivatives, probabilities, and falsification.
- `bang_technician`: @BangXBT HTF process — channels, demand/supply, liquidity sweeps, volume-profile levels, confirmation, and staged targets.
- `macro_liquidity`: rates, USD, yen/carry at the sovereign layer, policy, fiscal conditions, and cross-asset transmission.
- `glassnode_onchain`: holder behavior, cost basis, realized activity, and cycle diagnostics. BTC metrics do not transfer to L2 memes.
- `bitwise_fundamentals`: institutional investability, tokenomics, liquidity, listing half-life, and alt/meme due diligence.
- `leopold_ai_scaling`: AI capability scaling, compute and power buildout, national-security policy, miner infrastructure, and AI-token narrative testing.
- `cowen_cycle_risk`: market-cycle regime, BTC dominance, ETH/BTC and ALT/BTC relative strength, breadth, time-based capitulation, and listing micro-cycles.

Bench:
- `eth_platform`: ETH issuance/fees/staking, L2 security stages, and whether an L2 token has any ETH cash-flow link.
- `hayes_crypto_credit`: Tether and stablecoin plumbing, funding/basis, yen carry, and crypto-native dollar credit.
- `policy_regulation`: statutes, enforcement, ETFs, brokerage listings, and jurisdiction — labeled as law vs proposal vs rumor.
- `carter_monetary`: BTC as money vs casino, energy facts, stablecoin reserve quality, ETF plumbing.
- `murad_meme`: steelman then falsify attention/cult-coin claims; not an investability pass.
- `hasu_incentives`: MEV, staking agency, restaking, sequencer rents, mechanism failure.
- `cryptoquant_flows`: exchange netflow, miner-to-exchange, Asia-session premium as positioning prints.
- `options_vol`: skew, term structure, listed-options OI, and model touch odds vs physical probabilities.
- `capriole_systematic`: systematic long/short/cash vs buy-and-hold, Hash Ribbons and Energy Value, institutional demand vs issuance, and gold/equity/cash rotation. Not a live Capriole book.
- `risk_red_team`: Round-2 falsification of the leading thesis; not an independent market call.

The parent chat mediates the discussion. This is more reliable than asking agents to hold an unstructured group conversation: independent first-round work reduces anchoring, assigned challenges create useful disagreement, and the final synthesis preserves dissent rather than forcing consensus.

## Public research basis

These are analytical lenses, not endorsements or simulated identities.

- Killa: the user-provided profile identifies a quantitative-trader orientation; the prompt intentionally assumes nothing about private methods.
- BANG (@BangXBT): the user-specified prompt uses his published process (HTF structure, liquidity sweeps, demand/supply, volume profile) and plan format. This is an analytical lens, not an affiliation or a copy of private trades.
- Lyn Alden Research: [Bitcoin: A Global Liquidity Barometer](https://www.lynalden.com/bitcoin-a-global-liquidity-barometer/).
- Glassnode: [digital-asset market and on-chain intelligence](https://glassnode.com/).
- Bitwise: [rules-based crypto asset index methodology](https://bitwiseinvestments.com/indexes/methodologies/bitwise-crypto-asset-index-methodology) and [crypto research](https://bitwiseinvestments.com/crypto-market-insights).
- Leopold Aschenbrenner: [Situational Awareness: The Decade Ahead](https://situational-awareness.ai/), including published theses on AI scaling, compute clusters, power, industrial buildout, and national security.
- Benjamin Cowen: [Into The Cryptoverse quantitative market analysis](https://intothecryptoverse.com/) and his dated [Q2 2026 Crypto Risk Memo](https://www.benjamincowen.com/reports/crypto-risk-memo-q2-2026), covering public risk, cycle, dominance, breadth, and macro-regime concepts.
- Ethereum / L2 security: [L2Beat scaling and risk frameworks](https://l2beat.com/) and public protocol documentation.
- Arthur Hayes: published essays on dollar liquidity, yen, stablecoins, and crypto carry (for example [his Substack](https://cryptohayes.substack.com/)). The agent uses the public framework, not private positions.
- Policy: primary agency, legislative, and court sources, plus published research such as [Coin Center](https://www.coincenter.org/). This is not legal advice.
- Nic Carter / Castle Island: published work on BTC as money, proof-of-work energy, and stablecoin market structure, including [Castle Island research](https://castleisland.vc/research/).
- Murad Mahmudov: public supercycle and cult-coin arguments used only as a narrative steelman to falsify, not as a trade call.
- Hasu: published Uncommon Core / Flashbots-adjacent research on incentives, MEV, and staking.
- CryptoQuant / Ki Young Ju: published [exchange- and miner-flow methodology](https://cryptoquant.com/). The agent must not claim paid dashboard access it cannot retrieve.
- Options: public [Deribit Insights](https://insights.deribit.com/)-style market-structure writing. Model odds are not physical probabilities.
- Charles Edwards / Capriole: published [fund overview](https://capriole.com/fund), [Hash Ribbons](https://capriole.com/hash-ribbons-bitcoin-bottoms/), [Energy Value](https://medium.com/capriole/bitcoin-value-energy-equivalence-6d00d1baa34a), and [Capriole Charts](https://capriole.com/charts/). The agent uses public methods, not live holdings, paid charts, or private Trend King/Macro Index prints.

