#!/usr/bin/env python3
import sys, re
from glbase3 import *

# Get all the domains first. 

pfam = genelist(filename='pfam.txt', format=format.hmmer_tbl)

done = {}
gltab = []
for line in pfam:
    hmm = line['score'] # all in the wrong columns
    name = line['dom_acc']

    if (name, hmm) not in done:
        done[(name, hmm)] = 0
    done[(name, hmm)] += 1

newl = []
for dom in done:
    
    gltab = {'name': dom[0], 'acc': dom[1], 'count': done[dom]}
    newl.append(gltab)

gl = genelist()
gl.load_list(newl)
gl.sort('name')
gl.save('domains.glb')
gl.saveTSV('domains.txt', key_order=['name'])



