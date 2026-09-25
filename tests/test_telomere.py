import io, os
from jellyfish.telomere import count_motif, census, revcomp

def test_revcomp():
    assert revcomp("TTAGGG") == "CCCTAA"

def test_count_tandem():
    seq = "NNN" + "TTAGGG" * 10 + "NNN"
    assert count_motif(seq, "TTAGGG") == 10

def test_count_revcomp():
    seq = "CCCTAA" * 5
    assert count_motif(seq, "TTAGGG") == 5

def test_census_end_enrichment(tmp_path):
    body = "ACGT" * 5000  # 20 kb body
    tel = "TTAGGG" * 100
    p = tmp_path / "mini.fa"
    p.write_text(">c1\n" + tel + body + tel + "\n")
    res = census(str(p), motifs={"TTAGGG": "test"}, end_window=len(tel))
    m = res["motifs"]["TTAGGG"]
    assert m["end_count"] == 200
    assert m["end_enrichment"] and m["end_enrichment"] > 10
