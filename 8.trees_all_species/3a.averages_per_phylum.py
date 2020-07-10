#!/usr/bin/env python3
import sys, os, glob, pickle, numpy
from glbase3 import *
config.draw_mode = 'pdf'

sys.path.append('../')
import shared

e = glload('all_data.normed.glb')

#e.heatmap(filename='all_data.normed.pdf', row_label_key='assembly_name',
#    size=[6,12], heat_wid=0.5, bracket=[0, 5])

divs = {}
div_count = {}

for species in e:
    if species['division'] not in divs:
        divs[species['division']] = numpy.zeros(len(species['conditions']))
        div_count[species['division']] = 0

    divs[species['division']] += numpy.array(species['conditions'])
    div_count[species['division']] += 1

print(divs)
print(div_count)

for division in divs:
    divs[division] /= div_count[division]

freqs = [{'name': d, 'conditions': divs[d]} for d in divs]
freqs = expression(loadable_list=freqs, cond_names=['Cluster {0}'.format(i) for i in range(len(species['conditions']))])

print(freqs)

freqs.heatmap('by_division.pdf', figsize=[5,4], heat_wid=0.4, heat_hei=0.11, bracket=[-2, 2],
    grid=True)
