
inc="*.gtf.gz"
opt='--prune-empty-dirs'
#exc='*'

# retrieves the current genome DNA sequence FASTA files for all species in Ensembl
rsync $opt -avP --include="*/" --include=$inc --exclude="*" rsync:ftp://ftp.ensembl.org/pub/release-47/fungi/gtf/
#rsync $opt -avP --include="*/" --include=$inc --exclude="*" ftp://ftp.ensemblgenomes.org/pub/current/fungi/fasta/ pep/
#rsync $opt -avP --include="*/" --include=$inc --exclude="*" ftp://ftp.ensemblgenomes.org/pub/current/metazoa/fasta/ pep/
#rsync $opt -avP --include="*/" --include=$inc --exclude="*" ftp://ftp.ensemblgenomes.org/pub/current/plants/fasta/ pep/

lftp -c "set ftp:list-options -a;
open 'ftp://ftp.ensemblgenomes.org/pub/current/fungi/gtf/';
mirror -e -c --verbose --no-empty-dirs --include-glob $inc"

lftp -c "set ftp:list-options -a;
open 'ftp://ftp.ensemblgenomes.org/pub/current/fungi/fasta/';
lcd cdna/;
mirror -e -c --verbose --no-empty-dirs --include-glob $inc"

lftp -c "set ftp:list-options -a;
open 'ftp://ftp.ensemblgenomes.org/pub/current/plants/fasta/';
lcd cdna/;
mirror -e -c --verbose --no-empty-dirs --include-glob $inc"

lftp -c "set ftp:list-options -a;
open 'ftp://ftp.ensemblgenomes.org/pub/current/protists/fasta/';
lcd cdna/;
mirror -e -c --verbose --no-empty-dirs --include-glob $inc"
