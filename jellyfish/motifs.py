"""Regulatory motif discovery in locus-upstream regions.

k-mer enrichment with a binomial z-score against a genomic background:
    z(k) = (n_obs - n_exp) / sqrt(n_exp * (1 - p_k))
where p_k is the background fraction of windows containing k, n_exp = N * p_k.
Shared enriched k-mers between orthologous upstream regions of two species are
candidate conserved regulatory motifs.
"""
import math
from collections import Counter

RC_TABLE = str.maketrans("ACGT", "TGCA")

def revcomp(s):
    return s.translate(RC_TABLE)[::-1]

def canonical(kmer):
    rc = revcomp(kmer)
    return min(kmer, rc)

def kmers(seq, k):
    seq = seq.upper()
    return (canonical(seq[i:i+k]) for i in range(len(seq) - k + 1)
            if "N" not in seq[i:i+k])

def window_hits(seq, k, window=50):
    """Set of canonical k-mers present in each sliding window of `window` bp."""
    seq = seq.upper()
    out = []
    for i in range(0, max(1, len(seq) - window + 1), window):
        w = seq[i:i+window]
        out.append({canonical(w[j:j+k]) for j in range(len(w) - k + 1) if "N" not in w[j:j+k]})
    return out

def enrichment(target_seqs, background_seqs, k=6, window=50):
    """z-scores for k-mer presence: target windows vs background windows."""
    bg_windows = []
    for s in background_seqs:
        bg_windows.extend(window_hits(s, k, window))
    N = len(bg_windows)
    if N == 0:
        return {}
    bg_counts = Counter()
    for w in bg_windows:
        bg_counts.update(w)
    tgt_windows = []
    for s in target_seqs:
        tgt_windows.extend(window_hits(s, k, window))
    tgt_counts = Counter()
    for w in tgt_windows:
        tgt_counts.update(w)
    out = {}
    for kmer, n_obs in tgt_counts.items():
        p = (bg_counts.get(kmer, 0) + 0.5) / (N + 1)  # pseudocount: absent != impossible
        n_exp = len(tgt_windows) * p
        denom = math.sqrt(n_exp * (1 - p))
        z = (n_obs - n_exp) / denom if denom else 0
        out[kmer] = {"n_obs": n_obs, "n_exp": round(n_exp, 2), "z": round(z, 2)}
    return out

KNOWN_TFBS = {
    "E-box_CACGTG": "CACGTG", "Sp1_GGGCGG": "GGGCGG", "AP1_TGACTCA": "TGACTCA",
    "CREB_TGACGTCA": "TGACGTCA", "NFkB_GGGRNNYYCC_partial": "GGGACTTTCC",
    "E2F_TTTSSCGC": "TTTCGCGC", "Myc_max": "CACGTG",
}

def tfbs_counts(seq, motifs=None):
    motifs = motifs or KNOWN_TFBS
    seq = seq.upper()
    out = {}
    for name, m in motifs.items():
        m = m.upper()
        rc = revcomp(m)
        n = seq.count(m) + (seq.count(rc) if rc != m else 0)
        out[name] = n
    return out
