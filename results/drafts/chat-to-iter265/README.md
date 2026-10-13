# The leftovers of the chats of Iterations 213-265, as found

Two archives the owner asked that chat for after the switch at Iteration 265,
packed on its machine and filed here unchanged (Iterations 273 and 274):

- `MANIFEST.md` and `scripts/`, `jobs/`, `logs/`, `patches/`, `trees/` - the
  first archive: the scripts behind Iterations 241-264's figures, the check jobs
  and their logs, the /tmp patches (all also in the repository), the scratch
  trees as patches with their status.
- `trees/SORTED.md` - the scratch trees sorted (Iteration 276) and read (Iteration 277): every one's
  work reached master or a tracked draft - none is lost.
- `part2/` (its own `part2/MANIFEST.md`) - the second: every other script and source
  that chat's /tmp held, Iterations 213-243 (and elf.py, 250-251, missed by the
  first), the logs its job scripts wrote, source copies with other suffixes.

Each MANIFEST.md maps a file to its original path, the iteration and figure it
produced, and says "as found": nothing rewritten or reconstructed. The scripts
import the evolver from the paths of that machine (/home/claude/... or scratch
trees in /tmp) and read its build outputs; they are records, not tools - the
tracked tools are in lab/evolve/ and tools/.
