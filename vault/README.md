# Shared vault

Specialists write here. `chief_of_staff` reads all five lanes, then writes `briefs/`.

```
vault/
  watchlist.md
  tickers/{SYM}.json   # last quote + recent EDGAR index per name
  live/snapshot.json   # full watchlist snapshot for the board
  filings/
  earnings/
  sector/
  insider/
  chatter/
  briefs/
```

One file per run date, UTC date stamp `YYYY-MM-DD`. JSON inside Markdown fenced blocks is fine. Do not overwrite another agent's lane.

The original Grok-Bot desk used the same idea: narrow roles, shared storage, no cross-talk during inference, synthesizer in the morning. This repo keeps that loop in Codex agents rather than a separate Python orchestrator. Cron or a human can paste `prompts/run-equity-desk.md` overnight.

**Automatic per-ticker refresh** (quotes + EDGAR index only — not the six-agent brief):

```bash
python3 scripts/update_tickers.py           # once
python3 scripts/update_tickers.py --loop 300  # every 5 minutes while the terminal stays open
```

That writes `vault/tickers/{SYM}.json`, `vault/live/snapshot.json`, and `desk/live.js`. Open `desk/index.html` afterward; the tape and brief table are the live snapshot. GitHub Action `.github/workflows/equity-desk.yml` repeats this on weekdays at 09:00 / 13:00 / 20:00 UTC after it is merged to the default branch. No trades and no email.

The six-agent LLM pass is still a separate paste of `prompts/run-equity-desk.md`. Use `vault/live/snapshot.json` as the quote/filing packet so agents do not invent prices.
