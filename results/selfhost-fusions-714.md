# Self-hosting phase 6, first part: the run-time fusions kept in self-built images (Iteration 714)

The pre-mortem's gate (results/drafts/premortem-roles-707.md): a role ships its self-built image only if that image's
speed is the translator-built one's. Until now forth/cross-cv8.4 left cv8-fuse-var.4's VAR-OPS and cv8-fuse-inline.4's
INL-OPS as zeros (697), so in a self-built image the genes rtvar and rtinline were off - and an rtinline design did not
self-host at all. Most of the new roles' candidates carry rtinline (48a012411a, 9b15ba26f7, df097ba2e2, ea782c6094,
11f956db93, d727605472, 5f7e66b12d), the last two rtvar as well.

## What changed in forth/cross-cv8.4

- **VAR-OPS! and INL-OPS!**, run after LOOPTAB!: the two tables byte for byte as tools/layout.py writes them. VAR-OPS: vf,
  vs, @ and ! (under the tag in one-byte codes, all four or none), VARSLOT, SCALE 0, the tag, and DOES> @'s tail (R>,
  @;EXIT, the pair R> @) with its mask. INL-OPS: the whitelist's lengths two bits a code, the fold bitmap, the JIT's code
  and header, the fold pairs sorted by name as Python sorts them. An operation's name follows sod16.py's t2_names - later
  kinds name over earlier ones (the primitives, the fixed operations, the specialisations - named whenever the design has
  any -, the folds, the pairs, the format-10 operations); INL-OPS's name-to-code takes the last code with a byte, VAR-OPS's
  tail the last code whatever its byte, as layout.py's _code and _inv do.
- **I-FILL**: cv8-fuse-inline.4 zeroes INL-OPS with FILL outside a definition - the cross compiler had no host action
  for it ("no host action for FILL").
- **?DO** in TRANSIENT, for cv8-fuse-inline.4's two loops: (?DO)'s format-10 opcode as a branch past the loop's end (the
  translator's QDO, sod16.py's LOOPKIND), its LOOP resolving it; refused, naming itself, in a design without (?DO)'s
  format-10 opcode. LOOP's old body is LOOP-OP. No shipped design's sources use ?DO in a definition.

## The check - results/drafts/selfhost-ids-714.sh, results/drafts/fusetab-714.py

selfhost-ids-714.sh is tools/selfhost-lab.sh for designs off designs/ (each record from a list: export-designs.py,
export-genes.py, selfhost-check.sh - A = B, the gate), then fusetab-714.py on the translator-built image and A, each on
its engine (a JIT design's A on the engine rebuilt with A's layout): both tables printed from inside each image, two
probes compiled (a call of a one-operation word; a variable's @ and !), and the five selection programs' code
(evolve.app_size) with the tables as they are and with each zeroed - the fusion off in the same image, the control.
The eight designs' records: results/drafts/vartest-714.py (its docstring has the command).

| design | A | VAR-OPS | INL-OPS | probes | the five programs' code: the translator's / A's |
|---|---|---|---|---|---|
| 48a012411a (the knee; byte header) | 8,857 B | - | the same (41 bytes nonzero) | the same | 8,428 / 8,428 - zeroed INL-OPS 8,404 in both |
| ea782c6094 (x86-32; tag 2, JIT) | 9,273 B | - | the same (41) | the same | 9,989 / 9,985 |
| 11f956db93 (x86-32; tag 2, JIT) | 9,241 B | - | the same (40) | the same | 9,985 / 9,969 |
| 48a012411a with rtvar, varslot | 9,489 B | the same (8 of 12) | the same (41) | the same | 8,416 / 8,406 - the same -10 B with either table zeroed |
| 11f956db93 with varslot (rtvar expressed) | 9,873 B | the same (8) | the same (40) | the same | 9,895 / 9,842 |
| a8d35bdccc (ARMv7), 219878ec89, 90273721a1 (the smallest's) | 9,775 / 8,717 / 8,755 B | - | - | the same | 8,429 / 8,398; 8,390 / 8,390 twice |

Every check PASS. The tables are the translator's to the byte in all five designs that have them, at both header
families and with the JIT; zeroed, each changes the programs' code (the control: the comparison sees the fusions). The
programs' code differs only by A's layout: A is smaller (248-320 bytes at the byte header), so code laid after it sits nearer the kernel - a
call near rather than far, a VARSLOT slot of 2 bytes rather than 3, under the tag a call's 2-4 bytes by distance. The
byte header shows it plainly: the rtvar variant's -10 B stays -10 B with either table zeroed, and a8d35bdccc, with no
table at all, differs by -31 B. VAR-OPS is checked on two variants made for it (rtvar=1, varslot=1 on 48a012411a and
11f956db93): no rtvar design in chains B and C self-hosts yet (below).

## What the new roles still need of the cross compiler (export-genes.py's G-NOT-YET)

- **--guard-abort**: 9b15ba26f7 (the fastest on x86-64), df097ba2e2 (best all-round).
- **--factor, and the fused =I?BRANCH / DUP?NBRANCH** (and =I?BRANCH8): d727605472 and 5f7e66b12d (the fastest
  portable's pair). Every JIT-free rtvar design in chains A and B's lists needs one of the three: 127 have the gene
  factor, 5 a fused =I?BRANCH among their format-10 operations, ca04ccb8ec the gene abortif (--guard-abort).
- Self-hosting now: a8d35bdccc, 219878ec89, 90273721a1 (no tables to fill), 48a012411a, ea782c6094, 11f956db93.

Until those are built the gate ships the translator-built images for the four roles that need them, named so. The
speed half of the gate - the self-built images timed against the translator's - is the laptop's (phase 6's
re-measure). The ten shipped designs rebuild their images byte for byte as before (run-tests' make selfhost).
