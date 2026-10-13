#!/bin/sh
cd /tmp/b44s
{ echo "== reseed"; runuser -u claude -- sh tools/reseed.sh 2>&1 | tail -3; echo "exit $?"; } > /tmp/j24.log 2>&1
{ echo "== build"; runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh 2>&1 | tail -2; } >> /tmp/j24.log 2>&1
{ echo "== s6 by hand"; cd build/work 2>/dev/null || cd build; printf '1 0 / 7 . CR\n: T 1 0 / ; '"'"' T CATCH . CR\n: U 5 0 MOD ; '"'"' U CATCH . CR\n: V 7 0 0 UM/MOD ; '"'"' V CATCH . CR\n-24 THROW\n-1 THROW\n.( still here) CR\n' | ../s6-cv8b-64 ../s6-cv8b-64.img 2>&1; echo "status $?"; } >> /tmp/j24.log 2>&1
touch /tmp/job24.done
