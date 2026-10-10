\ To test the ANS Forth Double-Number word set and double number extensions

\ Copyright (C) Gerry Jackson 2006, 2007

\ This program is free software; you can redistribute it and/or
\ modify it any way.

\ This program is distributed in the hope that it will be useful,
\ but WITHOUT ANY WARRANTY; without even the implied warranty of
\ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

\ The tests are not claimed to be comprehensive or correct 

\ --------------------------------------------------------------------
\ Version 0.3   20 April 2007 ANS Forth words changed to upper case
\         0.2   30 Oct 2006 Updated following GForth test to include
\               various constants from core.fr
\         0.1   Oct 2006 First version released

\ --------------------------------------------------------------------
\ The tests are based on John Hayes test program for the core word set
\ and requires those files to have been loaded

\ Words tested in this file are:
\     D+ D- D0< D0= D2* D2/ D< D= 2CONSTANT 2LITERAL 2VARIABLE
\     DMAX DMIN D>S DABS DNEGATE D. D.R M* M+ 2ROT DU<

\ --------------------------------------------------------------------
\ Assumptions and dependencies:
\     - tester.fr has been included prior to this file
\ --------------------------------------------------------------------
\ Constant definitions copied from core.fr

0 INVERT 1 RSHIFT        CONSTANT max-int
0 INVERT 1 RSHIFT INVERT CONSTANT min-int
0 INVERT 1 RSHIFT        CONSTANT mid-uint
0 INVERT 1 RSHIFT INVERT CONSTANT mid-uint+1
0 INVERT CONSTANT 1s
1s 1 RSHIFT INVERT CONSTANT msb
0  CONSTANT <false>
1s CONSTANT <true>

\ --------------------------------------------------------------------
Testing Double-Number word set

DECIMAL

Testing D+ with simple small integers

{  0 S>D  5 S>D D+ ->  5  0 }
{  5 S>D  0 S>D D+ ->  5  0 }
{  0 S>D -5 S>D D+ -> -5 -1 }
{ -5 S>D  0 S>D D+ -> -5 -1 }
{  1 S>D  2 S>D D+ ->  3  0 }
{  1 S>D -2 S>D D+ -> -1 -1 }
{ -1 S>D  2 S>D D+ ->  1  0 }
{ -1 S>D -2 S>D D+ -> -3 -1 }
{ -1 S>D  1 S>D D+ ->  0  0 }

testing D+ with mid range integers

{  0  0  0  5 D+ ->  0  5 }
{ -1  5  0  0 D+ -> -1  5 }
{  0  0  0 -5 D+ ->  0 -5 }
{  0 -5 -1  0 D+ -> -1 -5 }
{  0  1  0  2 D+ ->  0  3 }
{ -1  1  0 -2 D+ -> -1 -1 }
{  0 -1  0  2 D+ ->  0  1 }
{  0 -1 -1 -2 D+ -> -1 -3 }
{ -1 -1  0  1 D+ -> -1  0 }

{ min-int 0 2DUP D+ -> 0 1 }
{ min-int S>D min-int 0 D+ -> 0 0 }

testing D+ with large double integers

{ 1s mid-uint 1 S>D D+ -> 0 mid-uint+1 }
{ 1 S>D 1s mid-uint D+ -> 0 mid-uint+1 }
{ min-int max-int min-int 0 D+ -> 0 min-int }
{ min-int max-int 2DUP D+ -> 0 1s }

: dbl1 1234567890123456789. ;
: dbl2 4321098765432109876. ;
: dbl3 -2345678901234567890. ;
: dbl4 -6543210987654321098. ;

{ dbl1 dbl2 D+ ->  5555666655555566665. }
{ dbl2 dbl1 D+ ->  5555666655555566665. }
{ dbl2 dbl3 D+ ->  1975419864197541986. }
{ dbl3 dbl2 D+ ->  1975419864197541986. }
{ dbl1 dbl3 D+ -> -1111111011111111101. }
{ dbl3 dbl1 D+ -> -1111111011111111101. }
{ dbl3 dbl4 D+ -> -8888889888888888988. }
{ dbl4 dbl3 D+ -> -8888889888888888988. }

\ --------------------------------------------------------------------

Testing D- with small integers

{  0 S>D  5 S>D D- -> -5. }
{  5 S>D  0 S>D D- ->  5. }
{  0 S>D -5 S>D D- ->  5. }
{ -5 S>D  0 S>D D- -> -5. }
{  1 S>D  2 S>D D- -> -1. }
{  1 S>D -2 S>D D- ->  3. }
{ -1 S>D  2 S>D D- -> -3. }
{ -1 S>D -2 S>D D- ->  1. }
{  0 S>D  1 S>D D- -> -1. }

