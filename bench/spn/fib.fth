\ The same FIB as bench/fib.fth, translated to native code by SPN.
S" ../forth/spn.4" INCLUDED
: FIB ( n1 --- n2 )
  DUP 2 < IF
    DROP 1
  ELSE
    DUP -1 + RECURSE
    SWAP -2 + RECURSE
    +
  THEN ;
' FIB TRANSLATE CONSTANT FIB-N
30 FIB . 30 FIB-N SPN-CALL . CR
