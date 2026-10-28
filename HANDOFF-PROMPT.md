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

Attach the bundle the old chat presented last, the packs of any laptop run
not yet processed (forth-vm-evolution-*_tar.gz), and any archive HANDOFF.md's
"Files a new chat needs" names (Iteration 415).

---

We are continuing my project forth-vm-evolution. Attached: the newest git
bundle of the repository, and the packs of any laptop runs not yet processed.

Set up first (Iteration 560 - tools/setup-sandbox.sh does steps 0-1 of the old list, HANDOFF-REFERENCE.md):

1. As root: `git clone -q /mnt/user-data/uploads/<bundle> /tmp/s && sh /tmp/s/tools/setup-sandbox.sh && rm -rf
   /tmp/s` - the compilers, the clone as claude in /home/claude/forth-vm-evolution, the owner's identity. Every git,
   build and tool command after it runs as `runuser -u claude -- ...` (git refuses root on this tree).
2. A returned seed: HANDOFF.md's "Processing a returned seed" - process-run.sh builds and checks everything. Any other
   chat: `CHECK=1` before the setup command starts the build, run-tests and validate (`sh tools/wait-for.sh
   /tmp/setup-check/status DONE`; run-tests PASS, validate 7 of 7 IDENTICAL). A tool call ends near 300 s and a turn
   has about fifty: anything long goes detached (setsid nohup ... &) and is polled.
3. Read HANDOFF.md whole - the state card, the routine, the owner's decisions, the open items, the conventions. The
   rest on demand: HANDOFF-REFERENCE.md (its lessons before changing the evolver or a measurement), GOALS.md (the aim,
   the stopping rule, the register of rejected ideas - before trying one), PROGRESS.md's newest entries, prompts/INDEX.md.

Please set up, confirm the checks pass, and tell me what you will do next.

---
