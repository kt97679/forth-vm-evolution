# Every word, audited against other Forths - the plan, and what is still to build (Iteration 127)

The owner: other genes on the todo list - can we add them? Have we switched to
the single SYSCALL? Grab the sources of other Forths and look for better
implementations; ideally audit every word in our sources.

## The todo list (GENES.md, ranked in Iteration 115) - where it stands

| item | status | worth now, under Iteration 127's selection |
|---|---|---|
| kstack | built (116) | - |
| a guarded ABORT" | built as abortif (117) | - |
| fbuf, fromzero | built (115) | fbuf took memory 184 -> 156 KB (seed 37) |
| opcall (Koopman) | built (121) | on 13 of seed 37's front |
| **knum** - NUMBER?'s plain cases in C | not built | was 19.1% of parse (now held out); 7.8% of the corpus |
| **more JIT stencils** - (+LOOP), (?DO), COUNT, DODOES, PICK; hotinl's list renewed | not built | **the most**: the fastest design runs bubble at 0.44 of s6 and ackermann at 0.57, against 0.06 on loop - what it cannot translate |
| **one SYSCALL primitive** | **not built** - agreed in principle (Iterations 100-103) | ~1.3 KB of engine, its handlers too; the OS words become Forth on it |
| 16-bit dispatch tables | not built | ~768 bytes |
| packed names | not built | ~500 bytes |
| promotion by synthesis, the primitive-set floor | not built (priced: no single demotion pays) | the large one - an instruction set evolution builds |
| INTERPRET's loop in C | not built | parse is held out now - little |
| immigrants, islands, against anchoring | not built | seed 36 answered the anchoring question no |

Each is priced before it is built and goes in behind a gene. The order I
propose: the JIT stencils first (bubble and ackermann are where the front is
weakest), then SYSCALL and the two byte trims (size, exact on the VM), then
knum; promotion by synthesis as its own project.

## The audit of every word

**What it covers**: forth/kernel.4 (165 colon words, 68 primitives), cross.4
(69), extend.4 (16), the compilers' copies (cv8.4, cv8t.4, sod16.4, cpt16.4)
and the k-gene overlays; the engines' handlers for the primitives.

**The method**:

1. *Weigh* every word by what it costs under the selection: its share of
   dispatches on each selected workload (profiling builds: exact on the VM),
   on s6 and on the front's fastest and smallest; its bytes in a CV8 image;
   its call sites. Most words are cold; the weights say which are worth time.
2. *Collect* other Forths' definitions of the same words. Code may come only
   from public-domain or permissive sources - pForth (public domain),
   jonesforth (public domain), zForth (MIT), sectorforth and milliForth (MIT),
   FICL (BSD-style), Retro (ISC) - each licence checked when fetched; and
   from the owner's own RelF. GPL ones - gforth, SP-Forth, bigFORTH, SOD32 -
   for ideas only (results/forth-collection-catalog.md has the rule).
3. *Compare in this VM's terms*: dispatches and bytes here, not elegance -
   another Forth's definition fits its own primitive set.
4. *Land* each batch of better definitions as an overlay gene, as kfast and
   kinput are: evolution weighs it, and with the gene off every recorded
   design stays identical. A correctness fault goes into the kernel itself,
   as in Iteration 125. Each batch: the gate, run-tests.sh, the Forth 2012
   suite, and the 98-design check before it lands.

## Premortem (prompts/16)

| reviewer | objection | verdict |
|---|---|---|
| a profiler | most words are cold: rewriting them buys nothing | accepted - the audit goes in weight order and stops (below) |
| a VM designer | other Forths' definitions fit other primitive sets and native code | accepted - compared in dispatches and bytes here (3) |
| the owner's rules | a kernel change alters every image and every recorded design | accepted - overlay genes (4) |
| the converter | words with opcodes are matched by their exact bodies | accepted - those keep their bodies, or their expected bodies move with them, as (+LOOP)'s did |
| a lawyer | code from GPL Forths cannot be copied | accepted - permissive sources only, licences recorded (2) |
| evolution | the k-genes already pick among variants - hand rewrites duplicate it | rejected - evolution picks among the variants it is given; it writes no Forth (that is genetic improvement, thread 5) |
| the measurer | the VM's timings are noise | accepted - dispatches and bytes here, time on the laptop |

**The ceilings.** *Speed*: kernel words carry most of the kernel and corpus
workloads (2 of the 6 selected) and almost none of fib, loop, bubble and
ackermann on the fast designs. If the audit makes those words 10% cheaper on
average - optimistic - the geometric mean moves by about (0.91 x 0.91 x
0.995^4)^(1/6), **3.4%**; at 5%, 1.7%. *Size*: the image is about 7.3 KB of
the smallest design's 20.4 KB; a kernel 5% shorter is ~350 bytes, **1.7%**.
*Memory*: nothing - pages touched are set by buffers and the dictionary, not
by how words are written.

**Stopping points**: after weighing (1), if the words worth a look - the
heaviest that together carry 90% of the kernel words' dispatches - are fewer
than 30, the speed audit is those 30; after the first batch, if it saves
under 1% of dispatches on the kernel and corpus workloads and under 100 bytes,
the audit stops there and the rest is recorded as looked at. **The boring
result**: a handful of shorter definitions, ~100-300 bytes and 1-3% of the
kernel and corpus workloads' dispatches - worth having, and less than the JIT
stencils above, which reach the workloads where the front is weakest.

**First step** (the next iteration): the sources fetched and their licences
recorded; the weights computed; the word table - every word, its weight, ours
and the others' - in results/word-audit.md.
