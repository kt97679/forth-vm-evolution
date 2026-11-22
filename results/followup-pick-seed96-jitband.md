# Seed 96-jitband's best beside the portable designs found before, re-measured on three machines, every session pooled (Iteration 725)

`python3 lab/evolve/final-pick.py results/followup-seed96-jitband.md results/chain-followup96-jitband/s1/loadtest.md results/chain-followup96-jitband/s1/*.out.json --also-session results/chain-followup96-jitband/s2 ... s10` - the laptop 7 sessions (10 rounds), dream 10 at 8-byte cells and 10 at 4-byte, the Tegra 0 (lab/evolve/process-followup.sh). The roles against results/handoff-relf-657.md: results/followup-roles-seed96-jitband.md.

# The final set, re-measured - 58 candidates, 58 re-measured at both widths (final-pick.py; GOALS.md step 3, the owner's decisions of Iteration 573)

Two or more sessions (Iteration 588): this one and results/chain-followup96-jitband/s2, results/chain-followup96-jitband/s3, results/chain-followup96-jitband/s4, results/chain-followup96-jitband/s5, results/chain-followup96-jitband/s6, results/chain-followup96-jitband/s7, results/chain-followup96-jitband/s8, results/chain-followup96-jitband/s9, results/chain-followup96-jitband/s10 - the laptop's re-measures each the geometric mean of the sessions that have it; each host's lines its mean in step 5, each named in step 4.

Chosen from the laptop's re-measures alone (loadtest.py --ids, idle), re-measured against re-measured: the four extremes, then by hypervolume to 10. Size and memory exact.

| # | design | why | speed alone (in-run) | binary + image | memory KB | 32-bit alone (in-run) | under load / alone | adds |
|---|---|---|---|---|---|---|---|---|
| 1 | 13a2b38e1b | fastest | 0.1922 (0.1879) | 36,408 | 216 | 0.2116 (0.2056) | 0.946 | 0.11958 |
| 2 | 61e5e8b2b3 | smallest | 0.2196 (0.2126) | 35,333 | 268 | 0.2385 (0.2342) | 0.952 | 0.00212 |
| 3 | da4a69ec26 | least memory | 0.2129 (0.2074) | 35,792 | 200 | 0.2345 (0.2225) | 0.959 | 0.01866 |
| 4 | fa38596098 | fastest at 32 bits | 0.1952 (0.1976) | 36,360 | 208 | 0.2094 (0.2097) | 0.948 | 0.00115 |
| 5 | 50e56fd555 | adds the most | 0.2304 (0.2220) | 35,360 | 208 | 0.2474 (0.2431) | 0.939 | 0.00095 |
| 6 | 4c0bcc453e | adds the most, the knee | 0.2151 (0.2050) | 35,540 | 200 | 0.2314 (0.2274) | 0.956 | 0.00018 |
| 7 | 893d4cb050 | adds the most | 0.2038 (0.2039) | 35,789 | 216 | 0.2154 (0.2138) | 0.950 | 0.00010 |
| 8 | 8ddaa8f03a | adds the most | 0.2117 (0.2075) | 35,830 | 204 | 0.2258 (0.2298) | 0.938 | 0.00005 |
| 9 | 15eda54ebd | adds the most | 0.1925 (0.1937) | 36,344 | 208 | 0.2165 (0.2111) | 0.932 | 0.00005 |
| 10 | eff1ca72dc | adds the most | 0.2137 (0.2091) | 35,349 | 252 | 0.2290 (0.2246) | 0.953 | 0.00003 |

Against the in-run set: in now 13a2b38e1b, 15eda54ebd, 4c0bcc453e, 50e56fd555, 61e5e8b2b3, 893d4cb050, 8ddaa8f03a, da4a69ec26, eff1ca72dc, fa38596098; out now none - both kept as candidates.
Under load: the extremes fastest 15eda54ebd; smallest 59a1461f03; least memory da4a69ec26; fastest at 32 bits c6f1c1331b; in the set under load only 08578f5e3d, 59a1461f03, aba773be87, c6f1c1331b, alone only 13a2b38e1b, 61e5e8b2b3, 893d4cb050, eff1ca72dc.

dream (4-byte cells): 28 candidates measured; its fastest 15eda54ebd 0.255; Spearman with the laptop alone 0.596 over 28; FLAGGED, among its fastest five and not in the set: c6f1c1331b, f13b982631, 3a5d7735b0.

