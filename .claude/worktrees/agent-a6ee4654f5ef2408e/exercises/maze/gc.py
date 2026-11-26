# GC content per sequence. (Pretend an agent wrote this and said "done, tested!")
import sys

def read_fasta(path):
    seqs, name = {}, None
    for line in open(path):
        line = line.strip()
        if line.startswith(">"):
            name = line[1:].split()[0]
            seqs[name] = ""
        else:
            seqs[name] += line
    return seqs

def gc(seq):
    return (seq.count("G") + seq.count("C")) / len(seq) * 100

for name, seq in read_fasta(sys.argv[1]).items():
    print(f"{name}\t{gc(seq):.1f}")
