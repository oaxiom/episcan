#PBS -l nodes=1:ppn=32
#PBS -q batch
#PBS -j oe
#PBS -o results.out
#PBS -V 
cd $PBS_O_WORKDIR

appl='PfamA-27.0,SMART-6.2,SuperFamily-1.75'

# E-value is relxed to catch a wide range of domains for the initial pool
hmmsearch -E 0.01 --cpu 30 --noali --domtblout pfam.txt ../pfam/Pfam-A.hmm ../1.extract_epifactors_FASTA/epifactor.hg38.fa >/dev/null





