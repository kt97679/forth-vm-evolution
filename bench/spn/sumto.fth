\ A counted loop over stack arithmetic: n + (n-1) + ... + 1.
S" ../forth/spn.4" INCLUDED
: SUMTO ( n --- s )
  0 SWAP BEGIN SWAP OVER + SWAP -1 + DUP 0 = UNTIL DROP ;
' SUMTO TRANSLATE CONSTANT SUMTO-N
1000 SUMTO . 1000 SUMTO-N SPN-CALL . CR
