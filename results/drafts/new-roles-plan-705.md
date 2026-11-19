# The new roles - the plan (Iteration 705; the search-reopen plan's step 6)

**The owner (705)**: "let's go straight to the new designs" - no confirmation run after the series stopped at seed 96
(704); the 573 rule's 5 % band as it is, in two chains (a screen, then a shortlist), the first 21 hours, dream and the
Tegra beside the laptop.

**Why new roles at all**: since 678/686 the size counts the five selection programs' code, and step 3's genes (rtvar,
rtconst, rtinline) exist; the ten roles of 649 were chosen under the old size. Under today's measure none of the eight
holders the series' pool lacks is on its fronts, and the smallest holder, d180351903, is 22,837 B against the pool's
22,409 (results/roles-holders-705.md). Each role is chosen again from the series' pool (seeds 92-96) with its holder
re-measured beside it.

## The pool and the lists (results/drafts/new-roles-705.py; its output results/drafts/new-roles-705.txt)

46,971 alive designs: seed 96's database (its own and seeds 92-95's strict fronts, measured again in its generation 0)
and seeds 92-95's results files (their fronts, in-run - 406 designs no carry brought; b25c984a48, the stall's one front
death, among them). The true front 483 (182 after merging); its JIT-free designs' 383 (105).

- **results/followup-seed96-roles.md** - 944 designs (526 JIT, 418 JIT-free), the laptop and dream at both widths:
  final-set.py's select() to 30 and candidates() on the whole pool and on its JIT-free designs (every alive design
  within 5 % of the fastest at either width - 239 and 264 builds on the whole, 170 and 96 JIT-free; the 5 smallest, the
  5 leanest, the merged), the knee (bee5d0daa2 both), the JIT-free true front after merging (no in-run reading sees
  ARMv7 - the ARM roles' screen), the 5 smallest JIT designs, the ten holders.
- **results/followup-seed96-roles-arm.md** - 437 for the Tegra: the JIT-free ones, the whole pool's set (19 JIT designs
  with the holders - each its JIT-off build there, final-pick.py's mark) and the ten holders.
- **results/roles-holders-705.md** - the ten holders under today's measure (results/drafts/holders-705.py, built here: the
  binary, the image and the programs' code exact - 782f3ad7ff and 3eb59b271d the same bytes as seed 96's records; the
  memory this sandbox's, 12-16 KB above the laptop's, so the chain measures them again: lab/evolve/measure-ids.py).

In-run, among them: the fastest 923951e8ab 0.1190 (JIT), at 32 bits 0fed6b2276 0.1470; JIT-free a4e502f224 0.2665, at 32
bits 3dc6d09801 0.2782; the smallest 21768033b7 22,409 B; the least memory 16560cb51f 108 KB; the smallest JIT design
d8f72aa60f 32,661 B. Every id resolves on the laptop (xcheck.py --also: 185 in results files, 759 in seed 96's
database, build/evolve/db.jsonl there - an experiment chain archives nothing).

## Chain A - the screen (this bundle's NEXT-RUN and REMOTES; about 21.5 hours)

- The laptop: `measure-ids.py --ids results/roles-holders-705.md --rounds 3` (the holders' size and memory as the laptop
  measures them), then loadtest.py --ids on the 944 - alone and loaded, both widths, 3 rounds - repeated while another
  session ends by the remote lines' deadline (repeat-fits.sh; at the final check's rate about 4 hours a session: 4-5).
- The Tegra: the 437 at 3 rounds, up to 3 sessions in 1,255 minutes (the final check's 438: 9.3 hours a session - one
  or two). The pre-flight: results/drafts/arm-preflight-705.md (clang's new-gene builds alive; GCC's tos=1 deaths a
  qemu artifact).
- dream: the 944 at both widths, 3 rounds, up to 8 sessions a width, 625 + 625 minutes.

## Its processing (the next chat)

1. `HANDOFF=results/handoff-relf-657.md sh lab/evolve/process-followup.sh 96-roles ITERATION ROLES` (ROLES the portable
   holders, role=id: fastest=782f3ad7ff,arm=3eb59b271d,knee=11a56ff9e4,smallarm=ae99617f06,memory=fb0d57c8a2,
   smallest=d180351903; and the x86 ones, fast64=c7c35f9c97,fast32=ee34931cd7,allround=06b188f45b,smalljit=c6f1c1331b)
   - before it, the holders' records in results/followup-seed96-roles.md replaced by the measure-ids pack's (the laptop's
   memory; final-pick.py keeps the candidates' size and memory). The readings by session, final-pick.py over them, each
   role against its holder (followup-roles.py's rule: speed 2 % at 2 SE, binary + image 1 %, memory 4 KB - the 8 KB of
   702 for the stopping rule is the owner's to extend here).
2. The shortlist: final-pick.py's shortlist() (580) per role - the set alone and loaded, the additions across machines,
   each width's fastest, each role's leaders on its own lines (the Tegra's for the ARM roles) - about 60 designs.
3. **Chain B**: the shortlist at 10 rounds on the three machines, several sessions each (the owner's hours); its
   processing picks the roles - the owner's trades, as at 611 and 649.

## After the roles

designs/ and the package made again for every role that changed (results/drafts/freeze-build-645.sh); self-hosting
phase 6 on the new roles (results/drafts/selfhost-plan-666.md: the cross compiler learns any new way of laying the
kernel - VAR-OPS and INL-OPS are zeros in self-built images today, 697); relf told how to fetch them; the article.
