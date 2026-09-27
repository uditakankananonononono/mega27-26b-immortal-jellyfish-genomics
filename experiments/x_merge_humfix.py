"""D9: merge the 37-query human fix (x-tblastn-humfix.json) into the restored
pre-D9 bc raw hits (wrong human keys dropped), rebuild the locus ledger with
the frozen x_map logic (cluster_loci, MIN_BITS=100), write final bc files."""
import json, sys
sys.path.insert(0, ".")
from jellyfish.loci import cluster_loci
MIN_BITS = 100  # frozen, matches experiments/x_map.py

FIXED37 = ["AKT1","APOE","APP","ATG5","ATM","ATR","BDNF","BECN1","C9orf72","FOXO3","FUS","GBA","GHR","GRN","HSF1","IGF1","IGF1R","INSR","MTOR","NGF","OPTN","PARK7","PINK1","PRKAA1","PRNP","PSEN1","PTEN","SIRT1","SIRT6","SNCA","SOD1","SQSTM1","TFEB","TP53","TREM2","UBQLN2","VCP"]

base = json.load(open("results/x-tblastn-bc.json"))          # restored pre-D9 (cnidarian hits good)
fix = json.load(open("results/x-tblastn-humfix.json"))       # 37 verified human queries
out_raw, out_led = {}, {}
for genome, per_key in base.items():
    pk = {k: v for k, v in per_key.items()
          if not (k.startswith("human_") and k.split("_", 1)[1] in FIXED37)}
    for k, v in fix.get(genome, {}).items():
        pk[k] = v
    out_raw[genome] = pk
    per_gene = {}
    for key, hs in pk.items():
        _, sym = key.split("_", 1)
        per_gene.setdefault(sym, []).extend(hs)
    out_led[genome] = {}
    for sym, hs in per_gene.items():
        loci = cluster_loci(hs)
        strong = [l for l in loci if l["total_bits"] >= MIN_BITS]
        out_led[genome][sym] = {"n_loci": len(loci), "n_strong": len(strong),
                                "best": (strong[0] if strong else (loci[0] if loci else None))}
json.dump(out_raw, open("results/x-tblastn-bc.json", "w"), indent=1)
json.dump(out_led, open("results/x-ledger-bc.json", "w"), indent=1)
for g in out_led:
    print(g, sum(1 for v in out_led[g].values() if v.get("best")), "genes with loci")
print("MERGEDONE")
