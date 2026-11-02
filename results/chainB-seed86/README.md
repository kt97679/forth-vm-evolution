# Chain B's readings (Iteration 587) - kept so the next session compares

From chain aee0a409c's re-packed archive (fury, 2026-11-02 16:06-19:02); read by results/final-pick-chainB-seed86.md and
results/drafts/chainB-agreement-587.py; final-pick.py takes the out.json files and loadtest.md as they are.

- `loadtest.md` - the laptop: loadtest.py --ids results/shortlist-seed86.md --rounds 5, the 40 alone and under load at both widths (its table, then one JSON line a design).
- `dream.lan-prebuilt32.md`, `dream.lan-prebuilt32.out.json` - dream at 4-byte cells: its report and its readings (the 40 and 4 sampled).
- `dream.lan-prebuilt64.md`, `dream.lan-prebuilt64.out.json` - dream at 8-byte cells, the same designs.
- `rage.lan-prebuiltarm.md`, `rage.lan-prebuiltarm.out.json` - the Tegra (ARMv7, 4-byte cells): 237 designs at 2 rounds - the 232 candidates, 1 msc design, 4 sampled; JIT designs measured with the JIT off.
