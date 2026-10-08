# Knockouts of seed 30's front (Iteration 109)

`experiment evolve.py --knockout --rounds 6` after seed 30 and its comparison,
commit 09d024de2, on the laptop (cpu 1): 22 designs of the run's front (its
speed-size frontier), each gene undone in each, measured against hand-made
s6 run by run - calibration: s6 against itself 0.998, its image exactly. The
speed is the geometric mean over kernel, fib, parse and corpus (loop and the
sieve per workload only).

## Each gene's worth, over the designs that carry it

Slower without it (median, range) and the image's size without it (median):

| gene | designs | slower without it | range | image without it |
|---|---|---|---|---|
| kfast | 22 | +175.4% | +118.4% .. +203.9% | +160 |
| escape | 22 | +123.2% | +55.3% .. +162.5% | +859 |
| kinput | 22 | +67.8% | +54.0% .. +93.1% | +147 |
| ops10 | 22 | +50.9% | +4.3% .. +81.2% | +160 |
| rtloop | 16 | +50.7% | +30.7% .. +68.3% | -128 |
| jit | 7 | +47.0% | +44.0% .. +87.4% | -122 |
| klookup | 22 | +26.7% | +21.6% .. +49.7% | +56 |
| tag2 | 22 | +11.0% | -0.7% .. +86.6% | -165 |
| tos | 3 | +11.0% | +10.8% .. +14.9% | 0 |
| t2wide | 22 | +8.4% | +1.9% .. +20.1% | +203 |
| supers | 21 | +7.1% | -3.9% .. +13.9% | +24 |
| nocet | 22 | +6.7% | +0.6% .. +14.9% | 0 |
| swapi | 13 | +6.3% | -0.6% .. +16.3% | +8 |
| folds | 22 | +5.6% | -3.0% .. +11.4% | +8 |
| guard | 10 | +4.9% | +0.3% .. +7.8% | 0 |
| d256 | 7 | +4.4% | +1.5% .. +6.6% | 0 |
| rtfuse, rtimm | 3 | +3.4% | | -624, -304 |
| noreorder | 11 | +3.2% | -1.4% .. +16.1% | 0 |
| jitx | 5 | +2.6% | +1.2% .. +2.6% | 0 |
| hotinl | 6 | +1.9% | +1.5% .. +6.1% | -56 |
| nocrossjump, align1, ipaclone, opt, varslot, peel | 1-14 | +1.2% .. +1.9% | | 0 |
| bss | 22 | +0.8% | -3.0% .. +3.3% | +1,056 |
| lean | 22 | +0.7% | -2.8% .. +3.5% | +1,832 |
| thinhdr | 22 | +0.5% | -1.6% .. +3.0% | +248 |
| opbody | 22 | +0.1% | -2.8% .. +4.8% | +128 |
| rtloopall | 16 | -0.1% | -1.7% .. +3.8% | +424 |
| t2hot | 19 | -0.1% | -2.5% .. +2.2% | 0 |
| tracer | 15 | -0.2% | -2.5% .. +2.6% | 0 |
| tfind | 17 | -0.5% | -3.6% .. +2.6% | 0 |
| spec | 11 | -1.1% | -5.1% .. +3.3% | +8 |
| rtempty | 1 | -1.2% | | -36 |
| tail | 10 | -8.7% | -32.0% .. -1.3% | +125 |

How to read it: a gene is worth what removing it costs IN that design,
interactions included ("also changed" in the tables below); differences
smaller than the calibration's distance from 1.000 are noise. **The new
genes**: t2wide pays in both (8.4%, 203 bytes), opbody in bytes (128), hotinl
a little speed for 56 bytes, jitx 2.6% here - its sieve is held out.
**Worth about nothing where they are**: rtloopall (and 424 bytes - but the
speed here leaves out loop: see its per-workload column), t2hot, tracer,
tfind, spec - candidates to retire, for simplicity, the owner's decision.
**tail** buys 125 bytes for ~9% of speed: a size trade, kept where size
rules.

## The report

pinned to cpu 1 (it and its sibling 24% busy; BENCH_CPU=N to choose)
# Knockouts

machine: AMD Ryzen 7 PRO 8840HS w/ Radeon 780M Graphics; commit 09d024de2; 2026-10-08 19:27 UTC; taskset -c 1; 6 rounds; every figure MEASURED (none modelled): CPU time over
hand-made s6's, paired run by run, geometric mean over kernel, fib, parse, corpus; size of the self-hosting image.

How these can mislead (prompts/03): each knockout measures a gene IN this design - interactions included, so the
changes do not add up to the total; "also changed" names what moved with it (the escape takes its slots, and
with them pairs and words; a dormant gene can wake: undoing multi-state caching turns on tail calls the genome
carries); a difference smaller than the calibration's distance from 1.000 is noise.

calibration, s6 against itself: speed expected 1.000, measured 0.998; size expected 10065, measured 10065 - ok

## 4ddd323cee

calibration, the design itself: speed in the run 0.125, measured now 0.134; size recorded 7784, measured 7784 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers, tfind | 0.362 | +170.8% | 7920 | +136 | kernel 0.844 fib 0.143 parse 0.705 corpus 0.775 loop 0.094 sieve 0.558 |
| escape | 2 -> 0 | ops10, rtfuse, rtimm, rtloopall, supers | 0.341 | +155.5% | 8016 | +232 | kernel 0.585 fib 0.180 parse 0.159 corpus 0.262 loop 1.053 sieve 1.032 |
| ops10 | 30 items -> 0 items | rtloop, rtloopall, supers | 0.229 | +71.3% | 7952 | +168 | kernel 0.358 fib 0.144 parse 0.088 corpus 0.163 loop 0.847 sieve 0.754 |
| tag2 | 1 -> 0 | hotcalls, hotinl, jit, t2hot, t2wide | 0.225 | +68.7% | 7437 | -347 | kernel 0.322 fib 0.642 parse 0.097 corpus 0.146 loop 0.197 sieve 0.521 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.222 | +66.0% | 7904 | +120 | kernel 0.591 fib 0.139 parse 0.223 corpus 0.305 loop 0.096 sieve 0.603 |
| rtloop | 1 -> 0 | rtloopall | 0.214 | +59.9% | 7656 | -128 | kernel 0.286 fib 0.141 parse 0.075 corpus 0.140 loop 1.046 sieve 0.699 |
| jit | 1 -> 0 | - | 0.194 | +45.0% | 7654 | -130 | kernel 0.338 fib 0.642 parse 0.082 corpus 0.136 loop 0.113 sieve 0.497 |
| klookup | 1 -> 0 | ops10, supers | 0.169 | +26.9% | 7840 | +56 | kernel 0.359 fib 0.145 parse 0.139 corpus 0.201 loop 0.096 sieve 0.453 |
| t2wide | 1 -> 0 | - | 0.146 | +9.2% | 8096 | +312 | kernel 0.362 fib 0.144 parse 0.088 corpus 0.150 loop 0.096 sieve 0.517 |
| d256 | 1 -> 0 | - | 0.142 | +6.6% | 7784 | +0 | kernel 0.358 fib 0.141 parse 0.084 corpus 0.146 loop 0.095 sieve 0.535 |
| nocet | 1 -> 0 | - | 0.141 | +5.2% | 7784 | +0 | kernel 0.324 fib 0.143 parse 0.083 corpus 0.148 loop 0.096 sieve 0.513 |
| rtfuse | 1 -> 0 | rtimm | 0.140 | +5.0% | 7160 | -624 | kernel 0.297 fib 0.192 parse 0.078 corpus 0.130 loop 0.093 sieve 0.534 |
| guard | 1 -> 0 | - | 0.140 | +4.8% | 7784 | +0 | kernel 0.323 fib 0.141 parse 0.084 corpus 0.152 loop 0.092 sieve 0.493 |
| nocrossjump | 1 -> 0 | - | 0.140 | +4.5% | 7784 | +0 | kernel 0.349 fib 0.139 parse 0.082 corpus 0.142 loop 0.094 sieve 0.497 |
| noreorder | 1 -> 0 | - | 0.138 | +3.5% | 7784 | +0 | kernel 0.337 fib 0.143 parse 0.083 corpus 0.136 loop 0.093 sieve 0.477 |
| lean | 1 -> 0 | - | 0.138 | +3.5% | 10030 | +2246 | kernel 0.334 fib 0.138 parse 0.080 corpus 0.137 loop 0.100 sieve 0.527 |
| rtimm | 1 -> 0 | - | 0.138 | +3.3% | 7472 | -312 | kernel 0.293 fib 0.186 parse 0.074 corpus 0.127 loop 0.097 sieve 0.429 |
| supers | 17 items -> 0 items | - | 0.138 | +3.0% | 7808 | +24 | kernel 0.334 fib 0.141 parse 0.081 corpus 0.137 loop 0.094 sieve 0.479 |
| hotinl | 10 -> 0 | - | 0.137 | +2.7% | 7728 | -56 | kernel 0.299 fib 0.141 parse 0.083 corpus 0.147 loop 0.096 sieve 0.444 |
| rtloopall | 1 -> 0 | - | 0.136 | +1.5% | 8200 | +416 | kernel 0.322 fib 0.146 parse 0.076 corpus 0.135 loop 0.095 sieve 0.440 |
| folds | 20 items -> 23 items | supers | 0.135 | +1.0% | 7776 | -8 | kernel 0.313 fib 0.145 parse 0.077 corpus 0.137 loop 0.094 sieve 0.422 |
| opbody | 1 -> 0 | - | 0.135 | +0.8% | 7912 | +128 | kernel 0.322 fib 0.144 parse 0.076 corpus 0.132 loop 0.095 sieve 0.438 |
| t2hot | 1 -> 0 | - | 0.133 | -0.1% | 7784 | +0 | kernel 0.308 fib 0.142 parse 0.074 corpus 0.138 loop 0.094 sieve 0.436 |
| tracer | 1 -> 0 | - | 0.133 | -0.2% | 7784 | +0 | kernel 0.302 fib 0.139 parse 0.077 corpus 0.135 loop 0.096 sieve 0.430 |
| thinhdr | 1 -> 0 | - | 0.133 | -0.4% | 8032 | +248 | kernel 0.296 fib 0.139 parse 0.075 corpus 0.142 loop 0.095 sieve 0.440 |
| bss | 1 -> 0 | - | 0.133 | -0.4% | 8840 | +1056 | kernel 0.303 fib 0.143 parse 0.074 corpus 0.135 loop 0.096 sieve 0.437 |
| tfind | 1 -> 0 | ops10 | 0.133 | -0.7% | 7784 | +0 | kernel 0.290 fib 0.139 parse 0.076 corpus 0.139 loop 0.096 sieve 0.446 |
| spec | 4 items -> 5 items | - | 0.132 | -1.0% | 7784 | +0 | kernel 0.301 fib 0.141 parse 0.075 corpus 0.137 loop 0.093 sieve 0.422 |

## 853e145460

calibration, the design itself: speed in the run 0.126, measured now 0.135; size recorded 7776, measured 7776 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers, tfind | 0.363 | +168.4% | 7912 | +136 | kernel 0.835 fib 0.142 parse 0.721 corpus 0.770 loop 0.096 sieve 0.585 |
| escape | 2 -> 0 | ops10, rtfuse, rtimm, rtloopall, supers | 0.338 | +149.8% | 8024 | +248 | kernel 0.592 fib 0.184 parse 0.170 corpus 0.264 loop 0.901 sieve 0.882 |
| ops10 | 31 items -> 0 items | rtloop, rtloopall, supers | 0.233 | +72.1% | 7936 | +160 | kernel 0.376 fib 0.139 parse 0.088 corpus 0.159 loop 0.940 sieve 0.723 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.223 | +64.9% | 7896 | +120 | kernel 0.569 fib 0.141 parse 0.232 corpus 0.308 loop 0.097 sieve 0.561 |
| rtloop | 1 -> 0 | rtloopall | 0.220 | +62.2% | 7656 | -120 | kernel 0.315 fib 0.140 parse 0.074 corpus 0.150 loop 1.049 sieve 0.756 |
| tag2 | 1 -> 0 | hotcalls, hotinl, jit, t2hot, t2wide | 0.218 | +61.0% | 7445 | -331 | kernel 0.307 fib 0.632 parse 0.090 corpus 0.138 loop 0.205 sieve 0.492 |
| jit | 1 -> 0 | - | 0.203 | +49.7% | 7638 | -138 | kernel 0.326 fib 0.694 parse 0.080 corpus 0.137 loop 0.138 sieve 0.536 |
| klookup | 1 -> 0 | ops10, supers | 0.167 | +23.7% | 7816 | +40 | kernel 0.359 fib 0.143 parse 0.139 corpus 0.191 loop 0.097 sieve 0.486 |
| guard | 1 -> 0 | - | 0.146 | +7.8% | 7776 | +0 | kernel 0.390 fib 0.141 parse 0.087 corpus 0.147 loop 0.094 sieve 0.574 |
| t2wide | 1 -> 0 | - | 0.145 | +7.3% | 8088 | +312 | kernel 0.363 fib 0.139 parse 0.089 corpus 0.155 loop 0.093 sieve 0.531 |
| supers | 15 items -> 0 items | - | 0.145 | +6.8% | 7792 | +16 | kernel 0.344 fib 0.141 parse 0.090 corpus 0.147 loop 0.098 sieve 0.548 |
| nocet | 1 -> 0 | - | 0.144 | +6.1% | 7776 | +0 | kernel 0.359 fib 0.144 parse 0.087 corpus 0.147 loop 0.093 sieve 0.547 |
| noreorder | 1 -> 0 | - | 0.140 | +3.7% | 7776 | +0 | kernel 0.359 fib 0.140 parse 0.081 corpus 0.143 loop 0.094 sieve 0.534 |
| rtimm | 1 -> 0 | - | 0.140 | +3.4% | 7472 | -304 | kernel 0.306 fib 0.189 parse 0.074 corpus 0.129 loop 0.097 sieve 0.505 |
| rtfuse | 1 -> 0 | rtimm | 0.140 | +3.4% | 7152 | -624 | kernel 0.307 fib 0.184 parse 0.076 corpus 0.128 loop 0.097 sieve 0.553 |
| thinhdr | 1 -> 0 | - | 0.139 | +2.8% | 8024 | +248 | kernel 0.339 fib 0.143 parse 0.077 corpus 0.143 loop 0.098 sieve 0.498 |
| d256 | 1 -> 0 | - | 0.139 | +2.5% | 7776 | +0 | kernel 0.337 fib 0.142 parse 0.079 corpus 0.141 loop 0.096 sieve 0.525 |
| hotinl | 10 -> 0 | - | 0.138 | +2.0% | 7720 | -56 | kernel 0.326 fib 0.139 parse 0.083 corpus 0.136 loop 0.097 sieve 0.494 |
| nocrossjump | 1 -> 0 | - | 0.138 | +1.9% | 7776 | +0 | kernel 0.339 fib 0.143 parse 0.076 corpus 0.144 loop 0.094 sieve 0.562 |
| folds | 20 items -> 23 items | supers | 0.136 | +0.7% | 7792 | +16 | kernel 0.321 fib 0.143 parse 0.078 corpus 0.139 loop 0.094 sieve 0.505 |
| lean | 1 -> 0 | - | 0.136 | +0.6% | 10022 | +2246 | kernel 0.314 fib 0.145 parse 0.079 corpus 0.136 loop 0.095 sieve 0.538 |
| bss | 1 -> 0 | - | 0.135 | +0.0% | 8832 | +1056 | kernel 0.336 fib 0.139 parse 0.075 corpus 0.133 loop 0.097 sieve 0.480 |
| rtloopall | 1 -> 0 | - | 0.135 | -0.1% | 8192 | +416 | kernel 0.322 fib 0.139 parse 0.078 corpus 0.133 loop 0.098 sieve 0.486 |
| swapi | 1 -> 0 | ops10 | 0.135 | -0.4% | 7776 | +0 | kernel 0.301 fib 0.147 parse 0.076 corpus 0.139 loop 0.095 sieve 0.486 |
| tfind | 1 -> 0 | ops10 | 0.134 | -1.2% | 7776 | +0 | kernel 0.305 fib 0.142 parse 0.077 corpus 0.136 loop 0.094 sieve 0.490 |
| t2hot | 1 -> 0 | - | 0.132 | -2.4% | 7768 | -8 | kernel 0.304 fib 0.143 parse 0.077 corpus 0.130 loop 0.093 sieve 0.487 |
| tracer | 1 -> 0 | - | 0.132 | -2.5% | 7776 | +0 | kernel 0.295 fib 0.137 parse 0.075 corpus 0.139 loop 0.095 sieve 0.489 |
| opbody | 1 -> 0 | - | 0.132 | -2.6% | 7904 | +128 | kernel 0.299 fib 0.142 parse 0.074 corpus 0.131 loop 0.097 sieve 0.491 |

