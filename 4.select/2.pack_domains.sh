
rm passed_domains.hmm*
cat passed_domains.tsv | cut -f1 | grep -v 'domain' | hmmfetch -f ../domains/domains.hmm - >passed_domains.hmm
hmmpress passed_domains.hmm
