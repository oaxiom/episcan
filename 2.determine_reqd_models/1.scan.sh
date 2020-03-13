#PBS -l nodes=1:ppn=2
#PBS -q batch
#PBS -j oe
#PBS -o results.out
#PBS -V 
cd $PBS_O_WORKDIR

appl='PfamA-27.0,SMART-6.2,SuperFamily-1.75'

hmmsearch -E 1e-2 --cpu 2 --noali --domtblout pfam.txt ../domains/domains.hmm ../1.extract_epifactors_FASTA/hs_epifactors.all.fa >/dev/null





