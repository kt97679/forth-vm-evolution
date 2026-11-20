# What early games lend the search (Iteration 713)

The owner: "performance and size were critical in the early computer days especially for the games ... a lot of older
games were reverse engineered, there are blog posts on that". Read here: the reverse-engineering write-ups of Starflight
(1986, written in Forth), Another World (a bytecode VM), Elite (Mark Moxon's annotated source), Pitfall!, Wolfenstein 3D,
Infocom's Z-machine, Wozniak's SWEET16 and UCSD p-code (Wizardry's VM). Each technique is set against the genes and
GOALS.md's register first. Most are here already. One is not, and it is about memory: **where the engine's data lies
decides how many pages a run touches, and the linker places it by luck - 1 to 4 pages, the 8 KB rule's size.**

## The one that pays: memory placed by luck - place it on purpose

The 8-bit games placed every byte of RAM by hand. The Atari 2600 has 128 bytes of RAM, and Pitfall! keeps only the
current room in memory (Evoniuk). Elite's memory maps account for every block: 21,906 bytes of game code and data, and
the screen at &6000 (Moxon). Revs' binary unpacks itself as a 13-piece jigsaw. The habit carries over because the
search's memory is counted in pages.

**What the memory reading is**: tools/cputime.c counts the child's page faults, 4 KB each. ru_maxrss reads 0 for a run
this short, and a page read before it is written counts twice (its comment, Iteration 75). fb0d57c8a2, the least-memory
holder, measured here (results/drafts/env-pages-713.py, resident-peak-713.py; an empty environment, medians of 15):

| run | faults | the peak resident (VmHWM) |
|---|---:|---:|
| start-up only (`BYE`) | 15 pages (60 KB) | 11 pages (44 KB) |
| the kernel workload (the memory objective's - rss is the largest but apps) | 27 pages (108 KB; the record's 108) | 23 pages (92 KB) |

**The pages a start-up touches** (results/drafts/bss-pages-713.py: /proc/PID/pagemap against engine.full's symbols):
the file's 2 pages, the dictionary's 3 (the image, 9,566 B), the process stack, and **4 BSS pages**:

- **2 for the stacks**: stackmem (320 KB, page-aligned) holds the data stack (256 KB) and then the return stack
  (64 KB). Both grow down, so their tops are 64 KB apart: pages 0x441 and 0x451.
- **2 for a few hundred bytes of small variables**: t_obuf (4 KB) falls between them. Page 0x452 holds dispatch.1 (the
  DISPOFF copy, 1 KB), g_argv, environ, the g_ VM registers and t_obuf's head. Page 0x453 holds t_obuf's tail, t_olen,
  t_fb, rt_errno, base, hot_tab, throw_off and heads' used start.

**The experiment** (results/drafts/layout-faults-713.py): the same designs built once more with the data sections
sorted by alignment (`-Wl,--sort-section=alignment`, through EVOLVE_CFLAGS). The code is unchanged and the files are
the same size (fb0d57c8a2 +32 B of .data padding). Medians of 15 runs, [the range]:

| design | start-up, as built | sorted | the kernel workload, as built | sorted |
|---|---:|---:|---:|---:|
| c7c35f9c97 (the x86-64 holder, JIT) | 32 [32-34] | **28** [28-29] | 58 [56-60] | **56** [54-58] |
| 21768033b7 (one of the six at 21,679 B) | 16 [15-17] | **14** [14-15] | 28 [27-29] | **27** [26-28] |
| fb0d57c8a2 (least memory) | 15 [14-16] | **17** [16-18] | 27 [26-28] | **29** [28-29] |

So the layout alone moves a design's memory by 1 to 4 pages either way, as much as the 8 KB rule. The least-memory
role's close calls (chain B's five reads) can be decided by where the linker happened to put t_obuf. This is the memory
analogue of 712's layout luck for speed (layout-noise.sh: 5-10 % on the stages).

**Proposed - a fixed layout of the engine's writable data** (an engine change, not a gene - a pure saving under the
standing rule once measured to cost no speed; for the reopened search, before its first seed; a prototype first):

1. Every small variable a run touches (the g_ registers, dispatch.1, t_olen, t_fb, rt_errno, base, hot_tab, throw_off,
   and the JIT's in its designs) in one block, and the big buffers (t_obuf, heads, the file system's buf[65536])
   after it. That gives 1 page where there are 2 today, deterministically on every design.
2. The two stack tops on one page: the return stack growing **up** from where the data stack's top is - the layout of
   the 6502 Forths, which kept the data stack in zero page and the return stack in the hardware stack. That saves
   1 page more, but it changes every return-stack handler, the JIT's stencils, and any Forth that does RP@ arithmetic
   (CATCH/THROW's frames). Price it apart; step 1 alone is the safe half.

The expected gain is -1 to -2 pages a run on every design (4-8 KB of 60-108), and no more layout luck. The least-memory
role's 108 KB would become 100-104 KB, as would every role's figure. It changes no ranking by itself: every design
gains alike. It touches engine/vm-lab.c and engine/rt-linux-*.c (an attribute, an order), not the image. Not built
here: it needs the batch's checks (run-tests, validate, the jail) and a measurement of no speed lost.

**And the environment's pages**: the same run with the sandbox's environment (17 KB) faults 3 pages more (19 at
start-up, 32 on the kernel workload), and 20 KB more of it adds 5 more. The memory reading carries the measuring
process's environment, about a page per 4 KB. That is a likely reason the sandbox read chain A's holders 4-16 KB above the laptop
(their records at 705). Running every workload with a fixed small environment (`env -i PATH=...`) would make memory
comparable across machines. That is the owner's call: it shifts every reading by the laptop's own environment, about
a page, and the series' records would then differ from the new ones by that page.

## Already here - each game's trick and where the project has it

| technique | where it was used | here |
|---|---|---|
| A bytecode VM under a thin host, the logic in its code | Another World: a 29-opcode VM in a 20 KB executable (Sanglard); the Z-machine; p-code | the design itself |
| Threaded code of 16-bit pointers | Starflight: indirect threading; more than 90 % of the executable 16-bit pointers, under 5 % x86 | the threading genes; indirect threading priced, not built (29) |
| Names removed from the image | Starflight kept 2,000 of about 6,000 names, encrypted | headerless internal words: priced, deferred by the owner (222-223) |
| A compact interpreter mixed with native code where speed does not matter | SWEET16: about 300 bytes, half the code size for 5-10x the time; Woz thought 1 KB of his 5 KB BASIC could go | the k genes (knumber, klookup, kinput, kfast) and fsys - a part in C or in Forth over the VM, evolution choosing; native code calling bytecode priced (220) |
| The constant in the opcode, short operands | p-code's SLDC 0-127; the Z-machine's 1-byte small constants | lit0, lit1, litm1, lit8, lit16, lit32, lit64, the fused lit8;exit; a literal 5 is 2 bytes (generic-apps-674.md) |
| Text as tokens and abbreviations | Elite's recursive and two-letter tokens; the Z-machine's 96 abbreviations and 5-bit text | packed names: priced, deferred by the owner (222, 231-233); the echo instruction (260); the refusals as one message (709) |
| Split or offset jump tables | the 6502's lo/hi tables | DISPOFF: the dispatch table as 4-byte offsets, about 500 B off every CV8 engine (237); 2 bytes refused - no limit a developer could hit |
| Code specialised in advance | Wolfenstein 3D's compiled scalers, about 83 KB of generated straight-line code | the JIT family; the run-time fusers (rtconst, rtvar, rtinline) |
| Generate, don't store | Pitfall!: 255 rooms from an 8-bit LFSR in 31 bytes of code | DISPOFF makes its table at start-up; the image is the kernel compiled once |
| Code overlays | Starflight: 105 overlay words | nothing to page out: the measure counts only pages touched, and the workloads touch what they use |
| Tail calls, shared exits, falling into the next routine | 6502 games | the tail and crossjumping genes; falling into the next word cannot happen in source order (a callee is defined before its caller) |
| Code rewritten as it runs | self-modifying 6502 code | the run-time fusers rewrite compiled code; rtfuse built and rejected by selection |
| Return-address dispatch (the RTS trick) | 6502 jump tables | real calls and returns for dispatch lost in the dispatch lab |
| Crunched binaries | Elite's crunchit; the demoscene's packers | a compressed image and engine: priced, not built (the owner, 236) |

## Priced here, not proposed

- **Short branches** (the Z-machine's 1-byte branch form, bit 6 set and a 6-bit offset; the 6502's rel8). IF THEN costs
  3 bytes here (0BRANCH and a 16-bit offset). kernel.4 has about 150 branch-compiling words and the five programs about
  106 (results/drafts/branch-census-713.py, a word count). The converter, which sees a whole word, could choose the short
  form exactly. The one-pass run-time compiler can do so only for backward branches (UNTIL, REPEAT: about 13 in the
  programs): a forward IF does not know its distance until THEN, and moving its body would break its relative calls.
  That is about 150 bytes (0.7 % of the smallest design) for two opcodes in the primary band, with the encoding taught
  again in the seven places 681 touched. Below the 1 % rule.
- **A CASE table** (Starflight's 127 switch-case words): CASE and OF hardly appear in kernel.4 or the five programs.
  Nothing to save.

## Sources

- Starflight: s-macke/starflight-reverse's README (via awesome.ecosyste.ms) - https://awesome.ecosyste.ms/projects/github.com%2Fs-macke%2Fstarflight-reverse
- Another World: Fabien Sanglard - https://fabiensanglard.net/anotherWorld_code_review and https://fabiensanglard.net/another_world_polygons
- SWEET16: https://en.wikipedia.org/wiki/SWEET16, https://kb.segger.com/Sweet_16
- Elite: Mark Moxon's deep dives - https://elite.bbcelite.com/deep_dives/printing_text_tokens.html, https://elite.bbcelite.com/deep_dives/the_elite_memory_map.html; Revs - https://revs.bbcelite.com/deep_dives/the_jigsaw_puzzle_binary.html
- Pitfall!: https://evoniuk.github.io/posts/pitfall.html, https://devnonsense.com/posts/pitfall-lfsr-math/
- Wolfenstein 3D: the Game Engine Black Book (excerpt) - https://wolfenstein3d.nl/?p=6913
- The Z-machine: https://www.inform-fiction.org/zmachine/standards/current/sect04.html, sect03.html; Labrande on Infocom's text compression - https://unbox.ifarchive.org/1ltwf62yp9/2/issue2.pdf
- UCSD p-code: https://archive.decromancer.ca/bitsavers.org/pdf/softech/Softech_Pascal/UCSD_p-System_II.0_-_Instructions-Opcodes.txt
