# colorForth's packed names - the encoding (from colorforth.com/chars.html, in forth.tgz)

48 characters, Huffman-like prefix codes; names packed into 32-bit words, up to
5 trailing zeros may follow the last character. Space and the 7 most common
characters take 4 bits (0xxx), the next 8 take 5 bits (10xxx), the remaining 32
take 7 bits (1100xxx-1111xxx); 5.2 bits a character on average. Characters are
ordered by frequency in English text; digits and specials unordered.

| code | chars (index) |
|---|---|
| 0 000-0 111 (4 bits) | space 0, r 1, t 2, o 3, e 4, a 5, n 6, i 7 |
| 10 000-10 111 (5 bits) | s 8, m 9, c 10, y 11, l 12, g 13, f 14, w 15 |
| 1100 000-111 (7 bits) | d 16, v 17, p 18, b 19, h 20, x 21, u 22, q 23 |
| 1101 000-111 | k 24, z 25, j 26, 3 27, 4 28, 5 29, 6 30, 7 31 |
| 1110 000-111 | 8 32, 9 33, 1 34, - 35, 0 36, . 37, 2 38, / 39 |
| 1111 000-111 | ; 40, : 41, ! 42, + 43, @ 44, * 45, , 46, ? 47 |

For THIS project: standard Forth names use characters outside the 48 - ( ) <
> = " # ' [ ] and others - so a packed-names gene needs an escape code (or a
frequency table from our own dictionary: results/word-audit.md lists the
names), and lookup compares packed cells (NAME=? as one or two cell
compares - the loop audit's measure, results/loop-audit.md).