## 2777363fd3

calibration, the design itself: speed in the run 0.126, measured now 0.136; size recorded 7720, measured 7720 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers, tfind | 0.351 | +157.6% | 7880 | +160 | kernel 0.762 fib 0.138 parse 0.702 corpus 0.761 loop 0.095 sieve 0.536 |
| escape | 2 -> 0 | ops10, rtfuse, rtimm, rtloopall, supers | 0.346 | +154.0% | 7960 | +240 | kernel 0.514 fib 0.189 parse 0.171 corpus 0.284 loop 1.058 sieve 0.975 |
| ops10 | 31 items -> 0 items | rtloop, rtloopall, supers | 0.247 | +81.2% | 7896 | +176 | kernel 0.353 fib 0.142 parse 0.096 corpus 0.181 loop 1.064 sieve 0.807 |
| tag2 | 1 -> 0 | hotcalls, jit, jitx, t2hot, t2wide | 0.230 | +68.4% | 7445 | -275 | kernel 0.321 fib 0.699 parse 0.094 corpus 0.145 loop 0.209 sieve 0.581 |
| rtloop | 1 -> 0 | rtloopall | 0.224 | +64.3% | 7600 | -120 | kernel 0.289 fib 0.142 parse 0.083 corpus 0.150 loop 1.104 sieve 0.747 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.216 | +58.3% | 7864 | +144 | kernel 0.497 fib 0.141 parse 0.227 corpus 0.310 loop 0.095 sieve 0.626 |
| jit | 1 -> 0 | jitx | 0.200 | +46.8% | 7590 | -130 | kernel 0.374 fib 0.642 parse 0.085 corpus 0.139 loop 0.113 sieve 0.539 |
| klookup | 1 -> 0 | ops10, supers | 0.170 | +24.8% | 7768 | +48 | kernel 0.360 fib 0.143 parse 0.142 corpus 0.201 loop 0.097 sieve 0.114 |
| supers | 15 items -> 0 items | - | 0.145 | +6.7% | 7744 | +24 | kernel 0.319 fib 0.140 parse 0.093 corpus 0.164 loop 0.096 sieve 0.111 |
| d256 | 1 -> 0 | - | 0.144 | +5.3% | 7720 | +0 | kernel 0.322 fib 0.137 parse 0.091 corpus 0.159 loop 0.095 sieve 0.111 |
| rtimm | 1 -> 0 | - | 0.143 | +5.3% | 7416 | -304 | kernel 0.297 fib 0.184 parse 0.081 corpus 0.142 loop 0.097 sieve 0.126 |
| guard | 1 -> 0 | - | 0.143 | +4.8% | 7720 | +0 | kernel 0.329 fib 0.142 parse 0.088 corpus 0.154 loop 0.094 sieve 0.114 |
| nocet | 1 -> 0 | - | 0.142 | +4.3% | 7720 | +0 | kernel 0.320 fib 0.143 parse 0.089 corpus 0.153 loop 0.093 sieve 0.120 |
| align1 | 1 -> 0 | - | 0.141 | +3.5% | 7720 | +0 | kernel 0.309 fib 0.136 parse 0.093 corpus 0.151 loop 0.095 sieve 0.116 |
| rtfuse | 1 -> 0 | rtimm | 0.140 | +2.9% | 7088 | -632 | kernel 0.297 fib 0.184 parse 0.081 corpus 0.129 loop 0.096 sieve 0.113 |
| jitx | 1 -> 0 | - | 0.140 | +2.5% | 7720 | +0 | kernel 0.347 fib 0.140 parse 0.082 corpus 0.142 loop 0.093 sieve 0.492 |
| lean | 1 -> 0 | - | 0.139 | +2.2% | 9942 | +2222 | kernel 0.332 fib 0.141 parse 0.083 corpus 0.142 loop 0.095 sieve 0.109 |
| t2wide | 1 -> 0 | - | 0.139 | +2.1% | 7920 | +200 | kernel 0.300 fib 0.140 parse 0.090 corpus 0.144 loop 0.096 sieve 0.112 |
| thinhdr | 1 -> 0 | - | 0.139 | +1.8% | 7968 | +248 | kernel 0.319 fib 0.142 parse 0.085 corpus 0.144 loop 0.093 sieve 0.116 |
| folds | 19 items -> 23 items | supers | 0.138 | +1.4% | 7728 | +8 | kernel 0.306 fib 0.140 parse 0.084 corpus 0.147 loop 0.095 sieve 0.106 |
| bss | 1 -> 0 | - | 0.137 | +0.3% | 8776 | +1056 | kernel 0.312 fib 0.140 parse 0.080 corpus 0.145 loop 0.095 sieve 0.118 |
| rtloopall | 1 -> 0 | - | 0.136 | -0.4% | 8136 | +416 | kernel 0.294 fib 0.144 parse 0.079 corpus 0.143 loop 0.097 sieve 0.118 |
| noreorder | 1 -> 0 | - | 0.136 | -0.6% | 7720 | +0 | kernel 0.303 fib 0.136 parse 0.082 corpus 0.142 loop 0.096 sieve 0.113 |
| swapi | 1 -> 0 | ops10 | 0.136 | -0.6% | 7720 | +0 | kernel 0.308 fib 0.133 parse 0.081 corpus 0.145 loop 0.095 sieve 0.120 |
| tfind | 1 -> 0 | ops10 | 0.135 | -0.8% | 7720 | +0 | kernel 0.285 fib 0.137 parse 0.082 corpus 0.152 loop 0.092 sieve 0.102 |
| t2hot | 2 -> 0 | - | 0.135 | -1.1% | 7720 | +0 | kernel 0.300 fib 0.138 parse 0.082 corpus 0.141 loop 0.092 sieve 0.116 |
| opbody | 1 -> 0 | - | 0.134 | -1.5% | 7848 | +128 | kernel 0.291 fib 0.145 parse 0.081 corpus 0.138 loop 0.092 sieve 0.106 |
| nocrossjump | 1 -> 0 | - | 0.133 | -2.2% | 7720 | +0 | kernel 0.300 fib 0.139 parse 0.078 corpus 0.136 loop 0.095 sieve 0.116 |

## b98b7dc2db

calibration, the design itself: speed in the run 0.130, measured now 0.139; size recorded 7144, measured 7144 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers | 0.366 | +163.5% | 7288 | +144 | kernel 0.754 fib 0.190 parse 0.680 corpus 0.722 loop 0.093 sieve 0.568 |
| escape | 2 -> 0 | ops10, rtloopall, supers | 0.310 | +123.3% | 8016 | +872 | kernel 0.389 fib 0.186 parse 0.149 corpus 0.242 loop 1.095 sieve 0.874 |
| tag2 | 1 -> 0 | hotcalls, hotinl, jit, jitx, t2hot, t2wide | 0.238 | +71.8% | 6843 | -301 | kernel 0.303 fib 0.887 parse 0.094 corpus 0.143 loop 0.212 sieve 0.601 |
| ops10 | 31 items -> 0 items | rtloop, rtloopall, supers | 0.235 | +69.3% | 7288 | +144 | kernel 0.307 fib 0.183 parse 0.089 corpus 0.153 loop 0.939 sieve 0.832 |
| rtloop | 1 -> 0 | rtloopall | 0.224 | +61.7% | 7016 | -128 | kernel 0.288 fib 0.187 parse 0.076 corpus 0.133 loop 1.043 sieve 0.803 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.223 | +60.4% | 7272 | +128 | kernel 0.483 fib 0.186 parse 0.221 corpus 0.292 loop 0.094 sieve 0.616 |
| jit | 1 -> 0 | jitx | 0.204 | +47.0% | 7022 | -122 | kernel 0.318 fib 0.658 parse 0.080 corpus 0.129 loop 0.163 sieve 0.571 |
| klookup | 1 -> 0 | ops10, supers | 0.171 | +22.9% | 7200 | +56 | kernel 0.345 fib 0.184 parse 0.133 corpus 0.179 loop 0.095 sieve 0.121 |
| supers | 15 items -> 0 items | - | 0.146 | +5.3% | 7168 | +24 | kernel 0.319 fib 0.186 parse 0.084 corpus 0.146 loop 0.092 sieve 0.107 |
| nocet | 1 -> 0 | - | 0.144 | +3.7% | 7144 | +0 | kernel 0.314 fib 0.187 parse 0.082 corpus 0.137 loop 0.094 sieve 0.120 |
| d256 | 1 -> 0 | - | 0.144 | +3.6% | 7144 | +0 | kernel 0.303 fib 0.187 parse 0.080 corpus 0.144 loop 0.093 sieve 0.112 |
| guard | 1 -> 0 | - | 0.144 | +3.4% | 7144 | +0 | kernel 0.317 fib 0.182 parse 0.083 corpus 0.137 loop 0.093 sieve 0.105 |
| t2wide | 1 -> 0 | - | 0.143 | +2.8% | 7336 | +192 | kernel 0.288 fib 0.189 parse 0.081 corpus 0.138 loop 0.097 sieve 0.110 |
| hotinl | 10 -> 0 | - | 0.141 | +1.9% | 7088 | -56 | kernel 0.306 fib 0.186 parse 0.080 corpus 0.134 loop 0.092 sieve 0.114 |
| align1 | 1 -> 0 | - | 0.141 | +1.6% | 7144 | +0 | kernel 0.316 fib 0.179 parse 0.081 corpus 0.131 loop 0.093 sieve 0.120 |
| noreorder | 1 -> 0 | - | 0.140 | +1.2% | 7144 | +0 | kernel 0.300 fib 0.183 parse 0.078 corpus 0.136 loop 0.094 sieve 0.111 |
| jitx | 1 -> 0 | - | 0.140 | +1.2% | 7144 | +0 | kernel 0.305 fib 0.194 parse 0.075 corpus 0.126 loop 0.097 sieve 0.558 |
| bss | 1 -> 0 | - | 0.140 | +0.7% | 8200 | +1056 | kernel 0.303 fib 0.192 parse 0.075 corpus 0.129 loop 0.095 sieve 0.114 |
| t2hot | 3 -> 0 | - | 0.139 | +0.5% | 7144 | +0 | kernel 0.298 fib 0.194 parse 0.074 corpus 0.129 loop 0.095 sieve 0.119 |
| folds | 19 items -> 23 items | supers | 0.139 | -0.0% | 7152 | +8 | kernel 0.285 fib 0.184 parse 0.078 corpus 0.133 loop 0.095 sieve 0.115 |
| thinhdr | 1 -> 0 | - | 0.138 | -0.4% | 7392 | +248 | kernel 0.289 fib 0.190 parse 0.075 corpus 0.131 loop 0.094 sieve 0.112 |
| opbody | 1 -> 0 | - | 0.136 | -1.7% | 7272 | +128 | kernel 0.292 fib 0.183 parse 0.076 corpus 0.128 loop 0.091 sieve 0.111 |
| rtloopall | 1 -> 0 | - | 0.136 | -1.7% | 7568 | +424 | kernel 0.278 fib 0.184 parse 0.075 corpus 0.132 loop 0.094 sieve 0.118 |
| tracer | 1 -> 0 | - | 0.136 | -1.8% | 7144 | +0 | kernel 0.288 fib 0.188 parse 0.074 corpus 0.131 loop 0.090 sieve 0.120 |
| lean | 1 -> 0 | - | 0.135 | -2.8% | 9062 | +1918 | kernel 0.275 fib 0.185 parse 0.076 corpus 0.121 loop 0.095 sieve 0.110 |
| nocrossjump | 1 -> 0 | - | 0.133 | -4.4% | 7144 | +0 | kernel 0.273 fib 0.184 parse 0.071 corpus 0.125 loop 0.092 sieve 0.113 |

## 844f5fbf81

