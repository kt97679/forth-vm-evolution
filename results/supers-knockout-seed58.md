# Do superinstruction pairs buy anything in tag-2 designs? Seed 58's front, knocked out (Iteration 385)

HANDOFF item 1 (results/drafts/supers-tag2.md, decided at Iteration 368): "if no front design builds a real
pair, or a knockout shows superinstructions buy nothing, the supers gene comes out of tag-2 designs". Seed 58,
the first run with the pool named right, answered the first half: 73 of its front's 74 tag-2 designs build
pairs. This is the second, by lab/evolve/supers-knockout.py - each design built as it is and with its supers
gene emptied, the profiler's dispatches over the six selection workloads (deterministic: this VM's noise does
not enter), and binary + image.

**They buy something - so the gene stays in tag-2 designs, by the rule of Iteration 368.** Over 19 of the 73
(every fourth by size, and the extremes) the pairs cut dispatches by 0.9% at the median (ratio 0.9907; from
nothing to 2.5%, the most at the small end - the 642ec43577 family, 2.4%). Their bytes run from -1,024 to +719
(median +216): in 6 of the 19 the design is smaller with its pairs than without. The control, d1e2c6b7de
(building none), changed by nothing; every as-built size equals its record's.

Two qualifications. The saving is in dispatches - in these JIT designs only those the JIT leaves to the
interpreter - so in time it is under 1%, inside the 2% within which selection counts speeds as tied: the speed
part is nearly invisible to selection, the bytes are not. Measuring the time is the laptop's (evolve.py
--knockout), if wanted. And 2 of the 19 carry pairs that never execute - 14ec7cd739 (+216 bytes) and
d79a57826d (+112), dispatches unchanged: each dominated by its own knockout, a mutation away.

---

# Superinstruction pairs knocked out - evolve-amd-ryzen-7-pro-8840hs-seed58.md

73 tag-2 designs of the front build pairs; 19 measured (every 4-th by size, the extremes), and d1e2c6b7de, building none, as the control. Dispatches summed over kernel, fib, corpus, loop, bubble, ackermann; a ratio below 1 is pairs saving dispatches.

| design | pairs built | binary + image | without pairs | bytes the pairs cost | dispatches | without pairs | ratio, geometric mean over workloads | largest saving |
|---|---|---|---|---|---|---|---|---|
| 642ec43577 | >R C!; SWAP R>; DROP !; DUP >R; @ RSHIFT; OVER C@; < +; R@ @; C@ >R | 25,207 | 24,791 | +416 | 14,611,611 | 15,050,376 | 0.9757 | corpus 0.9692 |
| 7e0996063e | >R C!; SWAP R>; DROP !; DUP >R; @ RSHIFT; OVER C@; < +; R@ @; C@ >R | 25,399 | 24,887 | +512 | 14,611,611 | 15,050,376 | 0.9757 | corpus 0.9692 |
| 17c5d098fa | >R C!; SWAP R>; DROP !; DUP >R; @ RSHIFT; OVER C@; < +; R@ @; C@ >R | 25,602 | 25,155 | +447 | 14,078,663 | 14,517,266 | 0.9748 | corpus 0.9679 |
| 9d1ca7198b | >R C!; SWAP R>; DROP !; DUP >R; R> =; DUP C@; < +; U< U< | 25,894 | 25,526 | +368 | 9,003,200 | 9,160,965 | 0.9849 | fib 0.9800 |
| c878b6904e | < +; >R OVER; R> =; DUP R@; C@ DUP; ROT ROT; DUP @ | 26,080 | 25,746 | +334 | 9,275,647 | 9,357,727 | 0.9925 | loop 0.9906 |
| 975bb3fe83 | >R C!; SWAP R>; DUP >R; DUP C@; >R >R; C@ OR; @ RSHIFT | 26,124 | 25,830 | +294 | 9,045,242 | 9,230,109 | 0.9836 | corpus 0.9782 |
| 032b7f295f | SWAP R>; DROP !; DUP >R; DUP C@; C@ OR | 26,217 | 26,025 | +192 | 8,797,455 | 8,955,176 | 0.9845 | fib 0.9795 |
| 9e94d5f910 | SWAP R>; DROP !; OVER C@ | 27,354 | 28,378 | -1024 | 5,355,328 | 5,417,941 | 0.9947 | corpus 0.9863 |
| 603da58d39 | DROP !; DUP >R; R> = | 27,513 | 27,345 | +168 | 5,495,169 | 5,554,133 | 0.9915 | corpus 0.9882 |
| a9c3404b3b | C! R>; >R OVER; SWAP R>; OVER R> | 28,617 | 28,651 | -34 | 9,203,600 | 9,247,787 | 0.9954 | loop 0.9928 |
| bb76117b80 | >R C!; SWAP R>; DROP !; DUP >R | 28,859 | 28,619 | +240 | 8,706,122 | 8,813,418 | 0.9899 | corpus 0.9874 |
| 14ec7cd739 | DROP !; R> =; C@ OR; RSHIFT < | 29,173 | 28,957 | +216 | 9,986,929 | 9,986,929 | 1.0000 | kernel 1.0000 |
| a5bcfa57fb | >R C!; SWAP R>; DROP !; DUP >R; >R >R; C@ OR; @ RSHIFT; ROT ROT; OVER C@; RSHIFT <; R@ @; ROT >R; ROT DUP; >R OVER; OVER R> | 30,116 | 29,397 | +719 | 8,583,388 | 8,857,641 | 0.9776 | corpus 0.9669 |
| 3f68b61e9e | DUP C@; @ RSHIFT; < +; RSHIFT <; DUP @; SWAP DUP | 30,236 | 31,084 | -848 | 5,616,386 | 5,675,343 | 0.9907 | fib 0.9865 |
| a239400b79 | DUP C@; @ RSHIFT; < + | 30,361 | 30,401 | -40 | 5,649,819 | 5,708,809 | 0.9913 | corpus 0.9878 |
| f4e8a8340a | DUP C@; @ RSHIFT; < + | 30,485 | 30,517 | -32 | 5,290,738 | 5,349,728 | 0.9907 | corpus 0.9869 |
| 52917e2595 | R> =; C@ OR; ROT ROT; DUP R@ | 31,221 | 32,157 | -936 | 5,221,697 | 5,224,933 | 0.9997 | kernel 0.9984 |
| 1a3e559904 | DROP !; R> =; C@ OR; OVER C@ | 34,325 | 34,101 | +224 | 5,224,949 | 5,280,296 | 0.9953 | corpus 0.9872 |
| d79a57826d | DROP !; R> =; C@ OR | 36,213 | 36,101 | +112 | 5,233,566 | 5,233,566 | 1.0000 | kernel 1.0000 |
| d1e2c6b7de (control) | none | 30,702 | 30,702 | +0 | 5,373,074 | 5,373,074 | 1.0000 | kernel 1.0000 |

Over the 19 designs that build pairs: dispatch ratio median 0.9907, range 0.9748-1.0000; bytes the pairs cost median +216, range -1024 to +719.

Size check: every design as it is built to the bytes its record holds.
