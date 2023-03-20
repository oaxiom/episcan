
import os

from glbase3 import glload, format, genelist

# First, get the FASTA containing the Episcan identified factors.

episcan_human = glload('../4.select/Hs.matches.glb').removeDuplicates('ensp')
print(episcan_human)

# Get all human pep FASTAs

fa = genelist('../gencode/gencode.v42.pc_translations.fa', format=format.fasta)
print(fa)

# gotta fix the names
for f in fa:
    f['ensp'] = f['name'].split('|')[0].split('.')[0]
    f['name'] = f['name'].split('|')[6]
    f['name'] = f"{f['ensp']}:{f['name']}"
fa._optimiseData()
print(fa)
print()
mapped = episcan_human.map(genelist=fa, key='ensp')

mapped.saveFASTA('Hs_episcan_hits.fa', name='name')

# Then search for all domains, with a pretty strict E-value
os.system('hmmsearch -E 1E-20 --cpu 3 --noali --tblout tbl.cooccuring.tsv --domtblout domtbl.coocurring.tsv ../domains/domains.hmm Hs_episcan_hits.fa >/dev/null')
