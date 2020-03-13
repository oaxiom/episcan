#PBS -l nodes=1:ppn=32
#PBS -q batch
#PBS -j oe
#PBS -o results.out
#PBS -V 
cd $PBS_O_WORKDIR

appl='PfamA-27.0,SMART-6.2,SuperFamily-1.75'

hmmsearch -E 1e-10 --cpu 30 --noali --domtblout pfam.txt ../pfam/Pfam-A.hmm ../1.extract_epifactors_FASTA/hs_epifactors.all.fa >/dev/null





