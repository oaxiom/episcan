
import sys, os, glob, gzip
from glbase3 import *

[os.remove(f) for f in glob.glob('annotations/*.glb')]
[os.remove(f) for f in glob.glob('annotations_tsv/*.tsv')]

keep_key = set(['gene_id', 'gene_biotype', 'gene_name'])

species_data = glload('../6.all_species/species_data/all_species.glb')
species_data = set(species_data['assembly_name'])
#print(species_data)

species_found = 0
valid_species = 0

other_keys_seen = set([])

for gtf in sorted(glob.glob('annotation_data/pep/*/pep/*.fa.gz')) + glob.glob('annotation_data/pep/*/*/pep.fa.gz'):
    if 'chr.' in gtf:
        continue
    if 'abinitio.' in gtf:
        continue

    species_found += 1

    assembly_name = os.path.split(gtf)[1].replace('.pep.all.fa.gz', '') # 47 is the release number

    if assembly_name[0] == '_':
        continue

    if assembly_name not in species_data:
        continue

    print('Doing {0}'.format(assembly_name))

    oh = gzip.open(gtf, 'rt')

    fasta_data = []

    try:
        for line in oh:
            if line[0] == '#':
                continue

            if line[0] == '>': # Only interested in the annotations
                #print(line)
                t = line.strip().lstrip('>').rstrip(';').split(' ')
                #print(t)

                result = {'ensp': t[0]}

                for item in t[2:]:
                    item = item.split(':')
                    if len(item) < 2:
                        continue
                    if item[0] == 'gene':
                        result['ensg'] = item[1]
                    elif item[0] == 'transcript':
                        result['enst'] = item[1]
                    elif item[0] == 'gene_biotype':
                        result['gene_biotype'] = item[1]
                    elif item[0] == 'gene_symbol':
                        result['name'] = item[1]
                    else:
                        other_keys_seen.add(item[0])

            fasta_data.append(result)


        # Save the kept keys:
        gl = genelist()
        gl.load_list(fasta_data)
        gl = gl.removeDuplicates('ensp')
        gl.save('annotations/{0}.glb'.format(assembly_name))
        gl.saveTSV('annotations_tsv/{0}.tsv'.format(assembly_name))
        valid_species += 1
    except (EOFError, ValueError):
        print('EOFError: {0}'.format(gtf))

    oh.close()

print(other_keys_seen)

print('Found {0} species'.format(species_found))
print('Found {0} valid species'.format(valid_species))
