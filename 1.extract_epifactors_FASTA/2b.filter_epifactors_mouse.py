#!/usr/bin/env python3
from glbase3 import *
user_path = os.path.expanduser("~")

form = {'force_tsv': False, 'name': 9} # Approved MGI_symbol

# extract the list of domains
epifactors_mm10 = genelist(filename='EpiGenes_main.20150522.csv', format=form)

# First, fix the name key, which is wrong in the EpiGenes table
annot = genelist(filename='mm_ensp_name.txt', format={'force_tsv': True, 'ensg': 0, 'ensp': 1, 'name': 2}) 

# trim the HNNC: from the ENSP accession
annot = annot.removeDuplicates('ensp') # remove the ' ' entries
annot.save('annot_mm10.glb')

print(epifactors_mm10)
print(annot)

epifactors_mm10 = epifactors_mm10.map(genelist=annot, key='name')

#TFs = glload('all_tfs.glb') # bad ideas as e.g. EP300 is in there 
#DUDEDB = glload('all_dudedb.glb')
start_len = len(epifactors_mm10)
# These two are a bad idea, e.g. KDM2B has an E-box. Best just not to chose these domains.
# These two are a bad idea, e.g. KDM2B has an E-box. Best just not to chose these domains...
# cut known TFs:
#epifactors_hg38 = TFs.map(genelist=epifactors_hg38, key='name', logic='notright')
# cut known UB and DEUB
#epifactors_hg38 = DUDEDB.map(genelist=epifactors_hg38, key='name', logic='notright')

# Also filter kinases and phosphatases
filt = [ # Must be a literal match:   
    '#',
    'Actb', 
    'Actl6a', 'Actl6b', 'Actr3b',
    'Actr5', 'Actr6', 'Actr8', 
    'Ankrd32',
    'Atm',
    'Atr',
    'Aurka', 'Aurkb', 'Aurkc',
    'Bub1','Bckdk',
    '0610010K14Rik', # 'C17orf49' in human # MYB TF
    'Cdk1', 'Cdk2', 'Cdk3-ps', 'Cdk5', 'Cdk7', 'Cdk9', 'Cdk17',
    'Cenpc1',
    'Chek1',
    'Chuk',
    'Cit',
    'Csnk2a1', 
    'Ctcf', 'Ctcfl', 
    'Dapk3',
    'Eny2', # A TF
    'Erbb4', # Kinase
    'Exosc1', 'Exosc2', 'Exosc3', 'Exosc4', 'Exosc5', 'Exosc6', 'Exosc7', 'Exosc8', 'Exosc9',
    'Foxa1', 'Foxo1', 'Foxp1', 'Foxp2', 'Foxp3', 'Foxp4',
    'Gfi1', 'Gfi1b',
    'Gsg2', # A kinase
    'Jak2',    
    'Map3k7', 'Mapkapk3', 
    'Mastl', # A kinase 
    'Myo1c', # Myosin?
    'Nek6', 'Nek8', 'Nek9',
    'Pak2', 'Pbk', 'Pdp1', 'Pdk1', 'Pdk2', 'Pdk3', 'Pdk4', 'Pkm', 'Pkn1', 
    'Ppm1g', 'Ppp2ca', 'Ppp4c', 
    'Prkaa1', 'Prkaa2', 'Prkab1', 'Prkab2', 'Prkag1', 'Prkag2', 'Prkag3', 'Prkca', 'Prkcb', 'Prkcd', 'Prkdc', 
    'Rps6ka3', 'Rps6ka4' ,'Rps6ka5',
    'Rest',
    'Akp1a', # SKP1 in human 
    'Stk4', 'Stk31',
    'Sf3b1', 'Sf3b3', # Splicesomal member
    'Smek1', 'Smek2',
    'Snai2',
    'Ttbk1', 'Tlk1', 'Tlk2', 'Tssk6', 'Trrap', 'Ttk',
    'Vrk1',    
    ]

newe = []
for e in epifactors_mm10:
    if True not in [f == e['name'] for f in filt]:
        newe.append(e)

epifactors_mm10.load_list(newe)

# These are just to get hte FASTA peptide files
epifactors_mm10 = epifactors_mm10.removeDuplicates('ensp')
epifactors_mm10.saveTSV('epifactors_mm10.all.tsv', key_order=['ensp', 'name'])
epifactors_mm10.save('epifactors_mm10.all.glb')

# These are the more useful human-readable versions, unqique for hgncid
epifactors_mm10 = epifactors_mm10.removeDuplicates('name')
end_len = len(epifactors_mm10)
epifactors_mm10.sort('name')
epifactors_mm10.saveTSV('epifactors_mm10.filtered.tsv', key_order=['ensp', 'name'])
epifactors_mm10.save('epifactors_mm10.filtered.glb')

print('%s -> %s (cut %s)' % (start_len, end_len, start_len - end_len))



