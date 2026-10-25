# An audit: where other models could help now (Iteration 524, prompt 20)

The owner asked, while seed 73 runs: audit the project, and ask other models wherever they can help. Each open
challenge weighed as prompts/20-ask-other-models.md asks - its kind, and whether a measurement here answers it faster.

| challenge | kind | other models? | why |
|---|---|---|---|
| More from the run's budget - the surrogate, cheaper first looks, operators, stagnation (the best speed's last 2% gain at generation 66 of 102) | a field's methods | **yes** - ask-search-524.md | surrogate-assisted and multi-fidelity evolution, adaptive operators are settled fields we would otherwise reinvent |
| The fast end's ~7% offset between the run and after it (noise, contention, a rebuild ruled out) | knowledge outside the repository | **yes** - ask-cpu-state-524.md | Zen 4 boost, amd_pstate, getrusage against cycles under load - and a diagnostic plan; the decisive test stays on the laptop |
| The evolver's evaluation and selection, after the loophole of 516 | a fresh reading of code | **yes** - ask-evolver-review-524.md (code embedded) | the loophole lived in plain sight for a run; the JIT's bug hunt (515) found a real bug among wrong claims |
| The JIT on 32-bit ARM | knowledge outside | no - asked (511), checked (512) | a tested recipe exists |
| jitfuse, jitdoes, jitexec taken up or not | measurement | no | genecost.py and instruction counts answer it (517, 519) |
| Throughput - the compile is half a fast design's time | measurement first | no | an engine cache measured at 1% (522); flags that speed compiles change the code - the product |
| The converter's and the JIT's correctness | tests | no | jit-diff, jit-ops, jit-marker at both widths, validate, ans-check |
| cpt16 designs and larger programs | measurement | no | settled (517): refused out loud, the output check holds them |
| Freezes, rules, run lengths | the owner's decisions | no | - |
| Documentation for a new reader | a reader | no | prompt 05: a real reader is worth more than a simulated one |

Three prompts, each self-contained, its premises taken from the code and the last runs (each named in it): the search
question and the CPU question suit a model with research and citations; the code review one with a long context and
strong code reading (26 KB, the code embedded). When the answers return: every claim checked before anything is used
(ask-*-answers-*.md).
