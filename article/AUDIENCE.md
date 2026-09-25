# Who this is for, and what that changes

The English version goes to ForthHub's discussion forum; the Russian
version to Habr. Reading the forum first changed several decisions, so
the reasons are written down rather than left implicit.

## Who is actually there

The regulars include Mitch Bradley (Open Firmware, and therefore FCode),
Bernd Paysan (Gforth), Anton Ertl by reference, ruv, alexshpilkin,
alextangent, Anthony Howe. Discussion #187, "An elevator description for
Forth's threaded code models?", is 28 comments of exactly the material
this article is about.

These are people who have implemented the thing being described. That
is a gift and a hazard: they will find any claim that does not hold.

## What the forum tells us to do

**Use the community's taxonomy, and map our names onto it in the first
few paragraphs.** The thread settles on direct / indirect / subroutine /
token threading and byte-coded, with Bradley noting the "token threaded
variant where the pointers are not full addresses, but instead some
extra-compact representation like indices into an array, or
variable-length identifiers". That sentence describes SOD16, CPT16 and
the varint experiments precisely. Our names - CPT16, CV8, PACK4, PACK8 -
are local inventions and must be introduced as such, against the
standard terms, or the article reads as if it were unaware of the field.

**Do not skip literals and control flow.** ruv's immediate response to
Bradley's summary was "what about literals and control-flow? ... The
devil is in the details." Every encoding here had to answer that
question, the answers are in the overlay sources, and they are the
interesting part rather than an appendix. Same for `DOES>`, which is
where three of the bugs were.

**Be precise with terms.** In the same thread ruv rejects "closure" as
inappropriate for an indirect-threaded code field. Loose analogies will
be corrected in public.

**Cite the canon.** Brad Rodriguez, *Moving Forth* - referenced three
separate times in one thread, and the standard shared reference.
Loeliger, *Threaded Interpretive Languages* (1981). Ertl on dispatch.
Not citing these signals that the work was done in isolation.

**Tradeoffs, plural, named.** Bradley's fuller answer lists "size,
speed, ease of implementation, relocation, cross-platform portability,
and interactions with machine architecture details like memory models
and caching". Four of those are axes we measured and two are ones we
did not - relocation and portability - and RelF's relative addressing
has something to say about both.

**They will run it.** This is a forum where people build Forth systems.
One command to build, one to test, byte-identical verification, and
SOD32 vendored at a pinned revision. That is worth more here than any
prose.

## One thing to fix before publishing

`CV8-REFERENCE.md` credits Open Firmware's FCode for the byte-token
format with an escape for two-byte codes, and the parent project's own
notes flag it: the general shape is remembered, the exact ranges are
not, and it should be checked against IEEE 1275. Mitch Bradley wrote
Open Firmware and reads this forum. Either the claim gets verified
against the standard or it gets softened to "the same general idea,
from memory, not checked" - but it does not get published as it stands.

## Tone

The forum is technical, unhurried and allergic to salesmanship. The
strongest material here is the part where the work was wrong: two
designs rejected on a benchmark that was four times too harsh, a
regression inherited by omission and not noticed for two hundred
iterations, a test suite that passed while the compiler was broken.
That should be the spine, not a footnote at the end.

---

# Habr, from reading it rather than guessing

Researched by reading Habr's own docs, the monthly "best articles"
round-ups, a meta-article on what makes a good Habr piece, and the
comment threads under a highly-rated deep-technical article. Sources and
figures below are from those, not from intuition.

## Views and rating are different currencies, and we want rating

The monthly round-ups filter on "more than 30,000 views OR rating above
+30" - two separate criteria, because they do not coincide. One author
in the July 2025 round-up appears with high view counts and a *negative*
rating. Clickbait buys views; the community's approval is a separate
thing and is what survives.

So: optimise for rating, bookmarks and comments, not for views. A
practical consequence is that the title must be exactly what the article
is. Habr's own commentary on the subject calls a strong headline
unconnected to the content "обман", and one whose content is empty and
holywar-ish "паразит".

## A hard, long, technical article can do very well

The counter-example that matters for us. "Оптимизация кода: процессор"
is marked **Сложный**, 18 minutes' reading, and scored **+97 (102 up, 5
down), 123K views, 718 bookmarks, 142 comments**.

