# The article's figures checked (Iteration 659; `python3 tools/article-check.py --self-test`, exit 0)

```
self-test: a digit changed (26 242 -> 26 224) and a number dropped (13 883) in a copy of the Russian draft - named, and nothing else
1. English and Russian: 23 sections, 0 with different numbers
2. distinctive figures of the English draft: 197, 195 of them in the records as written (318503 numbers in the records; found is not traced - the same digits can be another quantity)
   not found: 13380 (# Making a Forth virtual machine smaller)
   not found: 8108 (## 8. Attempt seven: the last place cell)
```

By hand, the two figures not in the records: both come out of the build at a105e59, the ladder article's commit
(2026-09-28, built in a fresh clone): s0-cell-k32.img 13,380 B, s5-cv8spec-k32.img 8,108 B; 8,108 is also 11,088 - 2,980,
both recorded. Part one's image sizes regenerate there and not at master - forth/kernel.4 changed 11 times since (to
Iteration 248) and every run-only image grew:

| run-only image | a105e59 | master (658) | grown |
|---|---|---|---|
| s0-cell, 4-byte cells | 13,380 | 14,976 | +11.9% |
| s0-cell, 8-byte cells | 24,320 | 27,264 | +12.1% |
| s5-cv8spec, 4-byte cells | 8,108 | 8,820 | +8.8% |
| s5-cv8spec, 8-byte cells | 11,088 | 11,776 | +6.2% |
| s6-cv8b, 4-byte cells | 6,749 | 7,497 | +11.1% |
| s6-cv8b, 8-byte cells | 7,609 | 8,385 | +10.2% |

s6 against s0 at 8-byte cells: 0.313 then, 0.308 now. The article says everything here regenerates from the
repository; for part one that holds at a105e59 - the owner's call: a tag and a sentence, or part one measured again.
