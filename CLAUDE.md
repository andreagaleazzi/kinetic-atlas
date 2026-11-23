# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Kinetic Atlas: a personal exposure tracker that models alcohol (BAC %), caffeine (mg) and nicotine (mg) over time from logged intake. It is for education, not medical use, and the UI says so.

**Today** it is one self-contained file, `kinetic_atlas.html` (~120 KB, minified-style long lines). It has no build step, no dependencies and no network calls, and it stores data in `localStorage`.
**Planned:** a proper web app with a backend, a database and user accounts. Keep the current file working until that migration actually starts. Code added now should not block the split described under "Migration direction".

## Commands

- Run: open `kinetic_atlas.html` in a browser, or serve it with `python3 -m http.server 8000` and visit `/kinetic_atlas.html`.
- There is no build, lint or test tooling yet. When you add tests, start with the pharmacokinetic (PK) math (see below). It is pure, and it is the part where a mistake actually matters.
- Lines are thousands of characters long. Find code with `grep -n` or `grep -o` plus `cut -c`, not by reading whole lines.

## Git workflow

- After finishing a coherent chunk of work, **ask the user whether to commit it** instead of leaving it uncommitted. Never commit without their go-ahead.
- Use Conventional Commits: `<type>: <short imperative summary>`, e.g. `feat: add combined timeline tab`, `fix: open Log intake on the viewed compound`, `docs: add icon and time-format items to FIXES.md`. Types: `feat`, `fix`, `docs`, `refactor`, `style`, `test`, `chore`. Add a scope when it helps (`fix(chart): ...`).
- One logical change per commit. Keep code (`kinetic_atlas.html`) and docs (`CLAUDE.md`, `FIXES.md`) in separate commits unless the docs describe that exact code change and must stay in sync.

## Architecture (single file)

Layout: `<head><style>` → one hidden SVG icon sprite (`<symbol id="i-…">`) → markup (`<main id="top">`, plus `<dialog id="profileDialog">` and `<dialog id="scienceDialog">`) → one `<script>` holding a strict-mode IIFE. No globals leak out.

Inside the script, in order:

1. **Constants and presets.** `KEY='kinetic-atlas-offline-v2'` (storage key), `defaults` (profile), and `P`, the drink/product presets. Presets are **positional arrays**, not objects, and the layout differs by type: alcohol and caffeine use `[id, label, volume, abv|mg, group]`, while nicotine adds duration and absorption fields and keeps its group at index 6. `setEntryType` / `assignPreset` / `getFormDose` read them by index, so keep them in sync when you edit presets. Nicotine pouches are one `pouch` row plus the `POUCH` table (`{brand: [mg,…]}`, filled into `#pouchBrand` / `#pouchMg` by `fillPouch`); the brand only sets the label and mg. `presetData` maps the legacy ids `pouch3`…`pouch12` in old saved entries to that row, so don't drop that fallback.
2. **State.** `state = {profile, profileSet, entries[]}`, plus UI vars (`entryType`, `chartType`, `plotScale`, `horizon`, `series`, `historyStack`, `editId`, `dupOpen`). `chartType` is a compound or `'all'` (the Combined tab, drawn by `drawCombined` on a relative 0–1 or log-mg axis per `plotScale`), so don't assume it indexes a series. Every mutation goes through `transaction(fn)`, which pushes an undo snapshot (max 10), calls `persist()`, then `renderAll()`.
3. **Trust boundaries.** `validateEntry` and `normalizeProfile` clamp and validate everything loaded from storage or JSON import. Import is capped at 2 MB. These define the de facto data schema, so they become the server-side validation later. Don't loosen them.
4. **PK model** (pure functions):
   - `instantAmount` / `amountFor`: one-compartment model with first-order absorption (`ka`) and elimination (`ke = ln2/half-life`). Intake is spread evenly over `durationMin`.
   - `alcoholScenario`: the absorbed ethanol fraction (`absorbedFrac`) is converted to BAC with Widmark `r`, then reduced at a constant `beta` %/h down to 0.
   - `buildSeries(now)`: a 5-minute grid from −96 h to +72 h. Each point holds a central `v` plus `low` and `high` uncertainty bands. Alcohol bands come from r ±0.06 and the clearance range; caffeine and nicotine bands from half-life ×0.7 and ×1.5.
   - `at`, `peakNext` and `settledTime` interpolate and query `series`.
