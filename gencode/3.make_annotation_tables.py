
from glbase3 import *

annot = genelist(filename='hs_map.tsv', format={'force_tsv': True, 'ensg': 0, 'ensp': 1, 'hgncid': 3, 'name': 2})

# trim the HNNC: from the ENSP accession
newl = []
for i in annot:
    if i['ensp'] and i['hgncid']: # i.e. remove the non-coding
        i['hgncid'] = int(i['hgncid'].split(':')[1])
        newl.append(i)
annot = genelist()
annot.load_list(newl)
print(annot)
annot.save('hs_annot.glb')



annot = genelist(filename='mm_map.tsv', format={'force_tsv': True, 'ensg': 0, 'ensp': 1, 'mgiid': 3, 'name': 2})

# trim the HNNC: from the ENSP accession
newl = []
for i in annot:
    if i['ensp'] and i['mgiid']: # i.e. remove the non-coding
        i['mgiid'] = int(i['mgiid'].split(':')[1])
        newl.append(i)
annot = genelist()
annot.load_list(newl)
print(annot)
annot.save('mm_annot.glb')



