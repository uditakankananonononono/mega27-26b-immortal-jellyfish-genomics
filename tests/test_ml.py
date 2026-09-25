import numpy as np
from jellyfish.ml import one_hot, kmer_vector, build_xy, kfold_indices

def test_one_hot_shape():
    assert one_hot("ACGT").shape == (4, 2000)

def test_one_hot_values():
    x = one_hot("A", maxlen=10)
    assert x[0, 0] == 1 and x.sum() == 1

def test_kmer_vector_normalized():
    v = kmer_vector("ACGTACGT", k=2)
    assert abs(v.sum() - 1.0) < 1e-9 and v.max() > 0

def test_build_xy():
    X, y = build_xy(["AAAA"], ["CCCC"], kmer_vector, k=2)
    assert X.shape[0] == 2 and list(y) == [1, 0]

def test_kfolds_partition():
    for tr, te in kfold_indices(20, k=5, seed=1):
        assert len(te) == 4 and not set(tr) & set(te)
