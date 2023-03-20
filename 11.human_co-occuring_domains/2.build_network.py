
import os
import networkx as nx

from glbase3 import glload, format, genelist

hmmer_hits = genelist('tbl.cooccuring.tsv', format=format.hmmer_tbl)
print(hmmer_hits)

# build the frequency dict
for ensp in hmmer_hits:
    # There are severla names for each ENSP, I use the NAME as unique
    name = ensp['name'].split(':')

G = Graph()
