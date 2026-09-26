#!/usr/bin/env python3
"""Part 3: ATG5 validation support + species grounding from external resources."""
import json, os, sys, time, urllib.request, urllib.parse
OUT = "results/xext"
def get(url, timeout=60, headers=None):
    h = {"User-Agent": "mega27-26b-research/1.0"}
    if headers: h.update(headers)
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")
def save(name, obj):
    json.dump(obj, open(f"{OUT}/x-ext-{name}.json", "w"), indent=1)
    print(f"{name}: {obj.get('status')}", flush=True)
step = sys.argv[1]
if step == "a":
    # InterPro: domains of human ATG5 (Q9H1Y0)
    try:
        j = json.loads(get("https://www.ebi.ac.uk/interpro/api/protein/UniProt/Q9H1Y0"))
        ents = [{"accession": e.get("metadata", {}).get("accession"), "name": e.get("metadata", {}).get("name"),
                 "db": e.get("metadata", {}).get("source_database")} for e in j.get("results", [])[:15]]
        save("interpro-atg5", {"status": f"ok n={j.get('count')}", "entries": ents})
    except Exception as e: save("interpro-atg5", {"status": f"error: {e}"})
    # STRING: ATG5-ATG7-BECN1 module network
    try:
        j = json.loads(get("https://string-db.org/api/json/network?identifiers=ATG5%0dATG7%0dBECN1%0dSQSTM1&species=9606"))
        edges = [{"a": e.get("preferredName_A"), "b": e.get("preferredName_B"), "score": e.get("score")} for e in j]
        save("string-module", {"status": f"ok n={len(edges)}", "edges": edges})
    except Exception as e: save("string-module", {"status": f"error: {e}"})
    # Reactome: human ATG5 pathways
    try:
        j = json.loads(get("https://reactome.org/ContentService/data/mapping/UniProt/Q9H1Y0/pathways"))
        pws = [{"id": p.get("stId"), "name": p.get("displayName")} for p in j[:20]]
        save("reactome-atg5", {"status": f"ok n={len(j)}", "pathways": pws})
    except Exception as e: save("reactome-atg5", {"status": f"error: {e}"})
    # PDBe: structures for human ATG5
    try:
        j = json.loads(get("https://www.ebi.ac.uk/pdbe/search/pdb/select?q=uniprot_accession:Q9H1Y0&wt=json&rows=10"))
        docs = [{"pdb": d.get("pdb_id"), "title": (d.get("title") or "")[:60]} for d in j.get("response", {}).get("docs", [])]
        save("pdbe-atg5", {"status": f"ok n={len(docs)}", "structures": docs})
    except Exception as e: save("pdbe-atg5", {"status": f"error: {e}"})
    # Open Targets: ATG5 disease associations
    try:
        body = json.dumps({"query": "{ search(queryString:\"ATG5\", entityNames:[\"target\"]) { hits { id name } } }"})
        j = json.loads(get("https://api.platform.opentargets.org/api/v4/graphql", headers={"Content-Type": "application/json"}))
        save("opentargets-atg5", {"status": "error: not-implemented-post"})
    except Exception as e: save("opentargets-atg5", {"status": f"error: {e}"})
    # Ensembl REST: human ATG5 xref
    try:
        j = json.loads(get("https://rest.ensembl.org/xrefs/symbol/homo_sapiens/ATG5?content-type=application/json"))
        save("ensembl-atg5", {"status": f"ok n={len(j)}", "ids": [e.get("id") for e in j[:5]]})
    except Exception as e: save("ensembl-atg5", {"status": f"error: {e}"})
elif step == "b":
    # NCBI Taxonomy: taxids of 8 species
    spp = ["Turritopsis dohrnii", "Turritopsis rubra", "Aurelia aurita", "Clytia hemisphaerica",
           "Nematostella vectensis", "Morbakka virulenta", "Hydra vulgaris"]
    tax = {}
    for s in spp:
        try:
            j = json.loads(get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=taxonomy&retmode=json&term=" + urllib.parse.quote(f'"{s}"[Scientific Name]')))
            tax[s] = (j.get("esearchresult", {}).get("idlist") or [None])[0]
        except Exception as e: tax[s] = f"error"
        time.sleep(0.35)
    save("ncbi-taxonomy", {"status": "ok", "taxids": tax})
    # WoRMS: T. dohrnii marine taxonomy
    try:
        j = json.loads(get("https://www.marinespecies.org/rest/AphiaRecordsByName/Turritopsis%20dohrnii?like=false&marine_only=false"))
        r = (j or [{}])[0]
        save("worms-td", {"status": "ok", "aphia": r.get("AphiaID"), "valid_name": r.get("valid_name"), "rank": r.get("rank")})
    except Exception as e: save("worms-td", {"status": f"error: {e}"})
    # GBIF: T. dohrnii occurrences
    try:
        j = json.loads(get("https://api.gbif.org/v1/species/match?name=Turritopsis%20dohrnii"))
        key = j.get("usageKey")
        c = json.loads(get(f"https://api.gbif.org/v1/occurrence/count?taxon_key={key}"))
        save("gbif-td", {"status": "ok", "usageKey": key, "occurrences": c})
    except Exception as e: save("gbif-td", {"status": f"error: {e}"})
    # Open Tree of Life: TNRS for 7 species
    try:
        names = "%2C".join(urllib.parse.quote(s) for s in spp)
        j = json.loads(get(f"https://api.opentreeoflife.org/v3/tnrs/match_names?names={names}", headers={"Content-Type": "application/json"}))
        matched = [r.get("matches", [{}])[0].get("taxon", {}).get("ott_id") for r in j.get("results", [])]
        save("otl-species", {"status": f"ok {sum(1 for m in matched if m)}/{len(spp)}", "ott_ids": matched})
    except Exception as e: save("otl-species", {"status": f"error: {e}"})
    # CrossRef: verify Kulviwat/ISEF-adjacent + key refs
    try:
        j = json.loads(get("https://api.crossref.org/works?query.bibliographic=claudin-5%20biomarker%20suicide%20Kulviwat&rows=3"))
        items = [{"title": (i.get("title") or [""])[0][:80], "doi": i.get("DOI")} for i in j.get("message", {}).get("items", [])]
        save("crossref-refs", {"status": "ok", "items": items})
    except Exception as e: save("crossref-refs", {"status": f"error: {e}"})
    # NCBI BioProject for the SRA census runs
    try:
        j = json.loads(get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=bioproject&retmode=json&term=" + urllib.parse.quote('"Turritopsis dohrnii"[Organism]')))
        save("ncbi-bioproject", {"status": "ok", "count": j.get("esearchresult", {}).get("count"), "ids": j.get("esearchresult", {}).get("idlist", [])[:10]})
    except Exception as e: save("ncbi-bioproject", {"status": f"error: {e}"})
