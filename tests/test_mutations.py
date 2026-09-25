from jellyfish.mutations import aligned_residue_map, consensus_positions, unique_substitutions

def test_aligned_map_identical():
    pairs = aligned_residue_map("MAGA", "MAGA")
    assert len(pairs) == 4 and all(q == s for _, q, _, s in pairs)

def test_consensus_requires_three_refs():
    refs = [{1: ("A", "G"), 2: ("V", "L")}, {1: ("A", "G"), 2: ("V", "L")}]
    assert consensus_positions(refs) == {}  # only 2 refs

def test_unique_substitution_detected():
    q = "ARND"
    refs = ["AGND", "AGND", "AGND", "AGND"]  # position 2: G in all refs, R in query
    subs = unique_substitutions(q, refs)
    assert any(s["query_pos"] == 2 and s["query_aa"] == "R" and s["consensus_aa"] == "G" for s in subs)

def test_no_substitution_when_matching():
    subs = unique_substitutions("AGND", ["AGND", "AGND", "AGND"])
    assert subs == []
