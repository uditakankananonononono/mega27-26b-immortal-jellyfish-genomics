"""P1 #16: fetch the full GenAge human set (307 genes) (olfaction/structural/digestion/vision/
blood) via UniProt exact-gene match - same verified route as the D9 repair."""
import json, os, time, urllib.parse, urllib.request
OUT = "data/xpanel_genage"
os.makedirs(OUT, exist_ok=True)
GENES = ['GHR', 'GHRH', 'SHC1', 'POU1F1', 'PROP1', 'TP53', 'TERC', 'TERT', 'ATM', 'PLAU', 'ERCC2', 'ERCC8', 'WRN', 'LMNA', 'IGF1R', 'TXN', 'KL', 'E2F1', 'PTPN11', 'NFKB2', 'STAT5B', 'STAT3', 'STAT5A', 'NRG1', 'HDAC3', 'GH1', 'IL7R', 'IGF1', 'IGF2', 'INS', 'NGF', 'IRS1', 'PTPN1', 'IRS2', 'AKT1', 'PIK3CB', 'NGFR', 'HRAS', 'MYC', 'EGFR', 'ERBB2', 'INSR', 'NCOR1', 'NBN', 'JUND', 'IL2', 'PDGFB', 'EGF', 'IL2RG', 'FOS', 'PDGFRB', 'EPOR', 'SST', 'PRKCD', 'PPARA', 'RET', 'PLCG2', 'PEX5', 'TCF3', 'PARP1', 'BRCA1', 'PIN1', 'PTEN', 'CREBBP', 'HIF1A', 'UBB', 'RPA1', 'BLM', 'BCL2', 'S100B', 'VCP', 'POLG', 'IGFBP3', 'HSP90AA1', 'NR3C1', 'EGR1', 'VEGFA', 'ABL1', 'BRCA2', 'TOP2A', 'TOP2B', 'NFKB1', 'TOP1', 'RAD51', 'UBE2I', 'TNF', 'PDPK1', 'CEBPA', 'CEBPB', 'MXI1', 'TGFB1', 'ERCC6', 'STK11', 'EP300', 'APTX', 'PML', 'GSK3B', 'HTT', 'PRKCA', 'SSTR3', 'HELLS', 'APOC3', 'EEF2', 'ERCC3', 'TERF1', 'PRKDC', 'CAT', 'ERCC5', 'AR', 'GTF2H2', 'XRCC5', 'PCNA', 'FEN1', 'FAS', 'TERF2', 'XRCC6', 'POLD1', 'BAX', 'RB1', 'EMD', 'GRB2', 'FOXO3', 'FOXO1', 'HSF1', 'XPA', 'MSRA', 'RECQL4', 'SOD2', 'SOD1', 'FOXM1', 'COQ7', 'CACNA1A', 'LRP2', 'AIFM1', 'UCHL1', 'APP', 'APOE', 'A2M', 'SNCG', 'PRDX1', 'PON1', 'RELA', 'IL6', 'RGN', 'ATP5O', 'RAD52', 'TOP3B', 'ERCC1', 'SIRT1', 'HDAC1', 'HSPA9', 'GPX1', 'GSR', 'GSS', 'GSTA4', 'GSTP1', 'MT-CO1', 'HSPD1', 'HSPA1A', 'HSPA1B', 'PCMT1', 'MAPK8', 'YWHAZ', 'PTK2B', 'PTK2', 'IL7', 'MAPK14', 'FGFR1', 'SP1', 'FLT1', 'JUN', 'MED1', 'MAPK9', 'MAPK3', 'HMGB1', 'CCNA2', 'HMGB2', 'MAP3K5', 'TAF1', 'LMNB1', 'SDHC', 'FOXO4', 'HESX1', 'PIK3R1', 'BSCL2', 'AGPAT2', 'BMI1', 'EEF1A1', 'TFAP2A', 'BDNF', 'CREB1', 'ATF2', 'TBP', 'APEX1', 'HBP1', 'BUB1B', 'PTGS2', 'HSPA8', 'SIN3A', 'CDK1', 'TFDP1', 'DDIT3', 'POLA1', 'MAPT', 'CTGF', 'HDAC2', 'MAX', 'MXD1', 'MDM2', 'SUMO1', 'H2AFX', 'HOXB7', 'HOXC4', 'JAK2', 'ESR1', 'LEP', 'LEPR', 'NFKBIA', 'CLU', 'MTOR', 'GHRHR', 'CTNNB1', 'PSEN1', 'DLL3', 'CDKN2A', 'PPP1CA', 'DBN1', 'NOG', 'ELN', 'ATR', 'UCP3', 'ZMPSTE24', 'TP63', 'UCP2', 'POLB', 'GCLC', 'GCLM', 'SIRT6', 'BUB3', 'RAE1', 'PMCH', 'MLH1', 'CSNK1E', 'STUB1', 'PPM1D', 'CHEK2', 'PCK1', 'ARHGAP1', 'CDC42', 'ARNTL', 'CLOCK', 'HIC1', 'PAPPA', 'ADCY5', 'PPARGC1A', 'GPX4', 'UCP1', 'FGF23', 'EFEMP1', 'ERCC4', 'CETP', 'PPARG', 'AGTR1', 'CISD2', 'EEF1E1', 'EPS8', 'KCNA3', 'SIRT7', 'SLC13A1', 'SOCS2', 'TPP2', 'TP53BP1', 'SIRT3', 'NCOR2', 'SUN1', 'BAK1', 'IGFBP2', 'PYCR1', 'TP73', 'CNR1', 'NFE2L2', 'CDKN1A', 'PDGFRA', 'PIK3CA', 'C1QA', 'CDKN2B', 'EIF5A2', 'MIF', 'DGAT1', 'MT1E', 'FGF21', 'HTRA2', 'GSK3A', 'NUDT1', 'IKBKB', 'SQSTM1', 'CDK7', 'GRN', 'SERPINE1', 'SPRTN', 'RICTOR', 'CTF1', 'TRAP1', 'TRPV1', 'NFE2L1', 'IFNB1', 'GDF11']
def get(url):
    for i in range(5):
        try:
            return urllib.request.urlopen(url, timeout=30).read().decode()
        except Exception:
            time.sleep(min(3*(i+1), 15))
    raise RuntimeError(f"fetch failed {url}")
