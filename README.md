# Prop Selling — public pick tracker

A free, public record of every pick, plus Instagram story images that pull from that record.

- `index.html`: public record page (record, units, ROI, win rate, streak, pending picks, full history). Put this link in your Instagram bio.
- `story.html`: makes 1080×1920 story images, with a "Today's picks" version for before games and a "Results" version for after.
- `scripts/picks.mjs`: adds and grades picks.
- `data/picks.json`: holds every pick. `data/config.json` holds your brand name, handle, paywall link and disclaimer.

## One-time setup

1. Edit `data/config.json` with your brand name, Instagram handle, and the link people use to pay (`joinUrl`).
2. Make the repo public and turn on GitHub Pages: Settings → Pages → Deploy from branch → `main` / root. The site will be live at `https://tylerhong3-creator.github.io/propselling/`.
3. Put that URL in your Instagram bio.

## Daily routine

Before games:

```bash
node scripts/picks.mjs add --sport NBA --game "Lakers @ Celtics" --pick "Lakers +4.5" --odds -110 --units 1
git commit -am "Picks for today" && git push
```

Pushing the commit before tip-off gives each pick a public timestamp. Open `story.html`, choose "Today's picks", download the PNG, and post it.

After games:

```bash
node scripts/picks.mjs list --pending
node scripts/picks.mjs grade 1 win      # win | loss | push | void
git commit -am "Results" && git push
```

Open `story.html` again, choose "Results", and post that image too. Post it on losing days as well.

`node scripts/picks.mjs record` prints your overall record. You can also edit `data/picks.json` directly in the GitHub app on your phone.

To preview the site locally, run `python3 -m http.server` and open http://localhost:8000. Opening the file directly from your computer won't load the data.
