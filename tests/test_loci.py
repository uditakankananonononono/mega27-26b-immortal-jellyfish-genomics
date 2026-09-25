from jellyfish.loci import cluster_loci, region_bounds

def h(contig, s, e, bits=100, pident=50, qcov=0.5):
    return {"contig": contig, "sstart": s, "send": e, "bits": bits,
            "pident": pident, "qcov": qcov}

def test_cluster_same_contig_close():
    loci = cluster_loci([h("c1", 1000, 2000), h("c1", 5000, 6000)])
    assert len(loci) == 1 and loci[0]["n_hsps"] == 2

def test_cluster_split_by_span():
    loci = cluster_loci([h("c1", 1000, 2000), h("c1", 200000, 201000)])
    assert len(loci) == 2

def test_cluster_split_by_contig():
    loci = cluster_loci([h("c1", 1000, 2000), h("c2", 1000, 2000)])
    assert len(loci) == 2

def test_ranked_by_bits():
    loci = cluster_loci([h("c1", 1000, 2000, bits=50), h("c2", 1000, 2000, bits=500)])
    assert loci[0]["contig"] == "c2"

def test_region_bounds_floor():
    lo, hi = region_bounds({"start": 100, "end": 5000}, flank=20000)
    assert lo == 1 and hi == 25000
