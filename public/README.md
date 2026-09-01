# The Paramaribo Letter

A local newsletter for desk notes. Issues are files. They are not deleted when you post again.

- Live site: [paramaribo-letter.vercel.app](https://paramaribo-letter.vercel.app) (also [paramaribo-letter-newsletter.vercel.app](https://paramaribo-letter-newsletter.vercel.app))
- GitHub: [edta27/paramaribo-letter](https://github.com/edta27/paramaribo-letter)
- Agents: [/agents.html](https://paramaribo-letter.vercel.app/agents.html)
- Equity desk: [/desk](https://paramaribo-letter.vercel.app/desk/)

The Vercel website root is `public/`. The letter is `/`. The equity board is `/desk`.

```bash
python3 scripts/publish_letter.py --rebuild
python3 -m http.server 8766 --directory public
```

Open http://127.0.0.1:8766/

To add an issue without touching old ones:

```bash
python3 scripts/publish_letter.py --title "Headline" --dek "Lede" --cover images/cover-new-unique.png --body-file notes.md

Every issue needs its own cover. Do not reuse another issue's photo; create `public/images/cover-{slug}.png` if needed.
```

If that id already exists, the script exits. Pick a new `--slug`.

## Vercel (team `michael-162c`)

Project `paramaribo-letter-newsletter` on team `michael-162c`, linked to this GitHub repo (`edta27/paramaribo-letter`). Framework: Other. Output directory is `public/`. Production domains: `paramaribo-letter.vercel.app` and `paramaribo-letter-newsletter.vercel.app`.

Pushes to `main` deploy the site. The GitHub Action **Equity desk ticker refresh** runs on weekdays (09:00 / 13:00 / 17:00 / 21:00 UTC), updates `public/desk/live.js`, commits, and that push redeploys `/desk` with fresh quotes.

**Web Analytics:** pages load Vercel’s `/_vercel/insights/script.js` (static HTML, not the Next.js React package). Enable Web Analytics in the Vercel project dashboard if it is not already on, then visit a few pages after deploy.

## New subscribers (email list)

Emails are **not** stored in git. They live in [Resend](https://resend.com) Contacts (optional Segment). The homepage and each issue page have a **New subscribers** form that posts to `/api/subscribe`.

When `public/catalog.json` changes on `main` and the featured issue id is new, the **Notify letter subscribers** GitHub Action calls `/api/notify`, which emails every active contact a short notice with a link to the issue.

### One-time setup

1. Create a Resend account. Verify a sending domain (or use `onboarding@resend.dev` for tests to your own inbox only).
2. Optional: create a Segment named “Paramaribo Letter” and copy its id.
3. In the Vercel project `paramaribo-letter-newsletter`, set environment variables (Production **and** Preview if you test previews):
   - `RESEND_API_KEY`
   - `RESEND_FROM_EMAIL` — verified domain, e.g. `The Paramaribo Letter <letter@paramariboletter.com>` (not `@gmail.com`)
   - `RESEND_REPLY_TO` — optional human inbox, e.g. `paramariboletter@gmail.com`
   - `RESEND_SEGMENT_ID` — optional
   - `NOTIFY_SECRET` — long random string
   - `SITE_URL` — `https://www.paramariboletter.com`
4. In **both** GitHub repos that can push `public/catalog.json` to the live site (`edta27/paramaribo-letter` and, if used, `edta27/investment-research`), add Actions secret `NOTIFY_SECRET` (same value). Optional variable: `SITE_URL`.
5. Redeploy the Vercel project so `/api/subscribe` picks up the env vars. Until keys are set, the form returns a clear “not configured” error.

Manual notify after a publish:

```bash
NOTIFY_SECRET=... python3 scripts/notify_subscribers.py
```

See `.env.example` for the full list.
