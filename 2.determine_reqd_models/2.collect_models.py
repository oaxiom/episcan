#!/usr/bin/env python3
import sys, re
from glbase3 import *

# Get all the domains first. 

pfam = genelist(filename='pfam.txt', format=format.hmmer_tbl)

done = {}
for line in pfam:
    hmm = line['score'] # all in the wrong columns
    name = line['dom_acc']

    if (name, hmm) not in done:
        done[(name, hmm)] = 0
    done[(name, hmm)] += 1

oh = open('counted_hmms.txt', 'w')
for m in sorted(done, key=done.get, reverse=True):
    #if done[m] < 1: # Don't restrict by the number of domains
    #    continue # reenable for the final table
    oh.write('%s\t%s\t%s\n' % (m[0] ,m[1], done[m]))
oh.close()



