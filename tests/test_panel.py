from jellyfish.panel import PANEL, GROUPS, SYMBOLS

def test_panel_size():
    assert len(PANEL) == 21

def test_symbols_unique():
    assert len(SYMBOLS) == len(set(SYMBOLS))

def test_groups_nonempty():
    assert GROUPS and all(isinstance(g, str) for g in GROUPS)

def test_accessions_present_except_rna():
    for sym, grp, refseq, uniprot in PANEL:
        if sym == "TERC":
            assert refseq is None  # RNA gene
        else:
            assert refseq and refseq.startswith("NP_"), sym
