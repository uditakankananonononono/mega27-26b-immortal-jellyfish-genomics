"""The DNA-repair / telomerase-pathway gene panel for MEGA27-26b.

Lane G's 18-gene panel, extended with the DNA-polymerase proofreading arm
(POLD1/POLD2/POLE) and telomerase-regulating pathway genes named in the
26b assignment. Each entry: gene symbol, pathway group, human RefSeq
protein accession (canonical), and UniProt id for cross-checking.
"""
PANEL = [
    # (symbol, group, human RefSeq protein, UniProt)
    ("TERT",  "telomerase", "NP_937983.2",  "O14746"),
    ("TERC",  "telomerase", None,           None),   # RNA gene, no protein
    ("DKC1",  "telomerase", "NP_001354.1",  "O60832"),
    ("POT1",  "shelterin",  "NP_056925.2",  "Q9NUX5"),
    ("TERF1", "shelterin",  "NP_059523.2",  "P54274"),
    ("TERF2", "shelterin",  "NP_005643.1",  "Q15554"),
    ("POLD1", "polymerase", "NP_002682.2",  "P28340"),
    ("POLD2", "polymerase", "NP_006221.1",  "P49005"),
    ("POLE",  "polymerase", "NP_006222.2",  "Q07864"),
    ("BRCA1", "repair-HR",  "NP_009225.1",  "P38398"),
    ("RAD51", "repair-HR",  "NP_002866.2",  "Q06609"),
    ("PARP1", "repair-BER", "NP_001609.2",  "P09874"),
    ("MLH1",  "repair-MMR", "NP_000240.1",  "P40692"),
    ("MSH2",  "repair-MMR", "NP_000242.1",  "P43246"),
    ("ERCC1", "repair-NER", "NP_001974.1",  "P07992"),
    ("ERCC2", "repair-NER", "NP_000391.1",  "P18074"),
    ("XRCC1", "repair-BER", "NP_006288.2",  "P18887"),
    ("XRCC5", "repair-NHEJ","NP_066964.1",  "P13010"),
    ("LIG4",  "repair-NHEJ","NP_002303.2",  "P49917"),
    ("FEN1",  "repair-BER", "NP_004102.1",  "P39748"),
    ("OGG1",  "repair-BER", "NP_002533.1",  "O15527"),
]
GROUPS = sorted({g for _, g, _, _ in PANEL})
SYMBOLS = [s for s, _, _, _ in PANEL]
