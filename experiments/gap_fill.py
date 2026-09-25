"""Gap-fill missing cnidarian orthologs with protein-name synonym queries.
Each fetched record is an accession-level dataset. Updates panel_manifest + data/panel."""
import json, time, sys, os, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
SYNONYMS = {
    "POLD1": ["POLD1[All Fields]", "polymerase delta catalytic[All Fields]", "DNA polymerase delta 1[All Fields]"],
    "PARP1": ["PARP1[All Fields]", "poly(ADP-ribose) polymerase 1[All Fields]", "poly ADP-ribose polymerase[All Fields]"],
    "ERCC2": ["ERCC2[All Fields]", "XPD[All Fields]", "TFIIH subunit XPD[All Fields]"],
    "XRCC5": ["XRCC5[All Fields]", "Ku80[All Fields]", "Ku 80[All Fields]"],
    "OGG1": ["OGG1[All Fields]", "8-oxoguanine DNA glycosylase[All Fields]", "oxoguanine glycosylase[All Fields]"],
    "DKC1": ["DKC1[All Fields]", "dyskerin[All Fields]"],
    "TERF1": ["TERF1[All Fields]", "telomeric repeat-binding factor 1[All Fields]", "TRF1[All Fields]"],
    "TERF2": ["TERF2[All Fields]", "telomeric repeat-binding factor 2[All Fields]", "TRF2[All Fields]"],
    "POT1": ["POT1[All Fields]", "protection of telomeres[All Fields]"],
    "LIG4": ["LIG4[All Fields]", "DNA ligase IV[All Fields]", "ligase IV[All Fields]"],
}
SPECIES = {"Nematostella": "Nematostella vectensis", "Hydra": "Hydra vulgaris", "Clytia": "Clytia hemisphaerica"}

def eutils(ep, **params):
    q = urllib.parse.urlencode(params) + "&tool=mega27_26b&email=udita@example.com"
    for a in range(4):
        try:
            with urllib.request.urlopen(BASE + ep + "?" + q, timeout=60) as r:
                return r.read()
        except Exception:
            time.sleep(1.5 * (a + 1))
    raise RuntimeError("eutils failed: " + q)

def resolve(sp, terms):
    for term in terms:
        q = f'"{sp}"[Organism] AND ({term}) AND refseq[filter]'
        root = ET.fromstring(eutils("esearch.fcgi", db="protein", term=q, retmax=5))
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
            return bacc, best, term
    return None, None, None

def main():
    m = json.load(open("results/panel_manifest.json"))
    filled = {}
    for short, sp in SPECIES.items():
        filled[sp] = {}
        for gene, terms in SYNONYMS.items():
            cur = m["cnidaria"].get(sp, {}).get(gene)
            if cur:
                continue
            acc, fa, term = resolve(sp, terms)
            if fa:
                open(f"data/panel/{short}_{gene}.faa", "w").write(fa)
                m["cnidaria"][sp][gene] = acc
                filled[sp][gene] = (acc, term)
                print(sp, gene, acc, flush=True)
    json.dump(m, open("results/panel_manifest.json", "w"), indent=1)
    print(json.dumps(filled, indent=1))

if __name__ == "__main__":
    main()
