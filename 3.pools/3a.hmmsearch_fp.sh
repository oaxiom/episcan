#PBS -l nodes=1:ppn=2
#PBS -q batch
#PBS -j oe
#PBS -o results.out
#PBS -V 
cd $PBS_O_WORKDIR

hmmsearch -E 1e-1 --cpu 2 --noali --domtblout round2_gencode_FP.txt domains_round1.hmm ../gencode/gencode.v32.pc_translations.fa >/dev/null