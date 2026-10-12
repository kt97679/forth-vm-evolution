# Names in the image, priced (Iteration 222)

The dictionary's names are a fifth of every image: on seed 43's front, 326
named words and 1,732 name bytes on the smallest design (add5ec8937, 20.0% of
its 8,680-byte image), 308 and 1,632 on a middle one (55229a92a3, 22.6%), 385
and 2,123 on seed 43's fastest (cc6d168e0a, 19.8%); 5.3-5.5 characters a
name. Two ways to spend fewer bytes on them.

## Packed names (the handoff's open item 4): ~300-380 bytes before the code

Every character in the front's names is one of 58: A-Z, 0-9 and 22 others
(`!"#'()*+,-./:;<=>?@[\]`) - a 64-character alphabet needs no escape. Six bits
a character instead of eight: -311 bytes on the smallest, -292 on the middle
design, -384 on the fastest - before the code that packs a name as a header is
made (at run time too), the key packed for every lookup or the stored name
unpacked as it is compared, and WORDS and the error messages unpacked; and
cross.4, the converter and the dump tools all read names. A kernel change, a
reseed, every image changed. Not built: under 2% of binary + image at the
small end, less after its code, for the largest change of the three here.

## Names nobody uses: -448 to -936 bytes, nothing else changed

results/drafts/hidden-names.py: the names that no program here writes - the
standard suite and the core tests, the benchmarks, the corpus, the shell
tests, and the sources compiled at run time (extend.4, cross.4, kernel.4) -
made headerless with the converter's existing switch (`--headerless`,
Iteration 190: the code stays, reached by what was compiled to it; the header
goes and the word is on no chain):

| design | names hidden | image | binary + image | the gate |
|---|---|---|---|---|
| add5ec8937, the smallest of all runs | 65 of 326 (some already hidden by fsys) | 8,680 -> 8,232 (-448) | 16,136 -> 15,688 (-2.8%) | alive |
| cc6d168e0a, seed 43's fastest | 103 of 385 | 10,710 -> 9,774 (-936) | 34,382 -> 33,446 (-2.7%) | alive |

What they are, on the smallest: the CV8 overlays' compiler helpers and
constants (`!CALL !W #FOLD-OPS 0BRANCH-OP <BRANCH, <RESOLVE >MARK >OP >RESOLVE
?BRANCH8-OP AGAIN8 BRANCH-OP BRANCH8-OP CV8-DOES-FAR? CV8-DOES-RESERVE
CV8-SHIFT CV8-SHIFT-DEFAULT CV8-SHIFT-V DODOES-OP DOVAR-OP ESC-OP EXIT-OP
FOLD-BASE FOLD-OP FOLD-OPS HDR-HEAD HDR-LEN LAST-OP LINK-LEN LIT, LIT16-OP
LIT32-OP LIT64-OP LIT8-OP LOOP-ALIGN OP, OPERAND-ALIGN W,`), the lookup's own
`NAME=?` and `NEXT-NFA8`, and fsys's FS- helpers (hidden already). No
standard word among them. Shorter chains too - fewer entries for every
lookup, and the misses walk whole chains (results/price-lookup-cache.md).

## Correction (Iteration 223): it does hurt - the standard suite says so

The owner asked whether hiding these names could hurt anything. The gate had
run on two designs; the standard suite had not. Run on three designs with
their lists hidden (ans-check.py, through E.build): seed 43's smallest 13 of 14
files as s6, its fastest 13 of 14, and a JIT design of the middle
(5f4a21fbdb) 0 of 14 - every file a segmentation fault right after the banner.
Two causes, found:

- **A library loaded at run time uses an internal name.** The suite's harness
  INCLUDEs forth/coreext.4, which builds TRAVERSE-WORDLIST from NEXT-NFA8;
  hidden, `Undefined word TRAVERSE-WORDLIST` in toolstest.fth. The scan had
  read extend.4, cross.4 and kernel.4 but not coreext.4, locals.4,
  save-system.4 or the shell's sources; read too, NEXT-NFA8 stays and the tools
  test matches.
- **A name reached in a way no source shows.** Bisected over 5f4a21fbdb's 67
  names: LEAVE8 alone crashes it at the first INCLUDED. LEAVE8 is defined in
  four overlays (cv8.4, cv8t.4, cv8-fuse-loop.4, cv8-fuse-loopall.4) and
  POSTPONEd by one; with its header gone the design dies - most likely a table
  the converter fills by name (rtloop=2's), or the newer of two definitions
  handing its place to the older. Not yet understood exactly.

So a list derived from what programs here happen to write is not safe, and
"it costs nothing" was wrong. The bytes are real (-2.7 to -2.8% on the two
designs that ran), but the only safe form is lists kept by hand per overlay,
each name's uses understood (by name, by table, by POSTPONE, by redefinition),
and checked on every gene combination with the gate and the standard suite.

## Inlining them instead (the owner's question)

Priced from the converter's call map (CALLMAP) on the smallest and seed 43's
fastest design, beyond what hiding the names saves:

- **The 14 opcode constants** (EXIT-OP, BRANCH-OP, ...) are 2-byte bodies; their
  uses turned into literals and the bodies dropped: ~28 bytes.
- **Words called from one place** (12 on the smallest, 5 on the fastest),
  inlined: the call and the EXIT, ~3 bytes each - 36 and 15 bytes.
- **Words with no call site at all** (5 on the smallest, 54 on the fastest -
  the CV8 versions of `:`, `IF`, `DO` and the like) are NOT dead: they are
  reached through another word's header, a table of execution tokens, or
  POSTPONE - the same ways LEAVE8 is. Nothing to drop without the same proof.

The bytes are in the headers - the name, its length and its link - not in the
bodies; inlining adds tens of bytes to hiding's hundreds.

**A candidate for the next batch, not built yet - in the hand-kept form only.** As a gene, the list must be
kept by hand per overlay - as FSYS_INTERNAL and RTLOOP_INTERNAL are - not
derived from what the tests happen to use: a user program may write any
standard word. The owner's call whether it is a gene or every design's: it
costs nothing but the internal words' names, which no standard program can
rely on.
