"""Telomeric-repeat census on raw assemblies.

Canonical metazoan telomere motif: TTAGGG (and its reverse complement CCCTAA).
Cnidarian variants reported in literature include TTAGGG (most) and others.
We count, per assembly: total tandem hexamer occurrences genome-wide, and
enrichment at sequence ends (first/last END_WINDOW bp of each contig/scaffold).
Enrichment ratio = end density / body density; a chromosome-end signal should
show >>1 for the true telomeric motif.
"""
from collections import Counter

MOTIFS = {
    "TTAGGG": "canonical vertebrate/cnidarian",
    "TAACCCT": "alternative (some invertebrates)",
    "TTAGG": "insect-type pentamer",
    "TCAGG": "nematode-type variant",
}
END_WINDOW = 10_000

def revcomp(s):
    return s.translate(str.maketrans("ACGT", "TGCA"))[::-1]

def count_motif(seq, motif):
    """Non-overlapping tandem repeat count of motif (and revcomp) in seq (upper)."""
    rc = revcomp(motif)
    n = 0
    for m in ({motif, rc} if rc != motif else {motif}):
        start = 0
        while True:
            i = seq.find(m, start)
            if i < 0:
                break
            n += 1
            start = i + len(m)
    return n

def parse_fasta(path):
    name, chunks = None, []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line.startswith(">"):
                if name is not None:
                    yield name, "".join(chunks)
                name, chunks = line[1:].split()[0], []
            else:
                chunks.append(line.upper())
    if name is not None:
        yield name, "".join(chunks)

def census(path, motifs=None, end_window=END_WINDOW):
    """Per-motif genome-wide and end-enriched counts for an assembly FASTA."""
    motifs = motifs or MOTIFS
    total_len = 0
    body = Counter()
    ends = Counter()
    end_len = 0
    n_seqs = 0
    min_len = 3 * end_window  # shorter sequences would make "ends" overlap the body
    n_used = 0
    for name, seq in parse_fasta(path):
        n_seqs += 1
        total_len += len(seq)
        for m in motifs:
            body[m] += count_motif(seq, m)
        if len(seq) >= min_len:
            n_used += 1
            head, tail = seq[:end_window], seq[-end_window:]
            end_len += len(head) + len(tail)
            for m in motifs:
                ends[m] += count_motif(head, m) + count_motif(tail, m)
    out = {"assembly": path, "n_sequences": n_seqs, "n_sequences_end_analysis": n_used,
           "total_bp": total_len, "end_window": end_window, "motifs": {}}
    for m in motifs:
        end_density = ends[m] / end_len if end_len else 0
        body_density = body[m] / total_len if total_len else 0
        out["motifs"][m] = {
            "description": motifs[m] if isinstance(motifs, dict) else "",
            "genome_count": body[m], "end_count": ends[m],
            "genome_density_per_kb": round(body_density * 1000, 6),
            "end_density_per_kb": round(end_density * 1000, 6),
            "end_enrichment": round(end_density / body_density, 2) if body_density else None,
        }
    return out
