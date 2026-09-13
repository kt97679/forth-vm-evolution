# Review prompt

Paste everything below into a fresh conversation with another model,
followed by the contents of `article/article-en.md`.

---

I'd like a hard review of a technical article. Please be blunt; I would
rather hear that a section does not work than be told it is fine.

## What it is

A write-up of a hobby project on Forth virtual machine implementation.
The author forked a VM called SOD32 in 2004, made a variant called RelF,
left it alone for twenty years, then recently rebuilt it for 64-bit and
found the image had doubled. The article is the sequence of things he
tried to get the size back, in the order he tried them, including two
approaches that failed.

## Audience

Two groups, and it has to work for both:

- Forth implementers, who will read it on a Forth forum. They know what
  threaded code, a dictionary, a cell and `DOES>` are. They will not
  tolerate hand-waving, and they will check the claims they can.
- General programmers who know roughly what Forth is and nothing about
  this project. They are the ones most likely to bounce off it.

An earlier draft was criticised by a reader in the second group for
opening with metrics before establishing why anything mattered, for
presenting an obvious result (hash tables speed up dictionary lookup) as
though it were a revelation, and for using terms without defining them.
The current draft is a rewrite intended to fix that. Please judge
whether it did.

## What has already been checked, so please don't spend effort there

- Every number is generated from a repository that builds and runs. I
  cannot ask you to verify arithmetic against data you do not have.
- Each figure carries a measured uncertainty, and the measurement method
  is described in section 10.
- Acronyms are expanded on first use.

## What I want from you

**1. Technical soundness.** Does each claim actually follow from what is
offered as evidence? Flag anything where the conclusion outruns the
measurement. Two known-delicate spots: the claim that deleting a lookup
table "recovers precisely what the table cost and nothing more", and the
claim that specialisation is worth more than every encoding change put
together. Are those stated defensibly?

**2. Where a reader gets lost.** Go through as the second audience -
someone who knows what a stack and a dictionary are, and nothing else.
Name the exact sentence or paragraph where you would have to re-read,
guess, or give up. Be specific; "section 3 is dense" is not useful,
"the phrase X in section 3 assumes I know Y" is.

**3. Unsupported or over-claimed statements.** Especially anywhere that
sounds like a general law rather than a measurement of one system. The
article ends with seven "things I would tell someone starting this
work". Are any of them broader than the evidence behind them?

**4. Structure.** The article is a narrative: attempt, failure, what the
failure taught, next attempt. Does that hold, or does it sag anywhere?
Is anything in the wrong place? Is anything there that should be cut -
be specific about what and why.

**5. Writing.** This was drafted with AI assistance and the author wants
it to read as a person wrote it. Flag anything that reads as machine
prose: over-balanced sentences, unnecessary hedging, portentous short
sentences for emphasis, repeated rhetorical shapes, tidy triads,
paragraphs that restate their own first line. Quote the offenders.

**6. Honesty of framing.** The article reports the author's own mistakes,
including one that went unnoticed for twenty years. Does it read as
candid, or as false modesty? Does any part read as showing off?

## What I do not want

- Copy-editing for its own sake. Report grammar only where it changes
  meaning.
- Praise. If a section works, one line saying so is enough.
- Suggested rewrites of whole sections unless you think the section
  cannot be repaired in place, in which case say why.

## Output

1. The three most serious problems, worst first, each with the specific
   passage and what is wrong with it.
2. Everything else, grouped by the numbered headings above.
3. One paragraph: would you keep reading this if you came across it
   unprompted, and where would you stop?

One flag: the expansion of "CV8" as "Code Vector" is a reconstruction,
not something recorded in the project's own files. If it reads as
though it might be wrong, say so.
