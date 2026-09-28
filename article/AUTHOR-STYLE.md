# How kt97679 actually writes, from his 14 Habr articles

Read the profile, all fourteen leads, and "Сколько нужно примитивов для
реализации форт системы?" in full - the direct predecessor of this
project, same sod32, same kernel.img, same Hayes tests.

## The numbers

| | |
|---|---|
| articles | 14, since 2013; karma 108 |
| reading time | 3, 3, 3, 3, 3, 4, 5, 5, 5, 6, 6, 7, 11 minutes |
| best rated | Sun vs Intel +122 (18K views); Графика в терминале +110 (37K views, 184 bookmarks) |
| the Forth one | 3 min, +27, 5.4K views, 30 comments |

**Nothing he has written is longer than 11 minutes, and the median is
five.** Our article is roughly 25-30. That is the single largest
difference between this piece and everything else under his name.

## The opening is always the same shape

A concrete external trigger, then curiosity stated outright, then the
question the article answers. Not one of the fourteen opens with a
summary of findings.

- "Эта статья является результатом посещения мной автосервиса. В
  ожидании машины я подключил свой ноутбук к гостевой wifi-сети…"
- "На моей домашней машине вот уже 7 лет работает пара дисков… И вот на
  днях один диск в зеркале наконец начал сыпаться. Появился повод…"
- "Эта история началась, когда я узнал о существовании bpytop. Меня
  поразила детализация графиков и я начал разбираться как это сделано."
- "В 1992-м году проходил очередной конкурс по обфусцированному
  программированию… Меня поразило, что виртуальная машина была
  реализована всего в 794 байтах… первоначальный восторг уступил место
  разочарованию… С этого момента меня терзал вопрос —"

The recurring verbs are **мне стало интересно**, **меня поразило**,
**меня терзал вопрос**. The trigger is usually mundane and specific: a
car service waiting room, a failing disk, a comment on reddit.

## Four more habits

**He disclaims practical value early, without apology.** "Хочу сразу
отметить, что вся эта деятельность имеет чисто академический смысл.
Применить полученные результаты на практике вряд ли получится из-за
потери производительности."

**He shows the exact commands.** Not a description of how he measured -
the command line, pasted.

**He states the result flatly, with the number and no flourish.**
"размер двоичного образа увеличился с 10164 до 15912 (+57%),
производительность упала в 708 раз".

**He ends by saying what still bothers him, and asking.** This is the
signature move, and it is the opposite of a list of lessons:

> Меня смущает то, что для доступа к памяти присутствует целых 3
> примитива: @, ! и lit, но я не придумал, как этого можно избежать. Я
> вполне мог что-то упустить, так что если вы знаете как можно
> избавиться от бОльшего количества примитивов — пожалуйста напишите в
> комментариях.

And in the cryptography article: "У меня нет глубоких криптографических
знаний… Очень рассчитываю на то, что в комментариях мне объяснят, что и
почему я сделал неправильно."

That ending does three things at once: it is honest, it is modest
without being coy, and it hands the comment section a specific job. The
Forth article got 30 comments on 5.4K views with it.

## What this means for our article

**Keep:** the measurements, the failures, the honesty about what was not
isolated. That register is already his.

**Change:** the opening, which leads with a summary of findings rather
than with what made him curious. And the ending, which is seven lessons
- the "что делать" template Habr readers mock, and which nothing in his
own writing resembles.

**Unresolved:** the length. Five minutes is his median, eleven his
maximum. This article reports a year of work rather than one experiment,
so it is a different kind of piece - but three times his longest is a
real divergence and splitting it is the honest option.

**Minor:** he lowercases tool and system names in Russian prose -
gentoo, ubuntu, linux, "форт система", sod32 - where our Russian text
capitalises Forth throughout.

## Corrections from the author

**His motivation was not idle curiosity.** "Из любопытства, а не по
необходимости" was my phrase and it read strangely to him. The real
account, in his words: he liked SOD32 for its стройность, minimalism and
simplicity, noticed its performance was fairly low, wondered whether it
could be improved, built RelF - and the gain was modest enough that he
lost interest for a long time. The opening now uses that almost
verbatim.

**The hash-table regression is out.** He judged it a курьёз rather than
something a reader needs, and removed it. Worth recording that reviewers
had called it the strongest section, so the next person does not
restore it without knowing it was cut on purpose. The findings remain in
FINDINGS-OUTER-INTERPRETER.md; only the article no longer tells them.

**Tell it in order.** The introduction had promised that the failures
were the interesting part and hinted at why, which he found hard to
follow and not how he writes. His actual account is sequential: first a
packed format that would suit both 32 and 64 bits, which meant nibbles;
it did not work out well, so the next attempt was bytes; and so on. The
nibble and byte schemes are therefore two attempts, not two variants of
one, which makes seven attempts and three failures - and the title now
says so.

Also rewritten because it read awkwardly in Russian: "во что на самом
деле обходятся альтернативы, а не во что я привык считать, что они
обходятся". Replaced with the plain version: he wanted the bytes back,
so he started trying other encodings, and here they are in order.

**Process is not result.** The synthetic-benchmark aside - predicted
1.90-2.05x, measured 1.08-1.18 - is gone too. His reasoning: it was
interesting while doing the work but does not matter to the outcome.
Checked before removing: nothing else in either article depended on it,
and the methodology lesson it carried is made more fully by the
measurement section. The finding itself remains in the repository.
