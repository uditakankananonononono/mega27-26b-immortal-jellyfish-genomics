#!/usr/bin/env python3
"""Part 2 of external annotation: cellage/anage/uniprot/kegg/europepmc/alphafold + aggregate."""
import json, os, sys, time, urllib.request, urllib.parse, zipfile, io, csv
OUT = "results/xext"
def get(url, raw=False, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "mega27-26b-research/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read() if raw else r.read().decode("utf-8", "replace")
def save(name, obj):
    with open(f"{OUT}/x-ext-{name}.json", "w") as f:
        json.dump(obj, f, indent=1)
    print(f"saved {name}", flush=True)
def hagr_csv(url):
    b = get(url, raw=True)
    if url.endswith(".zip"):
        z = zipfile.ZipFile(io.BytesIO(b))
        fn = [n for n in z.namelist() if n.endswith((".csv", ".tsv"))][0]
        txt = z.read(fn).decode("utf-8", "replace")
    else:
        txt = b.decode("utf-8", "replace")
    dialect = "excel-tab" if "\t" in txt.splitlines()[0] else "excel"
    return list(csv.DictReader(io.StringIO(txt), dialect=dialect))
from jellyfish.xpanel import SYMBOLS_B, SYMBOLS_C
PANEL = sorted(set(SYMBOLS_B) | set(SYMBOLS_C))
step = sys.argv[1] if len(sys.argv) > 1 else "all"
if step == "part1":
    agg = {}
    rows = hagr_csv("https://genomics.senescence.info/genes/human_genes.zip")
    gh = {(r.get("symbol") or "").strip().upper() for r in rows}
    agg["genage_human_hits"] = sorted(s for s in PANEL if s.upper() in gh)
    rows = hagr_csv("https://genomics.senescence.info/genes/models_genes.zip")
    gm = {(r.get("symbol") or "").strip().upper() for r in rows}
    agg["genage_model_hits"] = sorted(s for s in PANEL if s.upper() in gm)
    rows = hagr_csv("https://genomics.senescence.info/cells/cellAge.zip")
    ca = {(r.get("Gene symbol") or "").strip().upper() for r in rows}
    agg["cellage_hits"] = sorted(s for s in PANEL if s.upper() in ca)
    save("cellage", {"status": "ok", "n_rows": len(rows)})
    rows = hagr_csv("https://genomics.senescence.info/longevity/longevity_genes.zip")
    lm = {g.strip().upper() for r in rows for g in (r.get("Gene(s)") or r.get("symbol") or "").split(",") if g.strip()}
    agg["longevitymap_hits"] = sorted(s for s in PANEL if s.upper() in lm)
    try:
        rows = hagr_csv("https://genomics.senescence.info/species/anage_data.zip")
        cnid = [r for r in rows if r.get("Class") in ("Anthozoa","Hydrozoa","Scyphozoa","Cubozoa","Staurozoa")]
        recs = [{"species": f"{r.get('Genus','')} {r.get('Species','')}".strip(),
                 "max_longevity_yr": r.get("Maximum longevity (yrs)", "")} for r in cnid]
        save("anage-cnidaria", {"status": "ok", "n": len(recs), "records": recs[:40]})
        agg["anage_cnidaria_n"] = len(recs)
    except Exception as e:
        save("anage-cnidaria", {"status": f"error: {e}"})
    json.dump(agg, open(f"{OUT}/_agg1.json", "w"), indent=1)
    print(json.dumps({k: len(v) if isinstance(v, list) else v for k, v in agg.items()}), flush=True)
elif step == "part2":
    uni, ok = {}, 0
    for sym in PANEL:
        try:
            q = urllib.parse.quote(f"gene:{sym} AND organism_id:9606 AND reviewed:true")
            j = json.loads(get(f"https://rest.uniprot.org/uniprotkb/search?query={q}&fields=accession,protein_name&size=1&format=json"))
            ent = (j.get("results") or [{}])[0]
            uni[sym] = {"accession": ent.get("primaryAccession")}
            if ent.get("primaryAccession"): ok += 1
        except Exception as e:
            uni[sym] = {"error": str(e)[:100]}
        time.sleep(0.12)
    save("uniprot-panel", {"status": f"ok {ok}/{len(PANEL)}", "genes": uni})
    print(f"uniprot {ok}/{len(PANEL)}", flush=True)
elif step == "part3":
    txt = get("https://rest.kegg.jp/link/hsa/path:hsa04211") + get("https://rest.kegg.jp/link/hsa/path:hsa04213")
    kegg_long = {l.split(":")[1].strip() for l in txt.splitlines() if l.strip()}
    kegg_auto = {l.split(":")[1].strip() for l in get("https://rest.kegg.jp/link/hsa/path:hsa04140").splitlines() if l.strip()}
    id2sym = {}
    for line in get("https://rest.kegg.jp/list/hsa").splitlines():
        kid, desc = line.split("\t", 1)
        id2sym[kid.split(":")[1]] = desc.split(";")[0].split(",")[0].strip()
    long_hits = sorted(s for s in PANEL if s in {id2sym.get(k,"") for k in kegg_long})
    auto_hits = sorted(s for s in PANEL if s in {id2sym.get(k,"") for k in kegg_auto})
    save("kegg-longevity", {"status": "ok", "longevity_hits": long_hits, "autophagy_hits": auto_hits})
    epmc = {}
    for sym in ["ATG5","ATG7","BECN1","SIRT1","SIRT6","GRN","TERT","FOXO3"]:
        try:
            q = urllib.parse.quote(f'"Turritopsis dohrnii" AND "{sym}"')
            epmc[sym] = json.loads(get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={q}&format=json&pageSize=1")).get("hitCount", 0)
        except Exception as e:
            epmc[sym] = str(e)[:60]
        time.sleep(0.25)
    try:
        epmc["_Td_total"] = json.loads(get("https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%22Turritopsis%20dohrnii%22&format=json&pageSize=1")).get("hitCount",0)
    except Exception: pass
    save("europepmc-literature", {"status": "ok", "counts": epmc})
    try:
        r = json.loads(get("https://alphafold.ebi.ac.uk/api/prediction/Q9H1Y0"))[0]
        save("alphafold-atg5", {"status": "ok", "uniprot": r.get("uniprotAccession"), "gene": r.get("gene")})
    except Exception as e:
        save("alphafold-atg5", {"status": f"error: {e}"})
    # final aggregate
    agg = json.load(open(f"{OUT}/_agg1.json"))
    agg["uniprot_mapped"] = sum(1 for v in uni_all.values() if v.get("accession")) if (uni_all := json.load(open(f"{OUT}/x-ext-uniprot-panel.json"))["genes"]) else 0
    agg["kegg_longevity_hits"] = long_hits
    agg["kegg_autophagy_hits"] = auto_hits
    agg["panel_size"] = len(PANEL)
    json.dump(agg, open("results/x-aging-annotation.json", "w"), indent=1)
    print(json.dumps(agg)[:600], flush=True)
