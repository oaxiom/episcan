
echo 

for species in ../species_data/species_fastas/fastas/*.fa.gz
do
    root=`basename $species`
    base=`echo $root | sed -r 's/.pep.all.fa.gz//g'`
    
    echo Species = $base
    #qsub -N hmm.$base -v inp=$species,out=$base hmm_job.pbs 
    
    # expects:
    # inp = Location of the gzipped FASTA
    # out = the result name

    gunzip -c ${species} >tmp.fasta.fa
    hmmsearch -E 0.01 --cpu 1 --noali --tblout tbl/${base}.tsv --domtblout domtbl/${base}.tsv passed_domains.hmm tmp.fasta.fa >/dev/null

    # cleanup the results, and get the number of peptides

    #python3 clean.py
    rm tmp.fasta.fa
    gzip domtbl/${base}.tsv
    gzip tbl/${base}.tsv
done
