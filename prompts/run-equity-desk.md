# Equity Research Desk (Grok-Bot pattern on Codex)

Overnight-style six-agent desk: five specialists write independently into a shared vault; `chief_of_staff` synthesizes at the end. Specialists do not cross-talk. Cash/no-trade and dry-run are valid. Paste into a new Codex/Conductor chat. Select Sol High when available.

This is educational research, not a broker, not an email server, and not personalized advice. Do not send external messages unless the user wrote `APPROVE_SEND`.

```text
Run the six-agent equity research desk.

WATCHLIST: [Default: vault/watchlist.md. Maximum 20 tickers for this Codex run.]
AS-OF TIME: Use the current time and state the timezone.
MODE: [Default: dry-run. Write APPROVE_SEND only if a human is allowed to email the brief.]
LOOKBACK: [Default: last 7 calendar days of filings, transcripts, Form 4s, and 13Fs.]

Use these project-scoped agents:
Round 1, in parallel, no cross-talk: filings, earnings, sector, insider, chatter
Round 2 only: chief_of_staff

You are the moderator, not a forecaster. Do not let agents impersonate issuers, funds, or regulators.

Round 0 — packet
1. Establish as-of timestamp and timezone.
2. Load the watchlist. If more than 20 names, cut to 20 and say so.
3. Gather one shared packet from primary sources: last close, next dated catalyst, EDGAR links for recent 10-K/10-Q/8-K, any retrieved earnings transcript or 8-K exhibit, Form 4 / 13F if available, and one sector headline per industry. Mark paywalled, delayed, or missing series. Never substitute memory for live data.
4. Give every Round-1 agent the same packet. They may verify only critical gaps.

Round 1 — independent flags
Spawn filings, earnings, sector, insider, and chatter in parallel. They must not see each other's memos. Each writes structured flags only (ticker, date, source, severity 1-5, quote or stat, URL). Chatter may compute 3σ vs a 30-day mention baseline only if that series is in the packet; otherwise insufficient evidence. Insider must label 13F lag and 10b5-1 vs open-market. Wait for all five.

Round 2 — chief of staff
Send chief_of_staff the five flag lists and the packet, not a chatty debate. It must drop flags raised by only one specialist, except EDGAR-primary events with a retrieved accession (going-concern, restatement, auditor change, or the 8-K that is the event). Rank survivors. Produce a one-page morning brief plus an unsent email draft. Do not email unless MODE is APPROVE_SEND.

Write outputs as if saving to:
- vault/filings/{date}.md
- vault/earnings/{date}.md
- vault/sector/{date}.md
- vault/insider/{date}.md
- vault/chatter/{date}.md
- vault/briefs/{date}.md

If you can write those files in the workspace, do so. If not, paste them in the reply in that order.

Hard rules:
- Never fabricate filings, quotes, Form 4s, mention counts, or 13F holdings.
- Do not execute trades, size positions, or recommend leverage.
- A single-source rumor is noise. Multi-agent confirmation is the filter.
- Start small. A 20-ticker dry-run beats an untested 3,000-name book.
```

## How to read the brief

1. **Single-source filter:** if only chatter or only sector mentioned it, it should not be in the ranked list unless it is a retrieved EDGAR event.
2. **13F is lagged.** A fund name in a 13F is not a live book.
3. **No send.** The email body is a draft until a human sets `APPROVE_SEND`.

## Cadence

Nightly or pre-market. Do not run the crypto council in the same session. After a stable loop, add a post-mortem on `review-forecast.md` for equity flags you choose to score.
