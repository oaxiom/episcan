mm
library("biomaRt")
ensembl_hs = useMart("ensembl", dataset="hsapiens_gene_ensembl")
ensembl_mm = useMart("ensembl", dataset="mmusculus_gene_ensembl")

hs = getBM(attributes=c('ensembl_gene_id', 'ensembl_peptide_id', 'hgnc_symbol', 'hgnc_id'), 
      mart = ensembl_hs)

write.table(hs, 'hs_map.tsv', sep='\t', row.names=FALSE)

mm = getBM(attributes=c('ensembl_gene_id', 'ensembl_peptide_id', 'mgi_symbol', 'mgi_id'),
      mart = ensembl_mm)

write.table(mm, 'mm_map.tsv', sep='\t', row.names=FALSE)

