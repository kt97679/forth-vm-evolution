# Every gene's byte cost, and the profile tables refreshed (Iteration 519)

The owner asked, while seed 72 runs: does any other gene hide a cost like jitexec's 585 KB table (results/drafts/
jit-genes-517.md)? And are the profile tables, measured long before the applications joined the selection, stale?

**The sweep** (lab/evolve/genecost.py, the report below): seed 71's fastest JIT design (f83a64a706), a mid-front
interpreter (dc03d9535d) and the smallest (995c41c0a3), every gene of their family not frozen switched in turn, built,
the engine and image bytes compared - 92 switches, every one built. **Only jitexec is out of line** (+586,544, fixed in
the after-seed-72 batch). The rest cost what their mechanisms imply: the JIT itself about 17 KB (off: -17,739, and tos
or tag2 off with it), jitk 3,240, interpreter genes at most 3.8 KB (tag2 3,688, d256 2,656, escape 2,576, hotcalls
2,464). The genes seed 71 voted against are cheap - rtfuse +360, d256 +208 to +2,656, hotinl +48, rtempty +40, lto
+-160: what the search weighs there is speed against size, not a hidden penalty.

**The profile tables** (hotinl's hot call sites, factor's cold words, tag2's ranking - Iterations 92, 267, 66), made
again from seed 71's front with the project's tools - kept as lab/evolve/hotsites-v2.json (its fastest),
hotwords-v2.json (three of the front), tag2-rank-v2.json (two old-format designs: the tool counts one-byte codes as the
old format numbers them - on tag-2 designs its ranking is garbage). tag2-rank.py also needed to skip the profiler's
newer line kinds (I, C, W, T): fixed. The tables differ (?BRANCH, LIT32, OVER rank higher; XOR, >R lower), but a gene
choosing them (prof2, tried in a clone) bought nothing measurable - instructions on the seven, fair pairs:

| | f83a64a706 | b0116306e3 | bytes |
|---|---|---|---|
| the new ranking alone | 0.0% | 0.0% | 0 |
| hotinl 10, the new sites against the old | -0.2% | -0.2% | 0 |

The ranking only orders operations that all have one-byte codes in these designs; the hot sites move by noise. factor's
cold words could not be tried: the two smallest factor designs picked do not express it now. **Not made a gene**
(simplicity, and rule 11: no workload pays for it); the tables kept for a later look.

---

pinned to cpu 0 (it and its sibling 1% busy; BENCH_CPU=N to choose)
# What each gene costs in bytes (lab/evolve/genecost.py)

Each design's genes of its family, not frozen, one at a time to another value; built when the design then expresses something else. Bytes: the engine file and the image, against the design as it is.

## f83a64a706 (cv8, speed 0.1426): engine 36708, image 8032 bytes

| gene | from | to | engine | image | together |
|---|---|---|---|---|---|
| jitexec | 0 | 1 | +586544 | +0 | +586544 |
| jit | 1 | 0 | -17540 | -199 | -17739 |
| tos | 1 | 0 | -17412 | -199 | -17611 |
| tag2 | 1 | 0 | -16548 | -168 | -16716 |
| jitk | 3 | 0 | -3240 | +0 | -3240 |
| alignfn | 0 | 1 | -2352 | +0 | -2352 |
| kfast | 1 | 0 | -1840 | +208 | -1632 |
| kinput | 1 | 0 | -1824 | +208 | -1616 |
| jitfuse | 0 | 1 | +1472 | +0 | +1472 |
| t2wide | 1 | 0 | +1184 | +152 | +1336 |
| jitx | 1 | 0 | -1072 | +0 | -1072 |
| jittail | 1 | 0 | -976 | +0 | -976 |
| guard | 0 | 1 | +848 | +0 | +848 |
| klookup | 1 | 0 | -864 | +64 | -800 |
| fsys | 0 | 1 | -1312 | +512 | -800 |
| bfind | 0 | 1 | +736 | +0 | +736 |
| varslot | 1 | 0 | -544 | +0 | -544 |
| compiler | 1 | 0 | -520 | +0 | -520 |
| jitinl | 1 | 0 | -512 | +0 | -512 |
| knumber | 0 | 1 | +464 | +40 | +504 |
| escape | 1 | 2 | +496 | -8 | +488 |
| threads | 1 | 2 | +0 | +440 | +440 |
| jitdoes | 0 | 1 | +436 | +0 | +436 |
| rtiplus | 0 | 1 | +48 | +368 | +416 |
| jitcfa | 1 | 0 | -368 | +0 | -368 |
| rtfuse | 0 | 1 | +32 | +328 | +360 |
| rtloopall | 1 | 0 | +48 | +304 | +352 |
| tfind | 0 | 1 | +320 | -24 | +296 |
| d256 | 0 | 1 | +208 | +0 | +208 |
| jitret | 0 | 1 | +144 | +0 | +144 |
| jitvar | 0 | 1 | +128 | +0 | +128 |
| jitmul | 1 | 0 | +128 | +0 | +128 |
| opbody | 1 | 0 | +0 | +96 | +96 |
| jitimg | 1 | 0 | +0 | -80 | -80 |
| factor | 0 | 1 | +96 | -28 | +68 |
| hotinl | 0 | 10 | +0 | +48 | +48 |
| abortif | 1 | 0 | +0 | -48 | -48 |
| rtempty | 0 | 1 | +16 | +24 | +40 |
| opinline | 1 | 0 | +0 | +8 | +8 |
| t2hot | 2 | 3 | +0 | +0 | +0 |
| jitloop | 1 | 0 | +0 | +0 | +0 |
| fbuf | 0 | 1 | +0 | +0 | +0 |
| dskew | 0 | 1 | +0 | +0 | +0 |

## dc03d9535d (cv8, speed 0.4964): engine 8712, image 8694 bytes

| gene | from | to | engine | image | together |
|---|---|---|---|---|---|
| tag2 | 0 | 1 | +3808 | -120 | +3688 |
| d256 | 0 | 1 | +2656 | +0 | +2656 |
| escape | 0 | 1 | +2560 | +16 | +2576 |
| hotcalls | 0 | 8 | +2624 | -160 | +2464 |
| kfast | 1 | 0 | -1440 | +272 | -1168 |
| kinput | 1 | 0 | -1184 | +240 | -944 |
| compiler | 0 | 1 | +864 | +0 | +864 |
| regpin | 3 | 0 | +768 | +0 | +768 |
| klookup | 1 | 0 | -736 | +88 | -648 |
| noinls | 1 | 0 | +608 | +0 | +608 |
| fsys | 2 | 3 | -1256 | +675 | -581 |
| knumber | 0 | 1 | +384 | +40 | +424 |
| rtiplus | 0 | 1 | -32 | +384 | +352 |
| rtfuse | 0 | 1 | +0 | +336 | +336 |
| rtloopall | 1 | 0 | +0 | +296 | +296 |
| tfind | 1 | 0 | -288 | +32 | -256 |
| alignfn | 1 | 0 | +224 | +0 | +224 |
| bfind | 0 | 1 | -204 | +0 | -204 |
| opbody | 1 | 0 | +0 | +168 | +168 |
| lto | 1 | 0 | +160 | +0 | +160 |
| threads | 3 | 0 | +0 | +153 | +153 |
| tos | 1 | 0 | +96 | +0 | +96 |
| guard | 1 | 0 | -96 | +0 | -96 |
| abortif | 0 | 1 | +0 | +56 | +56 |
| gotodup | 2 | 0 | -32 | +0 | -32 |
| varslot | 0 | 1 | +0 | +0 | +0 |
| opinline | 1 | 0 | +0 | +0 | +0 |
| fbuf | 0 | 1 | +0 | +0 | +0 |
| dskew | 1 | 0 | +0 | +0 | +0 |

## 995c41c0a3 (cv8, speed 1.7628): engine 4920, image 9290 bytes

| gene | from | to | engine | image | together |
|---|---|---|---|---|---|
| tag2 | 0 | 1 | +2152 | +447 | +2599 |
| compiler | 1 | 0 | +2400 | +0 | +2400 |
| escape | 0 | 1 | +1928 | +0 | +1928 |
| kinput | 0 | 1 | +1324 | -129 | +1195 |
| d256 | 0 | 1 | +880 | +0 | +880 |
| guard | 0 | 1 | +320 | +0 | +320 |
| fsys | 3 | 4 | +128 | +188 | +316 |
| hotcalls | 32 | 0 | -192 | +495 | +303 |
| tfind | 0 | 1 | +300 | +0 | +300 |
| threads | 3 | 0 | +0 | +160 | +160 |
| abortif | 0 | 1 | +0 | +80 | +80 |
| tos | 0 | 1 | +48 | +0 | +48 |
| varslot | 0 | 1 | +0 | +0 | +0 |
| kfast | 1 | 0 | +0 | +0 | +0 |
| fbuf | 1 | 2 | +0 | +0 | +0 |
| dskew | 1 | 0 | +0 | +0 | +0 |
| alignfn | 0 | 1 | +0 | +0 | +0 |

**Over 10 KB**: tos on f83a64a706 (1 -> 0): -17611 bytes; tag2 on f83a64a706 (1 -> 0): -16716 bytes; jit on f83a64a706 (1 -> 0): -17739 bytes; jitexec on f83a64a706 (0 -> 1): +586544 bytes.
