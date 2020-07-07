#!/usr/bin/env python3
import sys, os, glob, pickle
from glbase3 import *
config.draw_mode = 'pdf'

sys.path.append('../')
import shared

e = glload('all_data.normed.glb')

row_cols = shared.get_division_cols(e)
e.heatmap(filename='all_data.normed.pdf', row_label_key='assembly_name',
    row_colbar=row_cols,
    size=[6,12], heat_wid=0.5, bracket=[-2, 2])

for div in ('Fungi', 'Vertebrates', 'Protists', 'Plants', 'Metazoa'):
    sub = e.getRowsByKey(key='division', values=[div,])
    sub.heatmap(filename='all_data.normed.{0}.pdf'.format(div), row_label_key='assembly_name',
        size=[6,12], heat_wid=0.5, bracket=[-2, 2])

# selected:

todo = dict(
    model_organisms = [
        # Plants
        'Arabidopsis_thaliana.TAIR10',
        'Glycine_max.Glycine_max_v2.1',
        'Oryza_sativa.IRGSP-1.0',
        'Triticum_aestivum.IWGSC',
        'Zea_mays.B73_RefGen_v4',
        # Vertebrates
        'Homo_sapiens.GRCh38',
        'Danio_rerio.GRCz10',
        'Gallus_gallus.Gallus_gallus-5.0',
        'Mus_musculus.GRCm38',
        'Rattus_norvegicus.Rnor_6.0',
        'Xenopus_tropicalis.JGI_4.2',
        'Takifugu_rubripes.FUGU4',
        # Metazoa
        'Apis_mellifera.Amel_4.5',
        'Caenorhabditis_elegans.WBcel235',
        'Drosophila_melanogaster.BDGP6.28',
        # Fungi
        'Saccharomyces_cerevisiae.R64-1-1',
        'Schizosaccharomyces_pombe.ASM294v2',
        'Aspergillus_nidulans.ASM1142v1',
        #Protists
        'Dictyostelium_discoideum.dicty_2.7',
        'Leishmania_major.ASM272v2',
        'Plasmodium_falciparum.ASM276v2',
        ],

    selected_organisms = [
        # Plants
        'Arabidopsis_thaliana.TAIR10',
        'Brassica_rapa.Brapa_1.0',
        'Glycine_max.Glycine_max_v2.1',
        'Oryza_sativa.IRGSP-1.0',
        'Triticum_aestivum.IWGSC',
        'Zea_mays.B73_RefGen_v4',

        # Vertebrates
        'Homo_sapiens.GRCh38',
        'Danio_rerio.GRCz10',
        'Gallus_gallus.Gallus_gallus-5.0',
        'Mus_musculus.GRCm38',
        'Rattus_norvegicus.Rnor_6.0',
        'Xenopus_tropicalis.JGI_4.2',
        'Takifugu_rubripes.FUGU4',

        # Metazoa
        'Aedes_aegypti_lvpagwg.AaegL5',
        'Apis_mellifera.Amel_4.5',
        'Caenorhabditis_elegans.WBcel235',
        'Drosophila_melanogaster.BDGP6.28',
        'Octopus_bimaculoides.PRJNA270931',

        # Fungi
        'Saccharomyces_cerevisiae.R64-1-1',
        'Schizosaccharomyces_pombe.ASM294v2',
        'Aspergillus_nidulans.ASM1142v1',

        #Protists
        'Dictyostelium_discoideum.dicty_2.7',
        'Leishmania_major.ASM272v2',
        'Plasmodium_falciparum.ASM276v2',
        ],

    primates = [
        'Homo_sapiens.GRCh38',
        'Gorilla_gorilla.gorGor3.1',
        'Pan_troglodytes.CHIMP2.1.4',
        'Nomascus_leucogenys.Nleu1.0',
        'Gorilla_gorilla.gorGor3.1',
        'Macaca_mulatta.Mmul_8.0.1',
        'Papio_anubis.PapAnu2.0',
        'Monodelphis_domestica.BROADO5',
        'Pongo_abelii.PPYG2',
        ],
    )

for k in todo:
    gl = genelist()
    gl.load_list([{'assembly_name': i} for i in todo[k]])

    newe = gl.map(genelist=e, key='assembly_name')

    row_cols = shared.get_division_cols(newe)

    newe.heatmap(filename='selected.normed.{0}.pdf'.format(k),
        row_label_key='assembly_name',
        row_colbar=row_cols,
        heat_hei=0.01*len(newe),
        size=[6,12], heat_wid=0.5, bracket=[-2, 2])
