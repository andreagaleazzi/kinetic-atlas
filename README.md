# Kinetic Atlas

A personal substance tracker. Log alcohol, caffeine and nicotine intake and see an estimated blood alcohol concentration (BAC %), caffeine (mg) and nicotine (mg) curve over time, with uncertainty bands, the next peak, and UK guidance.

**For education only. Not medical advice, and never a way to decide whether you are fit or legal to drive.**

## Run it

It is a single static file with no build step and no dependencies.

- Open `index.html` in a browser, or
- serve the folder: `python3 -m http.server 8000`, then visit <http://localhost:8000/>.

Any static host (GitHub Pages, Netlify, Cloudflare Pages, S3) can serve the repo root as is.

## Privacy

Everything stays in your browser's `localStorage`. The app makes no network requests. Use **Export JSON** in the app to back up or move your data.

Browser storage is tied to where the page is opened from. If you used the old `kinetic_atlas.html` file directly, export JSON there first and import it into `index.html`.

## How it works

- Caffeine and nicotine: a one-compartment model with first-order absorption and elimination.
- Alcohol: the Widmark formula with constant-rate elimination.
- Parameters, thresholds (EFSA caffeine limits, UK units, drink-driving limits per region) and sources are shown in the app under **How it's calculated**.

## Repository layout

| Path | What it is |
| --- | --- |
| `index.html` | The whole app: markup, styles and script |
| `docs/brand/` | Branding and style core: tokens, components, chart rules, logos (start with `docs/brand/README.md`) |
| `docs/FIXES.md` | Open fixes and to-dos |
| `docs/FIXES_ARCHIVE.md` | Shipped fixes |
| `docs/architecture.md` | Map of `index.html`: script sections, state, PK model, entry shape |
| `docs/change-impact.md` | What else must change when you change something |
| `CLAUDE.md` | Entry point for coding agents: routing and conventions |

## Contributing

Commits follow [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:` …). See `CLAUDE.md` for the code structure and rules.

## Roadmap

A web app with a backend, database and user accounts is planned. The PK model will be split into a tested standalone module first.
