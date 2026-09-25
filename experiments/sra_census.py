"""SRA run census for both jellyfish: transcriptome-data availability.

Fetches every SRA run accession for T. dohrnii and A. aurita (run metadata =
accession-level records), tabulates platform/size/date. Evidence that the
annotation desert is NOT a data desert: hundreds of runs exist, unannotated.
"""
import json, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def eutils(ep, **params):
    q = urllib.parse.urlencode(params) + "&tool=mega27_26b&email=udita@example.com"
    for a in range(4):
        try:
            with urllib.request.urlopen(BASE + ep + "?" + q, timeout=60) as r:
                return r.read()
        except Exception:
            time.sleep(1.5 * (a + 1))
    raise RuntimeError("eutils failed")

def runs_for(organism):
    root = ET.fromstring(eutils("esearch.fcgi", db="sra", term=f'"{organism}"[Organism]', retmax=1000))
    ids = [i.text for i in root.findall(".//Id")]
    runs = []
    for i in range(0, len(ids), 50):
        batch = ids[i:i+50]
        d = json.loads(eutils("esummary.fcgi", db="sra", id=",".join(batch), retmode="json"))
        for uid in d["result"]["uids"]:
            r = d["result"][uid]
            expxml = r.get("expxml", "")
            runs.append({"sra_uid": uid, "runs": r.get("runs", "")[:200],
                         "platform": r.get("platform", ""),
                         "spots": r.get("spots", ""), "bases": r.get("bases", ""),
                         "created": r.get("createdate", "")})
        time.sleep(0.5)
    return runs

out = {}
for org in ("Turritopsis dohrnii", "Aurelia aurita"):
    runs = runs_for(org)
    out[org] = {"n_uids": len(runs), "runs": runs}
    print(org, len(runs), flush=True)
json.dump(out, open("results/sra_census.json", "w"), indent=1)
