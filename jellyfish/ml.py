"""ML arms: one-hot CNN for locus-upstream detection, k-mer baselines, GNN
on k-mer co-occurrence graphs for species discrimination of upstream regions.
"""
import numpy as np

BASES = "ACGT"
BIDX = {b: i for i, b in enumerate(BASES)}

def one_hot(seq, maxlen=2000):
    """One-hot encode (4, maxlen); truncate or zero-pad. N -> all-zeros."""
    x = np.zeros((4, maxlen), dtype=np.float32)
    for i, ch in enumerate(seq[:maxlen].upper()):
        j = BIDX.get(ch)
        if j is not None:
            x[j, i] = 1.0
    return x

def kmer_vector(seq, k=6):
    """Normalized canonical k-mer count vector (4**k dims), N-skipping."""
    from jellyfish.motifs import canonical
    seq = seq.upper()
    v = np.zeros(4 ** k, dtype=np.float64)
    n = 0
    for i in range(len(seq) - k + 1):
        w = seq[i:i+k]
        if "N" in w:
            continue
        c = canonical(w)
        idx = 0
        for ch in c:
            idx = idx * 4 + BIDX[ch]
        v[idx] += 1.0
        n += 1
    return v / n if n else v

def build_xy(pos, neg, featurize, **kw):
    X = np.stack([featurize(s, **kw) for s in pos + neg])
    y = np.array([1] * len(pos) + [0] * len(neg), dtype=np.int64)
    return X, y

def kfold_indices(n, k=5, seed=0):
    rng = np.random.default_rng(seed)
    idx = rng.permutation(n)
    folds = np.array_split(idx, k)
    return [(np.setdiff1d(idx, f), f) for f in folds]
