#!/usr/bin/env python3
from glbase3 import *
user_path = os.path.expanduser("~")

form = {'force_tsv': False, 'uniprot': 6, 'hgncid': 3}

# extract the list of domains
epifactors_hg38 = genelist(filename='EpiGenes_main.20150522.csv', format=form)

# First, fix the name key, which is wrong in the EpiGenes table
annot = genelist(filename='ensp_hgnc_name.txt', format={'force_tsv': True, 'ensp': 0, 'hgncid': 1, 'name': 2}) 

# trim the HNNC: from the ENSP accession
for i in annot:
    if i['ensp'] and i['hgncid']:
        i['hgncid'] = int(i['hgncid'].split(':')[1])
annot._optimiseData()
annot = annot.removeDuplicates('ensp') # remove the ' ' entries
annot.save('annot.glb')

print(epifactors_hg38)
print(annot)

epifactors_hg38 = epifactors_hg38.map(genelist=annot, key='hgncid')

#TFs = glload('all_tfs.glb') # bad ideas as e.g. EP300 is in there 
#DUDEDB = glload('all_dudedb.glb')
start_len = len(epifactors_hg38)
# These two are a bad idea, e.g. KDM2B has an E-box. Best just not to chose these domains.
# These two are a bad idea, e.g. KDM2B has an E-box. Best just not to chose these domains...
# cut known TFs:
#epifactors_hg38 = TFs.map(genelist=epifactors_hg38, key='name', logic='notright')
# cut known UB and DEUB
#epifactors_hg38 = DUDEDB.map(genelist=epifactors_hg38, key='name', logic='notright')

# Also filter kinases and phosphatases
filt = [ # Must be a literal match:   
    '#',
    'ACTB', 
    'ACTL6A', 'ACTL6B', 'ACTR3B',
    'ACTR5', 'ACTR6', 'ACTR8', 
    'ANKRD32',
    'ATM',
    'ATR',
    'AURKA', 'AURKB', 'AURKC',
    'BUB1', 'BCKDK',
    'C17orf49', # MYB TF
    'CDK1', 'CDK2', 'CDK3', 'CDK5', 'CDK7', 'CDK9', 'CDK17',
    'CENPC',
    'CHEK1',
    'CHUK',
    'CIT',
    'CSNK2A1', 
    'CTCF', 'CTCFL', 
    'DAPK3',
    'DND1',
    'ENY2', # A TF
    'ERBB4', # Kinase
    'EXOSC1', 'EXOSC2', 'EXOSC3', 'EXOSC4', 'EXOSC5', 'EXOSC6', 'EXOSC7', 'EXOSC8', 'EXOSC9',
    'FOXA1', 'FOXO1', 'FOXP1', 'FOXP2', 'FOXP3', 'FOXP4',
    'GFI1', 'GFI1B',
    'GSG2',
    'JAK2',    
    'MAP3K7', 'MAPKAPK3', 'MASTL', 'MYO1C', # Myosin?
    'NEK6', 'NEK9', 'NEK8', 
    'PAK2', 'PBK', 'PDP1', 'PDK1', 'PDK2', 'PDK3', 'PDK4', 'PKM', 'PKN1', 
    'PPM1G', 'PPP2CA', 'PPP4C', 
    'PRKAA1', 'PRKAA2', 'PRKAB1', 'PRKAB2', 'PRKAG1', 'PRKAG2', 'PRKAG3', 'PRKCA', 'PRKCB', 'PRKCD', 'PRKDC',
    'RPS6KA3', 'RPS6KA4' ,'RPS6KA5',
    'REST',
    'SKP1', 'STK4', 'STK31',
    'SF3B1', 'SF3B3', # Splicesomal member
    'SMEK1', 'SMEK2',
    'SNAI1',
    'TTBK1', 'TLK1', 'TLK2', 'TSSK6', 'TRRAP', 'TTK',
    'VRK1',    
    ]

newe = []
for e in epifactors_hg38:
    if True not in [f == e['name'] for f in filt]:
        newe.append(e)

epifactors_hg38.load_list(newe)

# These are just to get hte FASTA peptide files
epifactors_hg38 = epifactors_hg38.removeDuplicates('ensp')
epifactors_hg38.saveTSV('epifactors.all.tsv', key_order=['ensp', 'name'])
epifactors_hg38.save('epifactors.all.glb')

# These are the more useful human-readable versions, unqique for hgncid
epifactors_hg38 = epifactors_hg38.removeDuplicates('hgncid')
end_len = len(epifactors_hg38)
epifactors_hg38.sort('name')
epifactors_hg38.saveTSV('epifactors.filtered.tsv', key_order=['uniprot', 'ensp', 'name'])
epifactors_hg38.save('epifactors.filtered.glb')

print('%s -> %s (cut %s)' % (start_len, end_len, start_len - end_len))



