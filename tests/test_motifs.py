from jellyfish.motifs import canonical, enrichment, tfbs_counts

def test_canonical():
    assert canonical("AACGTT") == "AACGTT"

def test_enrichment_positive_z():
    tgt = ["CACGTG" * 20] * 3
    bg = ["A" * 100] * 20
    res = enrichment(tgt, bg, k=6, window=40)
    assert res["CACGTG"]["z"] > 5

def test_tfbs_counts_both_strands():
    assert tfbs_counts("AAACACGTGTTT")["E-box_CACGTG"] == 1
    assert tfbs_counts("AAACACGTGTTT")["Myc_max"] == 1

def test_tfbs_revcomp_counted():
    # Sp1 motif GGGCGG revcomp is CCGCCC
    assert tfbs_counts("CCGCCCTTT")["Sp1_GGGCGG"] == 1
