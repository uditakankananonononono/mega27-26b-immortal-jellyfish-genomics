"""Statistics for the 26b expansion: BH FDR, Fisher wrappers, permutation test."""
from __future__ import annotations
import math
from itertools import permutations
from scipy.stats import fisher_exact, binomtest


def bh_adjust(pvals):
    """Benjamini-Hochberg adjusted q-values, input order preserved."""
    n = len(pvals)
    if n == 0:
        return []
    order = sorted(range(n), key=lambda i: pvals[i])
    q = [0.0] * n
    prev = 1.0
    for rank in range(n, 0, -1):
        i = order[rank - 1]
        prev = min(prev, pvals[i] * n / rank)
        q[i] = min(prev, 1.0)
    return q


def fisher(a, b, c, d):
    """Two-sided Fisher exact on [[a,b],[c,d]]; returns (oddsratio, p)."""
    return fisher_exact([[a, b], [c, d]])


def binom_ge(k, n, p0):
    """P(X >= k) under Binomial(n, p0)."""
    return binomtest(k, n, p0, alternative="greater").pvalue


def jaccard(set_a, set_b):
    u = set_a | set_b
    if not u:
        return 0.0
    return 1.0 - len(set_a & set_b) / len(u)


def separation_statistic(presence, group_a, group_b):
    """mean within-A Jaccard distance minus mean A-vs-B distance.

    presence: {genome: set of genes present}. Negative => A-genomes more
    similar to each other than to B-genomes (separation)."""
    da = [jaccard(presence[g1], presence[g2])
          for i, g1 in enumerate(group_a) for g2 in group_a[i + 1:]]
    dab = [jaccard(presence[g1], presence[g2])
           for g1 in group_a for g2 in group_b]
    ma = sum(da) / len(da) if da else 0.0
    mab = sum(dab) / len(dab) if dab else 0.0
    return ma - mab


def permutation_p_labels(presence, group_a, group_b, observed):
    """Exact permutation p over all distinct label assignments.

    p = fraction of assignments with stat <= observed (separation direction).
    Label sets are fixed: assignments choose which |A| genomes get label A."""
    genomes = sorted(presence)
    from itertools import combinations
    n_a = len(group_a)
    stats = []
    for combo in combinations(genomes, n_a):
        ga = list(combo)
        gb = [g for g in genomes if g not in ga]
        stats.append(separation_statistic(presence, ga, gb))
    p = sum(1 for s in stats if s <= observed + 1e-12) / len(stats)
    return p, len(stats), stats