calibration, the design itself: speed in the run 0.134, measured now 0.141; size recorded 7088, measured 7088 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers, tfind | 0.373 | +163.9% | 7256 | +168 | kernel 0.758 fib 0.192 parse 0.688 corpus 0.749 loop 0.097 sieve 0.578 |
| escape | 2 -> 0 | ops10, rtloopall, supers | 0.317 | +124.5% | 7944 | +856 | kernel 0.455 fib 0.183 parse 0.152 corpus 0.248 loop 1.023 sieve 0.969 |
| tag2 | 1 -> 0 | hotcalls, jit, jitx, t2hot, t2wide | 0.242 | +71.2% | 6852 | -236 | kernel 0.328 fib 0.886 parse 0.094 corpus 0.142 loop 0.215 sieve 0.610 |
| ops10 | 31 items -> 0 items | rtloop, rtloopall, supers | 0.240 | +69.6% | 7208 | +120 | kernel 0.303 fib 0.184 parse 0.093 corpus 0.166 loop 0.926 sieve 0.793 |
| rtloop | 1 -> 0 | rtloopall | 0.236 | +67.2% | 6960 | -128 | kernel 0.303 fib 0.195 parse 0.081 corpus 0.144 loop 1.067 sieve 0.774 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.228 | +61.5% | 7240 | +152 | kernel 0.520 fib 0.186 parse 0.226 corpus 0.297 loop 0.096 sieve 0.662 |
| jit | 1 -> 0 | jitx | 0.213 | +50.6% | 6966 | -122 | kernel 0.347 fib 0.646 parse 0.086 corpus 0.135 loop 0.168 sieve 0.563 |
| klookup | 1 -> 0 | ops10, supers | 0.174 | +23.1% | 7144 | +56 | kernel 0.331 fib 0.192 parse 0.136 corpus 0.187 loop 0.099 sieve 0.114 |
| align1 | 1 -> 0 | - | 0.151 | +6.5% | 7088 | +0 | kernel 0.324 fib 0.185 parse 0.091 corpus 0.147 loop 0.096 sieve 0.112 |
| supers | 15 items -> 0 items | - | 0.150 | +6.2% | 7112 | +24 | kernel 0.326 fib 0.188 parse 0.091 corpus 0.145 loop 0.094 sieve 0.119 |
| guard | 1 -> 0 | - | 0.149 | +5.6% | 7088 | +0 | kernel 0.329 fib 0.196 parse 0.087 corpus 0.142 loop 0.094 sieve 0.110 |
| d256 | 1 -> 0 | - | 0.148 | +4.6% | 7088 | +0 | kernel 0.307 fib 0.183 parse 0.089 corpus 0.149 loop 0.095 sieve 0.117 |
| nocet | 1 -> 0 | - | 0.145 | +2.9% | 7088 | +0 | kernel 0.310 fib 0.182 parse 0.087 corpus 0.143 loop 0.093 sieve 0.112 |
| jitx | 1 -> 0 | - | 0.145 | +2.6% | 7088 | +0 | kernel 0.321 fib 0.188 parse 0.080 corpus 0.135 loop 0.098 sieve 0.545 |
| t2wide | 1 -> 0 | - | 0.145 | +2.6% | 7304 | +216 | kernel 0.290 fib 0.190 parse 0.089 corpus 0.142 loop 0.092 sieve 0.104 |
| thinhdr | 1 -> 0 | - | 0.145 | +2.5% | 7336 | +248 | kernel 0.314 fib 0.192 parse 0.080 corpus 0.133 loop 0.099 sieve 0.118 |
| nocrossjump | 1 -> 0 | - | 0.144 | +1.8% | 7088 | +0 | kernel 0.311 fib 0.196 parse 0.077 corpus 0.136 loop 0.097 sieve 0.110 |
| lean | 1 -> 0 | - | 0.144 | +1.6% | 8982 | +1894 | kernel 0.285 fib 0.193 parse 0.083 corpus 0.141 loop 0.095 sieve 0.116 |
| tfind | 1 -> 0 | ops10 | 0.143 | +1.0% | 7088 | +0 | kernel 0.287 fib 0.190 parse 0.081 corpus 0.139 loop 0.097 sieve 0.113 |
| folds | 19 items -> 23 items | supers | 0.143 | +0.9% | 7096 | +8 | kernel 0.296 fib 0.188 parse 0.082 corpus 0.133 loop 0.098 sieve 0.106 |
| rtloopall | 1 -> 0 | - | 0.142 | +0.7% | 7512 | +424 | kernel 0.277 fib 0.188 parse 0.084 corpus 0.141 loop 0.096 sieve 0.117 |
| noreorder | 1 -> 0 | - | 0.141 | -0.6% | 7088 | +0 | kernel 0.287 fib 0.185 parse 0.082 corpus 0.135 loop 0.093 sieve 0.119 |
| bss | 1 -> 0 | - | 0.139 | -1.4% | 8144 | +1056 | kernel 0.279 fib 0.189 parse 0.079 corpus 0.134 loop 0.094 sieve 0.107 |
| opbody | 1 -> 0 | - | 0.138 | -2.1% | 7216 | +128 | kernel 0.277 fib 0.189 parse 0.079 corpus 0.130 loop 0.094 sieve 0.114 |
| t2hot | 2 -> 0 | - | 0.138 | -2.5% | 7088 | +0 | kernel 0.275 fib 0.186 parse 0.078 corpus 0.134 loop 0.093 sieve 0.116 |

## 9a0eb0b0fb

calibration, the design itself: speed in the run 0.137, measured now 0.148; size recorded 7064, measured 7064 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers | 0.397 | +168.8% | 7224 | +160 | kernel 0.845 fib 0.191 parse 0.767 corpus 0.829 loop 0.096 sieve 0.196 |
| escape | 2 -> 0 | ops10, rtloopall, supers | 0.347 | +135.1% | 8032 | +968 | kernel 0.507 fib 0.185 parse 0.182 corpus 0.289 loop 1.023 sieve 0.926 |
| ops10 | 31 items -> 0 items | rtloop, rtloopall, supers | 0.248 | +68.1% | 7248 | +184 | kernel 0.326 fib 0.190 parse 0.095 corpus 0.167 loop 0.959 sieve 0.807 |
| rtloop | 1 -> 0 | rtloopall | 0.235 | +58.9% | 6928 | -136 | kernel 0.297 fib 0.189 parse 0.087 corpus 0.148 loop 0.981 sieve 0.757 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.227 | +54.0% | 7216 | +152 | kernel 0.501 fib 0.190 parse 0.227 corpus 0.290 loop 0.097 sieve 0.188 |
| tag2 | 1 -> 0 | hotcalls, jit, jitx, t2hot, t2wide | 0.219 | +48.3% | 6830 | -234 | kernel 0.309 fib 0.691 parse 0.093 corpus 0.132 loop 0.193 sieve 0.530 |
| jit | 1 -> 0 | jitx | 0.213 | +44.0% | 6944 | -120 | kernel 0.352 fib 0.653 parse 0.085 corpus 0.137 loop 0.161 sieve 0.554 |
| klookup | 1 -> 0 | ops10, supers | 0.181 | +22.2% | 7120 | +56 | kernel 0.344 fib 0.192 parse 0.144 corpus 0.204 loop 0.099 sieve 0.115 |
| t2wide | 1 -> 0 | - | 0.155 | +4.9% | 7288 | +224 | kernel 0.335 fib 0.181 parse 0.094 corpus 0.166 loop 0.094 sieve 0.107 |
| d256 | 1 -> 0 | - | 0.154 | +4.4% | 7064 | +0 | kernel 0.314 fib 0.186 parse 0.096 corpus 0.159 loop 0.097 sieve 0.117 |
| nocet | 1 -> 0 | - | 0.153 | +3.3% | 7064 | +0 | kernel 0.327 fib 0.186 parse 0.093 corpus 0.152 loop 0.095 sieve 0.120 |
| nocrossjump | 1 -> 0 | - | 0.152 | +2.7% | 7064 | +0 | kernel 0.329 fib 0.187 parse 0.093 corpus 0.147 loop 0.096 sieve 0.118 |
| jitx | 1 -> 0 | - | 0.152 | +2.6% | 7064 | +0 | kernel 0.350 fib 0.187 parse 0.088 corpus 0.145 loop 0.096 sieve 0.566 |
| align1 | 1 -> 0 | - | 0.150 | +1.7% | 7064 | +0 | kernel 0.310 fib 0.180 parse 0.091 corpus 0.153 loop 0.098 sieve 0.114 |
| supers | 17 items -> 0 items | - | 0.150 | +1.3% | 7080 | +16 | kernel 0.309 fib 0.184 parse 0.095 corpus 0.155 loop 0.090 sieve 0.111 |
| guard | 1 -> 0 | - | 0.150 | +1.3% | 7064 | +0 | kernel 0.312 fib 0.181 parse 0.092 corpus 0.150 loop 0.096 sieve 0.121 |
| opbody | 1 -> 0 | - | 0.149 | +0.8% | 7192 | +128 | kernel 0.302 fib 0.191 parse 0.089 corpus 0.148 loop 0.096 sieve 0.110 |
| t2hot | 3 -> 0 | - | 0.149 | +0.6% | 7064 | +0 | kernel 0.326 fib 0.193 parse 0.086 corpus 0.141 loop 0.095 sieve 0.124 |
| bss | 1 -> 0 | - | 0.148 | +0.1% | 8120 | +1056 | kernel 0.297 fib 0.187 parse 0.088 corpus 0.150 loop 0.098 sieve 0.120 |
| lean | 1 -> 0 | - | 0.148 | -0.1% | 8966 | +1902 | kernel 0.295 fib 0.188 parse 0.090 corpus 0.147 loop 0.095 sieve 0.114 |
| rtloopall | 1 -> 0 | - | 0.147 | -0.3% | 7496 | +432 | kernel 0.288 fib 0.195 parse 0.088 corpus 0.146 loop 0.096 sieve 0.122 |
| tracer | 1 -> 0 | - | 0.147 | -0.8% | 7064 | +0 | kernel 0.293 fib 0.187 parse 0.090 corpus 0.141 loop 0.097 sieve 0.122 |
| thinhdr | 1 -> 0 | - | 0.145 | -1.6% | 7312 | +248 | kernel 0.290 fib 0.188 parse 0.088 corpus 0.141 loop 0.096 sieve 0.116 |
| folds | 22 items -> 23 items | supers | 0.143 | -3.0% | 7064 | +0 | kernel 0.275 fib 0.190 parse 0.087 corpus 0.140 loop 0.095 sieve 0.109 |

## 4dc36f9b92

calibration, the design itself: speed in the run 0.153, measured now 0.161; size recorded 7056, measured 7056 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers, tfind | 0.436 | +171.1% | 7224 | +168 | kernel 1.054 fib 0.182 parse 0.904 corpus 0.962 loop 0.095 sieve 0.796 |
| escape | 2 -> 0 | ops10, rtloopall, supers | 0.423 | +162.5% | 8048 | +992 | kernel 0.629 fib 0.181 parse 0.244 corpus 0.394 loop 1.231 sieve 1.205 |
| jit | 1 -> 0 | jitx | 0.302 | +87.4% | 6934 | -122 | kernel 0.399 fib 1.110 parse 0.109 corpus 0.160 loop 0.323 sieve 0.690 |
| tag2 | 1 -> 0 | hotcalls, jit, jitx, t2hot, t2wide | 0.300 | +86.6% | 6811 | -245 | kernel 0.351 fib 1.131 parse 0.109 corpus 0.165 loop 0.341 sieve 0.725 |
| ops10 | 30 items -> 0 items | rtloop, rtloopall, supers | 0.279 | +73.1% | 7216 | +160 | kernel 0.371 fib 0.182 parse 0.113 corpus 0.194 loop 1.136 sieve 0.999 |
| rtloop | 1 -> 0 | rtloopall | 0.271 | +68.3% | 6928 | -128 | kernel 0.347 fib 0.183 parse 0.110 corpus 0.172 loop 1.220 sieve 1.040 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.259 | +61.0% | 7216 | +160 | kernel 0.624 fib 0.184 parse 0.283 corpus 0.367 loop 0.098 sieve 0.789 |
| klookup | 1 -> 0 | ops10, supers | 0.196 | +21.6% | 7120 | +64 | kernel 0.402 fib 0.177 parse 0.182 corpus 0.234 loop 0.095 sieve 0.119 |
| t2wide | 1 -> 0 | - | 0.172 | +6.6% | 7272 | +216 | kernel 0.385 fib 0.186 parse 0.116 corpus 0.188 loop 0.095 sieve 0.110 |
| supers | 16 items -> 0 items | - | 0.167 | +3.7% | 7088 | +32 | kernel 0.368 fib 0.181 parse 0.109 corpus 0.180 loop 0.100 sieve 0.117 |
| nocet | 1 -> 0 | - | 0.165 | +2.7% | 7056 | +0 | kernel 0.358 fib 0.181 parse 0.112 corpus 0.177 loop 0.096 sieve 0.114 |
| jitx | 1 -> 0 | - | 0.165 | +2.6% | 7056 | +0 | kernel 0.397 fib 0.187 parse 0.105 corpus 0.164 loop 0.096 sieve 0.686 |
| peel | 1 -> 0 | - | 0.164 | +1.8% | 7056 | +0 | kernel 0.361 fib 0.185 parse 0.108 corpus 0.167 loop 0.098 sieve 0.116 |
| d256 | 1 -> 0 | - | 0.163 | +1.5% | 7056 | +0 | kernel 0.350 fib 0.186 parse 0.106 corpus 0.173 loop 0.097 sieve 0.118 |
| opbody | 1 -> 0 | - | 0.163 | +1.3% | 7184 | +128 | kernel 0.361 fib 0.181 parse 0.110 corpus 0.162 loop 0.099 sieve 0.115 |
| lean | 1 -> 0 | - | 0.162 | +0.8% | 8950 | +1894 | kernel 0.341 fib 0.186 parse 0.114 corpus 0.164 loop 0.095 sieve 0.122 |
| thinhdr | 1 -> 0 | - | 0.162 | +0.6% | 7304 | +248 | kernel 0.360 fib 0.183 parse 0.109 corpus 0.161 loop 0.097 sieve 0.121 |
| tfind | 1 -> 0 | ops10 | 0.162 | +0.4% | 7056 | +0 | kernel 0.357 fib 0.178 parse 0.108 corpus 0.164 loop 0.097 sieve 0.113 |
| rtloopall | 1 -> 0 | - | 0.161 | +0.3% | 7480 | +424 | kernel 0.370 fib 0.178 parse 0.109 corpus 0.163 loop 0.093 sieve 0.113 |
| guard | 1 -> 0 | - | 0.161 | +0.3% | 7056 | +0 | kernel 0.358 fib 0.178 parse 0.104 corpus 0.171 loop 0.097 sieve 0.112 |
| bss | 1 -> 0 | - | 0.161 | +0.3% | 8112 | +1056 | kernel 0.361 fib 0.178 parse 0.109 corpus 0.161 loop 0.097 sieve 0.113 |
| spec | 4 items -> 5 items | - | 0.161 | +0.2% | 7056 | +0 | kernel 0.341 fib 0.184 parse 0.109 corpus 0.167 loop 0.095 sieve 0.112 |
| nocrossjump | 1 -> 0 | - | 0.161 | -0.0% | 7056 | +0 | kernel 0.356 fib 0.179 parse 0.109 corpus 0.168 loop 0.093 sieve 0.115 |
| swapi | 1 -> 0 | ops10, supers | 0.161 | -0.1% | 7072 | +16 | kernel 0.349 fib 0.184 parse 0.104 corpus 0.170 loop 0.095 sieve 0.121 |
| t2hot | 3 -> 0 | - | 0.160 | -0.6% | 7056 | +0 | kernel 0.340 fib 0.179 parse 0.111 corpus 0.164 loop 0.095 sieve 0.108 |
| align1 | 1 -> 0 | - | 0.160 | -0.9% | 7056 | +0 | kernel 0.361 fib 0.178 parse 0.105 corpus 0.162 loop 0.094 sieve 0.114 |
| folds | 22 items -> 23 items | supers | 0.159 | -1.2% | 7064 | +8 | kernel 0.324 fib 0.177 parse 0.109 corpus 0.172 loop 0.094 sieve 0.110 |
| opt | Os -> O2 | - | 0.152 | -5.4% | 7056 | +0 | kernel 0.326 fib 0.185 parse 0.090 corpus 0.159 loop 0.095 sieve 0.110 |

