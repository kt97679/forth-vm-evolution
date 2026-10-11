\ paths.fth - the handlers no test ran (Iteration 159, the coverage audit):
\ ALLOCATE RESIZE FREE; the file words - CREATE-FILE WRITE-FILE READ-FILE
\ WRITE-LINE REPOSITION-FILE FILE-POSITION FILE-SIZE CLOSE-FILE DELETE-FILE;
\ SYSCALL.
\ Every answer is a non-negative number on a line of its own.
VARIABLE A  VARIABLE FD  CREATE BUF 64 ALLOT  CREATE BLK 8 CELLS ALLOT
16 ALLOCATE . A ! CR
77 A @ C! A @ 4096 RESIZE . A ! A @ C@ . CR
A @ FREE . CR
S" paths.tmp" R/W CREATE-FILE . FD ! CR
S" hello, file" FD @ WRITE-FILE . CR
S" !" FD @ WRITE-LINE . CR
FD @ CLOSE-FILE . CR
S" paths.tmp" R/O OPEN-FILE . FD ! CR
FD @ FILE-SIZE . . . CR
BUF 5 FD @ READ-FILE . . BUF C@ . BUF 4 + C@ . CR
7 0 FD @ REPOSITION-FILE . CR
FD @ FILE-POSITION . . . CR
BUF 4 FD @ READ-FILE . . BUF C@ . CR
FD @ CLOSE-FILE . S" paths.tmp" DELETE-FILE . CR
\ x86-64's number at both widths, as the shell's: the 32-bit engines translate it.
BLK 39 SYSCALL 0 > 1 AND . CR
: NE <> ; : INV INVERT ;
1 2 NE 1 AND . 5 INV 6 + . CR
