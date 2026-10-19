# Iteration 416: two programs past 4 MB of dictionary - calls across it, a DOES> child far from its defining word, a
# variable, EXECUTE (big1: 209 expected); and a DOES> defining word itself past 4 MB (big2: 5 expected).
import sys
fill = ''.join(': F%02d %d ;  49152 ALLOT\n' % (i, i) for i in range(100))   # 100 x 48 KB: 4.9 MB, no gap past 4 MB
big1 = (': A0 1 ;\n: MK CREATE , DOES> @ 1+ ;\nVARIABLE V0  5 V0 !\n' + fill +
        ': B1 A0 1+ ;\n: B2 B1 B1 + ;\n7 MK C7\n: B3 C7 V0 @ + ;\nVARIABLE V1  42 V1 !\n: B4 V1 @ B2 + ;\n'
        "' B4 CONSTANT XT4\n: B5 XT4 EXECUTE 1+ ;\n: B6 B5 B3 + F50 + F99 + ;\nB6 . CR\nBYE\n")
big2 = fill + ': MK2 CREATE , DOES> @ 2 + ;\n3 MK2 D3\nD3 . CR\nBYE\n'
open(sys.argv[1] + '/big1.fth', 'w').write(big1); open(sys.argv[1] + '/big2.fth', 'w').write(big2)