## 8c1e3c7d02

calibration, the design itself: speed in the run 0.189, measured now 0.202; size recorded 7048, measured 7048 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers, tfind | 0.614 | +203.9% | 7192 | +144 | kernel 0.894 fib 0.735 parse 0.769 corpus 0.814 loop 0.212 sieve 0.677 |
| escape | 1 -> 0 | ops10, rtloopall | 0.489 | +142.4% | 7887 | +839 | kernel 0.629 fib 0.842 parse 0.180 corpus 0.281 loop 1.050 sieve 0.996 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.390 | +93.1% | 7176 | +128 | kernel 0.615 fib 0.778 parse 0.247 corpus 0.311 loop 0.245 sieve 0.680 |
| ops10 | 30 items -> 0 items | rtloop, rtloopall, supers | 0.344 | +70.6% | 7118 | +70 | kernel 0.356 fib 0.945 parse 0.096 corpus 0.159 loop 0.946 sieve 0.841 |
| rtloop | 1 -> 0 | rtloopall | 0.313 | +54.9% | 6926 | -122 | kernel 0.358 fib 0.599 parse 0.090 corpus 0.149 loop 1.043 sieve 0.838 |
| klookup | 1 -> 0 | ops10 | 0.302 | +49.7% | 7096 | +48 | kernel 0.407 fib 0.893 parse 0.157 corpus 0.201 loop 0.219 sieve 0.588 |
| t2wide | 1 -> 0 | - | 0.241 | +19.5% | 7333 | +285 | kernel 0.367 fib 0.666 parse 0.098 corpus 0.162 loop 0.210 sieve 0.556 |
| noreorder | 1 -> 0 | - | 0.234 | +16.1% | 7048 | +0 | kernel 0.363 fib 0.718 parse 0.089 corpus 0.140 loop 0.219 sieve 0.608 |
| ipaclone | 1 -> 0 | - | 0.232 | +15.1% | 7048 | +0 | kernel 0.338 fib 0.726 parse 0.088 corpus 0.143 loop 0.218 sieve 0.554 |
| nocet | 1 -> 0 | - | 0.232 | +14.9% | 7048 | +0 | kernel 0.369 fib 0.829 parse 0.092 corpus 0.149 loop 0.160 sieve 0.562 |
| folds | 21 items -> 23 items | ops10 | 0.224 | +11.1% | 7065 | +17 | kernel 0.370 fib 0.696 parse 0.093 corpus 0.141 loop 0.169 sieve 0.554 |
| tag2 | 1 -> 0 | hotcalls, hotinl, t2hot, t2wide | 0.224 | +11.0% | 6829 | -219 | kernel 0.280 fib 0.868 parse 0.095 corpus 0.138 loop 0.177 sieve 0.491 |
| nocrossjump | 1 -> 0 | - | 0.216 | +7.1% | 7048 | +0 | kernel 0.350 fib 0.673 parse 0.090 corpus 0.145 loop 0.154 sieve 0.543 |
| opbody | 1 -> 0 | - | 0.212 | +4.8% | 7184 | +136 | kernel 0.344 fib 0.609 parse 0.089 corpus 0.148 loop 0.153 sieve 0.535 |
| rtloopall | 1 -> 0 | - | 0.210 | +3.8% | 7475 | +427 | kernel 0.350 fib 0.592 parse 0.089 corpus 0.145 loop 0.152 sieve 0.532 |
| hotinl | 10 -> 0 | - | 0.205 | +1.5% | 7000 | -48 | kernel 0.357 fib 0.598 parse 0.094 corpus 0.149 loop 0.122 sieve 0.541 |
| t2hot | 1 -> 0 | - | 0.204 | +0.8% | 7048 | +0 | kernel 0.328 fib 0.610 parse 0.090 corpus 0.143 loop 0.136 sieve 0.545 |
| tracer | 1 -> 0 | - | 0.204 | +0.8% | 7048 | +0 | kernel 0.329 fib 0.598 parse 0.092 corpus 0.142 loop 0.137 sieve 0.519 |
| lean | 1 -> 0 | - | 0.202 | -0.0% | 8910 | +1862 | kernel 0.349 fib 0.590 parse 0.090 corpus 0.148 loop 0.122 sieve 0.523 |
| thinhdr | 1 -> 0 | - | 0.201 | -0.2% | 7296 | +248 | kernel 0.350 fib 0.597 parse 0.092 corpus 0.138 loop 0.124 sieve 0.530 |
| tfind | 1 -> 0 | ops10 | 0.201 | -0.5% | 7048 | +0 | kernel 0.338 fib 0.592 parse 0.091 corpus 0.142 loop 0.127 sieve 0.522 |
| bss | 1 -> 0 | - | 0.200 | -0.9% | 8096 | +1048 | kernel 0.338 fib 0.607 parse 0.091 corpus 0.144 loop 0.120 sieve 0.538 |

## ecfba4404a

calibration, the design itself: speed in the run 0.198, measured now 0.208; size recorded 7038, measured 7038 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers, tfind | 0.632 | +203.7% | 7182 | +144 | kernel 0.935 fib 0.766 parse 0.717 corpus 0.791 loop 0.247 sieve 0.676 |
| escape | 2 -> 0 | ops10, rtloopall, supers | 0.491 | +136.1% | 7926 | +888 | kernel 0.637 fib 0.797 parse 0.184 corpus 0.304 loop 1.004 sieve 0.993 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.382 | +83.6% | 7166 | +128 | kernel 0.609 fib 0.824 parse 0.217 corpus 0.320 loop 0.233 sieve 0.608 |
| ops10 | 31 items -> 0 items | rtloop, rtloopall, supers | 0.320 | +53.8% | 7143 | +105 | kernel 0.350 fib 0.806 parse 0.090 corpus 0.165 loop 0.803 sieve 0.789 |
| rtloop | 1 -> 0 | rtloopall | 0.292 | +40.6% | 6916 | -122 | kernel 0.347 fib 0.571 parse 0.079 corpus 0.144 loop 0.946 sieve 0.837 |
| klookup | 1 -> 0 | ops10, supers | 0.256 | +23.1% | 7094 | +56 | kernel 0.390 fib 0.610 parse 0.139 corpus 0.195 loop 0.170 sieve 0.550 |
| supers | 17 items -> 0 items | - | 0.233 | +12.0% | 7055 | +17 | kernel 0.366 fib 0.785 parse 0.082 corpus 0.143 loop 0.203 sieve 0.559 |
| ipaclone | 1 -> 0 | - | 0.231 | +11.0% | 7038 | +0 | kernel 0.394 fib 0.786 parse 0.086 corpus 0.149 loop 0.165 sieve 0.568 |
| tos | 0 -> 1 | - | 0.231 | +11.0% | 7038 | +0 | kernel 0.355 fib 0.810 parse 0.079 corpus 0.145 loop 0.197 sieve 0.577 |
| nocet | 1 -> 0 | - | 0.230 | +10.8% | 7038 | +0 | kernel 0.364 fib 0.733 parse 0.084 corpus 0.142 loop 0.205 sieve 0.567 |
| align1 | 1 -> 0 | - | 0.222 | +6.6% | 7038 | +0 | kernel 0.371 fib 0.632 parse 0.079 corpus 0.137 loop 0.210 sieve 0.575 |
| hotinl | 20 -> 0 | - | 0.221 | +6.1% | 6958 | -80 | kernel 0.351 fib 0.578 parse 0.087 corpus 0.152 loop 0.196 sieve 0.587 |
| guard | 1 -> 0 | - | 0.220 | +5.7% | 7038 | +0 | kernel 0.378 fib 0.709 parse 0.086 corpus 0.144 loop 0.154 sieve 0.568 |
| folds | 21 items -> 23 items | supers | 0.219 | +5.6% | 7038 | +0 | kernel 0.349 fib 0.659 parse 0.080 corpus 0.135 loop 0.206 sieve 0.523 |
| t2wide | 1 -> 0 | - | 0.219 | +5.2% | 7282 | +244 | kernel 0.363 fib 0.603 parse 0.079 corpus 0.149 loop 0.193 sieve 0.522 |
| tag2 | 1 -> 0 | hotcalls, hotinl, t2wide | 0.217 | +4.6% | 6844 | -194 | kernel 0.284 fib 0.789 parse 0.088 corpus 0.132 loop 0.188 sieve 0.547 |
| noreorder | 1 -> 0 | - | 0.215 | +3.2% | 7038 | +0 | kernel 0.341 fib 0.590 parse 0.081 corpus 0.143 loop 0.197 sieve 0.578 |
| thinhdr | 1 -> 0 | - | 0.214 | +3.0% | 7286 | +248 | kernel 0.348 fib 0.580 parse 0.079 corpus 0.143 loop 0.196 sieve 0.594 |
| tfind | 1 -> 0 | ops10 | 0.212 | +2.0% | 7038 | +0 | kernel 0.349 fib 0.581 parse 0.080 corpus 0.143 loop 0.183 sieve 0.575 |
| bss | 1 -> 0 | - | 0.212 | +1.8% | 8094 | +1056 | kernel 0.346 fib 0.564 parse 0.080 corpus 0.140 loop 0.194 sieve 0.571 |
| varslot | 0 -> 1 | - | 0.210 | +1.2% | 7038 | +0 | kernel 0.330 fib 0.617 parse 0.084 corpus 0.132 loop 0.183 sieve 0.584 |
| lean | 1 -> 0 | - | 0.209 | +0.5% | 8902 | +1864 | kernel 0.340 fib 0.564 parse 0.084 corpus 0.139 loop 0.178 sieve 0.557 |
| opbody | 1 -> 0 | - | 0.206 | -0.7% | 7174 | +136 | kernel 0.323 fib 0.574 parse 0.080 corpus 0.138 loop 0.184 sieve 0.572 |
| rtloopall | 1 -> 0 | - | 0.206 | -0.8% | 7465 | +427 | kernel 0.334 fib 0.575 parse 0.080 corpus 0.139 loop 0.175 sieve 0.572 |

## 2707ccdbad

calibration, the design itself: speed in the run 0.203, measured now 0.214; size recorded 6994, measured 6994 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers, tfind | 0.628 | +193.8% | 7160 | +166 | kernel 0.924 fib 0.769 parse 0.709 corpus 0.795 loop 0.245 sieve 0.658 |
| escape | 2 -> 0 | ops10, rtloopall, supers | 0.499 | +133.5% | 7878 | +884 | kernel 0.649 fib 0.757 parse 0.190 corpus 0.325 loop 1.023 sieve 0.968 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.383 | +78.9% | 7146 | +152 | kernel 0.601 fib 0.833 parse 0.218 corpus 0.334 loop 0.225 sieve 0.594 |
| ops10 | 31 items -> 0 items | rtloop, rtloopall, supers | 0.321 | +50.1% | 7095 | +101 | kernel 0.357 fib 0.752 parse 0.092 corpus 0.169 loop 0.812 sieve 0.773 |
| rtloop | 1 -> 0 | rtloopall | 0.304 | +42.3% | 6868 | -126 | kernel 0.345 fib 0.579 parse 0.084 corpus 0.165 loop 0.944 sieve 0.851 |
| klookup | 1 -> 0 | ops10, supers | 0.262 | +22.3% | 7050 | +56 | kernel 0.404 fib 0.601 parse 0.144 corpus 0.202 loop 0.173 sieve 0.542 |
| tos | 0 -> 1 | - | 0.246 | +14.9% | 6994 | +0 | kernel 0.366 fib 0.814 parse 0.089 corpus 0.154 loop 0.220 sieve 0.568 |
| nocet | 1 -> 0 | - | 0.242 | +13.3% | 6994 | +0 | kernel 0.381 fib 0.731 parse 0.092 corpus 0.163 loop 0.201 sieve 0.577 |
| ipaclone | 1 -> 0 | - | 0.238 | +11.5% | 6994 | +0 | kernel 0.400 fib 0.759 parse 0.094 corpus 0.166 loop 0.163 sieve 0.575 |
| align1 | 1 -> 0 | - | 0.235 | +10.1% | 6994 | +0 | kernel 0.371 fib 0.652 parse 0.088 corpus 0.156 loop 0.216 sieve 0.576 |
| supers | 17 items -> 0 items | - | 0.234 | +9.5% | 7027 | +33 | kernel 0.356 fib 0.787 parse 0.088 corpus 0.162 loop 0.177 sieve 0.562 |
| guard | 1 -> 0 | - | 0.230 | +7.7% | 6994 | +0 | kernel 0.362 fib 0.709 parse 0.096 corpus 0.168 loop 0.156 sieve 0.592 |
| t2wide | 1 -> 0 | - | 0.227 | +6.2% | 7233 | +239 | kernel 0.370 fib 0.606 parse 0.084 corpus 0.164 loop 0.197 sieve 0.518 |
| folds | 21 items -> 23 items | supers | 0.226 | +5.8% | 6994 | +0 | kernel 0.349 fib 0.658 parse 0.086 corpus 0.146 loop 0.206 sieve 0.526 |
| noreorder | 1 -> 0 | - | 0.226 | +5.8% | 6994 | +0 | kernel 0.367 fib 0.693 parse 0.085 corpus 0.158 loop 0.173 sieve 0.567 |
| tag2 | 1 -> 0 | hotcalls, rtempty, t2wide | 0.219 | +2.4% | 6844 | -150 | kernel 0.292 fib 0.799 parse 0.089 corpus 0.132 loop 0.185 sieve 0.550 |
| opbody | 1 -> 0 | - | 0.218 | +2.0% | 7130 | +136 | kernel 0.346 fib 0.578 parse 0.086 corpus 0.155 loop 0.184 sieve 0.574 |
| tracer | 1 -> 0 | - | 0.218 | +1.9% | 6994 | +0 | kernel 0.337 fib 0.582 parse 0.085 corpus 0.155 loop 0.190 sieve 0.584 |
| varslot | 0 -> 1 | - | 0.217 | +1.4% | 6994 | +0 | kernel 0.326 fib 0.604 parse 0.087 corpus 0.142 loop 0.198 sieve 0.579 |
| thinhdr | 1 -> 0 | - | 0.216 | +1.0% | 7242 | +248 | kernel 0.358 fib 0.585 parse 0.085 corpus 0.151 loop 0.174 sieve 0.586 |
| lean | 1 -> 0 | - | 0.215 | +0.8% | 8782 | +1788 | kernel 0.339 fib 0.596 parse 0.086 corpus 0.153 loop 0.174 sieve 0.577 |
| rtloopall | 1 -> 0 | - | 0.213 | -0.2% | 7415 | +421 | kernel 0.344 fib 0.571 parse 0.085 corpus 0.157 loop 0.168 sieve 0.580 |
| tfind | 1 -> 0 | ops10 | 0.213 | -0.6% | 6994 | +0 | kernel 0.339 fib 0.569 parse 0.084 corpus 0.153 loop 0.176 sieve 0.576 |
| rtempty | 1 -> 0 | - | 0.211 | -1.2% | 6958 | -36 | kernel 0.349 fib 0.580 parse 0.082 corpus 0.147 loop 0.172 sieve 0.580 |
| bss | 1 -> 0 | - | 0.210 | -1.9% | 8050 | +1056 | kernel 0.345 fib 0.559 parse 0.085 corpus 0.150 loop 0.165 sieve 0.566 |

