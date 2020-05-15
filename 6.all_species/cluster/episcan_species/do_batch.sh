
echo 

for species in /share/apps/genomics/genome/ensembl_genomes/pep/*/pep/*.fa.gz
do
    root=`basename $species`
    base=`echo $root | sed -r 's/.pep.all.fa.gz//g'`
    
    echo Species = $base
    qsub -N hmm.$base -v inp=$species,out=$base hmm_job.pbs 
    echo
    sleep 1
done



