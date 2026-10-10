\ To test some of the ANS Forth Core Ext word set, version 0.1

\ Copyright (C) Gerry Jackson 2006, 2007

\ This program is free software; you can redistribute it and/or
\ modify it any way.

\ This program is distributed in the hope that it will be useful,
\ but WITHOUT ANY WARRANTY; without even the implied warranty of
\ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

\ The tests are not claimed to be comprehensive or correct 

\ --------------------------------------------------------------------
\ Version 0.2   20 April 2007 ANS Forth words changed to upper case
\                             Tests qd3 to qd6 by Reinhold Straub
\         0.1   Oct 2006 First version released

\ --------------------------------------------------------------------

\ This is only a partial test of the core extension words.
\ The tests are based on John Hayes test program for the core word set

\ Words tested in this file are:
\     TRUE FALSE :NONAME ?DO VALUE TO CASE OF ENDOF ENDCASE
\     C" CONVERT COMPILE, [COMPILE] SAVE-INPUT RESTORE-INPUT

\ --------------------------------------------------------------------
\ Assumptions:
\     - tester.fr has been included prior to this file
\ --------------------------------------------------------------------

Testing Core Extension words

DECIMAL

Testing TRUE FALSE

{ TRUE  -> 0 INVERT }
{ FALSE -> 0 }

\ --------------------------------------------------------------------

Testing :NONAME

VARIABLE nn1
VARIABLE nn2
:NONAME 1234 ; nn1 !
:NONAME 9876 ; nn2 !
{ nn1 @ EXECUTE -> 1234 }
{ nn2 @ EXECUTE -> 9876 }

\ --------------------------------------------------------------------

Testing ?DO

: qd ?DO I LOOP ;
{ 789 789 qd -> }
{ -9876 -9876 qd -> }
{ 5 0 qd -> 0 1 2 3 4 }

: qd1 ?DO I 10 +LOOP ;
{ 50 1 qd1 -> 1 11 21 31 41 }
{ 50 0 qd1 -> 0 10 20 30 40 }

: qd2 ?DO I 3 > if LEAVE else I then LOOP ;
{ 5 -1 qd2 -> -1 0 1 2 3 }

: qd3 ?DO I 1 +LOOP ;
{ 4  4 qd3 -> }
{ 4  1 qd3 -> 1 2 3 }
{ 2 -1 qd3 -> -1 0 1 }

: qd4 ?DO I -1 +LOOP ;
{  4 4 qd4 -> }
{  1 4 qd4 -> 4 3 2 1 }
{ -1 2 qd4 -> 2 1 0 -1 }

: qd5 ?DO I -10 +LOOP ;
{   1 50 qd5 -> 50 40 30 20 10 }
{   0 50 qd5 -> 50 40 30 20 10 0 }
{ -25 10 qd5 -> 10 0 -10 -20 }

VARIABLE iterations
VARIABLE increment

: qd6 ( limit start increment -- )
   increment !
   0 iterations !
   ?DO
      1 iterations +!
      I
      iterations @  6 = IF LEAVE THEN
      increment @
   +LOOP iterations @
;

{  4  4 -1 qd6 -> 0 }
{  1  4 -1 qd6 -> 4 3 2 1 4 }
{  4  1 -1 qd6 -> 1 0 -1 -2 -3 -4 6 }
{  4  1  0 qd6 -> 1 1 1 1 1 1 6 }
{  0  0  0 qd6 -> 0 }
{  1  4  0 qd6 -> 4 4 4 4 4 4 6 }
{  1  4  1 qd6 -> 4 5 6 7 8 9 6 }
{  4  1  1 qd6 -> 1 2 3 3 }
{  4  4  1 qd6 -> 0 }
{  2 -1 -1 qd6 -> -1 -2 -3 -4 -5 -6 6 }
{ -1  2 -1 qd6 -> 2 1 0 -1 4 }
{  2 -1  0 qd6 -> -1 -1 -1 -1 -1 -1 6 }
{ -1  2  0 qd6 -> 2 2 2 2 2 2 6 }
{ -1  2  1 qd6 -> 2 3 4 5 6 7 6 }
{  2 -1  1 qd6 -> -1 0 1 3 }

\ --------------------------------------------------------------------

Testing VALUE TO

{ 111 VALUE v1 -999 VALUE v2 -> }
{ v1 -> 111 }
{ v2 -> -999 }
{ 222 TO v1 -> }
{ v1 -> 222 }
{ : vd1 v1 ; -> }
{ vd1 -> 222 }
{ : vd2 TO v2 ; -> }
{ v2 -> -999 }
{ -333 vd2 -> }
{ v2 -> -333 }
{ v1 -> 222 }

