# s2-s5, frozen (Iteration 588)

The hand-made stages s2-cpt16, s3-cpt16f, s4-cv8 and s5-cv8spec, built once and kept: the values only they use - scale
1-3, bytehdr 0, varcall 0 (with sharedcall 0), doesfar 0 - are being retired from the source
(results/drafts/retire-stages-584.md; the owner, 584: "if it will not lose good designs"). tools/build-stages.sh copies
these files into build/ instead of building them; `evolve.py --validate` checks them against SHA256SUMS, and rebuilds
s0, s1 and s6 as before.

Built by tools/build-stages.sh (LAYOUTS=1, ENGINE_RT=nolibc - static) at Iteration 587's master, ee7a0ee - its recipe:
`git show ee7a0ee:tools/build-stages.sh` - with gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0: the same bytes as that master's own build in any
directory. Per stage and width (64: 8-byte cells, x86-64; 32: 4-byte cells, i386): the engine STAGE-W, the shell image
STAGE-W.img, the kernel image STAGE-kW.img and the self-hosting image STAGE-sW.img. Copied only where they run - an x86
Linux host, at the widths it builds (the Tegra has none; no tool there uses them) - and in one layout variant only.
