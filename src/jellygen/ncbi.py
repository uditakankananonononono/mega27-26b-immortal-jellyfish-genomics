"""Live NCBI fetch layer (used outside CI only; tests run on cached fixtures)."""
import json, time, urllib.parse, urllib.request

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def _get(path, params, retries=4):
    qs = urllib.parse.urlencode(params)
    url = f"{EUTILS}/{path}?{qs}"
    for i in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except Exception:
            time.sleep(2 + 2 * i)
    raise RuntimeError(f"eutils failed: {path} {params}")


def esearch(db, term, retmax=20):
    raw = _get("esearch.fcgi", dict(db=db, term=term, retmode="json", retmax=retmax,
                                    tool="mega27", email="uditakankana@gmail.com"))
    return json.loads(raw)["esearchresult"]["idlist"]


def efetch_fasta(db, ids):
    time.sleep(0.5)
    return _get("efetch.fcgi", dict(db=db, id=",".join(ids), rettype="fasta",
                                    retmode="text", tool="mega27",
                                    email="uditakankana@gmail.com")).decode()


def efetch_fasta_capped(db, ids, max_len=30000):
    time.sleep(0.5)
    return _get("efetch.fcgi", dict(db=db, id=",".join(ids), rettype="fasta",
                                    retmode="text", seq_start=1, seq_stop=max_len,
                                    tool="mega27",
                                    email="uditakankana@gmail.com")).decode()


def fetch_gene_set(gene, organism, retmax=4, max_len=30000):
    """Fetch RefSeq mRNA FASTA records for a gene in an organism, length-capped
    (avoids pulling whole-chromosome records into memory)."""
    for term in (f"{gene}[Gene Name] AND {organism}[Organism] AND biomol_mrna[PROP]",
                 f"{gene}[All Fields] AND {organism}[Organism] AND biomol_mrna[PROP]",
                 f"{gene}[All Fields] AND {organism}[Organism]"):
        ids = esearch("nucleotide", term, retmax)
        if ids:
            return efetch_fasta_capped("nucleotide", ids, max_len)
    return ""


def parse_fasta(text):
    """Minimal FASTA parser -> list of (header, seq)."""
    recs, header, seq = [], None, []
    for line in text.splitlines():
        if line.startswith(">"):
            if header is not None:
                recs.append((header, "".join(seq)))
            header, seq = line[1:], []
        else:
            seq.append(line.strip())
    if header is not None:
        recs.append((header, "".join(seq)))
    return recs