## ebade32d18

calibration, the design itself: speed in the run 0.199, measured now 0.218; size recorded 6976, measured 6976 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers | 0.611 | +179.7% | 7160 | +184 | kernel 0.897 fib 0.759 parse 0.708 corpus 0.781 loop 0.226 sieve 0.595 |
| escape | 2 -> 0 | ops10, rtloopall, supers | 0.458 | +110.0% | 7839 | +863 | kernel 0.587 fib 0.829 parse 0.175 corpus 0.262 loop 0.910 sieve 0.953 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.385 | +76.3% | 7144 | +168 | kernel 0.598 fib 0.773 parse 0.248 corpus 0.312 loop 0.236 sieve 0.646 |
| ops10 | 30 items -> 0 items | rtloop, rtloopall, supers | 0.351 | +60.7% | 7103 | +127 | kernel 0.402 fib 0.847 parse 0.098 corpus 0.166 loop 0.960 sieve 0.835 |
| rtloop | 1 -> 0 | rtloopall | 0.320 | +46.5% | 6852 | -124 | kernel 0.362 fib 0.670 parse 0.090 corpus 0.148 loop 1.036 sieve 0.887 |
| klookup | 1 -> 0 | ops10, supers | 0.276 | +26.6% | 7032 | +56 | kernel 0.409 fib 0.698 parse 0.151 corpus 0.192 loop 0.195 sieve 0.591 |
| folds | 20 items -> 23 items | supers | 0.243 | +11.4% | 6975 | -1 | kernel 0.372 fib 0.916 parse 0.096 corpus 0.149 loop 0.174 sieve 0.604 |
| t2wide | 1 -> 0 | - | 0.241 | +10.6% | 7203 | +227 | kernel 0.399 fib 0.760 parse 0.099 corpus 0.153 loop 0.178 sieve 0.600 |
| supers | 17 items -> 0 items | - | 0.234 | +7.1% | 6992 | +16 | kernel 0.359 fib 0.879 parse 0.094 corpus 0.147 loop 0.160 sieve 0.591 |
| nocet | 1 -> 0 | - | 0.231 | +6.0% | 6976 | +0 | kernel 0.341 fib 0.754 parse 0.091 corpus 0.140 loop 0.204 sieve 0.591 |
| ipaclone | 1 -> 0 | - | 0.230 | +5.3% | 6976 | +0 | kernel 0.344 fib 0.700 parse 0.088 corpus 0.143 loop 0.212 sieve 0.524 |
| tag2 | 1 -> 0 | hotcalls, t2wide | 0.229 | +4.7% | 6829 | -147 | kernel 0.287 fib 0.926 parse 0.097 corpus 0.136 loop 0.179 sieve 0.536 |
| noreorder | 1 -> 0 | - | 0.226 | +3.4% | 6976 | +0 | kernel 0.344 fib 0.699 parse 0.088 corpus 0.142 loop 0.193 sieve 0.603 |
| nocrossjump | 1 -> 0 | - | 0.225 | +3.0% | 6976 | +0 | kernel 0.355 fib 0.694 parse 0.090 corpus 0.143 loop 0.182 sieve 0.602 |
| lean | 1 -> 0 | - | 0.224 | +2.8% | 8806 | +1830 | kernel 0.359 fib 0.671 parse 0.093 corpus 0.145 loop 0.176 sieve 0.584 |
| thinhdr | 1 -> 0 | - | 0.224 | +2.6% | 7224 | +248 | kernel 0.378 fib 0.669 parse 0.090 corpus 0.138 loop 0.179 sieve 0.587 |
| bss | 1 -> 0 | - | 0.221 | +1.2% | 8032 | +1056 | kernel 0.327 fib 0.662 parse 0.090 corpus 0.144 loop 0.187 sieve 0.595 |
| opbody | 1 -> 0 | - | 0.221 | +1.1% | 7112 | +136 | kernel 0.356 fib 0.671 parse 0.089 corpus 0.137 loop 0.179 sieve 0.594 |
| swapi | 1 -> 0 | ops10 | 0.220 | +0.9% | 6976 | +0 | kernel 0.337 fib 0.691 parse 0.088 corpus 0.140 loop 0.181 sieve 0.591 |
| rtloopall | 1 -> 0 | - | 0.218 | -0.1% | 7395 | +419 | kernel 0.326 fib 0.666 parse 0.090 corpus 0.139 loop 0.182 sieve 0.577 |
| tracer | 1 -> 0 | - | 0.216 | -1.1% | 6976 | +0 | kernel 0.337 fib 0.662 parse 0.090 corpus 0.144 loop 0.162 sieve 0.581 |

## d9301ea8f8

calibration, the design itself: speed in the run 0.204, measured now 0.217; size recorded 6958, measured 6958 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers, tfind | 0.628 | +190.0% | 7118 | +160 | kernel 0.962 fib 0.762 parse 0.720 corpus 0.812 loop 0.229 sieve 0.660 |
| escape | 2 -> 0 | ops10, rtloopall, supers | 0.505 | +132.9% | 7846 | +888 | kernel 0.652 fib 0.778 parse 0.190 corpus 0.321 loop 1.057 sieve 0.960 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.391 | +80.6% | 7102 | +144 | kernel 0.637 fib 0.837 parse 0.220 corpus 0.334 loop 0.235 sieve 0.563 |
| ops10 | 31 items -> 0 items | rtloop, rtloopall, supers | 0.328 | +51.6% | 7063 | +105 | kernel 0.379 fib 0.789 parse 0.093 corpus 0.166 loop 0.822 sieve 0.787 |
| rtloop | 1 -> 0 | rtloopall | 0.305 | +40.8% | 6836 | -122 | kernel 0.354 fib 0.574 parse 0.087 corpus 0.159 loop 0.943 sieve 0.839 |
| klookup | 1 -> 0 | ops10, supers | 0.264 | +21.7% | 7014 | +56 | kernel 0.416 fib 0.620 parse 0.144 corpus 0.203 loop 0.169 sieve 0.540 |
| supers | 17 items -> 0 items | - | 0.247 | +13.9% | 6991 | +33 | kernel 0.396 fib 0.781 parse 0.089 corpus 0.160 loop 0.209 sieve 0.554 |
| t2wide | 1 -> 0 | - | 0.241 | +11.2% | 7161 | +203 | kernel 0.393 fib 0.661 parse 0.087 corpus 0.160 loop 0.226 sieve 0.552 |
| tos | 0 -> 1 | - | 0.240 | +10.8% | 6958 | +0 | kernel 0.375 fib 0.802 parse 0.087 corpus 0.157 loop 0.194 sieve 0.548 |
| ipaclone | 1 -> 0 | - | 0.240 | +10.7% | 6958 | +0 | kernel 0.402 fib 0.775 parse 0.096 corpus 0.164 loop 0.161 sieve 0.568 |
| nocet | 1 -> 0 | - | 0.239 | +10.4% | 6958 | +0 | kernel 0.376 fib 0.728 parse 0.089 corpus 0.161 loop 0.201 sieve 0.568 |
| align1 | 1 -> 0 | - | 0.236 | +8.8% | 6958 | +0 | kernel 0.394 fib 0.639 parse 0.087 corpus 0.157 loop 0.210 sieve 0.552 |
| folds | 21 items -> 23 items | supers | 0.229 | +5.6% | 6958 | +0 | kernel 0.358 fib 0.641 parse 0.090 corpus 0.146 loop 0.208 sieve 0.511 |
| guard | 1 -> 0 | - | 0.228 | +5.1% | 6958 | +0 | kernel 0.393 fib 0.689 parse 0.092 corpus 0.161 loop 0.152 sieve 0.585 |
| noreorder | 1 -> 0 | - | 0.224 | +3.2% | 6958 | +0 | kernel 0.385 fib 0.695 parse 0.082 corpus 0.146 loop 0.174 sieve 0.558 |
| thinhdr | 1 -> 0 | - | 0.223 | +2.7% | 7206 | +248 | kernel 0.379 fib 0.593 parse 0.087 corpus 0.152 loop 0.184 sieve 0.582 |
| tfind | 1 -> 0 | ops10 | 0.222 | +2.6% | 6958 | +0 | kernel 0.375 fib 0.569 parse 0.086 corpus 0.152 loop 0.195 sieve 0.578 |
| varslot | 0 -> 1 | - | 0.219 | +1.2% | 6958 | +0 | kernel 0.348 fib 0.607 parse 0.088 corpus 0.137 loop 0.200 sieve 0.573 |
| bss | 1 -> 0 | - | 0.219 | +1.1% | 8014 | +1056 | kernel 0.352 fib 0.567 parse 0.087 corpus 0.148 loop 0.197 sieve 0.567 |
| t2hot | 3 -> 0 | - | 0.217 | +0.1% | 6958 | +0 | kernel 0.360 fib 0.570 parse 0.086 corpus 0.150 loop 0.183 sieve 0.569 |
| lean | 1 -> 0 | - | 0.217 | -0.0% | 8790 | +1832 | kernel 0.361 fib 0.570 parse 0.087 corpus 0.144 loop 0.185 sieve 0.592 |
| tag2 | 1 -> 0 | hotcalls, t2hot, t2wide | 0.216 | -0.1% | 6844 | -114 | kernel 0.285 fib 0.792 parse 0.087 corpus 0.127 loop 0.191 sieve 0.569 |
| tracer | 1 -> 0 | - | 0.215 | -0.6% | 6958 | +0 | kernel 0.349 fib 0.581 parse 0.085 corpus 0.149 loop 0.181 sieve 0.575 |
| opbody | 1 -> 0 | - | 0.215 | -0.8% | 7094 | +136 | kernel 0.355 fib 0.577 parse 0.081 corpus 0.148 loop 0.185 sieve 0.572 |
| rtloopall | 1 -> 0 | - | 0.214 | -1.3% | 7385 | +427 | kernel 0.349 fib 0.582 parse 0.084 corpus 0.150 loop 0.174 sieve 0.581 |

## fde52046d2

calibration, the design itself: speed in the run 0.221, measured now 0.237; size recorded 6942, measured 6942 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers, tfind | 0.694 | +193.1% | 7110 | +168 | kernel 0.807 fib 1.087 parse 0.796 corpus 0.818 loop 0.281 sieve 0.694 |
| escape | 2 -> 0 | ops10, rtloopall, supers | 0.478 | +101.9% | 7846 | +904 | kernel 0.497 fib 1.012 parse 0.194 corpus 0.257 loop 0.992 sieve 0.972 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.406 | +71.6% | 7110 | +168 | kernel 0.504 fib 1.030 parse 0.252 corpus 0.293 loop 0.289 sieve 0.716 |
| ops10 | 30 items -> 0 items | rtloop, rtloopall, supers | 0.346 | +46.3% | 7071 | +129 | kernel 0.330 fib 1.040 parse 0.104 corpus 0.158 loop 0.884 sieve 0.835 |
| klookup | 1 -> 0 | ops10, supers | 0.321 | +35.8% | 6998 | +56 | kernel 0.367 fib 1.094 parse 0.172 corpus 0.207 loop 0.240 sieve 0.631 |
| rtloop | 1 -> 0 | rtloopall | 0.309 | +30.7% | 6812 | -130 | kernel 0.297 fib 0.747 parse 0.100 corpus 0.144 loop 0.885 sieve 0.863 |
| t2wide | 1 -> 0 | - | 0.282 | +19.0% | 7145 | +203 | kernel 0.328 fib 1.061 parse 0.113 corpus 0.158 loop 0.286 sieve 0.674 |
| tag2 | 1 -> 0 | hotcalls, t2hot, t2wide | 0.263 | +11.0% | 6836 | -106 | kernel 0.312 fib 1.004 parse 0.103 corpus 0.141 loop 0.275 sieve 0.630 |
| folds | 21 items -> 23 items | supers | 0.259 | +9.5% | 6951 | +9 | kernel 0.317 fib 0.960 parse 0.106 corpus 0.147 loop 0.247 sieve 0.676 |
| nocet | 1 -> 0 | - | 0.257 | +8.4% | 6942 | +0 | kernel 0.300 fib 0.988 parse 0.102 corpus 0.144 loop 0.256 sieve 0.631 |
| supers | 17 items -> 0 items | - | 0.255 | +7.9% | 6967 | +25 | kernel 0.325 fib 0.911 parse 0.102 corpus 0.152 loop 0.234 sieve 0.623 |
| thinhdr | 1 -> 0 | - | 0.240 | +1.3% | 7190 | +248 | kernel 0.305 fib 0.779 parse 0.102 corpus 0.141 loop 0.232 sieve 0.612 |
| ipaclone | 1 -> 0 | - | 0.239 | +1.0% | 6942 | +0 | kernel 0.313 fib 0.748 parse 0.101 corpus 0.142 loop 0.232 sieve 0.592 |
| t2hot | 3 -> 0 | - | 0.238 | +0.5% | 6942 | +0 | kernel 0.312 fib 0.765 parse 0.100 corpus 0.140 loop 0.228 sieve 0.612 |
| tracer | 1 -> 0 | - | 0.237 | +0.0% | 6942 | +0 | kernel 0.337 fib 0.744 parse 0.101 corpus 0.143 loop 0.206 sieve 0.602 |
| opbody | 1 -> 0 | - | 0.236 | -0.3% | 7070 | +128 | kernel 0.318 fib 0.742 parse 0.102 corpus 0.146 loop 0.208 sieve 0.610 |
| lean | 1 -> 0 | - | 0.235 | -0.5% | 8774 | +1832 | kernel 0.317 fib 0.774 parse 0.101 corpus 0.143 loop 0.205 sieve 0.601 |
| opt | Os -> O2 | - | 0.235 | -0.6% | 6942 | +0 | kernel 0.372 fib 0.756 parse 0.097 corpus 0.154 loop 0.170 sieve 0.561 |
| rtloopall | 1 -> 0 | - | 0.234 | -1.3% | 7368 | +426 | kernel 0.297 fib 0.755 parse 0.101 corpus 0.142 loop 0.215 sieve 0.598 |
| align1 | 1 -> 0 | - | 0.233 | -1.7% | 6942 | +0 | kernel 0.312 fib 0.747 parse 0.100 corpus 0.150 loop 0.195 sieve 0.605 |
| bss | 1 -> 0 | - | 0.230 | -3.0% | 7998 | +1056 | kernel 0.297 fib 0.760 parse 0.102 corpus 0.141 loop 0.197 sieve 0.604 |
| tfind | 1 -> 0 | ops10 | 0.228 | -3.6% | 6942 | +0 | kernel 0.279 fib 0.736 parse 0.102 corpus 0.141 loop 0.211 sieve 0.584 |
| tail | 1 -> 0 | jit | 0.173 | -26.9% | 7072 | +130 | kernel 0.473 fib 0.187 parse 0.108 corpus 0.167 loop 0.098 sieve 0.732 |

