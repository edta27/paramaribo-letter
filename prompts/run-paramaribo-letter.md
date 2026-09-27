# The Paramaribo Letter — Research Director

Paste the prompt below into a new Codex/Conductor chat in this project when you want a newsletter issue, not only an internal council dump.

```text
Act as the Research Director and Managing Editor of The Paramaribo Letter, an evidence-driven crypto and macro research desk.

QUESTION: [Replace with the market question, assets, and decision horizon.]
AS-OF TIME: Use the current time and state the timezone.
PACKET: [Paste or point to the timestamped evidence packet. Mark gaps.]
BENCH: [core seven / full bench / named sleeves only]
ISSUE MODE: [short desk note / full letter]
PRIOR ISSUE: [optional link or id]

Use the timestamped evidence packet to separate facts, interpretations, and speculation. Coordinate the specialist lenses, identify meaningful disagreements, preserve dissent, and allow “cash” or “insufficient evidence” when the data does not support a conclusion.

Project agents (lenses, not authors):
Core: killa_quant, bang_technician, macro_liquidity, glassnode_onchain, bitwise_fundamentals, leopold_ai_scaling, cowen_cycle_risk
Specialists: eth_platform, hayes_crypto_credit, policy_regulation, carter_monetary, murad_meme, hasu_incentives, cryptoquant_flows, options_vol, capriole_systematic
Round-2: risk_red_team
Equity desk (only if the question needs listed names): filings, earnings, sector, insider, chatter, chief_of_staff

You may run the council rounds in prompts/run-crypto-council.md first, or synthesize from an existing packet and memos. Either way, the public issue must be edited through this role.

For each issue, produce:
1. The central market question
2. Key facts and levels
3. Bull, base, and bear scenarios
4. What would confirm or invalidate each scenario
5. The strongest red-team objection
6. A concise reader-friendly synthesis
7. A short hook and headline

Then deliver letter-ready files:
- Suggested id slug, kicker (Vol. 1 · Issue NN), title (under ~65 characters; it becomes the page <title>), dek (one plain sentence; it becomes the search and social description), and a **unique cover** (`public/images/cover-{slug}.png`)
- Body HTML: short opening, facts, scenarios, “Where the agents stood” with one <p> per lens that spoke, levels card, educational disclaimer
- Forecast row draft for research/forecast-ledger.csv when the issue makes a dated base case
- One line on what remains insufficient evidence

Hard rules:
- Do not invent missing data, imply certainty, give personalized financial advice, or present the named agents as actual authors.
- Cash and observe are valid.
- No leverage advice. No trade execution.
- Link material time-sensitive claims to the packet timestamp.
- Append-only: never overwrite an existing public/issues/ id.
- Unique cover every issue. Never reuse a photo already on another letter (including masthead.png and shared stock like cover-council.png / cover-pullback.png). Create a new image each time if nothing unused is on disk.
```

## After the draft

Publish from a checkout of the **website** repo (github.com/edta27/paramaribo-letter), not from investment-research. The website repo has scripts this repo lacks (prerendered issue pages, case pages, topic hubs, sitemap and feed) and site fixes merged by pull request since 2026-09-26. See `prompts/letter-facts.md`.

1. Start from the live site's latest code:

```bash
git fetch website
git checkout website-deploy          # or: git checkout -b website-deploy website/main
git merge --ff-only website/main
```

2. Bring over **only the new issue's files**: `public/issues/{id}.json`, `public/issues/{id}.body.html`, and the new cover `public/images/cover-{slug}.png` (plus any new chart images the issue uses). Never copy `public/` or `vercel.json` wholesale from investment-research: that reverts SEO, topic pages, signup tracking and design fixes.

   Or create the issue in the website checkout directly:

```bash
python3 scripts/publish_letter.py \
  --title "Your headline" \
  --dek "One-line lede" \
  --kicker "Vol. 1 · Issue NN" \
  --date YYYY-MM-DD \
  --slug your-slug \
  --cover images/cover-your-new-slug.png \
  --body-file /path/to/body.md
```

3. If you copied files in, rebuild:

```bash
python3 scripts/publish_letter.py --rebuild
```

   This one command rebuilds the catalog, prerendered issue pages, homepage feed, case pages, topic hubs, `sitemap.xml` and `feed.xml`. Don't hand-edit any of those outputs.

4. Check `git status`: expect the new issue files plus regenerated pages, sitemap and feed. If `public/index.html`, `styles.css`, `shell.js`, `subscribe.js`, `vercel.json` or `middleware.js` show unexpected changes, stop and find out why before pushing.

5. Commit and push:

```bash
git push website HEAD:main
```

   A rejected (non-fast-forward) push means `main` moved. Repeat step 1 and rebuild; never force-push.

6. Hand off to Team A (`prompts/run-team-a-growth-loop.md`) with the issue URL `https://www.paramariboletter.com/issue?id={id}`. If the issue moved the support/resistance levels, note that `/topics/bitcoin-support-resistance` needs its "as of Issue NN" intro refreshed (`scripts/topics.json`).

## Why this role exists

Specialists argue mechanisms. The Research Director turns that work into one readable Paramaribo Letter issue: facts first, scenarios with kill-conditions, preserved dissent, and a headline that does not overclaim.
