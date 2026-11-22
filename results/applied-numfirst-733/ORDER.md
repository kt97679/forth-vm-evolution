# The gene numfirst - applied at Iteration 733 (batch-check PASS on 542372f4)

One patch, `numfirst.patch`: the gene numfirst (results/drafts/esolangs-717.md, numfirst-722.md) - while no name of
the form -?[0-9]+ is defined, a token of that form goes to NUMBER? without FIND's walk. The flag NF-FLAG is the
prologue's last padding byte (START + 2 cells - 1, never run), so SAVE-SYSTEM keeps it; HEADER8 sets it when it lays
such a name. Two forms: with klookup the engine's (FIND) answers c-addr 0 at once (-DNUMFIRST: NF_SKIP in vm-lab.c and
in tools/gen-msc.py's and gen-tos.py's copies of the op); without klookup, forth/cv8-numfirst.4's INTERPRET8 skips FIND
for [0-9]+. forth/cv8-numfirst.4 and cv8t-numfirst.4 in every dump with cv8b.4 or cv8bt.4: tools/layout.py --numfirst
c|forth keeps HEADER8 (INTERPRET8 too in the Forth form; DIGITS? and NF-FLAG headerless) and drops the file's words
without the gene - before the hot-inline pass, which foresees the X8 swap. lab/evolve/evolve.py's gene (CV8 byte
headers), nf_file, the dump guard and setup's copies; export-genes.py lists --numfirst in G-NOT-YET; GENES.md's row.

Checked on a scratch clone (results/drafts/numfirst-733.txt; chainorder-gene-732.py with GENES=numfirst,
numfirst-probe-733.py): off - run-tests PASS, validate, the ten roles' 40 engines and images byte for byte 718's; on -
the ten roles' outputs the same at 8-byte cells, three at 4, with hashk on three; the probe's programs the same off and
on in both forms. Then batch-check (run-tests PASS, validate 7 of 7 IDENTICAL, the jail PASS), `git apply`, the stages
rebuilt.

Apply, from the top of the tree:

    git apply results/applied-numfirst-733/numfirst.patch