dream (8-byte cells): 28 candidates measured; its fastest fa38596098 0.247; Spearman with the laptop alone 0.810 over 28; FLAGGED, among its fastest five and not in the set: c6f1c1331b.

dream (4-byte cells): 28 candidates measured; its fastest 15eda54ebd 0.254; Spearman with the laptop alone 0.583 over 28; FLAGGED, among its fastest five and not in the set: c6f1c1331b, 08578f5e3d, 70124be7f5, 3a5d7735b0.

dream (8-byte cells): 28 candidates measured; its fastest fa38596098 0.248; Spearman with the laptop alone 0.869 over 28; FLAGGED, among its fastest five and not in the set: c6f1c1331b, 08578f5e3d.

dream (4-byte cells): 28 candidates measured; its fastest c6f1c1331b 0.257; Spearman with the laptop alone 0.634 over 28; FLAGGED, among its fastest five and not in the set: c6f1c1331b, ad89e9f59c, 456bd9c43e, 80a9d8a2e4, f13b982631.

dream (8-byte cells): 28 candidates measured; its fastest fa38596098 0.248; Spearman with the laptop alone 0.831 over 28; FLAGGED, among its fastest five and not in the set: c6f1c1331b, 08578f5e3d.

dream (4-byte cells): 28 candidates measured; its fastest 15eda54ebd 0.254; Spearman with the laptop alone 0.604 over 28; FLAGGED, among its fastest five and not in the set: c6f1c1331b, 08578f5e3d, 3a5d7735b0, f13b982631.

dream (8-byte cells): 28 candidates measured; its fastest fa38596098 0.249; Spearman with the laptop alone 0.851 over 28; FLAGGED, among its fastest five and not in the set: c6f1c1331b, 08578f5e3d.

dream (4-byte cells): 28 candidates measured; its fastest c6f1c1331b 0.257; Spearman with the laptop alone 0.583 over 28; FLAGGED, among its fastest five and not in the set: c6f1c1331b, 3a5d7735b0, aba773be87, 80a9d8a2e4.

dream (8-byte cells): 28 candidates measured; its fastest fa38596098 0.247; Spearman with the laptop alone 0.882 over 28; FLAGGED, among its fastest five and not in the set: c6f1c1331b, 62e9ee3802.

dream (4-byte cells): 28 candidates measured; its fastest c6f1c1331b 0.256; Spearman with the laptop alone 0.600 over 28; FLAGGED, among its fastest five and not in the set: c6f1c1331b, 3a5d7735b0, 456bd9c43e, aba773be87.

dream (8-byte cells): 28 candidates measured; its fastest fa38596098 0.248; Spearman with the laptop alone 0.850 over 28; FLAGGED, among its fastest five and not in the set: c6f1c1331b, 08578f5e3d.

dream (4-byte cells): 28 candidates measured; its fastest c6f1c1331b 0.256; Spearman with the laptop alone 0.615 over 28; FLAGGED, among its fastest five and not in the set: c6f1c1331b, 3a5d7735b0, aba773be87, 456bd9c43e.

dream (8-byte cells): 28 candidates measured; its fastest fa38596098 0.249; Spearman with the laptop alone 0.875 over 28; FLAGGED, among its fastest five and not in the set: c6f1c1331b, f13b982631.

dream (4-byte cells): 28 candidates measured; its fastest 15eda54ebd 0.257; Spearman with the laptop alone 0.605 over 28; FLAGGED, among its fastest five and not in the set: c6f1c1331b, 3a5d7735b0, aba773be87, 08578f5e3d.

dream (8-byte cells): 28 candidates measured; its fastest fa38596098 0.248; Spearman with the laptop alone 0.828 over 28; FLAGGED, among its fastest five and not in the set: c6f1c1331b, 08578f5e3d.

dream (4-byte cells): 28 candidates measured; its fastest 15eda54ebd 0.255; Spearman with the laptop alone 0.609 over 28; FLAGGED, among its fastest five and not in the set: c6f1c1331b, aba773be87, 70124be7f5, f13b982631.

dream (8-byte cells): 28 candidates measured; its fastest c6f1c1331b 0.249; Spearman with the laptop alone 0.887 over 28; FLAGGED, among its fastest five and not in the set: c6f1c1331b, f13b982631.

