\ More tests on the the ANS Forth Core word set

\ This program is free software; you can redistribute it and/or
\ modify it any way.

\ This program is distributed in the hope that it will be useful,
\ but WITHOUT ANY WARRANTY; without even the implied warranty of
\ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

\ The tests are not claimed to be comprehensive or correct 

\ -----------------------------------------------------------------------------
\ Version 0.1  20 April 2007 Created

\ -----------------------------------------------------------------------------
\ The tests are based on John Hayes test program for the core word set
\ and requires those files to have been loaded

\ This file provides some more tests on Core words where the original Hayes
\ tests are thought to be incomplete

\ Words tested in this file are:
\     DO +LOOP
\
\     
\ -----------------------------------------------------------------------------
\ Assumptions and dependencies:
\     - tester.fr has been loaded prior to this file
\ -----------------------------------------------------------------------------


DECIMAL

0 INVERT CONSTANT <true>
0 CONSTANT <false>

Testing DO +LOOP with run-time increment, negative increment, infinite loop
\ Contributed by Reinhold Straub

VARIABLE iterations
VARIABLE increment
: gd7 ( limit start increment -- )
   increment !
   0 iterations !
   DO
      1 iterations +!
      I
      iterations @  6 = IF LEAVE THEN
      increment @
   +LOOP iterations @
;

{  4  4 -1 gd7 -> 4 1 }
{  1  4 -1 gd7 -> 4 3 2 1 4 }
{  4  1 -1 gd7 -> 1 0 -1 -2 -3 -4 6 }
{  4  1  0 gd7 -> 1 1 1 1 1 1 6 }
{  0  0  0 gd7 -> 0 0 0 0 0 0 6 }
{  1  4  0 gd7 -> 4 4 4 4 4 4 6 }
{  1  4  1 gd7 -> 4 5 6 7 8 9 6 }
{  4  1  1 gd7 -> 1 2 3 3 }
{  4  4  1 gd7 -> 4 5 6 7 8 9 6 }
{  2 -1 -1 gd7 -> -1 -2 -3 -4 -5 -6 6 }
{ -1  2 -1 gd7 -> 2 1 0 -1 4 }
{  2 -1  0 gd7 -> -1 -1 -1 -1 -1 -1 6 }
{ -1  2  0 gd7 -> 2 2 2 2 2 2 6 }
{ -1  2  1 gd7 -> 2 3 4 5 6 7 6 }
{  2 -1  1 gd7 -> -1 0 1 3 }
{ -20 30 -10 gd7 -> 30 20 10 0 -10 -20 6 }
{ -20 31 -10 gd7 -> 31 21 11 1 -9 -19 6 }
{ -20 29 -10 gd7 -> 29 19 9 -1 -11 5 }


\ -----------------------------------------------------------------------------

CR .( End of additional Core tests) CR