## ff95e96312

calibration, the design itself: speed in the run 0.224, measured now 0.238; size recorded 6934, measured 6934 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers, tfind | 0.695 | +191.6% | 7102 | +168 | kernel 0.779 fib 1.081 parse 0.791 corpus 0.799 loop 0.306 sieve 0.715 |
| escape | 2 -> 0 | ops10, rtloopall, supers | 0.529 | +121.8% | 7902 | +968 | kernel 0.530 fib 1.040 parse 0.227 corpus 0.307 loop 1.080 sieve 1.036 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.418 | +75.3% | 7086 | +152 | kernel 0.518 fib 1.115 parse 0.267 corpus 0.309 loop 0.269 sieve 0.709 |
| ops10 | 30 items -> 0 items | rtloop, rtloopall, supers | 0.343 | +43.7% | 7072 | +138 | kernel 0.314 fib 1.049 parse 0.105 corpus 0.150 loop 0.910 sieve 0.828 |
| klookup | 1 -> 0 | ops10, supers | 0.324 | +35.7% | 6998 | +64 | kernel 0.367 fib 1.103 parse 0.167 corpus 0.199 loop 0.264 sieve 0.642 |
| rtloop | 1 -> 0 | rtloopall | 0.313 | +31.4% | 6795 | -139 | kernel 0.301 fib 0.752 parse 0.099 corpus 0.140 loop 0.964 sieve 0.904 |
| t2wide | 1 -> 0 | - | 0.281 | +17.8% | 7153 | +219 | kernel 0.318 fib 1.044 parse 0.112 corpus 0.156 loop 0.302 sieve 0.688 |
| swapi | 1 -> 0 | ops10, supers | 0.268 | +12.5% | 6942 | +8 | kernel 0.333 fib 1.009 parse 0.103 corpus 0.151 loop 0.267 sieve 0.658 |
| folds | 22 items -> 23 items | supers | 0.260 | +9.1% | 6942 | +8 | kernel 0.322 fib 0.959 parse 0.104 corpus 0.147 loop 0.255 sieve 0.671 |
| nocet | 1 -> 0 | - | 0.259 | +8.7% | 6934 | +0 | kernel 0.314 fib 0.996 parse 0.104 corpus 0.142 loop 0.254 sieve 0.608 |
| tag2 | 1 -> 0 | hotcalls, t2hot, t2wide | 0.254 | +6.7% | 6811 | -123 | kernel 0.301 fib 0.956 parse 0.098 corpus 0.147 loop 0.257 sieve 0.637 |
| supers | 16 items -> 0 items | - | 0.252 | +5.7% | 6951 | +17 | kernel 0.336 fib 0.848 parse 0.101 corpus 0.144 loop 0.246 sieve 0.649 |
| tracer | 1 -> 0 | - | 0.244 | +2.4% | 6934 | +0 | kernel 0.335 fib 0.767 parse 0.098 corpus 0.144 loop 0.240 sieve 0.646 |
| spec | 4 items -> 5 items | - | 0.242 | +1.3% | 6934 | +0 | kernel 0.317 fib 0.764 parse 0.098 corpus 0.142 loop 0.244 sieve 0.632 |
| rtloopall | 1 -> 0 | - | 0.241 | +1.1% | 7361 | +427 | kernel 0.334 fib 0.743 parse 0.096 corpus 0.142 loop 0.240 sieve 0.645 |
| bss | 1 -> 0 | - | 0.240 | +0.6% | 7990 | +1056 | kernel 0.317 fib 0.745 parse 0.100 corpus 0.141 loop 0.240 sieve 0.652 |
| align1 | 1 -> 0 | - | 0.240 | +0.5% | 6934 | +0 | kernel 0.308 fib 0.769 parse 0.098 corpus 0.141 loop 0.242 sieve 0.642 |
| lean | 1 -> 0 | - | 0.239 | +0.1% | 8766 | +1832 | kernel 0.299 fib 0.767 parse 0.100 corpus 0.142 loop 0.239 sieve 0.643 |
| tfind | 1 -> 0 | ops10 | 0.239 | +0.1% | 6934 | +0 | kernel 0.293 fib 0.771 parse 0.100 corpus 0.144 loop 0.239 sieve 0.642 |
| t2hot | 3 -> 0 | - | 0.238 | -0.1% | 6934 | +0 | kernel 0.307 fib 0.758 parse 0.097 corpus 0.142 loop 0.239 sieve 0.640 |
| thinhdr | 1 -> 0 | - | 0.238 | -0.2% | 7182 | +248 | kernel 0.309 fib 0.764 parse 0.096 corpus 0.141 loop 0.239 sieve 0.657 |
| opbody | 1 -> 0 | - | 0.238 | -0.2% | 7062 | +128 | kernel 0.313 fib 0.766 parse 0.097 corpus 0.137 loop 0.239 sieve 0.648 |
| opt | Os -> O2 | - | 0.225 | -5.5% | 6934 | +0 | kernel 0.347 fib 0.702 parse 0.092 corpus 0.146 loop 0.179 sieve 0.529 |
| tail | 1 -> 0 | d256, jit | 0.168 | -29.7% | 7056 | +122 | kernel 0.425 fib 0.183 parse 0.107 corpus 0.163 loop 0.098 sieve 0.690 |

## 43cdfeef20

calibration, the design itself: speed in the run 0.227, measured now 0.247; size recorded 6917, measured 6917 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers | 0.699 | +182.8% | 7085 | +168 | kernel 0.787 fib 1.068 parse 0.793 corpus 0.825 loop 0.303 sieve 0.704 |
| escape | 2 -> 0 | ops10, rtloopall, supers | 0.552 | +123.2% | 7886 | +969 | kernel 0.598 fib 1.028 parse 0.243 corpus 0.319 loop 1.073 sieve 1.026 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.427 | +72.7% | 7069 | +152 | kernel 0.517 fib 1.090 parse 0.282 corpus 0.330 loop 0.270 sieve 0.711 |
| ops10 | 30 items -> 0 items | rtloop, rtloopall, supers | 0.357 | +44.5% | 7080 | +163 | kernel 0.331 fib 0.985 parse 0.119 corpus 0.164 loop 0.915 sieve 0.851 |
| klookup | 1 -> 0 | ops10, supers | 0.344 | +39.2% | 6965 | +48 | kernel 0.383 fib 1.092 parse 0.191 corpus 0.223 loop 0.271 sieve 0.636 |
| rtloop | 1 -> 0 | rtloopall | 0.331 | +34.0% | 6787 | -130 | kernel 0.306 fib 0.775 parse 0.106 corpus 0.154 loop 1.026 sieve 0.920 |
| swapi | 1 -> 0 | ops10, supers | 0.277 | +12.3% | 6917 | +0 | kernel 0.340 fib 1.018 parse 0.114 corpus 0.153 loop 0.272 sieve 0.641 |
| t2wide | 1 -> 0 | - | 0.274 | +10.8% | 7113 | +196 | kernel 0.335 fib 0.962 parse 0.117 corpus 0.161 loop 0.254 sieve 0.643 |
| nocet | 1 -> 0 | - | 0.273 | +10.6% | 6917 | +0 | kernel 0.334 fib 0.979 parse 0.116 corpus 0.156 loop 0.258 sieve 0.627 |
| folds | 22 items -> 23 items | supers | 0.271 | +9.8% | 6925 | +8 | kernel 0.322 fib 0.960 parse 0.114 corpus 0.162 loop 0.257 sieve 0.651 |
| supers | 16 items -> 0 items | - | 0.265 | +7.4% | 6942 | +25 | kernel 0.338 fib 0.834 parse 0.116 corpus 0.160 loop 0.250 sieve 0.629 |
| tag2 | 1 -> 0 | hotcalls, t2hot, t2wide | 0.262 | +6.2% | 6745 | -172 | kernel 0.317 fib 0.934 parse 0.108 corpus 0.153 loop 0.254 sieve 0.613 |
| align1 | 1 -> 0 | - | 0.252 | +2.1% | 6917 | +0 | kernel 0.353 fib 0.762 parse 0.108 corpus 0.144 loop 0.243 sieve 0.637 |
| ipaclone | 1 -> 0 | - | 0.252 | +2.0% | 6917 | +0 | kernel 0.335 fib 0.758 parse 0.106 corpus 0.157 loop 0.241 sieve 0.631 |
| lean | 1 -> 0 | - | 0.251 | +1.6% | 8750 | +1833 | kernel 0.344 fib 0.757 parse 0.108 corpus 0.150 loop 0.237 sieve 0.621 |
| bss | 1 -> 0 | - | 0.251 | +1.5% | 7973 | +1056 | kernel 0.342 fib 0.750 parse 0.109 corpus 0.151 loop 0.236 sieve 0.635 |
| opt | Os -> O2 | - | 0.250 | +1.2% | 6917 | +0 | kernel 0.431 fib 0.742 parse 0.104 corpus 0.180 loop 0.164 sieve 0.520 |
| rtloopall | 1 -> 0 | - | 0.249 | +0.6% | 7321 | +404 | kernel 0.315 fib 0.764 parse 0.110 corpus 0.148 loop 0.243 sieve 0.632 |
| thinhdr | 1 -> 0 | - | 0.248 | +0.4% | 7165 | +248 | kernel 0.312 fib 0.778 parse 0.108 corpus 0.150 loop 0.240 sieve 0.633 |
| t2hot | 2 -> 0 | - | 0.248 | +0.2% | 6917 | +0 | kernel 0.295 fib 0.784 parse 0.108 corpus 0.155 loop 0.242 sieve 0.624 |
| opbody | 1 -> 0 | - | 0.247 | -0.0% | 7045 | +128 | kernel 0.304 fib 0.782 parse 0.107 corpus 0.151 loop 0.240 sieve 0.624 |
| spec | 3 items -> 5 items | - | 0.238 | -3.7% | 6934 | +17 | kernel 0.313 fib 0.766 parse 0.094 corpus 0.140 loop 0.242 sieve 0.635 |
| tail | 1 -> 0 | d256, jit | 0.180 | -27.3% | 7032 | +115 | kernel 0.482 fib 0.184 parse 0.120 corpus 0.186 loop 0.094 sieve 0.689 |

## 073b373429

calibration, the design itself: speed in the run 0.251, measured now 0.264; size recorded 6909, measured 6909 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers, tfind | 0.577 | +118.4% | 7069 | +160 | kernel 0.576 fib 1.046 parse 0.621 corpus 0.629 loop 0.273 sieve 0.621 |
| escape | 2 -> 0 | ops10, rtloopall, supers | 0.548 | +107.2% | 7886 | +977 | kernel 0.588 fib 1.054 parse 0.240 corpus 0.324 loop 1.026 sieve 1.014 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.430 | +62.6% | 7053 | +144 | kernel 0.524 fib 1.080 parse 0.284 corpus 0.327 loop 0.280 sieve 0.634 |
| ops10 | 30 items -> 0 items | rtloop, rtloopall, supers | 0.362 | +36.9% | 7048 | +139 | kernel 0.325 fib 1.047 parse 0.117 corpus 0.168 loop 0.930 sieve 0.860 |
| rtloop | 1 -> 0 | rtloopall | 0.352 | +33.3% | 6779 | -130 | kernel 0.336 fib 0.964 parse 0.109 corpus 0.154 loop 1.000 sieve 0.929 |
| klookup | 1 -> 0 | ops10, supers | 0.331 | +25.3% | 6965 | +56 | kernel 0.369 fib 1.051 parse 0.182 corpus 0.220 loop 0.256 sieve 0.641 |
| swapi | 1 -> 0 | ops10, supers | 0.274 | +3.5% | 6917 | +8 | kernel 0.326 fib 1.022 parse 0.114 corpus 0.159 loop 0.255 sieve 0.650 |
| lean | 1 -> 0 | - | 0.273 | +3.2% | 8742 | +1833 | kernel 0.345 fib 0.923 parse 0.114 corpus 0.162 loop 0.256 sieve 0.640 |
| tag2 | 1 -> 0 | hotcalls, t2hot, t2wide | 0.271 | +2.5% | 6737 | -172 | kernel 0.351 fib 0.971 parse 0.113 corpus 0.159 loop 0.239 sieve 0.626 |
| opbody | 1 -> 0 | - | 0.269 | +1.9% | 7037 | +128 | kernel 0.348 fib 0.932 parse 0.113 corpus 0.152 loop 0.256 sieve 0.626 |
| t2wide | 1 -> 0 | - | 0.269 | +1.9% | 7096 | +187 | kernel 0.322 fib 0.836 parse 0.114 corpus 0.163 loop 0.282 sieve 0.658 |
| folds | 22 items -> 23 items | supers | 0.268 | +1.4% | 6917 | +8 | kernel 0.321 fib 0.917 parse 0.118 corpus 0.157 loop 0.253 sieve 0.616 |
| bss | 1 -> 0 | - | 0.267 | +0.9% | 7957 | +1048 | kernel 0.326 fib 0.958 parse 0.106 corpus 0.156 loop 0.263 sieve 0.623 |
| nocet | 1 -> 0 | - | 0.266 | +0.6% | 6909 | +0 | kernel 0.327 fib 0.966 parse 0.111 corpus 0.155 loop 0.244 sieve 0.625 |
| thinhdr | 1 -> 0 | - | 0.266 | +0.5% | 7157 | +248 | kernel 0.314 fib 0.966 parse 0.110 corpus 0.155 loop 0.256 sieve 0.616 |
| rtloopall | 1 -> 0 | - | 0.266 | +0.5% | 7313 | +404 | kernel 0.324 fib 0.967 parse 0.109 corpus 0.148 loop 0.260 sieve 0.637 |
| align1 | 1 -> 0 | - | 0.265 | +0.3% | 6909 | +0 | kernel 0.316 fib 0.951 parse 0.111 corpus 0.151 loop 0.261 sieve 0.624 |
| t2hot | 3 -> 0 | - | 0.264 | -0.2% | 6917 | +8 | kernel 0.316 fib 0.907 parse 0.113 corpus 0.156 loop 0.254 sieve 0.611 |
| tfind | 1 -> 0 | ops10 | 0.263 | -0.6% | 6909 | +0 | kernel 0.298 fib 0.956 parse 0.111 corpus 0.159 loop 0.250 sieve 0.632 |
| tracer | 1 -> 0 | - | 0.262 | -0.9% | 6909 | +0 | kernel 0.302 fib 0.977 parse 0.107 corpus 0.154 loop 0.253 sieve 0.633 |
| spec | 3 items -> 5 items | - | 0.256 | -3.1% | 6934 | +25 | kernel 0.321 fib 0.952 parse 0.102 corpus 0.141 loop 0.253 sieve 0.660 |
| supers | 16 items -> 0 items | - | 0.254 | -3.9% | 6942 | +33 | kernel 0.314 fib 0.799 parse 0.115 corpus 0.156 loop 0.236 sieve 0.618 |
| opt | Os -> O2 | - | 0.247 | -6.7% | 6909 | +0 | kernel 0.419 fib 0.690 parse 0.103 corpus 0.174 loop 0.176 sieve 0.535 |
| tail | 1 -> 0 | d256, jit | 0.180 | -32.0% | 7024 | +115 | kernel 0.465 fib 0.184 parse 0.121 corpus 0.194 loop 0.094 sieve 0.689 |

