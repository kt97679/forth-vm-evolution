# The cross compiler's fused branches on designs that use them all (Iteration 723)

722 put =I?BRANCH and DUP?NBRANCH into forth/cross-cv8.4 and portable-fastest d727605472 self-hosts with them - but
its DUP?NBRANCH never fires (sod16.py's keepbranch takes DUP before the fused 0= ?BRANCH, and the design has no
?NBRANCH), and it has neither short form. Three variants of its record (results/drafts/selfhost-variants-723.sh):
pfv-nq + ?NBRANCH; pfv-short + ?NBRANCH, DUP?NBRANCH8, =I?BRANCH8; pfv-nodn + ?NBRANCH - DUP?NBRANCH (a control).

**Self-hosting**: all three PASS at both widths through results/drafts/selfhost-ids-714.sh (A = B, the gate, the
run-time compiler's tables and the five programs' code the translator's).

| cells | | pfv-nq | pfv-short | pfv-nodn |
|---|---|---|---|---|
| 8 | translator T / cross A (B) | 10,264 / 9,977 | 10,241 / 9,938 | 10,256 / 9,977 |
| 4 | translator T / cross A (B) | 9,600 / 9,337 | 9,585 / 9,314 | 9,604 / 9,341 |

Sizes alone do not show the rewrites firing: an operation more or less in ops10 moves the tag-2 map, and bytes with it
(at 8-byte cells the translator's nodn - nq is -8, no count of sites; at 4 both say 4 DUP?NBRANCH sites).

**Dispatches** (results/drafts/fusedcount-723.py: the export's engine with -DPROFILE=1, by each fused branch's one-byte
code; T the translator's image, A the cross compiler's; outputs the same):

| variant | workload | =I?BRANCH(8) T / A | DUP?NBRANCH(8) T / A | ?NBRANCH T / A | all dispatches T / A |
|---|---|---|---|---|---|
| pfv-nq (long forms) | kernel | 2,949 / 4,811 | 951 / 903 | 3,976 / 3,865 | 1,797,938 / 1,779,279 |
| | corpus | 8,601 / 15,531 | 3,127 / 2,887 | 14,090 / 13,875 | 4,232,712 / 4,198,096 |
| pfv-short (short forms; the long ones 0 in both) | kernel | 2,949 / 4,811 | 951 / 903 | 3,976 / 3,865 | 1,797,561 / 1,778,902 |
| | corpus | 8,601 / 15,531 | 3,127 / 2,887 | 14,090 / 13,875 | 4,231,737 / 4,197,126 |

Every fused form fires in the self-built images, the short ones wherever the design has them. DUP?NBRANCH and
?NBRANCH run within 8 % of the translator's; =I?BRANCH runs 1.6-1.8 times as often in A - the cross compiler's earlier
passes leave more EQI n ?BRANCH to fuse than the translator's (not traced to the words); A dispatches 0.8-1.0 % fewer
in all, outputs the same, the gate passed.

**After chain D's rebuild rehearsed** (results/drafts/rebuild-rehearsal-723.sh): small-jit=15eda54ebd through
roles-build-718.sh's two phases in a scratch clone, now that all ten ship self-built - PASS: every file git has in
designs/small-jit the export's byte for byte (genes.4's first line apart, a comment naming the export's path from the
tree), make test 11 ok, make selfhost 20 of 20, make 32, libc, the package's lines right. roles-build's own "designs/
against the export: ... differ" line counts the export's untracked binaries and that comment - the rehearsal's check is
the one to read. 721's chainD-rehearsal-721.sh could not run: chain C's archive is not on this machine (it covers
process-followup.sh, which no self-hosting change touches).
