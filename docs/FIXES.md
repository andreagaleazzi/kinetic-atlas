# Fixes wanted

Shipped items are in `FIXES_ARCHIVE.md`.

- [ ] **Confirm retailer-sourced pouch strengths against a can.** on! 9, Killa 13.2 and Pablo 10.15 / 17 / 30 mg come from UK retailer pages, not the manufacturer. LOOP and several other strengths were left out because only one source listed them (see `FIXES_ARCHIVE.md`). Update the `POUCH` table and `#sciPouch` together.
- [ ] **Blood curve: cigarette peak comes out low.** At 75 kg the cigarette preset (1.2 mg, 5 min, ka 28) peaks at 9.1 ng/mL, against 12–16 in the literature and the ~10–15 target; pouches come out 18–37% high. Both errors point at how fast intake is spread, not only at the 1.3 L/kg central volume: a smaller volume lifts the cigarette and pushes pouches further out. Decide whether to accept it (the dialog says so), shorten the cigarette's modelled intake, or refit. Update `#sciBlood`, the test's ranges and `docs/change-impact.md` together.
- [ ] **Link the blood-model sources.** `#sciBlood` names the Hukkanen/Benowitz review (2.6 L/kg) and the 2020 Clin Pharmacokinet population model (7 min) without links. Add both to the sources list once the exact references are confirmed.
- [ ] **Add tests.** `tests/pk.test.js` covers the nicotine blood curve only (it lifts the PK block out of `index.html`). Next: the mg curves (`amountFor`, `pouchAmount`) and `alcoholScenario`, then `parseDate` / `parseClock` and `pouchF`, which are pure.
