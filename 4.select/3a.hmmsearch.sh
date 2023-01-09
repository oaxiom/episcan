
echo 'Human'
hmmsearch -E 1 --cpu 4 --noali --domtblout Hs.gencode.txt passed_domains.hmm ../gencode/gencode.v42.pc_translations.fa >/dev/null
echo 'Mouse'
hmmsearch -E 1 --cpu 4 --noali --domtblout Mm.gencode.txt passed_domains.hmm ../gencode/gencode.vM31.pc_translations.fa >/dev/null