\ --------------------------------------------------------------------

Testing CASE OF ENDOF ENDCASE

: cs1 CASE 1 OF 111 ENDOF
           2 OF 222 ENDOF
           3 OF 333 ENDOF
           >R 999 R>
      ENDCASE
;

{ 1 cs1 -> 111 }
{ 2 cs1 -> 222 }
{ 3 cs1 -> 333 }
{ 4 cs1 -> 999 }

: cs2 >R CASE -1 OF CASE R@ 1 OF 100 ENDOF
                            2 OF 200 ENDOF
                           >R -300 R>
                    ENDCASE
                 ENDOF
              -2 OF CASE R@ 1 OF -99  ENDOF
                            >R -199 R>
                    ENDCASE
                 ENDOF
                 >R 299 R>
         ENDCASE R> DROP
;

{ -1 1 cs2 ->  100 }
{ -1 2 cs2 ->  200 }
{ -1 3 cs2 -> -300 }
{ -2 1 cs2 -> -99  }
{ -2 2 cs2 -> -199 }
{  0 2 cs2 ->  299 }

\ --------------------------------------------------------------------

Testing C" CONVERT

: cq1 C" 1234" ;

{ cq1 COUNT EVALUATE -> 1234 }

VARIABLE conv1
VARIABLE conv2
{ : cq2 C" .98765A123:" ; -> }
{ cq2 COUNT DROP conv1 ! -> }
{ conv1 @ 6 CHARS + conv2 ! -> }
{ 0 0 conv1 @ CONVERT ->  98765 0 conv2 @ }
{ 3 0 conv1 @ CONVERT -> 398765 0 conv2 @ }
{ 0 0 conv1 @ CONVERT CONVERT -> 98765123. conv2 @ 4 CHARS + }
		
\ --------------------------------------------------------------------

Testing COMPILE, [COMPILE]

:NONAME DUP + ; CONSTANT dup+
{ : q dup+ COMPILE, ; -> }
{ : as [ q ] ; -> }
{ 123 as -> 246 }

{ : [c1] [COMPILE] DUP ; IMMEDIATE -> }
{ 123 [c1] -> 123 123 }                 \ With default compilation semantics
{ :  [c2] [COMPILE] [c1] ; -> }
{ 234 [c2] -> 234 234 }                 \ With an immediate word
{ : [cif] [COMPILE] IF ; IMMEDIATE -> }
{ : [c3] [cif] 111 ELSE 222 THEN ; -> } \ With special compilation semantics
{ -1 [c3] -> 111 }
{  0 [c3] -> 222 }

\ --------------------------------------------------------------------
\ Cannot automatically test SAVE-INPUT and RESTORE-INPUT from a console source


Testing SAVE-INPUT and RESTORE-INPUT with a file source

VARIABLE siv -1 siv !

: NeverExecuted
	." This should never be executed" ABORT
;

11111 SAVE-INPUT

siv @

[IF]
	0 siv !
	RESTORE-INPUT
	NeverExecuted
[ELSE]

Testing the [ELSE] part is executed
22222

[THEN]

{ -> 11111 0 22222 }	\ 0 comes from RESTORE-INPUT

Testing SAVE-INPUT and RESTORE-INPUT with a string source

VARIABLE si_inc 0 si_inc !

: si1
	si_inc @ >IN +!
	15 si_inc !
;

: s$ S" SAVE-INPUT si1 RESTORE-INPUT 12345" ;

{ s$ EVALUATE si_inc @ -> 0 2345 15 }

Testing nested SAVE-INPUT and RESTORE-INPUT

: read_a_line
	REFILL 0=
	ABORT" REFILL failed"
;

0 si_inc !

2VARIABLE 2res -1. 2res 2!

: si2
	read_a_line
	read_a_line
	SAVE-INPUT
	read_a_line
	read_a_line
	s$ EVALUATE 2res 2!
	RESTORE-INPUT
;

\ WARNING: do not delete or insert lines of text after si2 is called
\ otherwise the next test will fail

si2
33333					\ This line should be ignored
2res 2@ 44444		\ RESTORE-INPUT should return to this line

55555
Testing the nested results
{ -> 0 0 2345 44444 55555 }

\ End of warning

\ --------------------------------------------------------------------

CR .( End of Core Extension word tests) CR


