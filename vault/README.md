# Shared vault

Specialists write here. `chief_of_staff` reads all five lanes, then writes `briefs/`.

```
vault/
  watchlist.md
  filings/
  earnings/
  sector/
  insider/
  chatter/
  briefs/
```

One file per run date, UTC date stamp `YYYY-MM-DD`. JSON inside Markdown fenced blocks is fine. Do not overwrite another agent's lane.

The original Grok-Bot desk used the same idea: narrow roles, shared storage, no cross-talk during inference, synthesizer in the morning. This repo keeps that loop in Codex agents rather than a separate Python orchestrator. Cron or a human can paste `prompts/run-equity-desk.md` overnight.

Open `desk/index.html` in a browser for the dark swarm / night-run / morning-brief board. It is a dry-run layout, not a live broker feed.
