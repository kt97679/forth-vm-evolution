# Russian terminology, fixed before translating

Agreed up front because retrofitting consistent terms across a long
Habr article is worse than choosing them now. Where the Russian Forth
community has a settled term, it wins over a literal translation.

| English | Russian | note |
|---|---|---|
| threaded code | шитый код | settled; not "поточный" |
| direct threaded code | прямой шитый код | |
| indirect threaded code | косвенный шитый код | |
| subroutine threading | подпрограммный шитый код | |
| token threading | токенный шитый код | |
| byte-coded | байт-код | |
| inner interpreter | внутренний интерпретатор | |
| outer interpreter | внешний интерпретатор | the distinction carries the article's main finding; keep it sharp |
| dispatch | диспетчеризация | |
| cell | ячейка | |
| word (Forth word) | слово | |
| dictionary | словарь | |
| word list / vocabulary | список слов / словарь | `wordlist` as список слов to avoid colliding with словарь |
| thread (of a hashed wordlist) | цепочка | NOT поток - it is a hash chain, and поток means an OS thread |
| link field | поле связи | |
| name field | поле имени | |
| parameter field | поле параметров | |
| execution token (xt) | исполнительный токен | |
| primitive | примитив | |
| literal | литерал | |
| branch / offset | переход / смещение | |
| cross-compiler | кросс-компилятор | |
| image | образ | |
| self-hosting | самокомпиляция / самораскрутка | prefer самокомпиляция for the property, самораскрутка for the bootstrap act |
| relocatable / position independent | перемещаемый / позиционно-независимый | |
| specialisation (of opcodes) | специализация | |
| superinstruction | суперинструкция | |
| benchmark | бенчмарк | тест производительности on first use, then бенчмарк |
| regression | регрессия | |
| resolution floor (of a measurement) | порог разрешения измерения | |

## Things not to translate

Keep in Latin script: the stage names (SOD32, SOD16, CPT16, CV8, PACK4,
PACK8), all Forth word names (`DOES>`, `SEARCH-WORDLIST`, `NAMEBUF`),
file names, and the standard's name (ANS Forth).

## Two phrasings to get right

- "the outer interpreter" is the whole point of section 4.2 and Russian
  readers will otherwise read внешний as "external" in the sense of
  "foreign". Define it once explicitly: the part that reads text, looks
  words up and either executes or compiles them.
- "a test that could not fail" - тест, который не мог упасть. Not
  "провалиться"; упасть is the idiom for a failing test.
