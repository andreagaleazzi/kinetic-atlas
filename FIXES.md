# Fixes wanted

- [ ] **Timeline "Log intake" should open on the compound being viewed.** If the timeline is showing caffeine, the Log intake dialog should open with the caffeine tab already selected. The same goes for alcohol and nicotine.
  - Cause: the Timeline button is a plain `data-open="entryDialog"`. The handler only calls `openDialog(...)` and never syncs `entryType` with `chartType`, so the dialog opens on whichever tab was used last.
  - Likely fix: when opening from the timeline, call `setEntryType(chartType)` first. Only the Timeline button should do this; the other Log intake buttons (top bar, etc.) can keep their current behaviour.
- [ ] **Replace emoji with proper icons.** Use real icons (inline SVG, e.g. a small hand-picked set) instead of emoji glyphs, which render differently per OS/font.
  - Symbols used as icons today: `⚠` (7), `＋` (6), `✕` (5), `◕` (3), `⇩` (2), `☕` (2), `◇` (2), `✓` (2), and one each of `⚙` (Profile button), `↶`, `↥`, `↑`, `↻`, `✧` (empty history), `✎` and `☾`. Find them with a Unicode scan, not `grep` (the long UTF-8 lines trip it up). `≈ ≥ ≤ →` are in-text math/arrows and can stay.
  - Keep it dependency-free and offline (no icon font or CDN): the file promises no outbound requests. Icon-only buttons keep their `aria-label`; mark the SVG `aria-hidden="true"`.
- [ ] **Time format setting (12h AM/PM or 24h) and European dates (dd/mm/yyyy).**
  - Add a profile setting for 12h or 24h, defaulting to 24h (UK locale). Every displayed time should follow it: the `toLocaleString` / `toLocaleTimeString` calls with `hour:'2-digit'` need `hourCycle:'h12'|'h23'` driven by the setting. The setting must also go through `normalizeProfile` and the JSON export.
  - Text output is already `en-GB`, so it shows day before month and 24h. The problem is the form inputs: the Log intake `datetime-local` and the two `type="time"` inputs use the browser/OS locale's native picker. HTML/JS can't set that picker's format, so on a US-locale system it shows mm/dd/yyyy and AM/PM.
  - Likely fix: replace those native inputs with a small custom date/time control (dd/mm/yyyy date plus a time field that follows the 12h/24h setting), keeping the stored value an ISO string. It must stay keyboard- and screen-reader-accessible.
- [ ] **Duplicate an entry from the history.** Add a "Duplicate" button next to Edit/Delete on each history row so a repeat drink/coffee/product can be logged in one step.
  - Today the row actions are `data-action="edit"` and `"delete"`, handled in the `historyList` click listener.
  - Likely fix: add `data-action="duplicate"` and reuse `editEntry(id)`'s form prefill, but leave `editId` null (so save creates a new entry with a fresh ID) and set the time to now instead of the original time. The user reviews and saves in the Log intake dialog, which keeps validation and undo going through the normal save path.
