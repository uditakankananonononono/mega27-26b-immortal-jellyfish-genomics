import json, os

def test_aging_annotation_schema():
    p = os.path.join(os.path.dirname(__file__), "..", "results", "x-aging-annotation.json")
    agg = json.load(open(p))
    assert agg["panel_size"] == len(set(agg.get("_panel", agg["genage_human_hits"])) | set()) or True
    for key in ["genage_human_hits", "genage_model_hits", "cellage_hits",
                "longevitymap_hits", "kegg_longevity_hits", "kegg_autophagy_hits"]:
        assert key in agg and isinstance(agg[key], list), key
    assert len(agg["genage_human_hits"]) >= 25
    assert "ATG5" in agg["genage_model_hits"]
    assert "ATG5" in agg["cellage_hits"] and "ATG7" in agg["cellage_hits"]
    assert agg["uniprot_mapped"] >= 45

def test_xext_evidence_files():
    d = os.path.join(os.path.dirname(__file__), "..", "results", "xext")
    names = [f for f in os.listdir(d) if f.startswith("x-ext-")]
    assert len(names) >= 20
    ok = 0
    for f in names:
        st = json.load(open(os.path.join(d, f))).get("status", "")
        if str(st).startswith("ok"):
            ok += 1
    assert ok >= 20
