# The Paramaribo Letter

A local newsletter for desk notes. Issues are files. They are not deleted when you post again.

The Vercel website root is `public/`. The letter is `/`. The equity board is `/desk`.

```bash
python3 scripts/publish_letter.py --rebuild
python3 -m http.server 8766 --directory public
```

Open http://127.0.0.1:8766/

To add an issue without touching old ones:

```bash
python3 scripts/publish_letter.py --title "Headline" --dek "Lede" --cover images/cover-squeeze.png --body-file notes.md
```

If that id already exists, the script exits. Pick a new `--slug`.

## Vercel (team `michael-162c`)

Live: [https://paramaribo-letter-newsletter.vercel.app](https://paramaribo-letter-newsletter.vercel.app) (also [paramaribo-letter.vercel.app](https://paramaribo-letter.vercel.app)). Project `paramaribo-letter-newsletter` on team `michael-162c`. Framework: Other. Leave **Root Directory** empty. Vercel serves `public/` as the website root.