Testing D- with mid-range integers

{  0  0  0  5 D- ->  0 -5 }
{ -1  5  0  0 D- -> -1  5 }
{  0  0 -1 -5 D- ->  1  4 }
{  0 -5  0  0 D- ->  0 -5 }
{ -1  1  0  2 D- -> -1 -1 }
{  0  1 -1 -2 D- ->  1  2 }
{  0 -1  0  2 D- ->  0 -3 }
{  0 -1  0 -2 D- ->  0  1 }
{  0  0  0  1 D- ->  0 -1 }

{ min-int 0 2DUP D- -> 0. }
{ min-int S>D mid-uint 0 D- -> 1 1s }

Testing D- with large integers

{ 0 mid-uint+1 0 1 D- -> 0 mid-uint }
{ 0. 1s mid-uint   D- -> 1 mid-uint+1 }
{ 0 min-int min-int 0 D- -> min-int max-int }
{ min-int min-int max-int max-int D- -> 1 1 }
{ 0 mid-uint+1 0 1 D- -> 0 mid-uint }

{ dbl2 dbl1 D- ->  3086530875308653087. }
{ dbl1 dbl2 D- -> -3086530875308653087. }
{ dbl1 dbl3 D- ->  3580246791358024679. }
{ dbl3 dbl1 D- -> -3580246791358024679. }
{ dbl4 dbl3 D- -> -4197532086419753208. }
{ dbl3 dbl4 D- ->  4197532086419753208. }

\ --------------------------------------------------------------------

Testing D0< D0=

{ 1. D0< -> <false> }
{ min-int 0 D0< -> <false> }
{ 0 max-int D0< -> <false> }
{ -1 max-int D0< -> <false> }
{ 0. D0< -> <false> }
{ -1. D0< -> <true> }
{ 0 min-int D0< -> <true> }

{ 1. D0= -> <false> }
{ min-int 0 D0= -> <false> }
{ 0 max-int D0= -> <false> }
{ -1 max-int D0= -> <false> }
{ 0. D0= -> <true> }
{ -1. D0= -> <false> }
{ 0 min-int D0= -> <false> }

\ --------------------------------------------------------------------

Testing D2* D2/

{ min-int 0 D2* -> 0 1 }
{ 1s max-int 1 RSHIFT D2* -> -2 max-int }
{ min-int DUP D2* -> 0 1 }

{ 0 1 D2/ -> min-int 0 }
{ 1s DUP D2/ -> 1s DUP }
{ 1s 1 XOR 1s D2/ -> 1s 1s }
{ 0 msb D2/ msb AND -> 0 msb }

\ --------------------------------------------------------------------

Testing D< D=

{ 0. 1. D< -> <true> }
{ 0. 0. D< -> <false> }
{ 1. 0. D< -> <false> }
{ -1. 1. D< -> <true> }
{ -1. 0 max-int D< -> <true> }
{ max-int min-int 0 min-int 1+ D< -> <true> }
{ 0 max-int 1- 0 max-int D< -> <true> }
{ 0 min-int 1s max-int D< -> <true> }

{ -1. -1. D= -> <true>  }
{ -1.  0. D= -> <false> }
{ -1.  1. D= -> <false> }
{  0. -1. D= -> <false> }
{  0.  0. D= -> <true>  }
{  0.  1. D= -> <false> }
{  1. -1. D= -> <false> }
{  1.  0. D= -> <false> }
{  1.  1. D= -> <true>  }

{ 0 -1 0 -1 D= -> <true>  }
{ 0 -1 0  0 D= -> <false> }
{ 0 -1 0  1 D= -> <false> }
{ 0  0 0 -1 D= -> <false> }
{ 0  0 0  0 D= -> <true>  }
{ 0  0 0  1 D= -> <false> }
{ 0  1 0 -1 D= -> <false> }
{ 0  1 0  0 D= -> <false> }
{ 0  1 0  1 D= -> <true>  }

{ 0  max-int 0 min-int D= -> <false> }
{ 0  max-int 0 0 D= -> <false> }
{ 0  max-int 0 max-int D= -> <true> }
{ 1s max-int 0 max-int D= -> <false> }
{ 1s max-int 0 min-int D= -> <false> }
{ 0 min-int  0 min-int D= -> <true> }
{ 0 min-int 1s min-int D= -> <false> }
{ 0 min-int 1s max-int D= -> <false> }

\ --------------------------------------------------------------------

Testing 2CONSTANT 2LITERAL 2VARIABLE

