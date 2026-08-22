# Buy-Low / Sell-High Plan

Use this when the question is exposure timing, not a full-market essay. It turns Capriole-style public confluence and Bang's HTF confirmation into one plan. Cash is a valid state. Paste into a new parent chat. Select Sol High when available.

```text
Build one confirmation-first buy-low / sell-high plan. Do not execute, size, or recommend leverage. This is educational scenario research, not personalized financial advice.

ASSET: [Default BTC. Replace only if you want a second ticker mapped after BTC.]
AS-OF TIME: Use the current time and state the timezone.
HORIZON: [Choose one: 1 week, 1 month, or full cycle.]
MODE: [Default: observe until confirmation. Write "include reduce/cash path" to force an explicit sell-high / cash plan even if no buy is armed.]

Spawn these project agents in parallel after one shared evidence packet:
- bang_technician
- capriole_systematic
- glassnode_onchain

Also spawn `cryptoquant_flows` if exchange or miner-to-exchange prints are needed to judge absorption vs issuance.
Also spawn `killa_quant` if derivatives, funding, or vol would change whether "low" is a trap.
Also spawn `cowen_cycle_risk` if a four-year-cycle or dominance claim is being used as the buy/sell reason.
Do not spawn the rest of the bench unless the user wrote "full bench".

Round 0 — packet
Gather one timestamped packet from primary sources. Include: spot and Daily/H4 structure; 20d/60d range; volume; BTC dominance and ETH/BTC; funding/OI if available; hash-rate context for Hash Ribbons (1-month vs 2-month hash-rate SMA if public); miner-capitulation evidence; SOPR / realized P-L / LTH vs STH behavior; Energy Value inputs only if they can be computed or cited; ETF or treasury demand versus daily mined supply; gold, USD, and the next dated catalyst.
Mark delayed, paywalled, or missing Capriole Charts. Never invent Hash Ribbon, Energy Value, SOPR, or volume-profile numbers. Never substitute memory for live data.

Definitions the agents must use:
- "Low" is not a round number and not "it already dumped." Low requires at least two independent public tells: HTF demand/sweep (Bang) and one on-chain or miner-timing tell (Hash Ribbon recovery, SOPR/LTH capitulation, Energy Value discount, or demand absorbing issuance).
- "High" is not a round-number target. High requires HTF supply/liquidity (Bang) plus one distribution tell (LTH spending, SOPR profit-taking, Energy Value premium, or demand failing to absorb issuance).
- Keep Capriole's two overlays separate: trend (price is an input) vs fundamentals (price is not an input). If they disagree, the plan is cash or observe, not a blended long.
- One constructive print is not a leveraged-long. A calendar four-year-cycle date is not a sell. A fund CAGR or paid chart is not a live position.
- bang_technician keeps its native $TICKER plan format. capriole_systematic returns exposure: leveraged-long / long / cash / short, labeled as public confluence vs unobserved proprietary model. glassnode_onchain confirms or kills the holder-behavior half of "low" and "high".

Until a stated Daily or H4 close prints, the plan is observe. "Buy the dip" with no confirmation is not a plan.

Final output, maximum 900 words:
1. Timestamp, sources, and data gaps.
2. Current exposure state: observe / cash / long-armed / reduce-armed. Say which overlay supports it.
3. Bang $TICKER plan (observation zone, confirmation close, entry only after confirmation, TP1/TP2/Final, invalidation).
4. Buy-low checklist: which "low" tells are present, missing, or conflicting.
5. Sell-high / cash checklist: which "high" tells would flip the plan, with zones or conditions.
6. What would keep the plan in cash even if price looks cheap.
7. Bull/base/bear in 10-point increments totaling 100%. Do not average the agents if the overlays disagree.
8. Reassessment trigger and the one fact that would invalidate the whole plan.

If the named asset is an alt or meme, map it only after the BTC plan. If H4/LP/holder data are missing, say insufficient evidence for that ticker and do not invent a beta.
```

## How to read the plan

1. **Observe** until the confirmation candle closes. A wick into a zone is not an entry.
2. **Buy-low** only if Bang's HTF demand confirmation and at least one Capriole/Glassnode tell agree.
3. **Sell-high or cash** when HTF supply confirms and holders start distributing, or when the price-excluded overlay turns against the trend overlay.
4. If those two overlays disagree, do nothing. That is the point of the plan.

Public methods only: [Hash Ribbons](https://capriole.com/hash-ribbons-bitcoin-bottoms/), [Energy Value](https://medium.com/capriole/bitcoin-value-energy-equivalence-6d00d1baa34a), holder/SOPR-style metrics, and HTF structure. Not live Capriole Fund holdings and not paid Trend King prints.
