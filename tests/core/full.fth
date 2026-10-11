\ full.fth - an ALLOT past the dictionary's room is refused (Iteration 161):
\ it jumped over every guard and wrote past the engine's memory - a crash (gdb:
\ a byte store past the end). HERE stays, and the system goes on.
VARIABLE H  HERE H !
2000000000 ALLOT
HERE H @ = 1 AND . CR
: X 42 ; X . CR
