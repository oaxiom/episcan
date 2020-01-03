#!/usr/bin/env python3
import sys, os, glob
from glbase3 import *
user_path = os.path.expanduser("~")

# extract the list of domains
hs_pep_fasta = genelist('../gencode/gencode.v32.pc_translations.fa.gz', format=format.fasta, gzip=True)
#mm_pep_fasta = g

print(hs_pep_fasta)
found = 0
not_found = 0

for filename in glob.glob('*.glb'):
    stub = os.path.split(filename)[1].replace('.glb', '')
    epifactors = glload(filename)
    epifactors = frozenset(epifactors['ensp'])

    newf = []
    for i in hs_pep_fasta:
        t = i['name'].split('|')
        gene_symbol = t[6]
        ensp = t[0].split('.')[0]
        
        if ensp in epifactors:
            new_name = '{0} {1}'.format(ensp, gene_symbol)
            newf.append({'name': new_name, 'seq': i['seq']})    
            found += 1
        else:
            not_found += 1

    gl = genelist()
    gl.load_list(newf)
    gl.saveFASTA('{0}.fa'.format(stub), name='name')

    print('Found    :', found)
    print('Not found:', not_found)



