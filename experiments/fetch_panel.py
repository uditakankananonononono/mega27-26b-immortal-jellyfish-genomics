"""Fetch the 21-gene panel's reference proteins + run the live annotation-desert audit.

Desert audit: for each panel gene and each target jellyfish, query NCBI
gene/protein with organism scope. Zero hits = desert stands (at annotation level).
Reference fetch: human RefSeq protein per accession (accession-level records,
one fetch each), plus cnidarian orthologs (esearch -> best RefSeq protein).
Outputs: results/desert_audit.json, data/panel/*.faa, results/panel_manifest.json
"""
import json, time, urllib.parse, urllib.request, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jellyfish.panel import PANEL

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
CONTACT = "tool=mega27_26b&email=udita@example.com"
JELLIES = ["Turritopsis dohrnii", "Aurelia aurita"]
CNIDARIA = ["Nematostella vectensis", "Hydra vulgaris", "Clytia hemisphaerica"]

def eutils(ep, **params):
    q = urllib.parse.urlencode(params) + "&" + CONTACT
    last = None
    for attempt in range(5):
        try:
            with urllib.request.urlopen(BASE + ep + "?" + q, timeout=60) as r:
                return r.read()
        except Exception as e:
            last = e
            time.sleep(1.5 * (attempt + 1))
    print('FAILING URL:', BASE + ep + '?' + q)
    raise last

def esearch_count(db, term):
    import xml.etree.ElementTree as ET
    root = ET.fromstring(eutils("esearch.fcgi", db=db, term=term, retmax=5))
    return int(root.findtext("Count")), [i.text for i in root.findall(".//Id")]

def main():
    os.makedirs("data/panel", exist_ok=True)
    audit = {}
    # 1. desert audit (gene + protein db, both jellies, all genes)
    for jelly in JELLIES:
        audit[jelly] = {}
        for sym, grp, refseq, uniprot in PANEL:
            term = f'"{jelly}"[Organism] AND {sym}[Gene Name]'
            c_gene, _ = esearch_count("gene", term); time.sleep(0.4)
            c_prot, ids = esearch_count("protein", term); time.sleep(0.4)
            audit[jelly][sym] = {"gene_db": c_gene, "protein_db": c_prot, "protein_ids": ids}
    json.dump(audit, open("results/desert_audit.json", "w"), indent=1)

    # 2. human reference proteins: resolve current RefSeq live (no stale accessions)
    import xml.etree.ElementTree as ET
    def resolve_and_fetch(sp, sym):
        term = f'"{sp}"[Organism] AND {sym}[All Fields] AND refseq[filter]'
        root = ET.fromstring(eutils("esearch.fcgi", db="protein", term=term, retmax=5))
        ids = [i.text for i in root.findall(".//Id")]
        if not ids:
            return None, None
        # prefer the longest record (canonical isoform proxy) among first 5
        best, best_len, best_acc = None, -1, None
        for uid in ids[:5]:
            time.sleep(0.4)
            fa = eutils("efetch.fcgi", db="protein", id=uid, rettype="fasta", retmode="text").decode()
            seq = "".join(l for l in fa.splitlines() if not l.startswith(">"))
            acc = fa.split("|")[1].split()[0] if "|" in fa.splitlines()[0] else fa.splitlines()[0][1:].split()[0]
            if len(seq) > best_len:
                best, best_len, best_acc = fa, len(seq), acc
        return best_acc, best
    manifest = {"human": {}, "cnidaria": {}}
    for sym, grp, refseq, uniprot in PANEL:
        if sym == "TERC":
            manifest["human"][sym] = None; continue
        acc, fa = resolve_and_fetch("Homo sapiens", sym)
        if fa:
            open(f"data/panel/human_{sym}.faa", "w").write(fa)
        manifest["human"][sym] = acc
        time.sleep(0.4)

    # 3. cnidarian orthologs: best RefSeq protein per (species, gene)
    for sp in CNIDARIA:
        manifest["cnidaria"][sp] = {}
        for sym, grp, refseq, uniprot in PANEL:
            if sym == "TERC":
                manifest["cnidaria"][sp][sym] = None; continue
            acc, fa = resolve_and_fetch(sp, sym)
            if fa:
                open(f"data/panel/{sp.split()[0]}_{sym}.faa", "w").write(fa)
            manifest["cnidaria"][sp][sym] = acc
            time.sleep(0.4)
    json.dump(manifest, open("results/panel_manifest.json", "w"), indent=1)
    desert = {j: sum(1 for g in audit[j].values() if g["gene_db"] == 0 and g["protein_db"] == 0) for j in JELLIES}
    print("desert (genes with zero records):", desert)
    print("human fetched:", sum(1 for v in manifest["human"].values() if v))
    print("cnidaria:", {sp: sum(1 for v in d.values() if v) for sp, d in manifest["cnidaria"].items()})

if __name__ == "__main__":
    main()
