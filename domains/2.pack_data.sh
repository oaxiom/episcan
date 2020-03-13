
find rawdata/ascii/PANTHER15.0/books/ -maxdepth 2 -name "*.hmm" | xargs cat >panther.hmm

cat rawdata/panther.hmm rawdata/Pfam-A.hmm >domains.hmm

hmmpress domains.hmm

