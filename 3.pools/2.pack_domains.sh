

cat domains_round1.txt | cut -f1 -d':' | grep -v 'name' | hmmfetch -f ../domains/domains.hmm - >domains_round1.hmm

hmmpress domains_round1.hmm
