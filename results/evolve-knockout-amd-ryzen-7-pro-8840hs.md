# What each gene is worth - knockouts on the Ryzen 7 PRO 8840HS

`evolve.py --knockout 38d187239c,5b70f3dd64,83cb81c383` at 058a79c, 6
rounds, pinned to cpu 2, on the front of the first run
(`evolve-amd-ryzen-7-pro-8840hs-seed1.md`). Each gene that differs from
hand-made s6 was set back to s6's value, one at a time; the change is in
CPU time against the design measured in the same session. Every figure
measured.

Calibration: s6 against itself 1.003, size exactly 10,065. The designs
measured again in the session: 38d187239c 0.636 (run 0.623), 5b70f3dd64
0.671 (0.663), 83cb81c383 0.701 (0.686) - about 2% of run-to-run noise,
so changes under ~2% are not findings.

| gene undone | 38d187239c (13,480 B) | 5b70f3dd64 (9,801 B) | 83cb81c383 (9,761 B) |
|---|---|---|---|
| escape - with the pairs and words in its slots | +27.6% | +31.9% | +37.1% |
| superinstructions (all pairs) | +16.6% | +27.5% | +34.7% |
| guard pages for the stack checks | +19.3% | +8.9% | (not set) |
| relf's format-10 opcodes | +8.3% | +6.2% | +13.6% |
| -fcf-protection=none (no endbr64) | +8.1% | +5.6% | +13.2% |
| multi-state caching | +2.4% (tail calls instead) | +8.9% (tail calls instead) | +5.0% |
| byte headers on (scale 3 -> 0 with them) | +21.3%, 3,671 B smaller | | |
| scale 3 -> 0 | +9.6% | | |
| -fno-crossjumping | | | +7.9% |
| -fno-reorder-blocks | +0.9% | +0.5% | |
| specialisations as s6's | | | -2.7% |
| folds as s6's | | | -1.4% |

**What carries the 40%:** the escape and the superinstructions it makes
room for - in every design the largest; then guard pages instead of an
explicit bound check on every push; relf's format-10 opcodes; and
dropping the endbr64 that -fcf-protection puts at every handler's entry
(the dispatch lab, on the VM, had found that last one did not carry
over - on the Ryzen it is worth 6-13%). Multi-state caching, on every
design of the front, is worth only 2-9% - against tail calls, which
undoing it wakes in two of the three, 2-9%.

**How this can mislead** (prompts/03): each figure is a gene in its
design, interactions included - they do not add up; the escape's figure
includes the pairs and words its slots hold; and noise is ~2%.
