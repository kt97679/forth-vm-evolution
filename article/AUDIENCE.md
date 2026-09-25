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

---

# What sinks an article, from Habr's moderators and from hostile comments

The section above is about what works. This one is about what does not,
and it turned up things the successful examples could not.

## The formatting rules that cost rating automatically

From Habr's own moderation post, "10 супер обидных ошибок авторов" (+124,
40K views), which lists the mistakes that "напрочь проваливают нормальные,
на первый взгляд, материалы".

**The cut.** "Нет ката или докатный текст очень длинный. Как правило,
такие статьи слёту набирают минусы за оформление, потому что
«вытесняют» всю ленту и раздражают." Text before the cut is what shows
in everyone's feed. Our Russian intro runs 545 words before the first
section - that is a feed-flooding article that collects downvotes for
formatting alone, before anyone reads a word of the argument. **Put the
cut after the opening paragraphs, not after the vocabulary.**

**Too much bold and italic**: "такие статьи как будто внезапно вылезли
из веба девяностых. Это не лучший способ выделить в статье главное."
Our article bolds every one of the seven lessons, plus emphasis
throughout. Count them and cut most.

**Bare long URLs**: wrap the link on a word or two instead. Our
references are a column of raw `<https://...>`.

**КДПВ under 1 MB**, no gifs, no flashing.

**No full stop at the end of a subheading.** Ours comply.

## Machine translation is a named failure mode

The post lists "машинные переводы" among things moderators treat as
articles written in bad faith. Our Russian version was produced from the
finished English one, which is exactly the shape that reads as a
translation: calques, English sentence rhythm, terms left in English
where a Russian word exists. That is a specific, checkable risk, and it
is why the Russian version needs a reading pass by a Russian speaker
rather than another figure check.

## Condescension, itemised

"Пренебрежение к читателям" is listed as the mistake that experienced
authors make most:

- expand every abbreviation, in brackets or with the editor's function;
- never tell the reader to google a term - "не нужно показывать своё
  превосходство";
- use the Russian term where one exists without loss;
- do not estimate the reader's level: "не оценивайте знания вашего
  невидимого, анонимного читателя (если не в курсе, для тупых
  поясню, для тех кто в танке…) — он может оказаться новичком, а может
  суперпрофи, который вас и ваш код уделает за пару комментариев".

## Credentials belong at the end

"Самопиар без границ": opening with who you are reads as "не спорьте со
мной, я авторитет" and costs the article. Habr's editor has a "Персона"
card for the end. Our opening is a confession rather than a CV, which is
the right side of this line - but the instinct to establish standing
early is the one being warned against.

## The "что делать" ending is a known joke

From a comment thread on a piece that got exactly this reaction:

> вот этот вот абзац "Что делать?" в конце таких бесполезных статей …
> не несет как обычно реального ответа что делать а просто очередной
> набор кучи бесполезных советов

And, on the same article: "никакой новизны нет в статье", "типичная
писанина из серии кто виноват и что делать", "Капитан очевидность".

Our section 11 is a seven-item "what I would tell someone starting this
work". It is on exactly this template and will be read against it. What
saves it, if anything does, is that every item carries a measurement and
the scope it holds in - "the mean run here is about 1.3", "worth 34%
between them", "I measured one kernel, not a language". Any item that
degenerates into general advice should be cut rather than softened.

## Benchmark articles are judged against Shipilev

The sharpest technical criticism found was aimed at a performance
article, comparing it unfavourably to Aleksey Shipilev and Martin
Thompson:

> посмотрите на статью автора с его манипуляциями байткодом с пачкой
> необоснованных утверждений и статьи Шипилева или Томпсона, разница
> гигантская, так как у них идет разбор на уровне asm и иногда железа

Two things in that. **"Пачка необоснованных утверждений" is the phrase
that kills a performance article** - and it is precisely what six review
rounds have been removing from ours. And the bar for this audience is
analysis down to instructions and hardware, not ratios alone. We have
the counts, the operation profiles and the opcode budget; they should be
visible, not buried.

Related, from an interview with Andrey Akinshin on benchmarking: "для
любого результата бенчмарка в интернете можно найти неправильную
интерпретацию этого результата", and the typical mistake is
"бездумно бенчмаркать всё подряд". Our discarding of two workloads for
irreproducibility is the right story for this audience and is currently
in section 9, late. It is a credential; consider whether it earns an
earlier mention.

## Splitting the article

"Нелогичное дробление статей на серии" is listed as a mistake when done
for exposure, and acceptable when "объективно необходимо" - the examples
given are multi-part series where each piece is self-contained. If our
length becomes the problem, the split that would survive this test is
the encoding ladder as one article and the measurement methodology plus
the twenty-year regression as another. Splitting mid-ladder would not.

