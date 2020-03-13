#!/usr/bin/env python3
from glbase3 import *

'''

Round 1, we cut domains that are redundant with other doamins.

Basically, if they find the same proteins, we can trim them from the list

'''

model_matrix = glload('../2.determine_reqd_models/domains.glb')
all_models = model_matrix.getConditionNames()

for
