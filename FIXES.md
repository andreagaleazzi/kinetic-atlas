# Fixes wanted

- [ ] **Timeline "Log intake" should open on the compound being viewed.** If the timeline is showing caffeine, the Log intake dialog should open with the caffeine tab already selected. The same goes for alcohol and nicotine.
  - Cause: the Timeline button is a plain `data-open="entryDialog"`. The handler only calls `openDialog(...)` and never syncs `entryType` with `chartType`, so the dialog opens on whichever tab was used last.
  - Likely fix: when opening from the timeline, call `setEntryType(chartType)` first. Only the Timeline button should do this; the other Log intake buttons (top bar, etc.) can keep their current behaviour.
