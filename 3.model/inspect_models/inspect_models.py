
'''

Inspect some specific examples to see why they are failing

'''

import scipy
from glbase3 import *

#grep CHAF1B pfam.txt | tr -s ' ' | cut -f 4 -d ' ' | sort | uniq > chaf1b_models.txt
#grep EED pfam.txt | tr -s ' ' | cut -f 4 -d ' ' | sort | uniq > eed_models.txt

unfiltered_auc = glload('../AUCtable_raw.glb')

chaf1 = genelist('../../2.determine_reqd_models/chaf1b_models.txt', format={'force_tsv': True, 'domain': 0, 'skiplines': -1})
eed = genelist('../../2.determine_reqd_models/eed_models.txt', format={'force_tsv': True, 'domain': 0, 'skiplines': -1})

chaf1 = chaf1.map(genelist=unfiltered_auc, key='domain')
eed = eed.map(genelist=unfiltered_auc, key='domain')

chaf1.saveTSV('chaf1b_models_ann.tsv')
eed.saveTSV('eed_models_ann.tsv')