dream (4-byte cells): 28 candidates measured; its fastest c6f1c1331b 0.258; Spearman with the laptop alone 0.585 over 28; FLAGGED, among its fastest five and not in the set: c6f1c1331b, 70124be7f5, f13b982631, 3a5d7735b0.

dream (8-byte cells): 28 candidates measured; its fastest fa38596098 0.250; Spearman with the laptop alone 0.865 over 28; FLAGGED, among its fastest five and not in the set: c6f1c1331b, 08578f5e3d.

## Across machines (GOALS.md, Iteration 377; the owner's terms at 576)

Each class once - x86-64 (the laptop, dream), x86-32 (the laptop, dream); the mean their geometric mean (lower is faster). No ARMv7 reading - two classes. The veto (25%) removes nothing: it names the generic pick only.

| # | design | x86-64 | x86-32 | mean | behind its class's best | in the set |
|---|---|---|---|---|---|---|
| 1 | 00b9c7bca8 | 0.2027 | 0.2196 | 0.2110 | x86-64 +1% | ADDED |
| 2 | 058d79c378 | 0.2046 | 0.2210 | 0.2127 | x86-64 +2%, x86-32 +1% | ADDED |
| 3 | 458fe81373 | 0.2006 | 0.2255 | 0.2127 | x86-32 +3% | ADDED |
| 4 | a1ea1a59d0 | 0.2026 | 0.2257 | 0.2138 | x86-64 +1%, x86-32 +3% | - |
| 5 | fc5f98ee1b | 0.2046 | 0.2237 | 0.2139 | x86-64 +2%, x86-32 +2% | - |
| 6 | 74b2fd6bd1 | 0.2034 | 0.2253 | 0.2141 | x86-64 +1%, x86-32 +3% | - |
| 7 | bc5c7ddb04 | 0.2028 | 0.2262 | 0.2142 | x86-64 +1%, x86-32 +3% | - |
| 8 | 23814801d2 | 0.2032 | 0.2263 | 0.2144 | x86-64 +1%, x86-32 +3% | - |
| 9 | 9b200c7dee | 0.2056 | 0.2261 | 0.2156 | x86-64 +3%, x86-32 +3% | - |
| 10 | bc2a5876c0 | 0.2071 | 0.2245 | 0.2156 | x86-64 +3%, x86-32 +2% | - |
| 11 | 1a2d53f3d8 | 0.2091 | 0.2227 | 0.2158 | x86-64 +4%, x86-32 +1% | - |
| 12 | 676e73c93f | 0.2068 | 0.2262 | 0.2163 | x86-64 +3%, x86-32 +3% | - |
| 13 | da4a69ec26 | 0.2129 | 0.2345 | 0.2234 | x86-64 +6%, x86-32 +7% | yes |
| 14 | fa38596098 | 0.2202 | 0.2353 | 0.2276 | x86-64 +10%, x86-32 +7% | yes |
| 15 | 15eda54ebd | 0.2203 | 0.2357 | 0.2278 | x86-64 +10%, x86-32 +7% | yes |
| 16 | 13a2b38e1b | 0.2198 | 0.2365 | 0.2280 | x86-64 +10%, x86-32 +8% | yes |
| 17 | 893d4cb050 | 0.2303 | 0.2403 | 0.2352 | x86-64 +15%, x86-32 +9% | yes |
| 18 | 8ddaa8f03a | 0.2348 | 0.2429 | 0.2388 | x86-64 +17%, x86-32 +11% | yes |
| 19 | 4c0bcc453e | 0.2417 | 0.2488 | 0.2452 | x86-64 +21%, x86-32 +13% | yes |
| 20 | 50e56fd555 | 0.2575 | 0.2638 | 0.2606 | x86-64 +28%, x86-32 +20% | yes |
| 21 | eff1ca72dc | 0.2389 | 0.4114 | 0.3135 | x86-64 +19%, x86-32 +87% | yes |
| 22 | 61e5e8b2b3 | 0.2428 | 0.4204 | 0.3195 | x86-64 +21%, x86-32 +91% | yes |

**The generic pick**: 00b9c7bca8, the mean 0.2110, within 25% of every class's best.
Each class's fastest: x86-64 458fe81373; x86-32 00b9c7bca8.
**Added to the set across machines** (never taken out): 00b9c7bca8 - across machines: the best mean #1; 058d79c378 - across machines: the best mean #2; 458fe81373 - across machines: the best mean #3.
