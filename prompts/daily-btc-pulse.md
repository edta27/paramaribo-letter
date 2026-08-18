# Fast Daily BTC Pulse

Use this for a quick daily or event-driven check. It starts with three core agents and adds specialists only when needed.

```text
Produce a fast BTC market pulse.

QUESTION: What is the BTC regime and its likely effect on ETH and altcoin risk over the next 1 day and 1 week?
OPTIONAL EVENT OR WATCHLIST: [Add a catalyst or up to 5 assets.]

Use the strongest available parent model as moderator; Sol High is preferred when selectable. Spawn these project agents in parallel:
- killa_quant
- bang_technician
- macro_liquidity

Normally stop at those three. Also spawn `leopold_ai_scaling` only when the question or evidence packet contains a material AI-equity shock, compute/power policy event, Bitcoin-miner HPC conversion, or AI-token catalyst.

Also spawn `cowen_cycle_risk` only when BTC dominance, ETH/BTC, altcoin rotation, market breadth, or a multi-week cycle claim is central to the question.

Also spawn `eth_platform` when the watchlist or question includes ETH, staking, an L2, or an L2-native token.
Also spawn `hayes_crypto_credit` when stablecoins, Tether, funding, basis, or yen/carry are material.
Also spawn `policy_regulation` when ETFs, brokerage/exchange listings, bills, or enforcement are material.
Also spawn `carter_monetary` when money-vs-casino, energy, stablecoin reserves, or ETF plumbing is central.
Also spawn `murad_meme` when the watchlist includes a meme coin or an attention/cult claim.
Also spawn `hasu_incentives` when MEV, staking, restaking, or sequencer incentives are material.
Also spawn `cryptoquant_flows` when exchange netflow, miner-to-exchange, or Asia premium is material.
Also spawn `options_vol` when the question is a barrier event, listed options, skew, or implied-touch math.

If any Round-1 agents differ by at least 30 probability points on the base outcome, also spawn `risk_red_team` on the disagreement summary.

Efficiency rules:
1. Gather one shared evidence packet before spawning agents. Include exact timestamp/timezone, BTC spot and volume context, BTC dominance, ETH/BTC, funding/open interest, major macro markets, and the next dated catalyst. Prefer primary or authoritative sources.
2. Give every spawned agent the same packet. Do not let them independently rebuild it unless they identify a material missing or conflicting fact.
3. For killa_quant, macro_liquidity, and any spawned specialist except bang_technician, require each memo to contain only: bias, confidence 0-100, three decisive facts, bull/base/bear weights in 10-point increments totaling 100%, invalidation, and one alt-market implication. For bang_technician, keep the native $TICKER plan format, then the compact council block (timestamp/TF, invalidation, bull/base/bear, one objection). Do not rewrite Bang into the compact research memo.
4. Do not run a debate when the directional conclusions broadly agree. If any agent differs by at least 30 probability points on the base outcome, send only a short disagreement summary to the disagreeing agents and permit one rebuttal each.
5. Wait for all active agents, then synthesize. Do not blindly average probabilities: discount stale evidence, unsupported claims, and correlated signals.

Final output, maximum 900 words:
- Timestamp and data gaps
- BTC 1D and 1W regime
- Bull/base/bear table with triggers and invalidation
- BTC dominance and ETH/BTC implication
- Whether conditions favor BTC only, large-cap alts, broad alts, memes, or no-trade/watch mode
- Top three things to monitor next
- Agent disagreement, if material

Never fabricate live data or recommend leverage. This is educational scenario research, not personalized financial advice.
```
