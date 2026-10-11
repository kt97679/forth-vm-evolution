\ tabs.fth - a tab is a space to the parser and itself in a string (Iteration 145):
\ SKIP and SCAN take any control character for a space delimiter, and no tab
\ is made a space. Every line's answer differs from what converting gave.
	1	2	+ . CR
: TT	DUP	* ;	5 TT . CR
S" a	b" SWAP DROP . CR
S" a	b" DROP 1+ C@ . CR
S" 7	8	*" EVALUATE . CR
CHAR	A . CR
1	\ a comment after a tab
. CR