{ 1111 2222 2CONSTANT 2c1 -> }
{ 2c1 -> 1111 2222 }
{ : cd1 2c1 ; -> }
{ cd1 -> 1111 2222 }
{ : cd2 2CONSTANT ; -> }
{ dbl1 cd2 2c2 -> }
{ 2c2 -> dbl1 }
{ : cd3 [ dbl2 ] 2LITERAL ; -> }
{ cd3 -> dbl2 }
{ 2VARIABLE 2v1 -> }
{ 2c1 2v1 2! -> }
{ 2v1 2@ -> 2c1 }
{ : cd3 2VARIABLE ; -> }
{ cd3 2v2 -> }
{ : cd4 2v2 2! ; -> }
{ dbl2 cd4 -> }
{ 2v2 2@ -> dbl2 }

\ --------------------------------------------------------------------

Testing DMAX DMIN

{ dbl1 dbl2 DMAX -> dbl2 }
{ dbl2 dbl1 DMAX -> dbl2 }
{ dbl1 dbl1 DMAX -> dbl1 }
{ dbl1 dbl2 DMIN -> dbl1 }
{ dbl2 dbl1 DMIN -> dbl1 }
{ dbl1 dbl1 DMIN -> dbl1 }

{ dbl3 dbl4 DMAX -> dbl3 }
{ dbl4 dbl3 DMAX -> dbl3 }
{ dbl3 dbl3 DMAX -> dbl3 }
{ dbl3 dbl4 DMIN -> dbl4 }
{ dbl4 dbl3 DMIN -> dbl4 }
{ dbl3 dbl3 DMIN -> dbl3 }

{ dbl1 dbl3 DMAX -> dbl1 }
{ dbl3 dbl1 DMAX -> dbl1 }
{ dbl1 dbl3 DMIN -> dbl3 }
{ dbl3 dbl1 DMIN -> dbl3 }

{ -1 max-int 0 min-int DMAX -> -1 max-int }
{ -1 max-int 0 min-int DMIN ->  0 min-int }

\ --------------------------------------------------------------------

Testing D>S DNEGATE DABS

{  1234  0 D>S ->  1234 }
{ -1234 -1 D>S -> -1234 }
{ max-int  0 D>S -> max-int }
{ min-int -1 D>S -> min-int }

{ dbl1 DNEGATE dbl1 D+ -> 0 0 }
{ dbl3 DNEGATE dbl3 D+ -> 0 0 }
{ 0  1 DNEGATE -> 0 -1 }
{ 0 -1 DNEGATE -> 0 1 }

{ dbl1 DABS -> dbl1 }
{ dbl3 DABS -> dbl3 DNEGATE }


\ --------------------------------------------------------------------

Testing D. D.R

{ : DoubleOutput
	CR ." You should see lines duplicated:" CR
	5 SPACES ." 1234567890123456789"       CR 5 SPACES dbl1 D. CR
	5 SPACES ."    1234567890123456789"    CR 5 SPACES dbl1 22 D.R CR
	5 SPACES ." -2345678901234567890"      CR 5 SPACES dbl3 D. CR
	5 SPACES ."      -2345678901234567890" CR 5 SPACES dbl3 25 D.R CR
	CR
; -> }

{ DoubleOutput -> }

\ --------------------------------------------------------------------

Testing M*/ M+

{ dbl1  1 M+ -> dbl1  1. D+ }
{ dbl1 -1 M+ -> dbl1 -1. D+ }
{ dbl3  1 M+ -> dbl3  1. D+ }
{ dbl3 -1 M+ -> dbl3 -1. D+ }

{ 4153874092166845345. 2CONSTANT dp1 -> }
{ 98656350292512810.   2CONSTANT dp2 -> }
{ dp1          234567 9876321 M*/ -> dp2         }
{ dp1 DNEGATE  234567 9876321 M*/ -> dp2 DNEGATE }
{ dp1 DNEGATE -234567 9876321 M*/ -> dp2         }
{ dp1         -234567 9876321 M*/ -> dp2 DNEGATE }

\ --------------------------------------------------------------------

Testing 2ROT DU<

{ dbl1 dbl2 dbl3 2ROT -> dbl2 dbl3 dbl1 }

{ dbl1 dbl1 DU< -> <false> }
{ dbl1 dbl2 DU< -> <true> }
{ dbl2 dbl1 DU< -> <false> }
{ dbl3 dbl3 DU< -> <false> }
{ dbl3 dbl4 DU< -> <false> }
{ dbl4 dbl3 DU< -> <true> }
{ 0 min-int 0 min-int DU< -> <false> }
{ 0 min-int 0 min-int 1. D+ DU< -> <true> }
{ 0 min-int 1. D+ 0 min-int DU< -> <false> }

\ --------------------------------------------------------------------

CR .( End of Double-Number word tests) CR

