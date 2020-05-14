
from glbase3 import *

res = {}

oh = open('domains.hmm', 'rt')
for idx, line in enumerate(oh):
    if 'NAME' in line:
        cname = line.split()[1]
        res[cname] = {'acc': '', 'desc': ''}
    elif 'ACC' in line:
        res[cname]['acc'] = line.split()[1]
    elif 'DESC' in line:
        res[cname]['desc'] = line.split()[1]

    if (idx+1) % 1000000 == 0:
        print('Done {0:,} domains in {1:,} lines'.format(len(res), idx+1))


print('Found {0:,} domains'.format(len(res)))

gl = genelist()
gl.load_list([{'name': k, 'acc': res[k]['acc'], 'desc': res[k]['desc']} for k in res])
gl.saveTSV('annotation_table.tsv', key_order=['name', 'acc', 'desc'])
gl.save('annotation_table.glb')
