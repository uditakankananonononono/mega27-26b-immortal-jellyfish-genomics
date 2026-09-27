"""P1 #11: fetch 24 non-aging decoy genes (olfaction/structural/digestion/vision/
blood) via UniProt exact-gene match - same verified route as the D9 repair."""
import json, os, time, urllib.parse, urllib.request
OUT = "data/xpanel_decoy"
os.makedirs(OUT, exist_ok=True)
GENES = ["OR1A1","OR2J3","OR5AN1","KRT1","KRT5","KRT14","HBA1","HBB","MB","ALB",
         "AMY1A","LCT","TTN","DMD","MYH7","FLG","OPN1LW","CSN2","AMELX","ACTA1",
         "RHO","SLC26A5","TAS2R38","MUC7"]
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
print("DECOYDONE", sum(1 for v in rep.values() if v["status"]=="ok"), "/", len(GENES))
