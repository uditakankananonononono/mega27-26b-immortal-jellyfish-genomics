from jellyfish.xpanel import PANEL_B, PANEL_C, SYMBOLS_B, SYMBOLS_C, panel_of

def test_panel_sizes_frozen():
    assert len(SYMBOLS_B) == 24 and len(set(SYMBOLS_B)) == 24
    assert len(SYMBOLS_C) == 24 and len(set(SYMBOLS_C)) == 24

def test_apoe_shared_counted_once():
    assert "APOE" in SYMBOLS_B and "APOE" in SYMBOLS_C
    assert panel_of("APOE") == ("B", "C")

def test_entries_have_annotations():
    for sym, grp, note in PANEL_B + PANEL_C:
        assert sym and grp and note