That contradicts the general advice, also from Habr, that read articles
run to 10 minutes and rarely past 15 - which is real, but is advice for
the broad-audience category. The expert category plays by different
rules: depth is the product.

Note the ratio though: **718 bookmarks against 142 comments**. For a
technical reference piece, bookmarks are the signal. People saved it to
send to others - one commenter said outright he would use it instead of
writing his own explanations for juniors. Write something that can be
*re-sent*, and the numbers follow.

Our article is longer than 18 minutes. That is a risk taken knowingly,
not an oversight.

## What the comments actually reward

Read a comment thread under a deep technical piece and the pattern is
consistent.

**The standard positive comment is "спасибо за статью" plus a specific
correction or addition.** Readers add `restrict` from C99, point to
Agner Fog, supply the LFSR trick with `sbc eax,eax` on Z80. They are
co-authoring. Leave obvious room for that - the "Not measured" section
is exactly the right bait.

**They will run your examples.** Multiple commenters pasted the
article's code into godbolt mid-argument and reported back. One
disproved a claim that way. Our whole repository is built for this and
we should say so in the first screen, not in the references.

**They check your sources.** The author paraphrased a Carnegie Mellon
textbook; a commenter found the actual passage and quoted it back to
show the paraphrase was wrong ("Большинство компиляторов НЕ ПЫТАЮТСЯ
определить..." against the article's "тяжело определить"). Do not
paraphrase anything not verified.

**Missing versions are a complaint.** "Жаль не указана версия gcc."
Name the compiler, the flags and the machine. We do.

**Optimisation level is a trap.** The article compiled at `-Og` and a
commenter dismissed the whole thing: "автор один из тех, кто занимается
оптимизацией DEBUG-сборки". State the level and why.

## What the comments punish

**Categorical dismissiveness.** One commenter opened with "эти
оптимизации были актуальны году так в 90" and ignored the article's
counter-examples. Another user logged in after a year dormant purely to
say so: "невероятно самодовольный категоричный комментарий напрочь
игнорирующий контр-примеры из статьи".

That is a lesson about the article's own voice as much as about
commenting. Every categorical claim we make is a target, and the ones
reviewers have already made us withdraw - "recovers precisely what the
table cost", "worse on every machine and every workload" - are exactly
the shape that draws this.

**Appeal to authority instead of evidence.** "Я верю профессорам
Carnegie Mellon" did not survive contact with someone who opened the
book.

**Terminology slips.** "Оптимизируем цикл на несколько циклов" for
clock cycles drew: "программисты узнают слово такты, раньше чем начинают
учить ассемблер, и это статья от программиста!?" The author then asked
the thread whether to change it, which went down well. Russian technical
vocabulary is checked hard - see TERMINOLOGY-RU.md, and when in doubt
ask in the comments rather than defend.

## Format expectations

- **КДПВ** - a lead image. Habr readers expect one, and the meta-article
  spends paragraphs on how it works: neutral, roughly about the topic,
  pleasant, sometimes illustrating the thesis. We have none. The
  `COUNT` cell dump rendered as an image is the obvious candidate.
- **Anons** (the lead paragraph): start from something familiar, then
  introduce the intrigue. Our opening - a 2004 fork, a twenty-year gap,
  an image that doubled for no reason the author chose - already does
  this.
- Difficulty **Сложный**, up to 5 hubs, up to 10 keywords, all required
  at posting time.
- Over 10,000 characters is a "лонгрид" by their editors' definition.
  Ours is four times that.
- Habr uses HFM: underscores inside words are NOT italics, which
  protects `s6-cv8b` and `LOAD_FAST`; italics need asterisks; URLs
  autolink; tables are supported including merged cells.

## The one structural idea worth stealing

The meta-article's analysis of a popular piece notes that its sections
alternate: bright, neutral, neutral, bright, neutral, bright - "как в
кино, театре, музыке", and that this is why it does not tire the reader.

Our sequence is closer to uniformly dense. The natural bright points are
section 1 (the doubling), section 2 (the nibble scheme losing to the
byte scheme), and section 8 (the twenty-year regression). Section 7 is
the flattest and sits immediately before the payoff - which is what two
English reviewers independently identified as the place they would stop.
