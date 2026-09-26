import jellyfish.xaees as xa


def _ledger():
    best = {"total_bits": 600.0, "best_qcov": 0.8, "best_pident": 90.0}
    return {
        "Tdohrnii": {"G1": {"n_strong": 1, "best": dict(best)}, "G2": {"n_strong": 0}},
        "TdohrniiOviedo": {"G1": {"n_strong": 1, "best": dict(best)}, "G2": {"n_strong": 0}},
        "Trubra": {"G1": {"n_strong": 1, "best": dict(best)}},
    }


def test_absence_is_not_detected_never_absent():
    t = xa.aees_table(_ledger())
    assert t["Tdohrnii"]["G2"]["status"] == "not detected"
    assert t["Tdohrnii"]["G2"]["present"] is False


def test_concordance_boosts_tdohrnii_score():
    t = xa.aees_table(_ledger())
    td = t["Tdohrnii"]["G1"]
    tr = t["Trubra"]["G1"]
    assert td["components"]["concordance"] == 1.0
    # both at cap: td = 0.35*1 + 0.25*0.8 + 0.15*0.9 + 0.25*1 = 0.935
    assert abs(td["aees"] - 0.935) < 1e-3
    # single-assembly renormalized: (0.35*1+0.25*0.8+0.15*0.9)/0.75 = 0.9133
    assert abs(tr["aees"] - 0.9133) < 1e-3


def test_confidence_labels():
    assert xa.confidence_label(0.9) == "high"
    assert xa.confidence_label(0.5) == "moderate"
    assert xa.confidence_label(0.2) == "low"
