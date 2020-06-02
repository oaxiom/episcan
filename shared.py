
import numpy as np
import matplotlib.pyplot as plot

def get_division_cols(gl):
    row_cols = []
    for i in gl:
        if i['division'] == 'Fungi':
            row_cols.append('purple')
        elif i['division'] == 'Vertebrates':
            row_cols.append('red')
        elif i['division'] == 'Metazoa':
            row_cols.append('orange')
        elif i['division'] == 'Plants':
            row_cols.append('green')
        elif i['division'] == 'Protists':
            row_cols.append('blue')
        else:
            row_cols.append('grey')
            print(i['division'], 'Not found')
    return row_cols

def remove_duplicate_domains_by_overlap_and_e(domains, overlap_percent=90):
    # https://www.biostars.org/p/134579/

    # Filter domains by a given E-value and overlapping cut-off.
    cycles = 0
    num_overlaps = 1e6
    while num_overlaps > 0 and cycles < 100:
        cycles += 1
        domains.sort(key=lambda x: x['dom_loc'])

        # Work out and prune the number of overlapping domains for this criteria
        num_overlaps = 0
        to_prune = []
        for i1 in range(0, len(domains)):
            for i2 in range(0, len(domains)):
                if i1 < i2:
                    d1l = domains[i1]['dom_loc']
                    d2l = domains[i2]['dom_loc']
                    if d1l[1] >= d2l[0] and d1l[0] <= d2l[1]: # collision;
                        # domains
                        dom1len = d1l[1] - d1l[0]
                        dom2len = d2l[1] - d2l[0]
                        domlen = sorted([dom1len, dom2len])[0]
                        overlap = abs(d1l[1] - d2l[0])
                        if (overlap/domlen)*100 >= overlap_percent:
                            # keep the best e:
                            #print(d1l, d2l)
                            if domains[i1]['e'] >= domains[i2]['e']:
                                to_prune.append(i1)
                            else:
                                to_prune.append(i2)

                            num_overlaps += 1 # signal we still found an overlap;
                            continue
        filtered = []
        # prune domains from the list;
        for i in range(0, len(domains)):
            if i not in to_prune:
                filtered.append(domains[i])
        domains = filtered

    return filtered


def get_dynamic_e(hmmer_search, dynamicE):
    '''
    Criteria for selecting domains;

    '''
    skipped_too_short = 0
    matches = []
    for hit in hmmer_search:
        domain = hit['dom_name']

        e = float(hit['e'])

        #print(hit, e, dynamicE[domain], e < dynamicE[domain])
        if e < dynamicE[domain]:
            dom_len = hit['dom_loc'][1] - hit['dom_loc'][0]
            if dom_len < 20: # Some super short, dubious matches;
                skipped_too_short += 1
                continue

            to_add = {
                'e': e,
                'len': hit['tlen'],
                'qlen': hit['qlen'],
                'dom_loc': hit['dom_loc'],
                'domain': hit['dom_name'],
                }

            if '|' in hit['peptide']:
                print(hit['peptide'])
                t = hit['peptide'].split('|')
                to_add['ensp'] = t[0].split('.')[0] # Special for Ensembl data;
                to_add['ensg'] = t[2].split('.')[0]
                to_add['name'] = t[6]
            else:
                to_add['ensp'] = hit['peptide']

            to_add['unq_key'] = '{0}-{1}'.format(to_add['ensp'], hit['dom_name'])

            matches.append(to_add)

    # for each peptide, remove duplicate and overlapping domains;
    genes = {}
    for m in matches:
        if m['ensp'] not in genes:
            genes[m['ensp']] = []
        genes[m['ensp']].append(m)

    kept_hits = []
    for g in genes:
        filtered = remove_duplicate_domains_by_overlap_and_e(genes[g])

        for m in filtered:
            kept_hits.append(m)

    print('Trimmed {0} to {1} domains'.format(len(matches), len(kept_hits)))
    print('skipped_too_short={0}'.format(skipped_too_short))
    matches = kept_hits

    return matches


def radial_plot(filename, data, title):
    fig = plot.figure(figsize=(6,6))
    #fig.subplots_adjust(0.02, 0.02, 0.97, 0.97, wspace=0.1, hspace=0.1)

    ax = fig.add_subplot(111, polar=True)

    erad = 2*np.pi / (len(data)+1) # each segment gets 0.69813170079773 (or thereabouts) rads
    eradh = erad / 2.0
    eradq = eradh / 2.0
    theta = np.arange(0.0, 2*np.pi, 2*np.pi/len(data))
    width = (np.pi/4)*len(data) # in rads?
    width = 0.5

    ax.bar(theta+(0.6981317/2), data, width=erad, bottom=0.0, alpha=0.8, color='red')

    ax.set_title(title)
    ax.set_xticks(theta)
    ax.set_xticklabels("")
    #ax.set_yticklabels("") # For hte svg

    #l = ax.get_rlim()
    #ax.set_rticks([0.5, 1, 1.5, 2])

    l = ax.get_ylim()
    #print k, ["%s%%" % i for i in range(l[0], l[1]+5, l[1]//len(axes[k].get_yticklabels()))]
    #print [str(t) for t in axes[k].get_yticklabels()]
    [t.set_fontsize(6) for t in ax.get_yticklabels()]
    #print ["%s%%" % (i*10, ) for i, t in enumerate(axes[k].get_yticklabels())]
    #print [t.get_text() for t in axes[k].get_yticklabels()]
    ylabs = ["%s%%" % str(i) for i in range(int(l[0]), int(l[1])+5, int(l[1]//len(ax.get_yticklabels())))][1:]
    #axes[k].set_yticklabels(ylabs)

    fig.savefig(filename)

if __name__ == "__main__":
    data = [33, 83, 92, 94, 12, 66, 69, 73, 56, 87, 74, 42, 104, 34, 19, 57, 38, 67, 2, 42, 122, 113, 53, 67, 23, 128, 77, 16, 25, 86, 26, 109]

    radial_plot('Homo_sapiens.pdf',
        data=data,
        title='Homo Sapiens')
