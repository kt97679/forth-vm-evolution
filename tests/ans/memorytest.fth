\ To test the ANS Forth Memory-Allocation word set

\ Copyright (C) Gerry Jackson 2006, 2007

\ This program is free software; you can redistribute it and/or
\ modify it any way.

\ This program is distributed in the hope that it will be useful,
\ but WITHOUT ANY WARRANTY; without even the implied warranty of
\ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

\ The tests are not claimed to be comprehensive or correct 

\ --------------------------------------------------------------------
\ Version 0.2  20 April 2007  ANS Forth words changed to upper case
\         0.1  Oct 2006 First version released

\ --------------------------------------------------------------------
\ The tests are based on John Hayes test program for the core word set
\ and requires those files to have been loaded

\ Words tested in this file are:
\     ALLOCATE FREE RESIZE
\     
\ --------------------------------------------------------------------
\ Assumptions and dependencies:
\     - that 'addr -1 ALLOCATE' and 'addr -1 RESIZE' will return an error
\     - tester.fr has been loaded prior to this file
\     - testing FREE failing is not done as it is likely to crash the
\       system
\ --------------------------------------------------------------------

Testing Memory-Allocation word set

DECIMAL

0 CONSTANT <false>

\ --------------------------------------------------------------------

Testing ALLOCATE FREE RESIZE

VARIABLE addr

{ 100 ALLOCATE SWAP addr ! -> 0 }
{ addr @ 1 CELLS 1- and -> 0 }		\ Test address is aligned
{ addr @ FREE -> 0 }

{ 99 ALLOCATE SWAP addr ! -> 0 }

{ addr @ 1 CELLS 1- AND -> 0 }		\ Test address is aligned

{ addr @ FREE -> 0 }

{ 50 ALLOCATE SWAP addr ! -> 0 }

: writemem 0 DO I 1+ OVER C! 1+ LOOP DROP ;	( ad n -- )

: checkmem  ( ad n --- )
   0
   DO
      DUP C@ SWAP >R
      { -> R> I 1+ SWAP >R }  \ Luckily tester checks can be compiled
      R> 1+
   LOOP
   DROP
;

addr @ 50 writemem addr @ 50 checkmem

{ addr @ 28 RESIZE SWAP addr ! -> 0 }

addr @ 28 checkmem

{ addr @ 200 RESIZE SWAP addr ! -> 0 }

{ addr @ 28 checkmem

\ --------------------------------------------------------------------

Testing failure of RESIZE and ALLOCATE (unlikely to be enough memory)

{ addr @ -1 RESIZE 0= -> addr @ <false> }

{ addr @ FREE -> 0 }

{ -1 ALLOCATE SWAP DROP 0= -> <false> }		\ Memory allocate failed

\ --------------------------------------------------------------------

CR .( End of Memory-Allocation word tests) CR
