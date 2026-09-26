"""Comparative analysis of repair/telomerase gene sets (pure, hermetic)."""
from __future__ import annotations
from collections import Counter

DNA_REPAIR_GENES = ["ERCC1", "ERCC2", "XRCC1", "XRCC5", "RAD51", "BRCA1",
                    "MLH1", "MSH2", "OGG1", "PARP1", "FEN1", "LIG4"]
TELOMERASE_GENES = ["TERT", "TERC", "DKC1", "POT1", "TERF1", "TERF2"]


def gc_content(seq):
    s = seq.upper().replace("N", "")
    if not s:
        return 0.0
    return (s.count("G") + s.count("C")) / len(s)


def codon_usage(seq, frame_offset=0):
    """Codon frequencies over the sequence (rough, assumes CDS)."""
    s = seq.upper()
    c = Counter(s[i:i+3] for i in range(frame_offset, len(s) - 2, 3))
    total = sum(c.values()) or 1
    return {k: v / total for k, v in c.items()}


def kmer_spectrum(seq, k=4):
    s = seq.upper()
    c = Counter(s[i:i+k] for i in range(len(s) - k + 1))
    total = sum(c.values()) or 1
    return {kmer: v / total for kmer, v in c.items()}


def cosine(a: dict, b: dict) -> float:
    keys = set(a) | set(b)
    num = sum(a.get(k, 0) * b.get(k, 0) for k in keys)
    da = sum(v * v for v in a.values()) ** 0.5
    db = sum(v * v for v in b.values()) ** 0.5
    return num / (da * db + 1e-12)


def pairwise_signature_distance(seqs_a, seqs_b, k=4):
    """Mean cosine distance between k-mer spectra of two gene sets."""
    if not seqs_a or not seqs_b:
        return float("nan")
    spec_a = {}
    spec_b = {}
    for s in seqs_a:
        sp = kmer_spectrum(s, k)
        for key, v in sp.items():
            spec_a[key] = spec_a.get(key, 0) + v / len(seqs_a)
    for s in seqs_b:
        sp = kmer_spectrum(s, k)
        for key, v in sp.items():
            spec_b[key] = spec_b.get(key, 0) + v / len(seqs_b)
    return 1.0 - cosine(spec_a, spec_b)


def copy_number_signal(records, gene):
    """Count how many distinct records mention the gene (paralog/expansion proxy)."""
    return sum(1 for h, _ in records if gene.lower() in h.lower())
