# Gene usage: seed 59's front against seeds 53-58's (Iteration 403, HANDOFF items 4b and 4c)

`python3 lab/evolve/gene-usage.py results/evolve-amd-ryzen-7-pro-8840hs-seed59.md --vs results/evolve-amd-ryzen-7-pro-8840hs-seed53.md ... results/evolve-amd-ryzen-7-pro-8840hs-seed58.md`

Group 1: 171 front designs (evolve-amd-ryzen-7-pro-8840hs-seed59.md); group 2: 1093 (evolve-amd-ryzen-7-pro-8840hs-seed53.md, evolve-amd-ryzen-7-pro-8840hs-seed54.md, evolve-amd-ryzen-7-pro-8840hs-seed55.md, evolve-amd-ryzen-7-pro-8840hs-seed56.md, evolve-amd-ryzen-7-pro-8840hs-seed57.md, evolve-amd-ryzen-7-pro-8840hs-seed58.md) - an absent gene counted as off

| gene | group 1 on | group 2 on | difference |
|---|---|---|---|
| rtloopall | 65% | 9% | +56 |
| escape | 66% | 12% | +54 |
| supers | 65% | 12% | +53 |
| guard | 62% | 14% | +48 |
| tos | 54% | 93% | -39 |
| compiler | 65% | 30% | +35 |
| align1 | 16% | 47% | -31 |
| t2wide | 100% | 74% | +26 |
| regpin | 2% | 27% | -25 |
| opcall | 4% | 29% | -25 |
| opt | 94% | 70% | +24 |
| lto | 26% | 49% | -23 |
| threads | 67% | 89% | -22 |
| fbuf | 11% | 32% | -21 |
| dskew | 40% | 59% | -20 |
| hotinl | 56% | 38% | +18 |
| t2hot | 49% | 65% | -17 |
| tracer | 20% | 35% | -16 |
| tfind | 63% | 49% | +13 |
| bfind | 44% | 32% | +13 |
| nocet | 73% | 84% | -11 |
| noinls | 25% | 36% | -11 |
| peel | 13% | 23% | -11 |
| d256 | 13% | 4% | +10 |
| kfast | 94% | 84% | +9 |
| tag2 | 100% | 91% | +9 |
| varslot | 22% | 13% | +9 |
| jit | 50% | 58% | -8 |
| jitloop | 50% | 58% | -8 |
| alignfn | 66% | 58% | +8 |
| knumber | 11% | 4% | +7 |
| jitx | 50% | 57% | -7 |
| kstack | 9% | 2% | +6 |
| abortif | 12% | 5% | +6 |
| noreorder | 34% | 39% | -5 |
| gotodup | 19% | 23% | -4 |
| klookup | 36% | 32% | +3 |
| nocrossjump | 0% | 3% | -3 |
| jitimg | 4% | 1% | +3 |
| jitvar | 4% | 1% | +3 |
| hotcalls | 0% | 3% | -3 |
| fsys | 98% | 100% | -2 |
| jitos | 3% | 1% | +2 |
| opinline | 65% | 67% | -2 |
| factor | 89% | 87% | +2 |
| jittail | 37% | 35% | +2 |
| rtempty | 10% | 8% | +2 |
| ipaclone | 13% | 15% | -2 |
| jitk | 25% | 24% | +2 |
| rtimm | 6% | 4% | +1 |
| swapi | 37% | 36% | +1 |
| rtiplus | 5% | 4% | +1 |
| rtloop | 90% | 91% | -1 |
| rtfuse | 4% | 3% | +1 |
| opbody | 95% | 96% | -1 |
| kinput | 65% | 66% | -1 |
| jitinl | 50% | 50% | -1 |
| nogcse | 0% | 0% | -0 |
| bss | 100% | 100% | +0 |
| bytehdr | 100% | 100% | +0 |
| doesfar | 100% | 100% | +0 |
| enc | 100% | 100% | +0 |
| folds | 100% | 100% | +0 |
| lean | 100% | 100% | +0 |
| msc | 0% | 0% | +0 |
| ops10 | 100% | 100% | +0 |
| scale | 0% | 0% | +0 |
| spec | 100% | 100% | +0 |
| tail | 0% | 0% | +0 |
| thinhdr | 100% | 100% | +0 |
| varcall | 100% | 100% | +0 |
