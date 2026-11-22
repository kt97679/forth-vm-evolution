# The gene jitdead in the cross compiler; the queued genes rebased (Iteration 724)

**The queue no longer applied.** results/applied-genes-727' three patches (jitdead, fixenv, jitfew; batch-checked at 713
on 6f91bb0) failed `git apply` on 723's master: export-genes.py had moved (714-722's G-NOT-YET edits). Made again on
master, one commit each (`git apply --3way`): one conflict - G-NOT-YET's line, master's kept and jitdead's
--jit-dead added to it - the rest context only. The rebased patches replace the old in results/applied-genes-727, and
ORDER.md says so; its check, `env PENDING=results/applied-genes-727 RECORD=1 sh tools/batch-check.sh`, run on them.

**jitdead in the cross compiler** (results/applied-genes-727/jitdead-cross-after-seed96.patch, the queue's last;
forth/cross-cv8.4 and lab/evolve/export-genes.py), as tools/layout.py does it at 710:
- the JIT header on the outer interpreter's words (--jitimg 1) the JIT's code alone, not [code][four bytes];
- the body made four bytes long - NOOPs after its EXIT, never run (layout.py's jh_pad) - room for the native offset
  engine/jit.c writes there; both the plain words (END-DEF) and the opcode-bodied ones (the OPB path);
- jit_wends: each headed body's end before its pad; without --jitx, the headed words' rows alone (layout.py's rows_);
- the image's table: the header's length 1 (IA+96); JITN's code (65532 in the tag-2 map) read and written to the
  JIT's layout file (#define JITN_CODE);
- the genes: G-JITDEAD and G-JITX, read by name (GENE?) so an older genes.4 without them builds as before - the
  ten shipped designs' genes need no export for it (`make selfhost`: 20 of 20 with the new compiler, their genes);
  --jit-dead out of G-NOT-YET.

**Tested** (results/drafts/jitdead-cross-723.sh, on the queue applied - a scratch branch): four JIT records from
designs/ with jitdead on, through results/drafts/selfhost-ids-714.sh at both widths - all PASS (A = B, the gate, the
run-time compiler's tables and the five programs' code the translator's; JIT designs on their engine rebuilt with A's
layout); JITN's code the translator's in every one.

| variant | what it exercises | 8-byte A | 4-byte A | jit_wends rows T / A |
|---|---|---|---|---|
| jd-small (small-jit 15eda54ebd) | jitimg, jitx | 8,041 | 7,537 | 280 / 280 |
| jd-bar (best-all-round df097ba2e2) | jitimg, jitx | 10,004 | 9,028 | 290 / 291 |
| jd-lm (least-memory fb0d57c8a2) | no jitimg, no jitx: no layout file | 9,278 | 8,710 | - |
| jd-small-nx (small-jit, jitx off) | the headed words' rows alone, the pads off their ends | 8,041 | 7,537 | 14 / 13 |

The rows differ where the layouts do: the cross compiler gives the JIT header to 13 words where the translator's
_jitimg_pick takes 14 (one of INTERPRET, REFILL, ?STACK, (PARSE), (NUMBER?) - not traced; as before jitdead), and
best-all-round's code words one more. Found on the way: a stack slip in the rows' filter (the jitx-off path only - a
segfault, fixed) and an X and its X8 sharing one body (the check counts bodies found, not rows).

**The =I?BRANCH gap (723) not traced.** Self-built images run =I?BRANCH 1.6-1.8 times the translator's. Ruled out:
`=` a tiny word (it is not - specialise's LIT n = would miss it), constants (the cross compiler folds BL into a
literal, the translator's dump calls it - but the `BL =` sites are SCAN's and SKIP's Forth bodies, C operations in
these designs, and -TRAILING). A per-address profile names A's words but not the translator's (110 of its ~2,950
dispatches land on the opcode's byte at the profiled offset), so a word-by-word comparison needs layout.py's
--symbols and a map from the cross compiler - left open; outputs the same, the gate passed, fewer dispatches in all.
