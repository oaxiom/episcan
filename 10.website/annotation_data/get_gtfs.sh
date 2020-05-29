
inc="*.gtf.gz"
opt='--prune-empty-dirs'
#exc='*'

# retrieves the current genome DNA sequence FASTA files for all species in Ensembl
rsync $opt -avP --include="*/" --include=$inc --exclude="*" rsync:ftp://ftp.ensembl.org/pub/release-47/fungi/gtf/

lftp -c "set ftp:list-options -a;
open 'ftp://ftp.ensemblgenomes.org/pub/current/fungi/gtf/';
mirror -e -c --verbose --no-empty-dirs --include-glob $inc"

lftp -c "set ftp:list-options -a;
open 'ftp://ftp.ensemblgenomes.org/pub/current/plants/gtf/';
mirror -e -c --verbose --no-empty-dirs --include-glob $inc"

lftp -c "set ftp:list-options -a;
open 'ftp://ftp.ensemblgenomes.org/pub/current/protists/gtf/';
mirror -e -c --verbose --no-empty-dirs --include-glob $inc"

lftp -c "set ftp:list-options -a;
open 'ftp://ftp.ensembl.org/pub/release-100/gtf/';
mirror -e -c --verbose --no-empty-dirs --include-glob $inc"



