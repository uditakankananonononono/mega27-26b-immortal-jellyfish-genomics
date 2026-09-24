"""Fetch real repair/telomerase gene records from NCBI for the 3 species."""
import json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from jellygen.ncbi import fetch_gene_set, parse_fasta
from jellygen.compare import DNA_REPAIR_GENES, TELOMERASE_GENES

SPECIES = {"hvulgaris": "Hydra vulgaris"}
OUT = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT, exist_ok=True)
manifest = {}
for sp_key, sp_name in SPECIES.items():
    for gene in DNA_REPAIR_GENES + TELOMERASE_GENES:
        fn = os.path.join(OUT, f"{sp_key}_{gene}.fasta")
        if os.path.exists(fn):
            continue
        try:
            txt = fetch_gene_set(gene, sp_name, retmax=4)
            recs = parse_fasta(txt) if txt else []
            with open(fn, "w") as f:
                f.write(txt)
            manifest[f"{sp_key}_{gene}"] = len(recs)
            print(sp_key, gene, len(recs), flush=True)
        except Exception as e:
            manifest[f"{sp_key}_{gene}"] = f"ERROR {e}"
            print(sp_key, gene, "ERROR", e, flush=True)
        time.sleep(0.4)
with open(os.path.join(OUT, "manifest.json"), "w") as f:
    json.dump(manifest, f, indent=1)
print("DONE", sum(1 for v in manifest.values() if isinstance(v, int) and v > 0), "nonempty")
