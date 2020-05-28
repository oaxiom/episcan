
import glob, sys, os
from glbase3 import *
import matplotlib.pyplot as plot
import numpy as np

config.draw_mode = "png"

for filename in glob.glob("../../clusters_genes/*.tsv"):
    gl = genelist(filename, format={'force_tsv': True, 'ensg': 0})

    for gene in gl:
        gene['ensg'] = gene['ensg'].split('.')[0]
    gl._optimiseData()

    gl.saveTSV(os.path.split(filename)[1])
