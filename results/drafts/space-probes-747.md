# Space probes' flight software - against the register (Iteration 747)

The owner (747: "can you find information on space probes software? This also can help find some reusable ideas
probably?"), while seed 98 runs. The earlier surveys (other Forths 196, JITs and VMs 217, the early games and computers
713, esoteric languages 717, the demoscene and the IOCCC 727, small VMs 742) did not cover flight software: code that must
fit a few kilowords, run for decades and be changed from far away. Each technique against what the lab has; the measure
is dispatches, bytes and pages. Sources at the end (web, 2026-11-23).

## Forth and stack hardware in flight

| source | its technique | here |
|---|---|---|
| Harris RTX2010 (radiation-hardened; Philae's command and data management, ACE's C&DH and instruments, NEAR, TIMED) | a call is the address itself: the top bit 0, 15 bits of address | ours: tag2's tagged tokens, cv8's one-byte call forms; one-byte calls in the pairs' slots priced at 13 |
| the same (and the Novix NC4016 before it) | the subroutine return as a bit (bit 5) of an ALU instruction - EXIT costs nothing after an operation | ours: `folds` (23 primitives' prim;EXIT opcodes), a call then EXIT as BRANCH (tail calls), `jittail`, `opinline` |
| the same | a 5-bit literal in one instruction; two 256-cell stacks on the chip | ours: lit0, lit1, litm1, lit8 ...; the top of stack in a register (tos), the stacks in .bss (bss) |

## Interpreters and virtual machines on board

| source | its technique | here |
|---|---|---|
| The Apollo Guidance Computer's interpreter (Laning, Muntz; MIT IL) | interpretive code follows the native call that enters it and ends with an instruction to stop interpreting; 7-bit opcodes packed two to a word, a memory location that shifts right seven bits to get the second; vector and matrix operations one instruction each - more function per word of core, far more time | ours: the byte code itself (one byte an operation); whole words as one opcode (opbody, ops10: FILL, CMOVE, (FIND)); the JIT's split (the hot words native, the rest interpreted); native code calling byte code priced again at 220 |
| JPL's Virtual Machine Language (VML; 15 deep-space missions, MAVEN the latest named) | an onboard VM runs uploaded named blocks; a new mission adapts it by data-driven configuration, without changes to the flight code | ours: the engine and the image - the image changes, the engine stays. 746 measured the reason it matters here: a change to the engine's code moves every interpreted design's hot code in its cache line and re-rolls its time; an image does not |
| JWST's onboard scripts (a COTS JavaScript engine, Nombas ScriptEase 5.00e, running the uploaded operations scripts) | the same split: a fixed, qualified engine, behaviour as uploaded code | the same as VML's row |
| ESA's MicroPython for LEON (Euclid's onboard control procedures engine) | bytecodes combined for speed; heap use taken out of the VM's paths; the heap a dedicated buffer that can be locked | ours: supers and folds; the engines' buffers static (bss, the fixed layout of 734), the memory criterion counting the pages a run touches |
| Deep Space 1's Remote Agent (Lisp under VxWorks) | a read-eval-print loop on board - a race condition found and fixed in flight | ours: every image carries the text interpreter (the corpus and apps workloads compile source) - Forth's REPL is the default here |

## Living with little memory and far away

| source | its technique | here |
|---|---|---|
| Voyager's computers (CCS and AACS 4,096 18-bit words each - 6-bit opcode, 12-bit address; the FDS about 8,200 16-bit words; about 68 KB in all six) | in 2024 the code on a failed FDS chip was cut into pieces, placed in free memory across the FDS, every reference to it updated, and uplinked | ours: the converter lays out the image and resolves every reference (tools/layout.py); for scale: the smallest design here is 21,636 B, engine, image and the five programs' code |
| JPL's Power of Ten, rule 3 (Holzmann 2006), and JPL's C standard | no dynamic memory after initialization - memory bounded and known | ours: static buffers the norm; the memory measure is pages touched, however allocated |
| Galileo after its high-gain antenna failed | the onboard computers reprogrammed to edit and compress the data - about ten times the information on the low-gain antenna | ours: the compressed image and engine priced at 236 (on disk only: memory does not shrink) |