5. **Dates and times.** `profile.clock` (`'24h'` default, or `'12h'`) drives every displayed time through `displayTime` / `tf()` / `tickLab` / `hm`. Never call `toLocaleTimeString` with a fixed hour cycle. Date and time entry uses plain text fields, not native pickers (their format follows the OS locale): `#entryDate` + `#entryClock` in Log intake, `#pBed` / `#pWake` in Profile, parsed by `parseDate` / `parseClock`. Read and write the entry time only through `getEntryTime()` / `setEntryTime(ms)`. Stored values are unchanged: entry `time` is ISO, `bed` / `wake` are 24h `HH:MM`.
6. **Rendering.** `renderAll` recomputes `series` and redraws everything: summary, `renderChart` (hand-drawn `<canvas>`, DPR-aware, no chart library), `renderHistory`, `renderLedger`, `renderInterpretation` and `renderProfileSummary`. HTML is built from template strings, so interpolated user text must go through `esc()`. Icons come from the sprite via `ic(name)` (or `<svg class="ic" aria-hidden="true"><use href="#i-name"/>` in static markup): add a `<symbol>` for a new icon, never a Unicode glyph. `renderChart` draws dose markers in the gutter under the x-axis (`doseMarks`) and adds the nearby doses to `#chartTooltip`. `renderInterpretation` hides `#guideSec` unless a card applies to the current data. A `setInterval` runs `renderAll` every 60 s while the tab is visible.
7. **Wiring.** `addEventListener` calls near the bottom, using delegated clicks (`data-action`, `data-close`). History rows offer `edit`, `duplicate` and `delete`; `duplicateEntry` reuses `editEntry`'s prefill and then clears `editId`, so anything `editEntry` restores is duplicated too. Export/import is `exportJSON` (`{app, version:2, profile, entries}`) and `exportCSV`. `exportPNG` saves the chart as shown; it labels the image from the DOM (`.legend` spans, `#plotUnit`, `#plotNote`), so keep those in sync with what the canvas draws.

Entry shape (also the future DB row): `{id, type: 'alcohol'|'caffeine'|'nicotine', preset, label, time: ISO string, note, qty, durationMin, dose, ka, ...}`, plus type-specific fields: alcohol `units, volume, abv, food`; caffeine `mg, volume`; nicotine `mg, fraction`. IDs are generated on the client.

## Domain constraints

- The model parameters, guidance thresholds (EFSA caffeine limits, UK units) and cited sources are listed in `#scienceDialog`. If you change a formula or default, update that dialog in the same change. The app's stance is that showing the method is part of the feature.
- Locale is UK (`en-GB` formatting, day-first dates, UK units, NHS/999 wording). 24-hour time is the default; 12-hour is a profile option.
- Pouch absorption follows time in mouth: `pouchF(min) = POUCH_FMAX × (1 − e^(−min/POUCH_TAU))`, set when Duration changes on a pouch and still editable. The parameters, their sources and the brand strength sources are in `#sciPouch`.
- The "Data handling" block in `#scienceDialog` promises "no outbound requests" and local-only storage. Rewrite it as soon as any network or backend behaviour lands.

## Brand and design system

- `brand/` is the reference for the look, voice and chart style. Read `brand/README.md` before any UI, copy, chart or export change.
- `brand/tokens.json` is the source of truth for colours, type, spacing, radii and shadows. After editing it, run `python3 brand/build_tokens_css.py` to regenerate `brand/tokens.css`.
- `kinetic_atlas.html` still holds its own copy of these values (`:root` block and literal colours in `renderChart`). If you change a value the app uses, change it in `tokens.json` and in the app in the same change. Don't introduce raw colours that have no token.
- The web app should load `brand/tokens.css` and `brand/components.css` instead of copying values.

## Migration direction (backend, DB, users)

- Move the PK model (section 4) out first, into a standalone module with no DOM dependencies, so the browser and the server can share it and it can be unit-tested.
- The existing `exportJSON` format (version 2) is the natural path for importing local data into a new account. Keep it readable by the new system.
- The data is health-related (substance use, pregnancy, medications, liver condition), which counts as special-category personal data under UK GDPR. Plan for per-user authorization on every entry and profile access from the start.
