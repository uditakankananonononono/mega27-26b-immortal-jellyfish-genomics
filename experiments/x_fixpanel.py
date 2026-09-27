"""D9 repair: re-fetch all 47 human panel proteins via UniProt REST with
gene_exact matching (NCBI esearch 500ing on 2026-09-27). Reviewed entries
first; verifies the gene name matches before accepting. Writes fixed files
to data/xpanel_fixed/ + verify report; never touches originals."""
import json, os, time, urllib.parse, urllib.request

OUT = "data/xpanel_fixed"
os.makedirs(OUT, exist_ok=True)
GENES = sorted(json.load(open("data/xpanel/manifest.json")).keys())

def get(url):
    for i in range(5):
        try:
            return urllib.request.urlopen(url, timeout=30).read().decode()
        except Exception:
            time.sleep(min(3 * (i + 1), 15))
    raise RuntimeError(f"fetch failed {url}")

rep = {}
for g in GENES:
    rec = None
    for reviewed in ("true", "false"):
        q = urllib.parse.quote(f"gene:{g} AND organism_id:9606 AND reviewed:{reviewed}")
        url = f"https://rest.uniprot.org/uniprotkb/search?query={q}&fields=accession,gene_names,protein_name,length&format=tsv&size=25"
        rows = [l.split("\t") for l in get(url).splitlines()[1:] if l.strip()]
        # exact gene match: first-listed gene name equals g (case-insensitive)
        for r in rows:
            first_gene = r[1].split()[0] if len(r) > 1 and r[1] else ""
            if first_gene.upper() == g.upper():
                rec = r
                break
        if rec:
            break
        time.sleep(0.3)
    if not rec:
        rep[g] = {"status": "no_exact_gene_match"}
        print(g, "NO MATCH", flush=True)
        continue
    acc = rec[0]
    fa = get(f"https://rest.uniprot.org/uniprotkb/{acc}.fasta")
    header, seq_lines = fa.splitlines()[0], fa.splitlines()[1:]
    seq = "".join(seq_lines).strip()
    with open(f"{OUT}/human_{g}.faa", "w") as f:
        f.write(f">{acc} {rec[2][:80]} [Homo sapiens] (UniProt {acc}, gene {g})\n")
        for i in range(0, len(seq), 60):
            f.write(seq[i:i+60] + "\n")
    rep[g] = {"status": "ok", "acc": acc, "len": len(seq), "name": rec[2][:80]}
    print(g, acc, len(seq), flush=True)
    time.sleep(0.3)
json.dump(rep, open(f"{OUT}/verify_report.json", "w"), indent=1)
ok = sum(1 for v in rep.values() if v["status"] == "ok")
print(f"FIXDONE {ok}/{len(GENES)}")
