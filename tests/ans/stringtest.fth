\ To test the ANS Forth String word set

\ Copyright (C) Gerry Jackson 2006, 2007

\ This program is free software; you can redistribute it and/or
\ modify it any way.

\ This program is distributed in the hope that it will be useful,
\ but WITHOUT ANY WARRANTY; without even the implied warranty of
\ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

\ The tests are not claimed to be comprehensive or correct 

\ --------------------------------------------------------------------
\ Version 0.2  20 April 2007 ANS Forth words changed to upper case
\         0.1  Oct 2006 First version released

\ --------------------------------------------------------------------
\ The tests are based on John Hayes test program for the core word set
\ and requires those files to have been loaded

\ Words tested in this file are:
\     -TRAILING /STRING BLANK COMPARE SEARCH SLITERAL
\
\ Tests to be added:
\     CMOVE CMOVE>
\     
\ --------------------------------------------------------------------
\ Assumptions and dependencies:
\     - tester.fr has been loaded prior to this file
\     - COMPARE is case sensitive
\ --------------------------------------------------------------------

Testing String word set

DECIMAL

0 INVERT CONSTANT <true>
0 CONSTANT <false>

{ :  s1 S" abcdefghijklmnopqrstuvwxyz" ; -> }
{ :  s2 S" abc"   ; -> }
{ :  s3 S" jklmn" ; -> }
{ :  s4 S" z"     ; -> }
{ :  s5 S" mnoq"  ; -> }
{ :  s6 S" 12345" ; -> }
{ :  s7 S" "      ; -> }
{ :  s8 S" abc  " ; -> }
{ :  s9 S"      " ; -> }
{ : s10 S"    a " ; -> }

\ --------------------------------------------------------------------

Testing -TRAILING

{  s1 -TRAILING -> s1 }
{  s8 -TRAILING -> s8 2 - }
{  s7 -TRAILING -> s7 }
{  s9 -TRAILING -> s9 DROP 0 }
{ s10 -TRAILING -> s10 1- }

\ --------------------------------------------------------------------

Testing /STRING

{ s1  5 /STRING -> s1 SWAP 5 + SWAP 5 - }
{ s1 10 /STRING -4 /STRING -> s1 6 /STRING }
{ s1  0 /STRING -> s1 }

\ --------------------------------------------------------------------

Testing SEARCH

{ s1 s2 SEARCH -> s1 <true> }
{ s1 s3 SEARCH -> s1  9 /STRING <true> }
{ s1 s4 SEARCH -> s1 25 /STRING <true> }
{ s1 s5 SEARCH -> s1 <false> }
{ s1 s6 SEARCH -> s1 <false> }
{ s1 s7 SEARCH -> s1 <true> }

\ --------------------------------------------------------------------

Testing COMPARE

{ s1 s1 COMPARE -> 0 }
{ s1 PAD SWAP CMOVE -> }
{ s1 PAD OVER COMPARE -> 0 }
{ s1 PAD 6 COMPARE -> 1 }
{ PAD 10 s1 COMPARE -> -1 }
{ s1 PAD 0 COMPARE -> 1 }
{ PAD  0 s1 COMPARE -> -1 }
{ s1 s6 COMPARE ->  1 }
{ s6 s1 COMPARE -> -1 }
{ s1 S" abdde" COMPARE -> -1 }
{ s1 S" abbde" COMPARE ->  1 }
{ s1 S" abcdf"  COMPARE -> -1 }
{ s1 S" abcdee" COMPARE ->  1 }

: s11 S" 0abc" ;
: s12 S" 0aBc" ;

{ s11 s12  COMPARE -> 1 }
{ s12 s11  COMPARE -> -1 }

\ --------------------------------------------------------------------

Testing BLANK

{ PAD 25 CHAR a FILL -> }
{ PAD 5 + 6 BLANK -> }
{ PAD 12 S" aaaaa      a" COMPARE -> 0 }

\ --------------------------------------------------------------------

Testing SLITERAL

{ : s13 [ s1 ] SLITERAL ; -> }
{ s1 s13 COMPARE -> 0 }
{ s1 s13 ROT = ROT ROT = -> <true> <false> }


\ --------------------------------------------------------------------

CR .( End of String word tests) CR