## 93e59c300b

calibration, the design itself: speed in the run 0.279, measured now 0.296; size recorded 6875, measured 6875 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers | 0.895 | +202.4% | 7018 | +143 | kernel 0.754 fib 1.120 parse 0.787 corpus 0.796 loop 1.085 sieve 0.999 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.503 | +69.9% | 7002 | +127 | kernel 0.480 fib 0.888 parse 0.243 corpus 0.302 loop 1.028 sieve 1.028 |
| escape | 2 -> 0 | ops10, supers | 0.469 | +58.6% | 7318 | +443 | kernel 0.491 fib 0.967 parse 0.184 corpus 0.253 loop 1.028 sieve 0.987 |
| klookup | 1 -> 0 | ops10, supers | 0.412 | +39.2% | 6914 | +39 | kernel 0.344 fib 0.970 parse 0.168 corpus 0.206 loop 1.026 sieve 0.961 |
| tag2 | 1 -> 0 | hotcalls, hotinl, t2hot, t2wide | 0.344 | +16.3% | 6716 | -159 | kernel 0.302 fib 0.998 parse 0.105 corpus 0.152 loop 1.003 sieve 0.941 |
| t2wide | 1 -> 0 | - | 0.342 | +15.7% | 7002 | +127 | kernel 0.318 fib 1.048 parse 0.094 corpus 0.148 loop 1.012 sieve 0.927 |
| swapi | 1 -> 0 | ops10, supers | 0.341 | +15.3% | 6891 | +16 | kernel 0.316 fib 1.054 parse 0.095 corpus 0.144 loop 1.013 sieve 0.970 |
| supers | 17 items -> 0 items | - | 0.331 | +11.8% | 6894 | +19 | kernel 0.289 fib 0.932 parse 0.092 corpus 0.142 loop 1.122 sieve 0.979 |
| nocet | 1 -> 0 | - | 0.324 | +9.6% | 6875 | +0 | kernel 0.294 fib 0.858 parse 0.101 corpus 0.142 loop 0.992 sieve 0.928 |
| opt | Os -> O2 | - | 0.320 | +8.1% | 6875 | +0 | kernel 0.377 fib 0.713 parse 0.087 corpus 0.145 loop 0.989 sieve 0.893 |
| folds | 21 items -> 23 items | supers | 0.316 | +6.7% | 6875 | +0 | kernel 0.301 fib 0.861 parse 0.092 corpus 0.138 loop 0.961 sieve 0.888 |
| ops10 | 31 items -> 0 items | supers | 0.316 | +6.6% | 7136 | +261 | kernel 0.300 fib 0.870 parse 0.099 corpus 0.145 loop 0.832 sieve 0.837 |
| spec | 4 items -> 5 items | - | 0.306 | +3.3% | 6875 | +0 | kernel 0.333 fib 0.747 parse 0.093 corpus 0.134 loop 0.855 sieve 0.834 |
| bss | 1 -> 0 | - | 0.305 | +3.1% | 7931 | +1056 | kernel 0.297 fib 0.737 parse 0.090 corpus 0.137 loop 0.981 sieve 0.821 |
| thinhdr | 1 -> 0 | - | 0.303 | +2.3% | 7123 | +248 | kernel 0.316 fib 0.757 parse 0.092 corpus 0.135 loop 0.853 sieve 0.815 |
| t2hot | 3 -> 0 | - | 0.302 | +2.2% | 6875 | +0 | kernel 0.305 fib 0.766 parse 0.088 corpus 0.141 loop 0.874 sieve 0.846 |
| hotinl | 10 -> 0 | - | 0.300 | +1.5% | 6819 | -56 | kernel 0.305 fib 0.734 parse 0.096 corpus 0.135 loop 0.846 sieve 0.833 |
| opbody | 1 -> 0 | - | 0.300 | +1.3% | 7005 | +130 | kernel 0.301 fib 0.763 parse 0.088 corpus 0.141 loop 0.852 sieve 0.822 |
| lean | 1 -> 0 | - | 0.298 | +0.7% | 8582 | +1707 | kernel 0.307 fib 0.741 parse 0.093 corpus 0.133 loop 0.835 sieve 0.839 |
| ipaclone | 1 -> 0 | - | 0.298 | +0.7% | 6875 | +0 | kernel 0.299 fib 0.742 parse 0.089 corpus 0.138 loop 0.861 sieve 0.813 |
| tracer | 1 -> 0 | - | 0.297 | +0.5% | 6875 | +0 | kernel 0.292 fib 0.762 parse 0.087 corpus 0.137 loop 0.876 sieve 0.851 |
| tail | 1 -> 0 | jit | 0.276 | -6.7% | 7000 | +125 | kernel 0.408 fib 0.187 parse 0.098 corpus 0.167 loop 1.292 sieve 1.006 |

## 1cc823130f

calibration, the design itself: speed in the run 0.283, measured now 0.312; size recorded 6819, measured 6819 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers, tfind | 0.904 | +189.6% | 6970 | +151 | kernel 0.806 fib 1.113 parse 0.785 corpus 0.797 loop 1.076 sieve 1.007 |
| escape | 2 -> 0 | ops10, supers | 0.526 | +68.6% | 7269 | +450 | kernel 0.565 fib 1.014 parse 0.235 corpus 0.301 loop 0.994 sieve 0.986 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.516 | +65.3% | 6962 | +143 | kernel 0.518 fib 0.897 parse 0.246 corpus 0.306 loop 1.046 sieve 1.049 |
| klookup | 1 -> 0 | ops10, supers | 0.419 | +34.3% | 6866 | +47 | kernel 0.356 fib 0.984 parse 0.167 corpus 0.212 loop 1.042 sieve 0.931 |
| t2wide | 1 -> 0 | - | 0.350 | +12.1% | 6962 | +143 | kernel 0.312 fib 1.067 parse 0.107 corpus 0.153 loop 0.967 sieve 0.929 |
| tag2 | 1 -> 0 | hotcalls, t2hot, t2wide | 0.350 | +12.1% | 6716 | -103 | kernel 0.324 fib 1.001 parse 0.105 corpus 0.154 loop 1.004 sieve 0.905 |
| swapi | 1 -> 0 | ops10, supers | 0.347 | +11.0% | 6827 | +8 | kernel 0.328 fib 1.010 parse 0.101 corpus 0.146 loop 1.026 sieve 0.941 |
| supers | 17 items -> 0 items | - | 0.345 | +10.4% | 6830 | +11 | kernel 0.319 fib 0.911 parse 0.099 corpus 0.148 loop 1.139 sieve 0.933 |
| ops10 | 31 items -> 0 items | supers | 0.341 | +9.4% | 7055 | +236 | kernel 0.316 fib 1.015 parse 0.104 corpus 0.150 loop 0.927 sieve 0.851 |
| nocet | 1 -> 0 | - | 0.335 | +7.2% | 6819 | +0 | kernel 0.328 fib 0.839 parse 0.104 corpus 0.151 loop 0.968 sieve 0.894 |
| opt | Os -> O2 | - | 0.327 | +4.7% | 6819 | +0 | kernel 0.368 fib 0.702 parse 0.096 corpus 0.158 loop 0.950 sieve 0.857 |
| folds | 21 items -> 23 items | supers | 0.323 | +3.5% | 6819 | +0 | kernel 0.319 fib 0.827 parse 0.097 corpus 0.144 loop 0.953 sieve 0.865 |
| bss | 1 -> 0 | - | 0.320 | +2.5% | 7875 | +1056 | kernel 0.329 fib 0.753 parse 0.095 corpus 0.146 loop 0.977 sieve 0.821 |
| t2hot | 3 -> 0 | - | 0.312 | -0.0% | 6819 | +0 | kernel 0.319 fib 0.751 parse 0.095 corpus 0.147 loop 0.882 sieve 0.815 |
| lean | 1 -> 0 | - | 0.312 | -0.1% | 8502 | +1683 | kernel 0.322 fib 0.752 parse 0.097 corpus 0.145 loop 0.868 sieve 0.840 |
| spec | 4 items -> 5 items | - | 0.310 | -0.6% | 6819 | +0 | kernel 0.320 fib 0.734 parse 0.098 corpus 0.146 loop 0.856 sieve 0.840 |
| thinhdr | 1 -> 0 | - | 0.309 | -0.9% | 7067 | +248 | kernel 0.319 fib 0.766 parse 0.095 corpus 0.146 loop 0.834 sieve 0.825 |
| tfind | 1 -> 0 | ops10 | 0.308 | -1.4% | 6819 | +0 | kernel 0.311 fib 0.746 parse 0.096 corpus 0.143 loop 0.867 sieve 0.798 |
| ipaclone | 1 -> 0 | - | 0.308 | -1.4% | 6819 | +0 | kernel 0.323 fib 0.739 parse 0.094 corpus 0.142 loop 0.860 sieve 0.821 |
| tracer | 1 -> 0 | - | 0.305 | -2.4% | 6819 | +0 | kernel 0.297 fib 0.771 parse 0.094 corpus 0.141 loop 0.862 sieve 0.818 |
| opbody | 1 -> 0 | - | 0.303 | -2.8% | 6949 | +130 | kernel 0.293 fib 0.736 parse 0.097 corpus 0.144 loop 0.852 sieve 0.855 |
| tail | 1 -> 0 | jit | 0.284 | -8.9% | 6944 | +125 | kernel 0.432 fib 0.185 parse 0.105 corpus 0.176 loop 1.253 sieve 0.994 |

## e19afb09ff

calibration, the design itself: speed in the run 0.293, measured now 0.315; size recorded 6795, measured 6795 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers, tfind | 0.913 | +189.9% | 6954 | +159 | kernel 0.799 fib 1.122 parse 0.789 corpus 0.816 loop 1.098 sieve 1.015 |
| escape | 2 -> 0 | ops10, supers | 0.533 | +69.3% | 7261 | +466 | kernel 0.549 fib 1.017 parse 0.243 corpus 0.315 loop 1.005 sieve 0.993 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.530 | +68.3% | 6946 | +151 | kernel 0.536 fib 0.866 parse 0.263 corpus 0.319 loop 1.071 sieve 1.020 |
| klookup | 1 -> 0 | ops10, supers | 0.440 | +39.8% | 6842 | +47 | kernel 0.376 fib 0.993 parse 0.189 corpus 0.224 loop 1.042 sieve 0.959 |
| tag2 | 1 -> 0 | t2hot, t2wide | 0.380 | +20.9% | 6771 | -24 | kernel 0.372 fib 1.001 parse 0.120 corpus 0.177 loop 1.013 sieve 0.908 |
| t2wide | 1 -> 0 | - | 0.378 | +20.1% | 6930 | +135 | kernel 0.358 fib 1.049 parse 0.120 corpus 0.169 loop 1.014 sieve 0.921 |
| ops10 | 31 items -> 0 items | supers | 0.368 | +16.8% | 7039 | +244 | kernel 0.349 fib 1.004 parse 0.122 corpus 0.170 loop 0.926 sieve 0.847 |
| swapi | 1 -> 0 | ops10, supers | 0.366 | +16.3% | 6795 | +0 | kernel 0.320 fib 1.034 parse 0.117 corpus 0.164 loop 1.037 sieve 0.956 |
| opt | Os -> O2 | - | 0.365 | +16.0% | 6795 | +0 | kernel 0.436 fib 0.704 parse 0.112 corpus 0.196 loop 0.958 sieve 0.864 |
| supers | 17 items -> 0 items | - | 0.356 | +13.0% | 6798 | +3 | kernel 0.318 fib 0.904 parse 0.115 corpus 0.154 loop 1.121 sieve 0.939 |
| nocet | 1 -> 0 | - | 0.352 | +11.8% | 6795 | +0 | kernel 0.325 fib 0.835 parse 0.117 corpus 0.171 loop 0.989 sieve 0.896 |
| folds | 21 items -> 23 items | supers | 0.347 | +10.4% | 6795 | +0 | kernel 0.352 fib 0.835 parse 0.113 corpus 0.163 loop 0.938 sieve 0.919 |
| tracer | 1 -> 0 | - | 0.323 | +2.6% | 6795 | +0 | kernel 0.342 fib 0.752 parse 0.103 corpus 0.154 loop 0.859 sieve 0.827 |
| bss | 1 -> 0 | - | 0.323 | +2.5% | 7851 | +1056 | kernel 0.291 fib 0.755 parse 0.105 corpus 0.149 loop 1.023 sieve 0.834 |
| tfind | 1 -> 0 | ops10 | 0.317 | +0.8% | 6795 | +0 | kernel 0.323 fib 0.739 parse 0.105 corpus 0.151 loop 0.851 sieve 0.804 |
| thinhdr | 1 -> 0 | - | 0.316 | +0.4% | 7043 | +248 | kernel 0.314 fib 0.748 parse 0.106 corpus 0.150 loop 0.844 sieve 0.811 |
| opbody | 1 -> 0 | - | 0.315 | +0.1% | 6925 | +130 | kernel 0.299 fib 0.753 parse 0.105 corpus 0.154 loop 0.857 sieve 0.821 |
| t2hot | 3 -> 0 | - | 0.314 | -0.1% | 6795 | +0 | kernel 0.320 fib 0.745 parse 0.100 corpus 0.149 loop 0.861 sieve 0.807 |
| lean | 1 -> 0 | - | 0.314 | -0.3% | 8478 | +1683 | kernel 0.296 fib 0.755 parse 0.106 corpus 0.150 loop 0.853 sieve 0.805 |
| ipaclone | 1 -> 0 | - | 0.312 | -0.9% | 6795 | +0 | kernel 0.315 fib 0.733 parse 0.100 corpus 0.149 loop 0.859 sieve 0.823 |
| tail | 1 -> 0 | jit | 0.311 | -1.3% | 6920 | +125 | kernel 0.505 fib 0.189 parse 0.120 corpus 0.207 loop 1.223 sieve 0.953 |
| spec | 3 items -> 5 items | - | 0.309 | -1.8% | 6819 | +24 | kernel 0.321 fib 0.743 parse 0.096 corpus 0.142 loop 0.865 sieve 0.826 |