rep = {}
for g in GENES:
    q = urllib.parse.quote(f"gene:{g} AND organism_id:9606 AND reviewed:true")
    rows = [l.split("\t") for l in get(f"https://rest.uniprot.org/uniprotkb/search?query={q}&fields=accession,gene_names,protein_name,length&format=tsv&size=25").splitlines()[1:] if l.strip()]
    rec = next((r for r in rows if r[1].split()[0].upper() == g.upper()), None)
    if not rec:
        rep[g] = {"status": "no_match"}; print(g, "NO MATCH", flush=True); continue
    fa = get(f"https://rest.uniprot.org/uniprotkb/{rec[0]}.fasta")
    seq = "".join(fa.splitlines()[1:]).strip()
    with open(f"{OUT}/human_{g}.faa", "w") as f:
        f.write(f">{rec[0]} {rec[2][:80]} [Homo sapiens] (UniProt {rec[0]}, gene {g})\n")
        for i in range(0, len(seq), 60): f.write(seq[i:i+60] + "\n")
    rep[g] = {"status": "ok", "acc": rec[0], "len": len(seq)}
    print(g, rec[0], len(seq), flush=True)
    time.sleep(0.3)
json.dump(rep, open(f"{OUT}/verify_report.json", "w"), indent=1)
print("GENAGEDONE", sum(1 for v in rep.values() if v["status"]=="ok"), "/", len(GENES))
