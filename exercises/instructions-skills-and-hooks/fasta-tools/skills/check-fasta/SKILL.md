---
name: check-fasta
description: Count the records in a FASTA file and find duplicate IDs. Use before running any analysis on a new FASTA file.
---

1. Run `grep -c '>' FILE` to count the records.
2. Run `grep '>' FILE | sort | uniq -d` to list duplicated header lines.
3. Report the exact commands you ran and their output. Do not modify FILE.
