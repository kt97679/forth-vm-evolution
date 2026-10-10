\ tests/core/fixes.fth - Iteration 125: what the Forth 2012 test suite and
\ RelF found wrong in this kernel and its engines, fixed - one test each
\ (results/forth-standard-tests.md). Needs tester.fr loaded first. The
\ +LOOP cases are coreplus-loop.fth (RelF's, from the standard suite); the
\ refusals - a name over 31 characters, IF outside a definition - abort,
\ so tools/run-tests.sh checks them on their own; DELETE-FILE likewise.

DECIMAL

\ PARSE skips no leading delimiter, so an empty string is empty and the
\ rest of the line is left alone (S" " took the rest of the line).
{ : FX1 S" " ; FX1 SWAP DROP -> 0 }
{ : FX2 ." " 7 ; FX2 -> 7 }
{ S" " SWAP DROP -> 0 }
{ : FX3 ( ) 5 ; FX3 -> 5 }
{ 41 PARSE ) SWAP DROP -> 0 }
{ : FX4 S" ab" ; FX4 SWAP DROP -> 2 }

\ CONVERT converts from c-addr1 + 1 (it began two bytes early).
CREATE FXN 3 C, CHAR 1 C, CHAR 2 C, CHAR 3 C,
{ 0 0 FXN CONVERT DROP -> 123 0 }

\ The file words: doubles where the standard has them, iors 0 or not.
CREATE FXB 16 ALLOT
VARIABLE FXF
{ S" fixes-test.tmp" R/W CREATE-FILE SWAP FXF ! -> 0 }
{ S" abcdefgh" FXF @ WRITE-LINE -> 0 }
{ FXF @ CLOSE-FILE -> 0 }
{ S" fixes-test.tmp" R/O OPEN-FILE SWAP FXF ! -> 0 }
{ FXF @ FILE-POSITION -> 0 0 0 }
{ FXB 0 FXF @ READ-LINE -> 0 TRUE 0 }
{ FXB 3 FXF @ READ-LINE -> 3 TRUE 0 }
{ FXF @ FILE-POSITION -> 3 0 0 }
{ 1 0 FXF @ REPOSITION-FILE -> 0 }
{ FXF @ FILE-POSITION -> 1 0 0 }
{ FXF @ FILE-SIZE -> 9 0 0 }
{ FXF @ CLOSE-FILE -> 0 }
{ S" fixes-test.tmp" DELETE-FILE -> 0 }
