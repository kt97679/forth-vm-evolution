\ To test the ANS Forth search-order word set and search order extensions

\ Copyright (C) Gerry Jackson 2006, 2007

\ This program is free software; you can redistribute it and/or
\ modify it any way.

\ This program is distributed in the hope that it will be useful,
\ but WITHOUT ANY WARRANTY; without even the implied warranty of
\ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

\ The tests are not claimed to be comprehensive or correct 

\ --------------------------------------------------------------------
\ Version 0.3  20 April 2007 ANS Forth words changed to upper case
\         0.2  30 Oct 2006 updated following GForth tests to get
\               initial search order into a known state
\         0.1  Oct 2006 First version released

\ --------------------------------------------------------------------
\ The tests are based on John Hayes test program for the core word set
\ and requires those files to have been loaded

\ Words tested in this file are:
\     FORTH-WORDLIST GET-ORDER SET-ORDER ALSO ONLY FORTH GET-CURRENT
\     SET-CURRENT DEFINITIONS PREVIOUS SEARCH-WORDLIST WORDLIST FIND
\ Words not fully tested:
\     ORDER ONLY tests that it executes, display is implementation
\           dependent

\ --------------------------------------------------------------------
\ Assumptions and dependencies:
\     - tester.fr has been loaded prior to this file
\     - that ONLY FORTH DEFINITIONS will work at the start of the file
\       to ensure the search order is in a known state
\ --------------------------------------------------------------------

ONLY FORTH DEFINITIONS

Testing Search-order word set

DECIMAL

VARIABLE wid1  VARIABLE wid2

: save-orderlist ( widn ... wid1 n -> ) DUP , 0 ?DO , LOOP ;

\ --------------------------------------------------------------------

Testing FORTH-WORDLIST GET-ORDER SET-ORDER

{ FORTH-WORDLIST wid1 ! -> }

CREATE order-list

{ GET-ORDER save-orderlist -> }

: get-orderlist  ( -- widn ... wid1 n )
   order-list DUP @ CELLS  ( -- ad n )
   OVER +                  ( -- AD AD' )
   ?DO I @ -1 CELLS +LOOP  ( -- )
;

{ GET-ORDER OVER -> GET-ORDER wid1 @ } \ Forth wordlist at top
{ GET-ORDER SET-ORDER -> }             \ Effectively noop
{ GET-ORDER -> get-orderlist }         \ Check nothing changed
{ get-orderlist DROP get-orderList 2* SET-ORDER -> }
{ GET-ORDER -> get-orderlist DROP get-orderList 2* }
{ get-orderlist SET-ORDER GET-ORDER -> get-orderlist }

\ --------------------------------------------------------------------

Testing ALSO ONLY FORTH

{ ALSO GET-ORDER -> get-orderlist OVER SWAP 1+ }
{ ONLY FORTH GET-ORDER -> get-orderlist }    \ See assumptions above

\ --------------------------------------------------------------------

Testing GET-CURRENT SET-CURRENT WORDLIST (simple)

{ GET-CURRENT -> wid1 @ }        \ See assumptions above
{ WORDLIST wid2 ! -> }
{ wid2 @ SET-CURRENT -> }
{ GET-CURRENT -> wid2 @ }
{ wid1 @ SET-CURRENT

\ --------------------------------------------------------------------

Testing minimum search order list contains FORTH-WORDLIST and SET-ORDER

: so1 SET-ORDER ;    \ In case it is unavailable in the forth wordlist

{ ONLY FORTH-WORDLIST 1 SET-ORDER get-orderlist so1 -> }
{ GET-ORDER -> get-orderlist }

\ --------------------------------------------------------------------

Testing GET-ORDER SET-ORDER with 0 and -1 number of wids argument

: so2a GET-ORDER get-orderlist SET-ORDER ; \  To recover search order
: so2 0 SET-ORDER so2a ;

{ so2 -> 0 }         \ 0 set-order leaves an empty search order

: so3 -1 SET-ORDER so2a ;
: so4 ONLY so2a ;

{ so3 -> so4 }       \ -1 SET-ORDER = ONLY

\ --------------------------------------------------------------------

Testing DEFINITIONS PREVIOUS

{ ONLY FORTH DEFINITIONS -> }
{ GET-CURRENT -> FORTH-WORDLIST }
{ GET-ORDER wid2 @ SWAP 1+ SET-ORDER DEFINITIONS GET-CURRENT -> wid2 @ }
{ GET-ORDER -> get-orderlist wid2 @ SWAP 1+ }
{ PREVIOUS GET-ORDER -> get-orderlist }
{ DEFINITIONS GET-CURRENT -> forth-wordlist }

\ --------------------------------------------------------------------

Testing SEARCH-WORDLIST WORDLIST FIND

ONLY FORTH DEFINITIONS
VARIABLE xt  ' DUP xt !
VARIABLE xti ' .( xti !    \ Immediate word

{ S" DUP" wid1 @ SEARCH-WORDLISt -> xt  @ -1 }
{ S" .("  wid1 @ SEARCH-WORDLIST -> xti @  1 }
{ S" DUP" wid2 @ SEARCH-WORDLIST ->        0 }

: c"dup" C" DUP" ;
: c".("  C" .(" ;
: c"x" C" unknown word"  ;

{ c"dup" FIND -> xt  @ -1 }
{ c".("  FIND -> xti @  1 }
{ c"x"   FIND -> c"x"   0 }

\ --------------------------------------------------------------------

Testing new definitions are put into the correct wordlist

: alsowid2 ALSO GET-ORDER wid2 @ ROT DROP SWAP SET-ORDER ;
alsowid2
: w1 1234  ;
DEFINITIONS
: w1 -9876 ; IMMEDIATE

ONLY FORTH
{ w1 -> 1234 }
DEFINITIONS
{ w1 -> 1234 }
alsowid2
{ w1 -> -9876 }
DEFINITIONS
{ w1 -> -9876 } 

ONLY FORTH DEFINITIONS

: so5  DUP IF SWAP EXECUTE THEN ;

{ S" w1" wid1 @ SEARCH-WORDLIST so5 -> -1  1234 }
{ S" w1" wid2 @ SEARCH-WORDLIST so5 ->  1 -9876 }

: c"w1" C" w1" ;
{ alsowid2 c"w1" FIND so5 ->  1 -9876 }
{ previous c"w1" FIND so5 -> -1  1234 }

\ --------------------------------------------------------------------

Testing ORDER  \ Should display search order and compilation wordlist

cr .( ONLY FORTH DEFINITIONS search order and compilation list) cr
{ ONLY FORTH DEFINITIONS ORDER -> }

cr .( Plus another unnamed wordlist at the head of the search order) cr
{ alsowid2 DEFINITIONS ORDER -> }

\ --------------------------------------------------------------------

CR .( End of Search Order word tests) CR

ONLY FORTH DEFINITIONS		\ Leave search order in the standard state
