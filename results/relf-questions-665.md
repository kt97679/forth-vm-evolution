# What relf asked this lab, answered as far as the search can (Iteration 665)

relf asked (its Iteration 716; vendor/relf/tree/docs/CV8-LEDGER.md, "Applicable, not done"; RELF.md, "What relf asks
of this lab") about what its realistic shell script spends dispatches on that CV8 does not do natively - "all of them
new instructions, so forth-vm-evolution's to inform". This lab's search was generic by the owner's order (RELF.md, the
order of the work, Iteration 365): it answers where its gene pool held the question, on its own workloads, never on
relf's shell. The winners are the ten designs of results/handoff-relf-657.md, their genes as lab/evolve/evolve.py
expresses them (`express(canon(genome))`, the code frozen at 656; designs/NAME/record.json).

| relf's question (its share of the realistic script's dispatches) | in the search | what the ten winners show | answer |
|---|---|---|---|
| XF@ and XV@, a tree's fields read directly (4.9 %) | no - relf's own words (`1+ CELLS + X@`, `2 + CELLS + X@`), not in the lab's workloads | the nearest generic form, the pair `+ @` (a fetch at an offset), in three: portable-arm, portable-knee, portable-small | none |
| DEFER's call inline (2.5 %) | no gene - DEFER is a colon word here too (forth/coreext.4: `CREATE ... DOES> @ EXECUTE`) | - | none |
| (+LOOP) inline (1.7 %) | yes - (+LOOP) as an opcode with an operand (ops10), the image's compiler emitting the loop opcodes (rtloop), native on the JIT (jitloop) | an opcode in nine of the ten (all but smallest), rtloop in the same nine, native in the four JIT designs | keep (+LOOP) an instruction |
| PICK inline (1.5 %) | no - a colon word here too (forth/kernel.4); a JIT stencil for it ranked in lab/evolve/GENES.md, never built | - | none |
| fused instructions (about 8 %): compares with IF/WHILE/UNTIL, OVER with an op, DUP 0= IF, more ops taking a literal | yes - a test fused with its branch by the image's compiler (rtfuse), ops with their literal operand (spec imm; rtimm at run time), pairs from each design's own hottest (supers) | ops with an operand in seven (all but the three smallest), rtimm in three; a test fused with its branch in two (portable-knee, portable-small); one pair or none in seven, two, three and six in portable-small, portable-knee and portable-arm; OVER C@ in two | operand forms: yes; a test fused with its branch, and pairs: rarely chosen |
| the kernel's own code folded and inlined by the cross compiler (not priced) | inlining at the hottest call sites (hotinl), by the lab's converter, not relf's cross.4 | in the four JIT designs, 10-40 sites | not for relf's cross compiler |

What the lab cannot say: anything on relf's workloads (its shell scripts, its bench-vm.py), on AArch64 or RISC-V, or
inside relf's 64 one-byte opcodes (QUESTIONS.md A15), where every new instruction displaces one to the escape band - the
lab's designs have their own opcode maps. Those are phase 2's, in relf (RELF.md, the order of the work).

Also for relf: results/relf-patches/tests-tmp-cleanup.patch. relf's tests/shell/run-case and run-return leave their
temporary scripts in /tmp, one each per shell tested: the cleanup comes before later cases that write the script again.
The lab's copies of both files were the same until Iteration 658 fixed and tested them here (run-tests, no file left);
the patch applies to relf's tree as vendored (vendor/relf/UPSTREAM, 2026-10-17) - relf master may have moved.