---

# English-language venues: Hacker News, Lobsters, and the craft advice

ForthHub is the primary target, but the English version can also go to
Hacker News, Lobsters and r/Forth. Those have their own rules, and the
best craft advice I found is Michael Lynch's "How to Write Blog Posts
that Developers Read" (Refactoring English) - nine years of software
blogging, 30+ Hacker News front pages. Four of his points land directly
on this article.

## "Get to the point" - and we do not

His diagnosis of the commonest failure is uncomfortably close to home:

> the author has some valuable insight to share, but they squander their
> first seven paragraphs on the history of functional programming and a
> trip they took to Bell Labs in 1973.

His rule: **the title plus the first three sentences must answer two
questions** - is this written for someone like me, and how do I benefit?
"If you find yourself in paragraph two and you haven't answered either
question, you're in trouble."

Ours answers the first (the title says Forth virtual machine, six
attempts, two failures). It does not answer the second until section 11.
A reader learns *what happened to me in 2004* before learning *what they
get*. The fix is one sentence in the opening: what this article will
tell them that they cannot get elsewhere - measured costs for six
encoding schemes, including the two that failed and why.

This is the same finding as the Habr cut, arrived at independently: the
opening is too long and too much about us.

## "Think one degree bigger"

The audience is Forth implementers. One degree out is anyone who has
written an interpreter or a VM; two degrees is systems programmers who
care about code density - firmware, embedded, bytecode formats. Lynch's
point is that the widening usually costs "an extra sentence or two early
in the article to introduce a concept or replace jargon".

We have done some of this - cell, threading, dispatch loop, inner and
outer interpreter are all defined now. The remaining jargon wall is in
sections 3 to 5. Worth one pass asking, for each paragraph: would
someone who has written a bytecode VM but never touched Forth follow
this?

## "Plan the route to your readers"

Ask before publishing, not after: how does anyone find this?

- **ForthHub discussion** - the natural home, and the one audience
  guaranteed to care. Post there first.
- **Hacker News** - friendly to VMs, compilers, retro-computing and
  "surprising benchmark" stories. The Amplify study of front-page
  stories found the strongest angles are "a technical lesson learned
  while building something", "a surprising failure, tradeoff, benchmark,
  or teardown", and "a clear argument that invites informed
  disagreement". Ours is all three. But HN is a lottery - "the same
  story can get 1 upvote or 400" - and Lynch notes one blogger whose top
  three posts of the year all flopped on first submission and only
  succeeded on the second or third, months later. **Resubmission is
  normal, not shameful.**
- **Lobsters** - narrower and more consistent than HN, invite-only, with
  public moderation logs and strong norms against drive-by
  self-promotion. Tags `compilers`, `plt`, `performance`, `retro`. A
  post that stands on its own technically does well; anything that looks
  like traffic-seeking does not.
- **r/Forth** - small but exactly on topic. Check it accepts links.

Give the post more than one chance. Betting everything on one
submission to one site is how good articles disappear.

## "Show more pictures" - our worst failing

> The biggest bang-for-your-buck change you can make to a blog post is
> adding pictures.

Counted, this article contains **zero images**. Fourteen headings, 32
table rows, five code blocks - and nothing visual at all.

He is explicit that quality matters less than presence: free stock
photos and AI images "are better than nothing, but they're worse than
anything else, including terrible MS Paint drawings". Excalidraw is
named as the free tool he uses for his own diagrams.

Five things in this article are already diagrams pretending to be
monospace text, and would be better drawn:

1. `COUNT` as seven cells, with the low bit marked - section 1
2. the same word in three encodings, 28 / 14 / 5 bytes, to scale
3. the two word-number tables pointing opposite ways - section 3
4. the byte-granular link, read backwards from the name - section 7
5. image size across the ladder, 24,320 down to 7,609

Number 5 is the one a skimmer would stop on, and it is currently a
column of numbers in a table.

## "Accommodate skimmers"

His test: strip everything but headings and images, and ask whether what
remains makes you want to read.

Ours survives this better than most, because the headings carry the
narrative - "Attempt one: pack several operations into a cell",
"Attempt two: a 16-bit token through a word table", "The premise I never
checked". A skimmer sees the shape of the story.

But with no images, the skim is headings only, against page after page
of dense prose. "The worst thing for a skimmer to see is a wall of
text."

## The one thing all three sources agree on

Habr's moderators, the Habr meta-article, and Lynch independently arrive
at the same two instructions: **get to the point faster, and show
something visual.** We have done neither, and both are cheap.
