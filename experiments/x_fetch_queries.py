"""Fetch query proteins for expansion panels B/C via NCBI eutils.

Per symbol: human RefSeq (longest NP_) + cnidarian homologs (longest RefSeq
per species: Clytia hemisphaerica, Hydra vulgaris, Acropora millepora,
Nematostella vectensis). Deterministic: longest sequence wins, accession
tiebreak alphabetical. Everything logged to data/xpanel/manifest.json.
"""
import json, os, sys, time, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jellyfish.xpanel import SYMBOLS_B, SYMBOLS_C

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
OUT = os.path.join("data", "xpanel")
os.makedirs(OUT, exist_ok=True)
SYMS = sorted(set(SYMBOLS_B) | set(SYMBOLS_C))
CNIDARIA = ["Clytia hemisphaerica", "Hydra vulgaris", "Acropora millepora",
            "Nematostella vectensis"]

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "mega27-26b-expansion"})
    delay = 3
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < 5:
                time.sleep(delay); delay *= 2; continue
            raise

def esearch(term, retmax=8):
    q = urllib.parse.urlencode({"db": "protein", "term": term, "retmax": retmax,
                                "retmode": "json", "sort": ""})
    d = json.loads(get(f"{EUTILS}/esearch.fcgi?{q}"))
    return d.get("esearchresult", {}).get("idlist", [])

def efetch_fasta(ids):
    q = urllib.parse.urlencode({"db": "protein", "id": ",".join(ids), "rettype": "fasta", "retmode": "text"})
    return get(f"{EUTILS}/efetch.fcgi?{q}")

def parse_fasta(txt):
    recs, h, s = [], None, []
    for line in txt.splitlines():
        if line.startswith(">"):
            if h is not None: recs.append((h, "".join(s)))
            h, s = line[1:], []
        else:
            s.append(line.strip())
    if h is not None: recs.append((h, "".join(s)))
    return recs

def pick_longest_refseq(fasta_txt):
    recs = parse_fasta(fasta_txt)
    ref = [r for r in recs if r[0].split()[0].startswith(("NP_", "XP_"))]
    if not ref: ref = recs
    if not ref: return None
    return max(sorted(ref), key=lambda r: len(r[1]))

def fetch_symbol(sym, orgn):
    # mirrors the closed phase's fetch_panel.py: All Fields + refseq filter
    ids = esearch(f'"{orgn}"[Organism] AND {sym}[All Fields] AND refseq[filter]')
    if not ids:
        ids = esearch(f'"{orgn}"[Organism] AND {sym}[Gene Name]')
    if not ids:
        return None
    return pick_longest_refseq(efetch_fasta(ids))

def main():
    manifest = {}
    for sym in SYMS:
        if sym in manifest and "human" in manifest[sym] and \
                os.path.exists(os.path.join(OUT, f"human_{sym}.faa")):
            print(sym, "SKIP (done)", flush=True)
            continue
        entry = manifest.get(sym, {})
        got = fetch_symbol(sym, "Homo sapiens")
        if got:
            entry["human"] = {"header": got[0], "len": len(got[1])}
            with open(os.path.join(OUT, f"human_{sym}.faa"), "w") as f:
                f.write(f">{got[0]}\n" + "\n".join(got[1][i:i+60] for i in range(0, len(got[1]), 60)) + "\n")
        time.sleep(0.8)
        for sp in CNIDARIA:
            got = fetch_symbol(sym, sp)
            tag = sp.split()[0]
            if got:
                entry[tag] = {"header": got[0], "len": len(got[1])}
                with open(os.path.join(OUT, f"{tag}_{sym}.faa"), "w") as f:
                    f.write(f">{got[0]}\n" + "\n".join(got[1][i:i+60] for i in range(0, len(got[1]), 60)) + "\n")
            time.sleep(0.8)
        manifest[sym] = entry
        print(sym, {k: v["len"] for k, v in entry.items()}, flush=True)
        json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
    print("FETCHDONE", sum(1 for v in manifest.values() if "human" in v), "of", len(SYMS), "human")

if __name__ == "__main__":
    main()