## What it comes to

Nothing for the series or the roles: every technique is here already or was priced - the RTX2010's free EXIT is `folds`,
its address-as-call is the tag, the AGC's interpreter is the byte code's own trade. Two things worth keeping:

- **For relf's handoff - freeze the engines, change the images.** Flight software's practice (VML, JWST's scripts,
  ESA's OBCPs) is a fixed, qualified engine with behaviour uploaded as data. 746 gives it a measured reason here: an
  engine change re-rolls the interpreted designs' placement (clang -Os' loop median 1.256 across the batch, the
  instructions the same), an image change does not. After the roles are named, a change to an engine's code means the
  roles measured again; a change to an image does not move the engine's code.
- **For the article, if the owner wants it** - Forth's flight record as context: the RTX2010 in Philae's computer and
  in ACE's command and data handling (listed by APL as RTX2010, Forth/13500).

## Sources

- [Forth in space](https://www.ratfactor.com/forth/forth-in-space) (after James Rash's NASA GSFC list; APL's flight
  software table); [Forth in Space Applications](https://www.forth.com/resources/space-applications/);
  [Here comes Philae! Powered by an RTX2010](https://www.cpushack.com/tag/rtx2010/)
- [Koopman, Stack Computers, 4.5: the RTX 2000](https://users.ece.cmu.edu/~koopman/stack_computers/sec4_5.html);
  [4.4: the NC4016](https://users.ece.cmu.edu/%7Ekoopman/stack_computers/sec4_4.html)
- [The AGC assembly-language manual (yaYUL), on the interpreter](https://www.ibiblio.org/apollo/assembly_language_manual.html);
  [E-2052, AGC4 Basic Training Manual](https://ibiblio.org/apollo/NARA-SW/E-2052.pdf)
- [Virtual Machine Language (NTRS)](https://ntrs.nasa.gov/citations/20110016376);
  [Flight-Ground Integration - VML on 15 missions](https://katalog.lib.cas.cz/KNAV/EdsRecord/edsair,edsair.doi...........2e3d58a215c0b742a47ae8985b301e8e)
- [Event-driven JWST operations using on-board JavaScripts (SPIE 2006)](https://ui.adsabs.harvard.edu/abs/2006SPIE.6274E..0AB/abstract);
  [JWST runs ScriptEase 5.00e](https://mybroadband.co.za/news/science/457177-james-webb-space-telescope-runs-20-year-old-javascript-engine-report.html)
- [MicroPython for LEON (ESA)](https://essr.esa.int/project/micropython-for-leon-pre-qualified-version);
  [MicroPython on LEON (George)](https://indico.esa.int/event/145/contributions/820/attachments/873/1052/06a_-_Micropython.pdf)
- [Lisping at JPL / Remote Agent](https://retrocomputingforum.com/t/lisping-at-jpl-story-of-the-rise-and-fall-of-lisp-at-jpl/964)
- [Voyager's FDS memory and the 2024 fix (EE Journal)](https://eejournal.com/article/jpl-software-update-rescues-failing-voyager-1-spacecraft);
  [Voyager's six computers, 68 KB](https://spacedaily.com/t-voyager-1-six-computers-68-kilobytes-memory/);
  [the Voyager computers](https://www.allaboutcircuits.com/news/voyager-mission-anniversary-computers-command-data-attitude-control/)
- [Holzmann, The Power of 10](https://www.cs.otago.ac.nz/cosc345/resources/nasa-10-rules.pdf)
- [Galileo's rescue by compression](https://maketecheasier.com/?p=863155);
  [Galileo's low-gain antenna link (NTRS)](https://ntrs.nasa.gov/api/citations/19940025160/downloads/19940025160.pdf)
