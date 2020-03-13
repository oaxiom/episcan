#!/usr/bin/env python3
import sys, os
from glbase3 import *
user_path = os.path.expanduser("~")

form = {'force_tsv': False, 'uniprot': 6, 'hgncid': 3}

# extract the list of domains
epifactors_hg38 = genelist(filename='EpiGenes_main.csv', format=form)

# First, fix the name key, which is wrong in the EpiGenes table
annot = glload('../gencode/hs_annot.glb')

print(epifactors_hg38)
print(annot)

epifactors_hg38 = epifactors_hg38.map(genelist=annot, key='hgncid')

start_len = len(epifactors_hg38)

# I remove a selection of epifactors that I don't consider as epifactors!
filt = [ # Must be a literal match:
    '#',
    'ACTB',
    'ACTL6A', 'ACTL6B', 'ACTR3B',
    'ACTR5', 'ACTR6', 'ACTR8',
    'ADNP',
    'AEBP2', 'APEX1',
    'ARNTL',
    'ANKRD32',
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
    'CSNK2A1',
    'CTCF', 'CTCFL',
    'DAPK3','DDX50',
    'DPF1',
    'DND1',
    'E2F6',
    'ELP5',
    'ENY2', # A TF
    'ERBB4', # Kinase
    'EXOSC1', 'EXOSC2', 'EXOSC3', 'EXOSC4', 'EXOSC5', 'EXOSC6', 'EXOSC7', 'EXOSC8', 'EXOSC9',
    'FBL',
    'FOXA1', 'FOXO1', 'FOXP1', 'FOXP2', 'FOXP3', 'FOXP4',
    'GFI1', 'GFI1B',
    'GSG2',
    'HLCS',
    'HDGFL2',
    'HIF1AN',
    'HSPA1A', 'HSPA1B',
    'IKZF1',
    'JAK2',
    'MAX', 'MAZ',
    'MAP3K7', 'MAPKAPK3', 'MASTL', 'MYO1C', # Myosin?
    'MGA',
    'MYSM1',
    'NAP1L4',
    'NEK6', 'NEK9', 'NEK8',
    'NFYC',
    'PAK2', 'PBK', 'PDP1', 'PDK1', 'PDK2', 'PDK3', 'PDK4', 'PKM', 'PKN1',
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
    'SENP3',
    'SKP1', 'STK4', 'STK31',
    'SF3B1', 'SF3B3', # Splicesomal member
    'SMEK1', 'SMEK2',
    'SFMBT2',
    'SFPQ',
    'SRCAP',
    'SNAI1', 'SNAI2',
    'TAF2', 'TAF4', 'TAF6', 'TAF9',
    'TTBK1', 'TLK1', 'TLK2', 'TSSK6', 'TRRAP', 'TTK',
    'TFDP1',
    'UBE2D3', 'UBE2T', 'UBR7',
    'USP12', 'USP17L2',
    'USP21', 'USP22', 'USP3', 'USP46', 'USP49', 'USP7',
    'YWHAE', 'YY1',
    'VRK1',
    'ZCWPW1', 'ZFP57', 'ZMYM3', 'ZMYND8', 'ZNF516',
    ]

newe = []
for e in epifactors_hg38:
    if True not in [f == e['name'] for f in filt]:
        newe.append(e)

epifactors_hg38.load_list(newe)

# These are just to get hte FASTA peptide files
epifactors_hg38 = epifactors_hg38.removeDuplicates('ensp')
epifactors_hg38.saveTSV('hs_epifactors.all.tsv', key_order=['ensp', 'name'])
epifactors_hg38.save('hs_epifactors.all.glb')

# These are the more useful human-readable versions, unqique for hgncid
epifactors_hg38 = epifactors_hg38.removeDuplicates('hgncid')
end_len = len(epifactors_hg38)
epifactors_hg38.sort('name')
epifactors_hg38.saveTSV('hs_epifactors.filtered.tsv', key_order=['uniprot', 'ensp', 'name'])
epifactors_hg38.save('hs_epifactors.filtered.glb')

print('%s -> %s (cut %s)' % (start_len, end_len, start_len - end_len))



