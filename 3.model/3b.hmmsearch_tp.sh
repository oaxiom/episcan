#PBS -l nodes=1:ppn=2
#PBS -q batch
#PBS -j oe
#PBS -o results.out
#PBS -V 
cd $PBS_O_WORKDIR

hmmsearch -E 1e-1 --cpu 2 --noali --domtblout round2.epifactors.TP.txt domains_round1.hmm ../1.extract_epifactors_FASTA/hs_epifactors.all.fa >/dev/null
