
echo 

for species in ../species_data/species_fastas/fastas/*.fa.gz
do
    root=`basename $species`
    base=`echo $root | sed -r 's/.pep.all.fa.gz//g'`
    
    echo Species = $base
    sbatch -J hmm.$base --output=$base.out --export=ALL,species=$species,base=$base hmm_search.slurm 
    
done
