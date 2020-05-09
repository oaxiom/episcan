
'''

Inspect some specific examples to see why they are failing

'''

import os
from glbase3 import *

todo = [
    'EED', # No good domains
    'SUZ12',
    'ASH2L',
    'ATF7IP',
    'BAP1',
    'CHAF1B',
    'SET',
    'TET2',
    'TEX10',
    ]

unfiltered_auc = glload('../AUCtable_raw.glb')

for gene in todo:
    print(gene)
    os.system("grep {0} ../../2.determine_reqd_models/pfam.txt | tr -s ' ' | cut -f 4 -d ' ' | sort | uniq > temp.txt".format(gene))

    data = genelist('temp.txt', format={'force_tsv': True, 'domain': 0, 'skiplines': -1})

    data = data.map(genelist=unfiltered_auc, key='domain')
    data.sort('TP/FP ratio')
    data.reverse()
    data.saveTSV('models_ann_{0}.tsv'.format(gene))

os.remove('temp.txt')
