---
id: 22-setup-is-a-script
when: about to change a machine's environment by hand - install a package, make a link, a user, a directory or its owner, set an identity or a config, make a scratch copy of the tree - in work that later sessions start again from scratch; or when a step fails because something is missing
applies-when:
  - sessions are short-lived and each starts on a fresh machine (a chat's sandbox, a CI runner, a new container)
  - the work is handed between sessions often - every switch pays the setup again
  - a document tells the reader to run setup steps by hand
skip-when:
  - a one-off session whose environment nobody will rebuild
produces: one setup script that runs twice with no change the second time, and no setup step written anywhere else
cost: low - each requirement moved into the script once, when it is first met
---
# 22 — The environment is one idempotent script

**Use it** the moment you are about to fix an environment by hand, and whenever a
step fails for something missing - a compiler, a header, an owner, an identity.

**Why this exists.** A session's machine does not outlive it, and long sessions get
switched for fresh ones because a long one re-reads itself every turn (prompt 21).
So the setup is paid at every switch, and whatever it costs by hand is multiplied
by the number of sessions. In one project (forth-vm-evolution) the setup was a list
of commands in the handoff documents until Iteration 560:

* **a few tool calls every session** went on it, with a stumble or two - a directory
  the build user could not write, git refusing to work as root in that user's tree;
* **a requirement found by failing**: a fresh machine lacked the 32-bit compiler
  support, the stages quietly built at one width, and a test failed later, far from
  the cause (Iteration 553) - the fix went into the state file as one more manual
  line, for every later session to type;
* **the commit identity was missing** from a new session's setup, found only by
  doing it (prompt 07);
* **a scratch tree** - a clone to test a batch of patches in - was made by hand
  each time, and git refused root in it again (Iteration 567).

One script replaced the list (Iteration 560): one command, as root, from bare
machine to a clone that builds. Then the owner asked for the rule this prompt
states: setup only by the script, the script idempotent, every new requirement a
change to the script.

---

```
Before changing an environment by hand, and when a step fails for something missing:

1. One command from a bare machine to a working one. Every step a session would
   otherwise type - packages, links, users, owners, directories, the identity,
   a scratch copy of the tree - is a step of the script.

2. A requirement met by hand goes into the script in the same turn, then the
   script is run again to apply it. A document never carries a setup step: a
   line saying "install X first" is a bug in the script, and the document says
   only "run the script". One home for each requirement (prompt 21, item 3).

3. Idempotent: run twice, the second run changes nothing and says so. Each step
   looks before it acts - installed? there? running? done? - and prints what it
   found or what it did, one line each. A long job it starts is not started
   again while it runs, or once it is done (a pid it can check, a status with
   an end line); a job a crash or a suspended machine cut off is started again.
   A tree that is already there is left as it is - and the script says how it
   stands against the input it was given (the same, ahead, or another).

4. It fails loudly and early where the rest cannot work (no input, the clone
   failed), and goes on past what is independent (a package mirror down), naming
   the log to read.

5. The setup is not the work. Optional checks it can start (a build, the tests)
   are a switch, off by default; what the session then does is not in it.

6. Test it as it will be used: word for word on a fresh machine, and a second
   time on the same one. Test each guard by provoking it - a job alive, a job
   done, a tree there - since a guard that never fired is not known to work
   (prompt 15).

7. Keep it plain - the machine's own shell, no framework, inputs as arguments
   and environment variables with defaults, its usage at its top.
```

## Artifact required

The setup command run and its output. When the script changed: the diff, a run on
a fresh machine or directory, and a second run showing nothing changed - each guard
provoked once. At the session's end, the environment steps taken by hand: none, or
each one now in the script.
