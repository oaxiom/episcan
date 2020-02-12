#PBS -l nodes=1:ppn=1
#PBS -q batch
#PBS -j oe
#PBS -o results.out
#PBS -V 
cd $PBS_O_WORKDIR

hmmpress Pfam-A.hmm 

