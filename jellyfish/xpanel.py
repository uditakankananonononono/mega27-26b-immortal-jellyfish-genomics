"""Expansion panels for MEGA27-26b: aging/longevity (B) and neurology (C).

Gene lists frozen in docs/EXPANSION-PREREGISTRATION.md (main @ 08d8be0).
Each entry: (symbol, subgroup, human-disease/role annotation for routing).
TERC-style RNA genes are excluded: translated search requires protein product.
"""

PANEL_B = [
    ("FOXO3", "stress/longevity-TF", "forkhead longevity-associated TF (GenAge human)"),
    ("SIRT1", "sirtuin", "NAD-dependent deacetylase, aging/metabolism"),
    ("SIRT6", "sirtuin", "chromatin/DNA-repair sirtuin, lifespan in models"),
    ("MTOR", "nutrient-sensing", "mTOR kinase, canonical aging pathway"),
    ("IGF1", "insulin/IGF", "insulin-like growth factor 1"),
    ("IGF1R", "insulin/IGF", "IGF1 receptor, longevity-associated"),
    ("INSR", "insulin/IGF", "insulin receptor"),
    ("AKT1", "insulin/IGF", "AKT kinase, IIS effector"),
    ("PTEN", "insulin/IGF", "PI3K antagonist, tumor suppressor"),
    ("TP53", "genome-guardian", "p53, senescence/apoptosis hub"),
    ("CDKN2A", "senescence", "p16INK4a, canonical senescence marker"),
    ("ATM", "repair-signaling", "ataxia-telangiectasia kinase, aging"),
    ("ATR", "repair-signaling", "ATR checkpoint kinase"),
    ("BLM", "helicase", "Bloom syndrome helicase, progeria"),
    ("WRN", "helicase", "Werner syndrome helicase, adult progeria"),
    ("NFE2L2", "stress/NRF2", "NRF2 oxidative-stress TF, longevity"),
    ("HSF1", "proteostasis", "heat-shock TF, proteostasis in aging"),
    ("ATG5", "autophagy", "autophagy core, lifespan in models"),
    ("ATG7", "autophagy", "autophagy E1 enzyme"),
    ("BECN1", "autophagy", "beclin-1, autophagy initiation"),
    ("TFEB", "lysosome", "lysosomal biogenesis TF"),
    ("PRKAA1", "AMPK", "AMPK catalytic alpha1, energy sensing"),
    ("GHR", "GH axis", "growth hormone receptor, Laron dwarfism longevity"),
    ("APOE", "lipid/neuro", "apolipoprotein E, longevity AND Alzheimer risk"),
]

PANEL_C = [
    ("APP", "Alzheimer", "amyloid precursor protein, Alzheimer disease"),
    ("PSEN1", "Alzheimer", "presenilin-1, early-onset Alzheimer"),
    ("PSEN2", "Alzheimer", "presenilin-2, early-onset Alzheimer"),
    ("MAPT", "tauopathy", "tau, frontotemporal dementia/Alzheimer"),
    ("SNCA", "Parkinson", "alpha-synuclein, Parkinson disease"),
    ("LRRK2", "Parkinson", "LRRK2 kinase, Parkinson disease"),
    ("PARK7", "Parkinson", "DJ-1, early-onset Parkinson"),
    ("PINK1", "Parkinson", "PINK1 kinase, mitophagy, Parkinson"),
    ("PRNP", "prion", "prion protein, CJD/GSS"),
    ("GBA", "LSD/Parkinson", "glucocerebrosidase, Gaucher/Parkinson risk"),
    ("HTT", "Huntington", "huntingtin, polyQ repeat disease"),
    ("SOD1", "ALS", "superoxide dismutase 1, ALS"),
    ("TARDBP", "ALS/FTD", "TDP-43, ALS/frontotemporal dementia"),
    ("FUS", "ALS/FTD", "FUS RNA-binding protein, ALS"),
    ("C9orf72", "ALS/FTD", "C9orf72 repeat expansion, ALS/FTD"),
    ("GRN", "FTD", "progranulin, frontotemporal dementia"),
    ("SQSTM1", "proteostasis/ALS", "p62, ALS/FTD/PDB"),
    ("OPTN", "ALS/glaucoma", "optineurin, ALS"),
    ("VCP", "MSP/ALS", "valosin-containing protein, multisystem proteinopathy"),
    ("UBQLN2", "ALS", "ubiquilin-2, ALS/dementia"),
    ("TREM2", "neuroimmune", "TREM2, Alzheimer risk, microglia"),
    ("BDNF", "neurotrophin", "brain-derived neurotrophic factor"),
    ("NGF", "neurotrophin", "nerve growth factor"),
    # APOE is shared with Panel B per preregistration ("APOE shared with B,
    # counted once"): fetched once, analyzed as a member of BOTH panels -
    # it is the major common Alzheimer-risk gene.
    ("APOE", "lipid/neuro", "apolipoprotein E, Alzheimer risk (shared with B)"),
]

GROUPS_B = sorted({g for _, g, _ in PANEL_B})
GROUPS_C = sorted({g for _, g, _ in PANEL_C})
SYMBOLS_B = [s for s, _, _ in PANEL_B]
SYMBOLS_C = [s for s, _, _ in PANEL_C]
ALL_XSYMBOLS = sorted(set(SYMBOLS_B + SYMBOLS_C + ["APOE"]))

def panel_of(symbol):
    """Return tuple of panels a symbol belongs to ('B','C')."""
    out = []
    if symbol in SYMBOLS_B: out.append("B")
    if symbol in SYMBOLS_C: out.append("C")
    return tuple(out)
