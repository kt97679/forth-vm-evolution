# Locals ({: (LOCAL) TO) without a kernel hook (Iteration 193)

The question put to the owner - a hook in the kernel's name lookup for
locals - is not needed. The kernel's FIND (kernel.4 line 965) already walks
the search order: CONTEXT's wordlists, each by SEARCH-WORDLIST. A wordlist of
the current definition's local names, first in the search order while it
compiles, is found by the ordinary interpreter - before the global words and
before number conversion, as the standard asks ("local names supersede global
names and numbers"). What forth/locals.4 avoided - headers in the middle of a
definition's code - is avoided another way: the local names' headers go into
a scratch area, with HERE, LAST and CURRENT saved and restored around them.

## The prototype, on a built tag-2 design (oc-fix-9586059a75, the batch's tree)

    WORDLIST CONSTANT LWL  CREATE LNAMES 2048 ALLOT  VARIABLE LNP  LNAMES LNP !
    : LOCAL-WORD ( i "name" -- )  CREATE , IMMEDIATE DOES> @ POSTPONE LITERAL ;
    \ MAKE-LOCAL ( i c-addr u -- ): HERE, LAST, CURRENT saved; HERE := the scratch
    \ area, CURRENT := LWL; EVALUATE "LOCAL-WORD name"; all three restored
    : TESTL [ 42 S" ZZ" MAKE-LOCAL  GET-ORDER LWL SWAP 1+ SET-ORDER ] ZZ 1+ ;
    GET-ORDER NIP 1- SET-ORDER

TESTL gives 43; ZZ afterwards is an undefined word; a definition made after it
works and TESTL still runs - the dictionary and LAST intact.

## The design (coreext.4, the eleventh wave)

- Run time: a locals stack (LP, growing down). (LENTER) ( x1..xk k n -- ): n
  cells reserved, all 0, the k initialized ones popped in (the last declared
  takes the top); (L@) ( i -- x ), (L!) ( x i -- ), (LEXIT) ( n -- ).
- Compile time: #LOCALS and #LINIT; a local name is an IMMEDIATE word in LWL,
  made in the scratch area (EVALUATE in interpret state), compiling i (L@).
  (LOCAL) ( c-addr u -- ): a name declares one, initialized; u 0 compiles the
  entry. {: parses names, | then uninitialized ones, -- skipped to :}.
- The scope's end - ; and DOES> redefined (DOES> ends the defining part's
  locals; its own part may declare new ones), EXIT immediate while locals are
  active: compile n (LEXIT), pop LWL, empty its threads, reset the scratch.
- TO: a local first (SEARCH-WORDLIST in LWL), compiling i (L!); else >IN put
  back and the old TO.
- localstest asks also: :NONAME, recursion (LAST restored, so RECURSE calls
  the definition), 16 locals, two definitions with the same local names.

Next: build it, localstest on s6, the held-out check on the front.
