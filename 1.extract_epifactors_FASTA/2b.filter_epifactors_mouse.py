#!/usr/bin/env python3
import sys, os
from glbase3 import *
user_path = os.path.expanduser("~")

form = {'force_tsv': False, 'mgiid': 10}

# extract the list of domains
epifactors_mm10 = genelist(filename='EpiGenes_main.csv', format=form)

# First, fix the name key, which is wrong in the EpiGenes table
annot = glload('../gencode/mm_annot.glb')

print(epifactors_mm10)
print(annot)

epifactors_mm10 = epifactors_mm10.map(genelist=annot, key='mgiid')

# These are just to get hte FASTA peptide files
epifactors_mm10_unfiltered = epifactors_mm10.removeDuplicates('ensp')
epifactors_mm10_unfiltered.saveTSV('hs_epifactors.unfiltered.tsv', key_order=['ensp', 'name'])
epifactors_mm10_unfiltered.save('hs_epifactors.unfiltered.glb')

start_len = len(epifactors_mm10)

# Also filter kinases and phosphatases
filt = [ # Must be a literal match:
    '#',
    'ACTB',
    'ACTL6A', 'ACTL6B', 'ACTR3B',
    'ACTR5', 'ACTR6', 'ACTR8',
    'AIRE',
    'ADNP',
    'AEBP2', 'APEX1','ARRB1',
    'ARNTL',
    'ANKRD32',
    'ATF2',
    'ATM',
    'ATR',
    'AURKA', 'AURKB', 'AURKC',
    'BUB1', 'BCKDK',
    'C17orf49', # MYB TF
    'CDK1', 'CDK2', 'CDK3', 'CDK5', 'CDK7', 'CDK9', 'CDK17', 'CDC6',
    'CENPC',
    'CHEK1',
    'CHUK',
    'CIT',
    'CSNK2A1', 'CRB2',
    'CTCF', 'CTCFL', 'CLNS1A',
    'DAPK3','DDX50', 'DPPA3', 'DDB2',
    'DPF1',
    'DND1',
    'E2F6',
    'ELP5',
    'ENY2', # A TF
    'ERBB4', # Kinase
    'EXOSC1', 'EXOSC2', 'EXOSC3', 'EXOSC4', 'EXOSC5', 'EXOSC6', 'EXOSC7', 'EXOSC8', 'EXOSC9',
    'FBL', 'FBRS', 'FBRSL1',
    'FOXA1', 'FOXO1', 'FOXP1', 'FOXP2', 'FOXP3', 'FOXP4',
    'GFI1', 'GFI1B', 'GATAD1',
    'GSG2',
    'HLCS', 'HASPIN',
    'HDGFL2', 'HMGB1', 'HINFP',
    'HIF1AN',
    'HSPA1A', 'HSPA1B',
    'IKZF1','IKZF3',
    'JAK2', 'JDP2',
    'MAX', 'MAZ',
    'MAP3K7', 'MAPKAPK3', 'MASTL', 'MYO1C', # Myosin?
    'MGA', 'MST1',
    'MYSM1',
    'NAP1L4',
    'NEK6', 'NEK9', 'NEK8',
    'NFYC',
    'PARG',
    'PAK2', 'PBK', 'PDP1', 'PDK1', 'PDK2', 'PDK3', 'PDK4', 'PKM', 'PKN1',
    'PIWIL4', 'PRR14',
    'POGZ',
    'PPM1G', 'PPP2CA', 'PPP4C',
    'PRKAA1', 'PRKAA2', 'PRKAB1', 'PRKAB2', 'PRKAG1', 'PRKAG2', 'PRKAG3', 'PRKCA', 'PRKCB', 'PRKCD', 'PRKDC',
    'PRPF31',
    'PSIP1',
    'RAG2',
    'RAI1',
    'RARA',
    'RB1',
    'RCC1',
    'RPS6KA3', 'RPS6KA4' ,'RPS6KA5',
    'REST',
    'SENP3', 'SENP1', 'SRSF3',
    'SKP1', 'STK4', 'STK31',
    'SF3B1', 'SF3B3', # Splicesomal member
    'SMEK1', 'SMEK2',
    'SFMBT2',
    'SFPQ',
    'SRCAP',
    'SNAI1', 'SNAI2',
    'SP1',
    'TAF2', 'TAF4', 'TAF6', 'TAF9', 'TAF12', 'TAF6L', 'TAF7', 'TAF9B',
    'TTBK1', 'TLK1', 'TLK2', 'TSSK6', 'TRRAP', 'TTK',
    'TFDP1',
    'UBE2A', 'UBE2B', 'UBE2D1','UBE2E1','UBE2H','UBE2N','UBE2D3', 'UBE2T', 'UBR7', # UB system;
    'USP12', 'USP17L2',
    'USP21', 'USP22', 'USP3', 'USP46', 'USP49', 'USP7',
    'UBR2', 'UBR5', 'USP11',
    'USP16',
    'USP44',
    'WSB2',
    'YWHAE', 'YY1',
    'VRK1',
    'ZCWPW1', 'ZFP57', 'ZMYM3', 'ZMYND8', 'ZNF516',
    'ZNF217', 'ZNF532', 'ZNF592', 'ZNF687', 'ZNF711',
    'ZHX1', 'ZMYM2',
    ]

# Do a simple convert from the human to mouse;
newfilt = []
for i in filt:
    newfilt.append(i[0] + i[1:].lower())
filt = newfilt

newe = []
for e in epifactors_mm10:
    if True not in [f == e['name'] for f in filt]:
        newe.append(e)

epifactors_mm10.load_list(newe)

# These are just to get hte FASTA peptide files
epifactors_mm10 = epifactors_mm10.removeDuplicates('ensp')
epifactors_mm10.saveTSV('mm_epifactors.all.tsv', key_order=['ensp', 'name'])
epifactors_mm10.save('mm_epifactors.all.glb')

# These are the more useful human-readable versions, unqique for hgncid
epifactors_mm10 = epifactors_mm10.removeDuplicates('mgiid')
end_len = len(epifactors_mm10)
epifactors_mm10.sort('name')
epifactors_mm10.saveTSV('mm_epifactors.readable.tsv', key_order=['mgiid', 'ensp', 'name'])
#epifactors_mm10.save('hs_epifactors.filtered.glb')

print('%s -> %s (cut %s)' % (start_len, end_len, start_len - end_len))