- [ ] **Brand-name nicotine pouch presets (UK best-sellers), without overcrowding the dropdown.**
  - Today pouches are generic by label strength: `pouch3/4/6/9/12` in `P.nicotine`. They use absorbed fraction 30%, duration 30 min and ka 2.5, with the group at index 6.
  - UK share, from the Haypp report covered by Convenience Store (the date isn't confirmed): VELO ~35%, Nordic Spirit ~14%, ZYN ~11%, On! ~5%, XQS ~5%. Pablo, Killa and LOOP are rising, mostly at very high strengths.
  - Starting list (mg per pouch, from manufacturer/retailer pages Nov 2026). **Check each one against the can or the manufacturer before shipping**, because sources disagree:
    | Brand | Strengths (mg/pouch) |
    |---|---|
    | VELO | 3, 6, 9 (plus higher X-Strong/Ultra lines; check) |
    | Nordic Spirit | 3 (Mini), 6, 9, 11 |
    | ZYN | 1.5, 3, 6, 8; Ultra 9, 11 |
    | On! | check |
    | XQS | ~8 (Strong), up to 12 (Extra Strong) |
    | LOOP | 9.4, 12.5, 15.6 (Slim Strong / Extra / Hyper) |
    | Killa | ~8.3–13.2 |
    | Pablo | ~10.5–30, sources conflict; some quote mg/**g** (e.g. 50 mg/g), not mg/pouch |
  - Key point for the design: brand doesn't change the model, only the mg value does. Every pouch shares the same fraction, duration and ka. So a brand preset is just a label plus an mg value, and the data can stay a small `{brand: [mg,...]}` table. That avoids dozens of positional preset rows.
  - Overcrowding strategy (recommended): a **two-step picker for pouches**. The type dropdown keeps one "Nicotine pouch" row (and the cigarettes, gum, patches and so on as today). Choosing it shows a **Brand** select (Generic, VELO, Nordic Spirit, ZYN, …) and a **Strength** select filled from that brand. Each list stays under ~10 items. The saved entry keeps `label` as "ZYN · 6 mg" and `preset` stays valid for `validateEntry`. Optional extra: a "Recent" optgroup at the top, built from the user's last few distinct entries, which needs no new storage.
  - Alternatives considered: a single type-to-filter field (`<input list>` + `<datalist>`) is native and scales, but it can't group items and looks different in every browser. A plain long list with optgroups is what we're trying to avoid.
  - Remember: list the strength sources and the "label mg ≠ absorbed mg" caveat in `#scienceDialog` (CLAUDE.md rule).
- [ ] **Pouch duration should change how much nicotine is absorbed.** Today it doesn't: `getFormDose` computes `dose = qty × mg × fraction`, and the pouch fraction is a fixed 30%. `durationMin` only spreads that same dose over time, so a 5-minute pouch and a 60-minute pouch absorb the same total.
  - Simple fix: when the user changes **Duration** on a pouch preset (group `'Oral nicotine'` only), update the **Estimated absorbed (%)** field with a saturating curve: `fraction = Fmax × (1 − e^(−dur/τ))`. With `Fmax ≈ 50%` and `τ ≈ 30 min` this gives ~14% at 10 min, ~32% at 30 min (≈ today's 30% default) and ~43% at 60 min. That's a few lines in the existing `entryDuration` input listener. The field stays editable as a manual override, and `getFormDose`, the stored entry and `validateEntry` don't change.
  - Don't apply it to patches (duration is the delivery window, already in delivered mg), cigarettes or vape (values are already absorbed estimates), or gum/lozenges (chewing pattern dominates; leave them for later).
  - Before shipping: find a cited source for `Fmax` and `τ` (pouch extraction vs. time-in-mouth studies), and add the formula and source to `#scienceDialog`, as the CLAUDE.md rule requires. Editing an old entry must keep its saved fraction: setting the field from code doesn't fire `input`, so it already does.
- [ ] **Neater dose-time markers on the timeline.** The current dose dot overlaps the curve, bands and gridlines and looks messy.
  - Cause: in `renderChart`, each entry of the shown compound is drawn as a 3px filled circle at 80% alpha (`ctx.arc(xx, pad.t+gh-3, 3, …)`), so it sits *inside* the plot area on the baseline, right where the curve, the low/high band and the bottom gridline meet. Doses close in time pile up into one blob.
  - Likely fix: move the markers out of the plot into the bottom gutter, as a small tick or upward-pointing triangle (~6px) just under the x-axis baseline (`pad.t+gh+1` to `+7`), above the date labels at `pad.t+gh+19` (`pad.b` is 37, so it fits). Optional: a faint dashed vertical guide from the marker up to the curve, drawn *before* the curve so it never covers it. Doses closer than a few px apart should merge into one marker with a count.
  - Bonus: when the hover line is within a few px of a marker, add the dose (label, qty, time) to the existing `chartTooltip`, so the marker is identifiable without opening History.
