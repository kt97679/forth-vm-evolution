\ The harness's words the kernel lacks (Iteration 124), for tester.fr,
\ utilities.fth, errorreport.fth and coreplustest's helpers - not the words
\ under test. Core words only; TRUE is the kernel's.
: FALSE 0 ;
: .( [CHAR] ) PARSE TYPE ; IMMEDIATE
: NIP SWAP DROP ;
: TUCK SWAP OVER ;
: 2>R R> ROT ROT SWAP >R >R >R ;
: 2R> R> R> R> SWAP ROT >R ;
: 2R@ R> R> R> 2DUP >R >R SWAP ROT >R ;
