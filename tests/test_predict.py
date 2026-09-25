from jellyfish.predict import translate, revcomp, stitch

def test_translate_atg():
    assert translate("ATGGCTTAA") == "MA*"

def test_revcomp():
    assert revcomp("AAGC") == "GCTT"

def test_stitch_single():
    # embed a known ORF in a fake locus
    orf = "ATG" + "GCT" * 30 + "TAA"
    seq = "N" * 100 + orf + "N" * 100
    hsps = [{"qstart": 1, "qend": 31, "sstart": 101, "send": 101 + len(orf) - 1,
             "bits": 100, "pident": 90, "qcov": 0.9}]
    res = stitch(hsps, seq, 1)
    assert res["protein"].startswith("MAA") or "A" * 10 in res["protein"]
    assert res["n_segments"] == 1

def test_stitch_orders_by_query():
    seq = "N" * 1000
    hsps = [{"qstart": 50, "qend": 60, "sstart": 500, "send": 560, "bits": 50, "pident": 50, "qcov": 0.2},
            {"qstart": 1, "qend": 40, "sstart": 100, "send": 160, "bits": 50, "pident": 50, "qcov": 0.2}]
    res = stitch(hsps, seq, 1)
    assert [s["qstart"] for s in res["segments"]] == [1, 50]
