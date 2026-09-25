"""Expand the ortholog reference panel with 5 more species (accession-level fetches).
Acropora + Orbicella + Exaiptasia (anthozoan cnidarians), Drosophila (bilaterian outgroup),
Xenoturbella (basal bilaterian). Same live-resolution method as fetch_panel."""
import json, time, sys, os, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jellyfish.panel import PANEL

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
SPECIES = {"Acropora": "Acropora digitifera", "Orbicella": "Orbicella faveolata",
           "Exaiptasia": "Exaiptasia diaphana", "Drosophila": "Drosophila melanogaster",
           "Xenoturbella": "Xenoturbella bocki"}

def eutils(ep, **params):
    q = urllib.parse.urlencode(params) + "&tool=mega27_26b&email=udita@example.com"
    for a in range(4):
        try:
            with urllib.request.urlopen(BASE + ep + "?" + q, timeout=60) as r:
                return r.read()
        except Exception:
            time.sleep(1.5 * (a + 1))
    raise RuntimeError("eutils failed")

def resolve(sp, sym):
    for term in (f'"{sp}"[Organism] AND {sym}[All Fields] AND refseq[filter]',
                 f'"{sp}"[Organism] AND {sym}[All Fields]'):
        root = ET.fromstring(eutils("esearch.fcgi", db="protein", term=term, retmax=5))
        ids = [i.text for i in root.findall(".//Id")]
        time.sleep(0.4)
        if ids:
            best, blen, bacc = None, -1, None
            for uid in ids[:5]:
                fa = eutils("efetch.fcgi", db="protein", id=uid, rettype="fasta", retmode="text").decode()
                time.sleep(0.4)
                seq = "".join(l for l in fa.splitlines() if not l.startswith(">"))
                acc = fa.split("|")[1].split()[0] if "|" in fa.splitlines()[0] else fa.splitlines()[0][1:].split()[0]
                if len(seq) > blen:
                    best, blen, bacc = fa, len(seq), acc
            return bacc, best
    return None, None

def main():
    m = json.load(open("results/panel_manifest.json"))
    m.setdefault("expanded", {})
    for short, sp in SPECIES.items():
        m["expanded"][sp] = {}
        for sym, grp, refseq, uniprot in PANEL:
            if sym == "TERC":
                continue
            if os.path.exists(f"data/panel/{short}_{sym}.faa"):
                continue
            acc, fa = resolve(sp, sym)
            if fa:
                open(f"data/panel/{short}_{sym}.faa", "w").write(fa)
            m["expanded"][sp][sym] = acc
            time.sleep(0.3)
        print(sp, sum(1 for v in m["expanded"][sp].values() if v), "fetched", flush=True)
        json.dump(m, open("results/panel_manifest.json", "w"), indent=1)
    json.dump(m, open("results/panel_manifest.json", "w"), indent=1)

if __name__ == "__main__":
    main()
