# The prompts for switching chats (Iteration 214; HANDOFF.md since Iteration 272)

Two messages: one to close the old chat, one to start the new chat. A chat's
work survives only in the bundles it presents; its machine and transcript do
not carry over. So close the old chat first, and start the new one only with
the bundle the old one presents last - never one whose name ends in
-checkpoint.

## 1. To the old chat, before switching

---

We are switching to a new chat. Before it starts: commit everything that
should survive - a script that produced a figure recorded in PROGRESS.md goes
into the repository; every other file you wrote in /tmp is deleted or listed
in /tmp/handoff-disposable.txt with a reason - bring HANDOFF.md up to date,
write the PROGRESS entry, then run `runuser -u claude -- sh
tools/make-bundle.sh /mnt/user-data/outputs` (it runs tools/handoff-check.py
and refuses a bundle a new chat could not start from) and present the bundle.
Tell me what the check made you track or throw away.

---

## 2. To the new chat

Attach the bundle the old chat presented last, and the packs of any laptop run
not yet processed (forth-vm-evolution-*_tar.gz).

---

We are continuing my project forth-vm-evolution. Attached: the newest git
bundle of the repository, and the packs of any laptop runs not yet processed.

Set up first:

0. As root: `apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get
   install -y -qq gcc-multilib clang clang-19` - gcc-multilib because the build
   makes 4-byte cells too, as the laptop's does; clang because the gene
   compiler is offered only where clang is installed; clang-19 for
   preserve_none.
   Then `[ -e /usr/include/asm ] || ln -s x86_64-linux-gnu/asm /usr/include/asm`
   - the 32-bit builds' asm/ headers, where only gcc-13-multilib came in (Iteration 382).
   Optional, for tools/arm-qemu-check.sh only: `gcc-arm-linux-gnueabihf qemu-user`.
1. Clone as the user claude, into a directory it owns: `cd /home/claude &&
   mkdir -p forth-vm-evolution && chown claude:claude forth-vm-evolution &&
   runuser -u claude -- git clone /mnt/user-data/uploads/<bundle>
   forth-vm-evolution`, and give the clone the owner's identity, which every
   commit carries: `runuser -u claude -- git -C forth-vm-evolution config
   user.name "Kirill Timofeev" && runuser -u claude -- git -C
   forth-vm-evolution config user.email kt97679@gmail.com`. Every git, build
   and tool command runs as `runuser -u claude -- ...` (git refuses root on
   this tree).
2. Build and check, in /home/claude/forth-vm-evolution: `runuser -u claude --
   env LAYOUTS=1 bash tools/build-stages.sh`; `runuser -u claude -- bash
   tools/run-tests.sh` (PASS - no regressions); `runuser -u claude -- python3
   lab/evolve/evolve.py --validate` (7 of 7 IDENTICAL). A tool call ends the
   jobs it started in the background, and about 300 s is a call's limit:
   start anything long with `setsid nohup ... &` and poll it (run-tests takes
   about six minutes). A turn also has a budget of tool calls (about fifty).
3. Read HANDOFF.md whole - the state, the routine for a returned seed, the
   owner's decisions, the open items, the lessons, and what every turn does
   before it ends - then GOALS.md (the aim, how success is measured, the
   register of rejected ideas: look there before trying one), then
   PROGRESS.md's entries after the iteration HANDOFF.md names, then
   prompts/INDEX.md. README.md's "Documents" section indexes everything else.

Please set up, confirm the checks pass, and tell me what you will do next.

---
