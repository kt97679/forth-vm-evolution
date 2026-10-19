# Gene usage on seeds 53-60's fronts together (Iteration 408, HANDOFF item 4b)

`python3 lab/evolve/gene-usage.py results/evolve-amd-ryzen-7-pro-8840hs-seed53.md ... -seed60.md`

1431 front designs (evolve-amd-ryzen-7-pro-8840hs-seed53.md, evolve-amd-ryzen-7-pro-8840hs-seed54.md, evolve-amd-ryzen-7-pro-8840hs-seed55.md, evolve-amd-ryzen-7-pro-8840hs-seed56.md, evolve-amd-ryzen-7-pro-8840hs-seed57.md, evolve-amd-ryzen-7-pro-8840hs-seed58.md, evolve-amd-ryzen-7-pro-8840hs-seed59.md, evolve-amd-ryzen-7-pro-8840hs-seed60.md), an absent gene counted as off

on in every design: bytehdr, doesfar, enc, folds, ops10, spec, thinhdr, varcall
on in none: msc, scale, tail

| gene | on | share | values |
|---|---|---|---|
| bytehdr | 1431 | 100% | 1 1431 |
| doesfar | 1431 | 100% | 1 1431 |
| enc | 1431 | 100% | "cv8" 1431 |
| folds | 1431 | 100% | ["+", "=", "!", "@", "LS 139, ["@", "SWAP", "AND", "DR 109, ["@", "+", "AND", "DROP" 90, ["@", "SWAP", "+", "AND" 86 |
| ops10 | 1431 | 100% | ["(FIND)", "(>NUMBER)",  322, ["SWAP+I", "THREAD-FIND" 282, ["THREAD-FIND", "SCAN",  207, ["?BRANCH8", "BRANCH8",  113 |
| spec | 1431 | 100% | ["loc", "var", "tiny", " 520, ["var", "tiny", "small", 370, ["loc", "tiny", "small", 275, ["tiny", "small", "imm"] 252 |
| thinhdr | 1431 | 100% | 1 1431 |
| varcall | 1431 | 100% | 1 1431 |
| bss | 1430 | 100% | 1 1430, "off" 1 |
| lean | 1429 | 100% | 1 1429, "off" 2 |
| fsys | 1427 | 100% | 2 1063, 3 299, 5 31, 1 17 |
| opbody | 1361 | 95% | 1 1361, "off" 70 |
| tag2 | 1334 | 93% | 1 1334, "off" 97 |
| rtloop | 1289 | 90% | 2 993, 1 296, "off" 142 |
| factor | 1264 | 88% | 3 784, 2 313, 1 167, "off" 167 |
| kfast | 1238 | 87% | 1 1238, "off" 193 |
| tos | 1219 | 85% | 1 1219, 0 212 |
| threads | 1203 | 84% | 3 1137, "off" 228, 1 40, 2 26 |
| nocet | 1168 | 82% | 1 1168, 0 263 |
| t2wide | 1131 | 79% | 1 1131, "off" 300 |
| opt | 1087 | 76% | "Os" 1082, "O2" 344, "O3" 5 |
| opinline | 957 | 67% | 1 957, "off" 474 |
| kinput | 903 | 63% | 1 903, "off" 528 |
| t2hot | 881 | 62% | "off" 550, 3 343, 2 321, 1 217 |
| dskew | 839 | 59% | 1 839, "off" 592 |
| alignfn | 837 | 58% | 1 837, "off" 594 |
| jit | 777 | 54% | 1 777, "off" 654 |
| jitloop | 775 | 54% | 1 775, "off" 656 |
| jitx | 761 | 53% | 1 761, "off" 670 |
| tfind | 760 | 53% | 1 760, "off" 671 |
| jitinl | 688 | 48% | "off" 743, 1 688 |
| lto | 614 | 43% | "off" 817, 1 614 |
| compiler | 570 | 40% | "off" 861, 1 570 |
| hotinl | 551 | 39% | "off" 880, 10 339, 20 173, 40 39 |
| align1 | 550 | 38% | "off" 570, 1 550, 0 311 |
| jittail | 498 | 35% | "off" 933, 1 498 |
| noreorder | 496 | 35% | "off" 570, 1 496, 0 365 |
| swapi | 492 | 34% | "off" 939, 1 492 |
| noinls | 476 | 33% | "off" 955, 1 476 |
| bfind | 471 | 33% | "off" 960, 1 471 |
| klookup | 465 | 32% | "off" 966, 1 465 |
| tracer | 431 | 30% | "off" 1000, 1 431 |
| fbuf | 400 | 28% | "off" 1031, 1 298, 2 102 |
| escape | 362 | 25% | 0 1069, 1 301, 2 61 |
| guard | 351 | 25% | 0 1080, 1 351 |
| opcall | 328 | 23% | "off" 1103, ["@"] 116, ["0="] 102, ["1+"] 57 |
| jitk | 319 | 22% | "off" 1112, 3 319 |
| regpin | 309 | 22% | "off" 1122, 1 289, 3 16, 2 4 |
| supers | 288 | 20% | [] 1143, [[">R", "C!"], ["SWAP",  53, [[">R", "C!"], ["DROP",  25, [["DUP", "@"], ["R>", "D 24 |
| peel | 285 | 20% | "off" 1146, 1 285 |
| gotodup | 280 | 20% | "off" 1151, 1 169, 2 111 |
| rtloopall | 259 | 18% | "off" 1172, 1 259 |
| varslot | 207 | 14% | 0 1224, 1 207 |
| ipaclone | 202 | 14% | "off" 1229, 1 202 |
| rtempty | 167 | 12% | "off" 1264, 1 167 |
| d256 | 99 | 7% | 0 1332, 1 99 |
| abortif | 86 | 6% | "off" 1345, 1 86 |
| rtimm | 78 | 5% | "off" 1353, 2 43, 1 35 |
| kstack | 77 | 5% | "off" 1354, 1 77 |
| rtfuse | 64 | 4% | "off" 1049, 0 318, 1 64 |
| knumber | 60 | 4% | "off" 1371, 1 60 |
| rtiplus | 56 | 4% | "off" 1375, 1 56 |
| jitimg | 36 | 3% | "off" 1395, 1 36 |
| jitvar | 34 | 2% | "off" 1397, 1 34 |
| nocrossjump | 31 | 2% | 0 830, "off" 570, 1 31 |
| hotcalls | 28 | 2% | "off" 1403, 32 23, 8 4, 16 1 |
| jitos | 12 | 1% | "off" 1419, 1 12 |
| nogcse | 4 | 0% | 0 857, "off" 570, 1 4 |
| msc | 0 | 0% | 0 1219, "off" 212 |
| scale | 0 | 0% | 0 1431 |
| tail | 0 | 0% | 0 1219, "off" 212 |
