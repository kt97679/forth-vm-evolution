# shellmix the fifth selection program; mechanism 8 deferred (Iteration 686; the owner, after results/relf-reply-685.md)

## shellmix.fth in the selection

The owner: relf's shellmix.fth (relfsh's mix - variables, DEFER-style hooks, `DOES> @` buffers) joins sim16, gc16,
scan and evo. Since 686:

- **The apps workload** (evolve.py's APPS_IN) runs `150 SHELLMIX` after the four - 150 of its turns, to take about a
  fifth of the workload (at 250 turns: 19-39 % of it on s6, smallest, portable-fastest and fastest-x86-64). Loaded
  after the four, it prints the same line as alone (checked at 250 on those four systems: `250 31375 5111 2000`): the
  four redefine no word shellmix uses (its redefinitions are names of its own - RUN, >NUM, NUM>, CHECKSUM).
- **The size score** counts its code too (appsize.py's SELECTION: five programs; about 1.6-1.8 KB a design).
- **The measures never pool**: appsize.size_key() is how many applications a record's size counts - 0 before 678, 4
  from 678, 5 from 686; one_size() refuses to pool two keys (compare-fronts, final-pick, stopping.py, whose ledger
  line now carries the count), and evolve.py resumes only a database of five. No run was measured with 678's four
  (the new series had not started), so nothing is lost.
- What it brings into the selection (results/relf-reply-685.md): DOES> words (seven uses of BUFFER: children, two
  hooks), DODOES 1.68 % of its dispatches on the knee, and the JIT designs at 1.11-1.49 of relf64's time on it -
  mechanism 3 (DOES> @ as VAR@) and the JIT's DODOES stencil are step-3 candidates again.

## Mechanism 8 deferred, and no limitation imposed

The owner asked that nothing be dropped that limits a general-purpose Forth. Checked:

- **No word is dropped.** Mechanism 8 is an encoding, not a word: an address literal (`[']`, `TO`'s address, a
  LITERAL of an address) laid in 5 bytes instead of 9 at 8-byte cells. TO, VALUE, 2VALUE, `[']` and LITERAL stay with
  their full meaning; run-tests' ANS suite (tests/ans: VALUE, 2VALUE, TO) checks them, passing at 680 and since.
- **The lab's form is the general one.** A 9-byte literal (opcode and a full cell) reaches any address; relf's 5-byte
  form relies on relf's dictionary lying below 4 GB. At 4-byte cells both are 5 bytes already. Not building it limits
  nothing - such code is 4 bytes a literal longer (674's construct table: `[']` 9 bytes on every lab design at 8-byte
  cells, 5 on relfasm64).
- **Its price**: 4 B on the selection (one `[']`), 1,220-1,245 B on brainless (its 250 TO), 0 on shellmix and in
  relf's code. GOALS.md's register holds it as deferred: built when a selection program leans on TO or `[']`.
