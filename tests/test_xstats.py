from jellyfish.xstats import (bh_adjust, fisher, binom_ge, jaccard,
                              separation_statistic, permutation_p_labels)

def test_bh_monotone_and_bounded():
    q = bh_adjust([0.001, 0.01, 0.5, 0.9])
    assert all(0 <= x <= 1 for x in q)
    assert q[0] <= q[1] <= q[2] <= q[3]
    assert abs(q[0] - 0.004) < 1e-9  # 0.001 * 4/1

def test_bh_empty_and_single():
    assert bh_adjust([]) == []
    assert bh_adjust([0.03]) == [0.03]

def test_fisher_basic():
    _, p = fisher(10, 1, 1, 10)
    assert p < 0.01
    _, p2 = fisher(5, 5, 5, 5)
    assert p2 > 0.5

def test_binom_ge():
    assert binom_ge(10, 10, 0.5) < 0.001
    assert binom_ge(0, 10, 0.5) == 1.0

def test_jaccard():
    assert jaccard({1, 2}, {1, 2}) == 0.0
    assert jaccard({1}, {2}) == 1.0
    assert jaccard(set(), set()) == 0.0

def test_separation_and_permutation():
    pres = {"T1": {"a", "b", "c"}, "T2": {"a", "b", "c"},
            "N1": {"x"}, "N2": {"y"}}
    obs = separation_statistic(pres, ["T1", "T2"], ["N1", "N2"])
    assert obs < 0
    p, n, _ = permutation_p_labels(pres, ["T1", "T2"], ["N1", "N2"], obs)
    assert n == 6  # C(4,2)
    assert p <= 1/6 + 1e-9

def test_permutation_null_high_p():
    pres = {"T1": {"a"}, "T2": {"a"}, "N1": {"a"}, "N2": {"a"}}
    obs = separation_statistic(pres, ["T1", "T2"], ["N1", "N2"])
    p, n, _ = permutation_p_labels(pres, ["T1", "T2"], ["N1", "N2"], obs)
    assert p == 1.0
