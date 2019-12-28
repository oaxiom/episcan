
from glbase3 import *

annot = genelist(filename='../gencode/hs_map.tsv', format={'force_tsv': True, 'engs': 0, 'ensp': 1, 'hgncid': 3, 'name': 2})

# trim the HNNC: from the ENSP accession
newl = []
for i in annot:
    if i['ensp'] and i['hgncid']: # i.e. remove the non-coding 
        i['hgncid'] = int(i['hgncid'].split(':')[1])
        newl.append(i)
annot = genelist()
annot.load_list(newl)
print(annot)
annot.save('annot.glb')



