#!/usr/bin/env python3
"""External-database annotation of the 48-gene aging/longevity panel (exploratory enrichment).
Queries real external resources; each result lands in results/xext/x-ext-<name>.json.
Aggregate membership matrix -> results/x-aging-annotation.json."""
import json, os, sys, time, urllib.request, urllib.parse, zipfile, io, csv

OUT = "results/xext"
os.makedirs(OUT, exist_ok=True)

def get(url, raw=False, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "mega27-26b-research/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        b = r.read()
    return b if raw else b.decode("utf-8", "replace")

def save(name, obj):
    with open(f"{OUT}/x-ext-{name}.json", "w") as f:
        json.dump(obj, f, indent=1)
    print(f"saved {name}: {obj.get('status','?')}", flush=True)

from jellyfish.xpanel import SYMBOLS_B, SYMBOLS_C
PANEL = sorted(set(SYMBOLS_B) | set(SYMBOLS_C))

def fetch_hagr(name, urls):
    for url in urls:
        try:
            b = get(url, raw=True)
            if url.endswith(".zip"):
                z = zipfile.ZipFile(io.BytesIO(b))
                fn = [n for n in z.namelist() if n.endswith(".csv")][0]
                txt = z.read(fn).decode("utf-8", "replace")
            else:
                txt = b.decode("utf-8", "replace")
            rows = list(csv.DictReader(io.StringIO(txt)))
            save(name, {"status": "ok", "source": url, "n_rows": len(rows),
                        "cols": list(rows[0].keys())[:12] if rows else []})
            return rows
        except Exception as e:
            last = str(e)
    save(name, {"status": f"error: {last}", "sources": urls})
    return []

def main():
    agg = {}
    # 1. GenAge human
    rows = fetch_hagr("genage-human", ["https://genomics.senescence.info/genes/human_genes.zip"])
    gh = set()
    for r in rows:
        sym = (r.get("symbol") or r.get("Symbol") or "").strip()
        if sym: gh.add(sym.upper())
    agg["genage_human_hits"] = sorted(s for s in PANEL if s.upper() in gh)
    # 2. GenAge model organisms
    rows = fetch_hagr("genage-models", ["https://genomics.senescence.info/genes/models_genes.zip"])
    gm = set()
    for r in rows:
        sym = (r.get("symbol") or "").strip()
        if sym: gm.add(sym.upper())
    agg["genage_model_hits"] = sorted(s for s in PANEL if s.upper() in gm)
    # 3. CellAge senescence genes
    rows = fetch_hagr("cellage", ["https://genomics.senescence.info/cells/cellAge.zip"])
    ca = set()
    for r in rows:
        sym = (r.get("Gene symbol") or r.get("symbol") or "").strip()
        if sym: ca.add(sym.upper())
    agg["cellage_hits"] = sorted(s for s in PANEL if s.upper() in ca)
    # 4. LongevityMap
    rows = fetch_hagr("longevitymap", ["https://genomics.senescence.info/longevity/longevity_genes.zip"])
    lm = set()
    for r in rows:
        sym = (r.get("symbol") or "").strip()
        if sym: lm.add(sym.upper())
    agg["longevitymap_hits"] = sorted(s for s in PANEL if s.upper() in lm)
    # 5. AnAge cnidarian longevity records
    try:
        txt = get("https://genomics.senescence.info/species/anage_data.txt", timeout=120)
        rdr = csv.DictReader(io.StringIO(txt), delimiter="\t")
        cnid = [r for r in rdr if r.get("Class") in ("Anthozoa", "Hydrozoa", "Scyphozoa", "Cubozoa", "Staurozoa")]
        recs = [{"species": f"{r.get('Genus','')} {r.get('Species','')}".strip(),
                 "max_longevity_yr": r.get("Maximum longevity (yrs)", "")} for r in cnid]
        save("anage-cnidaria", {"status": "ok", "n": len(recs), "records": recs[:40]})
    except Exception as e:
        save("anage-cnidaria", {"status": f"error: {e}"})
    # 6. UniProt annotations for panel genes (human, reviewed)
    uni = {}
    ok = 0
    for sym in PANEL:
        try:
            q = urllib.parse.quote(f"gene:{sym} AND organism_id:9606 AND reviewed:true")
            j = json.loads(get(f"https://rest.uniprot.org/uniprotkb/search?query={q}&fields=accession,protein_name,go_p,cc_function&size=1&format=json"))
            ent = (j.get("results") or [{}])[0]
            uni[sym] = {"accession": ent.get("primaryAccession"),
                        "name": ((ent.get("proteinDescription") or {}).get("recommendedName") or {}).get("fullName", {}).get("value")}
            if ent.get("primaryAccession"): ok += 1
        except Exception as e:
            uni[sym] = {"error": str(e)[:120]}
        time.sleep(0.15)
    save("uniprot-panel", {"status": f"ok {ok}/{len(PANEL)}", "genes": uni})
    agg["uniprot_mapped"] = ok
    # 7. KEGG longevity + autophagy pathways
    try:
        txt = get("https://rest.kegg.jp/link/hsa/path:hsa04211")  # longevity regulating pathway
        kegg_long = set(l.split(":")[1].strip() for l in txt.splitlines() if l.strip())
        txt2 = get("https://rest.kegg.jp/link/hsa/path:hsa04213")  # longevity multiple species
        kegg_long |= set(l.split(":")[1].strip() for l in txt2.splitlines() if l.strip())
        txt3 = get("https://rest.kegg.jp/link/hsa/path:hsa04140")  # autophagy
        kegg_auto = set(l.split(":")[1].strip() for l in txt3.splitlines() if l.strip())
        # map via gene symbols
        symtxt = get("https://rest.kegg.jp/list/hsa")
        id2sym = {}
        for line in symtxt.splitlines():
            kid, desc = line.split("\t", 1)
            id2sym[kid.split(":")[1]] = desc.split(";")[0].split(",")[0].strip()
        long_syms = {id2sym.get(k, "") for k in kegg_long}
        auto_syms = {id2sym.get(k, "") for k in kegg_auto}
        save("kegg-longevity", {"status": "ok",
             "longevity_hits": sorted(s for s in PANEL if s in long_syms),
             "autophagy_hits": sorted(s for s in PANEL if s in auto_syms)})
        agg["kegg_longevity_hits"] = sorted(s for s in PANEL if s in long_syms)
        agg["kegg_autophagy_hits"] = sorted(s for s in PANEL if s in auto_syms)
    except Exception as e:
        save("kegg-longevity", {"status": f"error: {e}"})
    # 8. Europe PMC literature counts (T. dohrnii x gene)
    epmc = {}
    for sym in ["ATG5", "ATG7", "BECN1", "SIRT1", "SIRT6", "GRN", "TERT", "FOXO3"]:
        try:
            q = urllib.parse.quote(f'"Turritopsis dohrnii" AND "{sym}"')
            j = json.loads(get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={q}&format=json&pageSize=1"))
            epmc[sym] = j.get("hitCount", 0)
        except Exception as e:
            epmc[sym] = f"error: {str(e)[:80]}"
        time.sleep(0.3)
    try:
        j = json.loads(get("https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%22Turritopsis%20dohrnii%22&format=json&pageSize=1"))
        epmc["_Td_total"] = j.get("hitCount", 0)
    except Exception: pass
    save("europepmc-literature", {"status": "ok", "counts": epmc})
    # 9. AlphaFold DB: human ATG5 canonical structure
    try:
        j = json.loads(get("https://alphafold.ebi.ac.uk/api/prediction/Q9H1Y0"))
        r = j[0]
        save("alphafold-atg5", {"status": "ok", "uniprot": r.get("uniprotAccession"),
             "gene": r.get("gene"), "model_url": r.get("cifUrl", "")[:80]})
    except Exception as e:
        save("alphafold-atg5", {"status": f"error: {e}"})
    # aggregate
    agg["panel_size"] = len(PANEL)
    with open("results/x-aging-annotation.json", "w") as f:
        json.dump(agg, f, indent=1)
    print("AGG:", json.dumps(agg)[:400], flush=True)

if __name__ == "__main__":
    main()
