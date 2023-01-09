
# Ensembl Main
lftp -e 'cd pub/release-108/fasta/ ; find . ; bye' ftp.ensembl.org > file_list_main
grep '.pep.all.fa.gz' file_list_main | sed 's#^./#wget -c http://ftp.ensembl.org/pub/release-108/fasta/#g' | sed 's#$# fastas/#g' > get_main.sh

# Metazoa
lftp -e 'cd pub/metazoa/release-55/fasta/ ; find . ; bye' ftp.ensemblgenomes.org > file_list_metazoa
grep '.pep.all.fa.gz' file_list_metazoa | sed 's#^./#wget -c http://ftp.ensemblgenomes.org/pub/metazoa/release-55/fasta/#g' | sed 's#$# fastas/#g'  > get_metazoa.sh

# Plant
lftp -e 'cd pub/plants/release-55/fasta/ ; find . ; bye' ftp.ensemblgenomes.org > file_list_plants
grep '.pep.all.fa.gz' file_list_plants | sed 's#^./#wget -c http://ftp.ensemblgenomes.org/pub/plants/release-55/fasta/#g' | sed 's#$# fastas/#g'  > get_plants.sh

# Fungi
lftp -e 'cd pub/fungi/release-55/fasta/ ; find . ; bye' ftp.ensemblgenomes.org > file_list_fungi
grep '.pep.all.fa.gz' file_list_fungi | sed 's#^./#wget -c http://ftp.ensemblgenomes.org/pub/fungi/release-55/fasta/#g' | sed 's#$# fastas/#g'  > get_fungi.sh

# Protists
lftp -e 'cd pub/protists/release-55/fasta/ ; find . ; bye' ftp.ensemblgenomes.org > file_list_protists
grep '.pep.all.fa.gz' file_list_protists | sed 's#^./#wget -c http://ftp.ensemblgenomes.org/pub/protists/release-55/fasta/#g' | sed 's#$# fastas/#g'  > get_protists.sh