## ad34255b18

calibration, the design itself: speed in the run 0.310, measured now 0.336; size recorded 6787, measured 6787 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers, tfind | 0.894 | +166.2% | 6946 | +159 | kernel 0.761 fib 1.065 parse 0.800 corpus 0.804 loop 1.094 sieve 1.014 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.567 | +68.8% | 6930 | +143 | kernel 0.529 fib 1.098 parse 0.282 corpus 0.329 loop 1.087 sieve 1.037 |
| escape | 2 -> 0 | ops10, supers | 0.538 | +60.4% | 7295 | +508 | kernel 0.547 fib 1.038 parse 0.241 corpus 0.318 loop 1.042 sieve 1.014 |
| klookup | 1 -> 0 | ops10, supers | 0.451 | +34.4% | 6834 | +47 | kernel 0.375 fib 1.110 parse 0.189 corpus 0.231 loop 1.029 sieve 0.907 |
| t2wide | 1 -> 0 | - | 0.380 | +13.0% | 6936 | +149 | kernel 0.354 fib 0.967 parse 0.122 corpus 0.166 loop 1.129 sieve 0.991 |
| nocet | 1 -> 0 | - | 0.367 | +9.3% | 6787 | +0 | kernel 0.349 fib 0.995 parse 0.114 corpus 0.164 loop 1.033 sieve 0.918 |
| swapi | 1 -> 0 | ops10, supers | 0.366 | +9.1% | 6787 | +0 | kernel 0.326 fib 1.005 parse 0.116 corpus 0.165 loop 1.052 sieve 0.945 |
| folds | 22 items -> 23 items | supers | 0.365 | +8.7% | 6797 | +10 | kernel 0.341 fib 0.975 parse 0.113 corpus 0.162 loop 1.064 sieve 0.950 |
| ops10 | 30 items -> 0 items | supers | 0.364 | +8.5% | 7048 | +261 | kernel 0.332 fib 1.056 parse 0.118 corpus 0.163 loop 0.949 sieve 0.867 |
| supers | 16 items -> 0 items | - | 0.362 | +7.7% | 6805 | +18 | kernel 0.337 fib 0.841 parse 0.117 corpus 0.165 loop 1.128 sieve 0.944 |
| opt | Os -> O2 | - | 0.361 | +7.7% | 6787 | +0 | kernel 0.432 fib 0.747 parse 0.104 corpus 0.191 loop 0.968 sieve 0.818 |
| tag2 | 1 -> 0 | hotcalls, t2hot, t2wide | 0.347 | +3.5% | 6628 | -159 | kernel 0.320 fib 0.953 parse 0.109 corpus 0.158 loop 0.961 sieve 0.872 |
| bss | 1 -> 0 | - | 0.343 | +2.0% | 7843 | +1056 | kernel 0.312 fib 0.794 parse 0.108 corpus 0.155 loop 1.138 sieve 0.920 |
| lean | 1 -> 0 | - | 0.338 | +0.7% | 8470 | +1683 | kernel 0.322 fib 0.763 parse 0.111 corpus 0.158 loop 1.028 sieve 0.917 |
| opbody | 1 -> 0 | - | 0.337 | +0.5% | 6915 | +128 | kernel 0.316 fib 0.799 parse 0.107 corpus 0.157 loop 1.030 sieve 0.905 |
| tfind | 1 -> 0 | ops10 | 0.335 | -0.3% | 6787 | +0 | kernel 0.328 fib 0.751 parse 0.110 corpus 0.157 loop 0.996 sieve 0.919 |
| t2hot | 2 -> 0 | - | 0.334 | -0.7% | 6787 | +0 | kernel 0.317 fib 0.767 parse 0.110 corpus 0.154 loop 1.001 sieve 0.923 |
| ipaclone | 1 -> 0 | - | 0.333 | -0.8% | 6787 | +0 | kernel 0.317 fib 0.744 parse 0.108 corpus 0.161 loop 1.000 sieve 0.926 |
| noreorder | 1 -> 0 | - | 0.331 | -1.4% | 6787 | +0 | kernel 0.297 fib 0.767 parse 0.110 corpus 0.155 loop 1.031 sieve 0.916 |
| thinhdr | 1 -> 0 | - | 0.331 | -1.4% | 7035 | +248 | kernel 0.319 fib 0.775 parse 0.105 corpus 0.151 loop 1.008 sieve 0.905 |
| spec | 4 items -> 5 items | - | 0.319 | -5.1% | 6795 | +8 | kernel 0.310 fib 0.778 parse 0.098 corpus 0.143 loop 0.979 sieve 0.931 |
| tail | 1 -> 0 | jit | 0.309 | -8.1% | 6912 | +125 | kernel 0.494 fib 0.180 parse 0.124 corpus 0.207 loop 1.228 sieve 0.956 |

## 0df9664b32

calibration, the design itself: speed in the run 0.314, measured now 0.342; size recorded 6779, measured 6779 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers, tfind | 0.863 | +152.5% | 6946 | +167 | kernel 0.784 fib 0.911 parse 0.782 corpus 0.793 loop 1.079 sieve 0.993 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.571 | +67.2% | 6930 | +151 | kernel 0.536 fib 1.110 parse 0.283 corpus 0.328 loop 1.098 sieve 1.041 |
| escape | 2 -> 0 | ops10, supers | 0.531 | +55.3% | 7295 | +516 | kernel 0.553 fib 0.965 parse 0.237 corpus 0.314 loop 1.060 sieve 1.027 |
| klookup | 1 -> 0 | ops10, supers | 0.448 | +31.2% | 6826 | +47 | kernel 0.370 fib 1.069 parse 0.185 corpus 0.231 loop 1.075 sieve 0.927 |
| t2wide | 1 -> 0 | - | 0.368 | +7.7% | 6920 | +141 | kernel 0.331 fib 0.927 parse 0.118 corpus 0.170 loop 1.093 sieve 0.966 |
| supers | 16 items -> 0 items | - | 0.367 | +7.5% | 6805 | +26 | kernel 0.342 fib 0.908 parse 0.115 corpus 0.165 loop 1.129 sieve 0.952 |
| folds | 22 items -> 23 items | supers | 0.362 | +6.0% | 6797 | +18 | kernel 0.336 fib 0.957 parse 0.113 corpus 0.162 loop 1.055 sieve 0.960 |
| tag2 | 1 -> 0 | hotcalls, t2hot, t2wide | 0.361 | +5.5% | 6628 | -151 | kernel 0.350 fib 0.920 parse 0.114 corpus 0.164 loop 1.018 sieve 0.920 |
| ops10 | 30 items -> 0 items | supers | 0.356 | +4.3% | 7048 | +269 | kernel 0.334 fib 0.941 parse 0.116 corpus 0.168 loop 0.943 sieve 0.828 |
| swapi | 1 -> 0 | ops10, supers | 0.356 | +4.1% | 6787 | +8 | kernel 0.327 fib 0.907 parse 0.115 corpus 0.169 loop 0.987 sieve 0.919 |
| nocet | 1 -> 0 | - | 0.354 | +3.5% | 6779 | +0 | kernel 0.327 fib 0.954 parse 0.113 corpus 0.161 loop 0.973 sieve 0.877 |
| bss | 1 -> 0 | - | 0.353 | +3.3% | 7835 | +1056 | kernel 0.325 fib 0.820 parse 0.108 corpus 0.161 loop 1.189 sieve 0.905 |
| opt | Os -> O2 | - | 0.349 | +2.1% | 6779 | +0 | kernel 0.400 fib 0.731 parse 0.099 corpus 0.185 loop 0.962 sieve 0.766 |
| lean | 1 -> 0 | - | 0.346 | +1.4% | 8454 | +1675 | kernel 0.327 fib 0.854 parse 0.109 corpus 0.157 loop 1.047 sieve 0.919 |
| align1 | 1 -> 0 | - | 0.341 | -0.1% | 6779 | +0 | kernel 0.318 fib 0.844 parse 0.107 corpus 0.158 loop 1.021 sieve 0.935 |
| tfind | 1 -> 0 | ops10 | 0.340 | -0.4% | 6779 | +0 | kernel 0.341 fib 0.816 parse 0.106 corpus 0.154 loop 1.007 sieve 0.925 |
| thinhdr | 1 -> 0 | - | 0.340 | -0.4% | 7027 | +248 | kernel 0.331 fib 0.811 parse 0.109 corpus 0.154 loop 1.010 sieve 0.940 |
| ipaclone | 1 -> 0 | - | 0.339 | -0.7% | 6779 | +0 | kernel 0.311 fib 0.832 parse 0.109 corpus 0.156 loop 1.026 sieve 0.933 |
| t2hot | 3 -> 0 | - | 0.338 | -1.0% | 6787 | +8 | kernel 0.300 fib 0.851 parse 0.107 corpus 0.159 loop 1.021 sieve 0.928 |
| opbody | 1 -> 0 | - | 0.337 | -1.4% | 6907 | +128 | kernel 0.316 fib 0.820 parse 0.108 corpus 0.156 loop 0.989 sieve 0.925 |
| spec | 3 items -> 5 items | - | 0.328 | -4.0% | 6795 | +16 | kernel 0.326 fib 0.821 parse 0.097 corpus 0.146 loop 1.005 sieve 0.925 |
| tail | 1 -> 0 | d256, jit | 0.313 | -8.5% | 6904 | +125 | kernel 0.494 fib 0.181 parse 0.123 corpus 0.212 loop 1.281 sieve 1.000 |

## 42238f7fd1

calibration, the design itself: speed in the run 0.326, measured now 0.345; size recorded 6771, measured 6771 - ok

| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |
|---|---|---|---|---|---|---|---|
| kfast | 1 -> 0 | kinput, klookup, ops10, supers, tfind | 0.916 | +165.8% | 6946 | +175 | kernel 0.803 fib 1.050 parse 0.798 corpus 0.826 loop 1.159 sieve 1.022 |
| kinput | 1 -> 0 | klookup, ops10, supers | 0.561 | +62.7% | 6930 | +159 | kernel 0.503 fib 1.102 parse 0.286 corpus 0.321 loop 1.088 sieve 1.004 |
| escape | 2 -> 0 | ops10, supers | 0.541 | +56.9% | 7261 | +490 | kernel 0.569 fib 1.014 parse 0.244 corpus 0.321 loop 1.024 sieve 0.990 |
| klookup | 1 -> 0 | ops10, supers | 0.437 | +26.8% | 6826 | +55 | kernel 0.367 fib 1.035 parse 0.183 corpus 0.227 loop 1.005 sieve 0.936 |
| ops10 | 30 items -> 0 items | supers | 0.379 | +10.0% | 7048 | +277 | kernel 0.341 fib 1.057 parse 0.123 corpus 0.169 loop 1.039 sieve 0.909 |
| swapi | 1 -> 0 | ops10, supers | 0.366 | +6.3% | 6779 | +8 | kernel 0.353 fib 0.986 parse 0.115 corpus 0.164 loop 1.006 sieve 0.909 |
| supers | 16 items -> 0 items | - | 0.362 | +5.0% | 6805 | +34 | kernel 0.330 fib 0.879 parse 0.115 corpus 0.167 loop 1.109 sieve 0.994 |
| t2wide | 1 -> 0 | - | 0.360 | +4.6% | 6920 | +149 | kernel 0.313 fib 0.921 parse 0.116 corpus 0.164 loop 1.106 sieve 0.971 |
| nogcse | 1 -> 0 | - | 0.358 | +4.0% | 6771 | +0 | kernel 0.339 fib 0.839 parse 0.117 corpus 0.167 loop 1.062 sieve 0.962 |
| folds | 21 items -> 23 items | supers | 0.355 | +3.0% | 6797 | +26 | kernel 0.327 fib 0.953 parse 0.112 corpus 0.159 loop 1.013 sieve 0.933 |
| bss | 1 -> 0 | - | 0.352 | +2.2% | 7819 | +1048 | kernel 0.322 fib 0.837 parse 0.107 corpus 0.159 loop 1.180 sieve 0.934 |
| tracer | 1 -> 0 | - | 0.351 | +1.9% | 6771 | +0 | kernel 0.342 fib 0.869 parse 0.110 corpus 0.157 loop 1.047 sieve 0.917 |
| nocet | 1 -> 0 | - | 0.349 | +1.4% | 6771 | +0 | kernel 0.332 fib 0.834 parse 0.116 corpus 0.160 loop 1.009 sieve 0.903 |
| lean | 1 -> 0 | - | 0.349 | +1.3% | 8446 | +1675 | kernel 0.334 fib 0.896 parse 0.110 corpus 0.154 loop 1.028 sieve 0.944 |
| opbody | 1 -> 0 | - | 0.347 | +0.8% | 6899 | +128 | kernel 0.332 fib 0.863 parse 0.105 corpus 0.157 loop 1.070 sieve 0.931 |
| thinhdr | 1 -> 0 | - | 0.346 | +0.5% | 7019 | +248 | kernel 0.332 fib 0.849 parse 0.109 corpus 0.158 loop 1.030 sieve 0.945 |
| opt | Os -> O2 | - | 0.344 | -0.2% | 6771 | +0 | kernel 0.408 fib 0.647 parse 0.101 corpus 0.188 loop 0.958 sieve 0.842 |
| t2hot | 3 -> 0 | - | 0.343 | -0.4% | 6779 | +8 | kernel 0.321 fib 0.874 parse 0.107 corpus 0.151 loop 1.050 sieve 0.944 |
| tag2 | 1 -> 0 | hotcalls, t2hot, t2wide | 0.342 | -0.7% | 6628 | -143 | kernel 0.314 fib 0.939 parse 0.107 corpus 0.162 loop 0.912 sieve 0.885 |
| align1 | 1 -> 0 | - | 0.341 | -1.0% | 6771 | +0 | kernel 0.312 fib 0.850 parse 0.111 corpus 0.150 loop 1.049 sieve 0.923 |
| spec | 3 items -> 5 items | - | 0.341 | -1.1% | 6795 | +24 | kernel 0.340 fib 0.846 parse 0.104 corpus 0.151 loop 1.023 sieve 0.930 |
| tfind | 1 -> 0 | ops10 | 0.341 | -1.1% | 6771 | +0 | kernel 0.308 fib 0.859 parse 0.108 corpus 0.155 loop 1.038 sieve 0.928 |
| tail | 1 -> 0 | d256, jit | 0.318 | -7.8% | 6896 | +125 | kernel 0.484 fib 0.184 parse 0.127 corpus 0.205 loop 1.395 sieve 1.025 |

