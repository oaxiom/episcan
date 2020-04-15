#PBS -l nodes=1:ppn=32
#PBS -q batch
#PBS -j oe
#PBS -o results.out
#PBS -V 
cd $PBS_O_WORKDIR

hmmsearch -E 1e-5 --cpu 2 --noali --domtblout round2_gencode_TPFP.txt domains_round1.hmm ../gencode/gencode.v32.pc_translations.fa.gz >/dev/null