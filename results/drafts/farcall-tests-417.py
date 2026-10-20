fill = ''.join(': F%02d %d ;  49152 ALLOT\n' % (i, i) for i in range(100))
pre = ': A0 1 ;\n3000000 ALLOT\n: B1 A0 1+ ;\n'
P = {'big1': (': A0 1 ;\n: MK CREATE , DOES> @ 1+ ;\nVARIABLE V0  5 V0 !\n' + fill + ": B1 A0 1+ ;\n: B2 B1 B1 + ;\n7 MK C7\n: B3 C7 V0 @ + ;\n"
              "VARIABLE V1  42 V1 !\n: B4 V1 @ B2 + ;\n' B4 CONSTANT XT4\n: B5 XT4 EXECUTE 1+ ;\n: B6 B5 B3 + F50 + F99 + ;\nB6 . CR\nBYE\n", '209'),
     'big2': (fill + ': MK2 CREATE , DOES> @ 2 + ;\n3 MK2 D3\nD3 . CR\nBYE\n', '5'),
     'plus3': (pre + ': B2 B1 3 + ;\nB2 . CR\nBYE\n', '5'), 'two': (pre + ': B2 B1 B1 + ;\nB2 . CR\nBYE\n', '4'),
     'swap': (pre + ': B2 B1 3 SWAP ;\nB2 . . CR\nBYE\n', '2 3')}
import json; json.dump({k: v for k, v in P.items()}, open('/tmp/tr/progs.json', 'w'))
