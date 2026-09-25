"""Unique-mutation analysis: positions where a target protein differs from a
conserved reference set.

For each verified gene: align the predicted jellyfish protein to each reference
ortholog (global pairwise, BLOSUM62). A position is CONSERVED if the same amino
acid occurs in >= CONSERVATION of aligned reference positions; it is a UNIQUE
SUBSTITUTION if the jellyfish residue differs from the conserved residue at a
conserved position. Positions where references disagree or align to gaps are
excluded. This is alignment-based comparative analysis - no ancestral
reconstruction - and the paper says so.
"""
from Bio import Align
from Bio.Align import substitution_matrices

CONSERVATION = 0.75

def _aligner():
    a = Align.PairwiseAligner()
    a.substitution_matrix = substitution_matrices.load("BLOSUM62")
    a.open_gap_score = -10
    a.extend_gap_score = -0.5
    a.mode = "global"
    return a

def aligned_residue_map(query, subject, aligner=None):
    """Align query (jellyfish) to subject (reference). Returns list of
    (query_pos, query_aa, subject_pos, subject_aa) for aligned columns where
    both sides are residues (no gaps). Positions are 1-based."""
    aligner = aligner or _aligner()
    aln = aligner.align(subject, query)[0]
    s_blocks, q_blocks = aln.aligned
    pairs = []
    for (s0, s1), (q0, q1) in zip(s_blocks, q_blocks):
        for k in range(int(s1) - int(s0)):
            pairs.append((int(q0) + k + 1, query[int(q0) + k],
                          int(s0) + k + 1, subject[int(s0) + k]))
    return pairs

def consensus_positions(references):
    """references: list of per-reference {query_pos: (qaa, saa)} maps (same
    query coordinate system). Returns {query_pos: consensus_aa} where >=
    CONSERVATION of covering references agree on the residue."""
    from collections import Counter
    cov = {}
    for ref in references:
        for qp, (qaa, saa) in ref.items():
            cov.setdefault(qp, []).append(saa)
    out = {}
    for qp, aas in cov.items():
        if len(aas) < 3:
            continue
        aa, n = Counter(aas).most_common(1)[0]
        if n / len(aas) >= CONSERVATION:
            out[qp] = (aa, len(aas), n)
    return out

def unique_substitutions(query, reference_seqs, aligner=None):
    """Full pipeline: query vs each reference; find conserved reference
    positions where query differs. Returns list of
    {query_pos, query_aa, consensus_aa, n_refs, n_agree}."""
    aligner = aligner or _aligner()
    maps = []
    for ref in reference_seqs:
        pairs = aligned_residue_map(query, ref, aligner)
        maps.append({qp: (qaa, saa) for qp, qaa, sp, saa in pairs})
    cons = consensus_positions(maps)
    subs = []
    for qp, (caa, n_refs, n_agree) in sorted(cons.items()):
        qaa = None
        for m in maps:
            if qp in m:
                qaa = m[qp][0]
                break
        if qaa and qaa != caa:
            subs.append({"query_pos": qp, "query_aa": qaa, "consensus_aa": caa,
                         "n_refs": n_refs, "n_agree": n_agree})
    return subs


def unique_substitutions_with_stats(query, reference_seqs, aligner=None):
    """As unique_substitutions, plus alignment diagnostics:
    n_aligned_positions = distinct query positions covered by >=1 reference;
    n_conserved_positions = positions passing the conservation rule;
    rates per eq. 12 (substitutions per aligned / per conserved position)."""
    aligner = aligner or _aligner()
    maps = []
    for ref in reference_seqs:
        pairs = aligned_residue_map(query, ref, aligner)
        maps.append({qp: (qaa, saa) for qp, qaa, sp, saa in pairs})
    covered = set()
    for m in maps:
        covered |= set(m)
    cons = consensus_positions(maps)
    subs = []
    for qp, (caa, n_refs, n_agree) in sorted(cons.items()):
        qaa = None
        for m in maps:
            if qp in m:
                qaa = m[qp][0]
                break
        if qaa and qaa != caa:
            subs.append({"query_pos": qp, "query_aa": qaa, "consensus_aa": caa,
                         "n_refs": n_refs, "n_agree": n_agree})
    n_aln, n_cons = len(covered), len(cons)
    stats = {"n_aligned_positions": n_aln,
             "n_conserved_positions": n_cons,
             "rate_per_aligned_position": (len(subs) / n_aln) if n_aln else None,
             "rate_per_conserved_position": (len(subs) / n_cons) if n_cons else None}
    return subs, stats
