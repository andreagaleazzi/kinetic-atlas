# Fixes wanted

Shipped items are in `FIXES_ARCHIVE.md`.

- [ ] **Combined tab: rainbow stripe should curve into the bottom corners like the other tabs.** For now `.tabs .all.active` uses a flat 2px gradient strip with no bleed, but it doesn't follow the corner radius. The other tabs use `box-shadow: inset 0 -2px`, which curves but only takes a solid colour.
  - Tried and dropped: (1) gradient `border-bottom` via padding-box/border-box backgrounds, which leaks ~1px of gradient at the anti-aliased top corners; (2) `::after` with `mask-composite: exclude`, which leaves a faint gradient ring because both mask layers anti-alias the same edge; (3) (1) plus a button-coloured underlay above the corner radius, which rendered cleanly in Chrome but the user still saw the corners as cut.
  - To try: an inline SVG or a `::after` limited to the bottom corner area (`top: auto; height: radius`, with `border-radius` only on the bottom corners), so no gradient layer shares the top or side edges. Check in Chrome, Safari and Firefox.
- [ ] **Confirm retailer-sourced pouch strengths against a can.** on! 9, Killa 13.2 and Pablo 10.15 / 17 / 30 mg come from UK retailer pages, not the manufacturer. LOOP and several other strengths were left out because only one source listed them (see `FIXES_ARCHIVE.md`). Update the `POUCH` table and `#sciPouch` together.
- [ ] **Nicotine y-axis shows repeated tick labels.** With small values the ticks read "2, 2, 1, 1, 0" because `renderChart` formats them with `fmt(v,0)`. Use enough decimals for the axis range.
- [ ] **Hour repeated when the clocks go back.** A time typed inside the repeated hour (for example 01:30 on the last Sunday of October) is always read as the first one, so editing an entry logged in the second one moves it an hour earlier. The old native picker behaved the same way.
- [ ] **Log intake keeps the last edited or duplicated product.** After closing an Edit or Duplicate without saving, the next plain Log intake opens on that entry's compound and preset (`clearEdit` resets note, quantity and time only).
- [ ] **Add tests.** There is still no test tooling. Start with the PK functions, then `parseDate` / `parseClock` and `pouchF`, which are pure.
