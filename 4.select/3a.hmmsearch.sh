
hmmsearch -E 1e-1 --cpu 4 --noali --domtblout Hs.gencode.txt passed_domains.hmm ../gencode/gencode.v32.pc_translations.fa >/dev/null

hmmsearch -E 1e-1 --cpu 4 --noali --domtblout Mm.gencode.txt passed_domains.hmm ../gencode/gencode.vM24.pc_translations.fa >/dev/null