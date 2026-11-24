# Change impact

Before changing something, find it here: **Hits** lists what must change in the same commit, and **Does not hit** lists what looks related but isn't. Names are explained in [architecture.md](architecture.md). If this page and the code disagree, fix this page.

## Rules for every change

- Locale is UK: `en-GB` formatting, day-first dates, UK units, NHS/999 wording. 24-hour time is the default; 12-hour is a profile option.
- Showing the method is part of the feature: `#scienceDialog` must describe what the code does.
- Never phrase a result as "under the limit means fit or legal to drive". The key and tooltip say the curve is an estimate.
- Interpolated user text goes through `esc()`. New icons are a `<symbol>` in the sprite, never a Unicode glyph.
- Never call `toLocaleTimeString` with a fixed hour cycle; go through `displayTime` / `tf()` / `tickLab` / `hm`.

## If you change…

| Change | Hits (same commit) | Does not hit |
|---|---|---|
| A preset in `P` (fields or order) | `setEntryType`, `assignPreset`, `getFormDose`, which read by index. Nicotine's group is at index 6, not 4. Renaming or removing an id: saved entries keep their `preset` id, and editing one falls back via `presetData` to the type's last preset. | Saved curves: entries keep their own `dose` and `ka`. |
| The pouch row, `POUCH` brands or mg | `fillPouch`; the brand strength sources in `#sciPouch`. Keep `presetData`'s `pouch3`…`pouch12` fallback, which old saved entries need. | `pouchF`: the brand sets the label and mg only. |
| `POUCH_FMAX`, `POUCH_TAU` or `pouchF` | `#sciPouch` parameters and sources. | Brand table. |
| A PK formula or default (`ka`, half-life, `r`, `beta`, bands) | `#scienceDialog` in the same change. Any future PK tests. | Stored entries (the series is recomputed on every render). |
| `validateEntry` / `normalizeProfile` | They are the data schema and the future server validation. Tighten only; never loosen. Old exports must still import. | Rendering. |
| The entry shape | `validateEntry`, `exportJSON`, `exportCSV`, `editEntry` (and so `duplicateEntry`), the future DB row. | `KEY`, unless old data can no longer be read. |
| `KEY` (storage key) | Every user's saved data becomes invisible. Needs a migration path, as the `kinetic_atlas.html` → `index.html` README note does for the file rename. | Nothing else. |
| The `exportJSON` format (`version:2`) | The importer, and the future account import path. Keep v2 readable. | `exportCSV`. |
| What `editEntry` prefills | `duplicateEntry` duplicates it too. | — |
| What the canvas draws (series, lines, legal lines) | `.legend` spans, `#plotUnit`, `#plotNote`, which `exportPNG` labels the image from. | — |
| `chartType` handling | `'all'` (Combined, `drawCombined`, `plotScale`) is not a series key. | — |
| `REGIONS` or `LIMITS` | The "checked" date in the code comments, `#sciLaw` and `#lawKey`. | The model, UK unit counts and UK guidance cards, which `region` never changes. |
| Date/time fields or parsing | `parseDate` / `parseClock`; entry time only via `getEntryTime()` / `setEntryTime(ms)`. | Stored format: ISO `time`, 24h `HH:MM` for `bed` / `wake`. |
| A state mutation | Route it through `transaction(fn)` so undo, `persist()` and `renderAll()` happen. | — |
| A colour, type, spacing, radius or shadow | `docs/brand/tokens.json`, then `python3 docs/brand/build_tokens_css.py`, **and** the app's `:root` block and literal colours in `renderChart`. No raw colour without a token. | `docs/brand/tokens.css` by hand: it is generated. |
| UI, copy, chart or export look | Read `docs/brand/README.md` first; `docs/brand/charts.md` for charts. | — |
| A component's look or class names | `docs/brand/components.css`, `components.md` and `gallery.html` together, plus the matching rules in `index.html`'s `<style>`. | `tokens.json`, unless a value changes. |
| Anything that sends a request or adds a backend | Rewrite the "Data handling" block in `#scienceDialog`, the privacy, GDPR and cookie text in `#legalDialog` (it promises no collection, no cookies and no controller) and the Privacy section of `README.md`. Adding any cookie or a second storage key means updating "Cookies & storage" there too. | — |
| The page title, tagline, brand look or site URL | The `og:*` / `twitter:card` tags in `index.html`'s `<head>`, and `/og.png`: edit `docs/brand/og.html`, then re-render with the command at its top. | — |
| A fix from `docs/FIXES.md` | Move the item to `docs/FIXES_ARCHIVE.md` when it ships. | — |
