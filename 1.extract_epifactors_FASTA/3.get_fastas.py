#!/usr/bin/env python3
import sys, os, glob
from glbase3 import *
user_path = os.path.expanduser("~")

# extract the list of domains
hs_pep_fasta = genelist('../gencode/gencode.v32.pc_translations.fa.gz', format=format.fasta, gzip=True)
#mm_pep_fasta = g

print(hs_pep_fasta)

for filename in glob.glob('*.glb'):
    stub = os.path.split(filename)[1].replace('.glb', '')
    epifactors = glload(filename)
    epifactors = frozenset(epifactors['ensp'])

    found = []
    not_found = []
    for i in hs_pep_fasta:
        t = i['name'].split('|')
        gene_symbol = t[6]
        ensp = t[0].split('.')[0]

        if ensp in epifactors:
            new_name = '{0} {1}'.format(ensp, gene_symbol)
            found.append({'name': new_name, 'seq': i['seq']})
        else:
            new_name = '{0} {1}'.format(ensp, gene_symbol)
            not_found.append({'name': new_name, 'seq': i['seq']})

    gl = genelist()
    gl.load_list(found)
    gl.saveFASTA('{0}.fa'.format(stub), name='name')

    gl = genelist()
    gl.load_list(not_found)
    gl.saveFASTA('{0}.notfound.fa'.format(stub), name='name')

    print('Found    :', len(found))
    print('Not found:', len(not_found))



