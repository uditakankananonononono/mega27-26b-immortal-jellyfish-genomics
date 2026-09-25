"""Cluster tBLASTn HSPs into candidate gene loci and extract genomic regions.

A locus = set of HSPs for one panel gene on one contig within LOCUS_SPAN bp.
Regions are extracted from the BLAST db (blastdbcmd) with FLANK bp of flank
for downstream exon-aware alignment.
"""
LOCUS_SPAN = 50_000
FLANK = 20_000

def cluster_loci(hits, span=LOCUS_SPAN):
    """hits: list of HSP dicts for one gene vs one genome. Returns list of loci:
    {contig, start, end, hsps, total_bits}."""
    by_contig = {}
    for h in hits:
        by_contig.setdefault(h["contig"], []).append(h)
    loci = []
    for contig, hs in by_contig.items():
        hs = sorted(hs, key=lambda h: min(h["sstart"], h["send"]))
        cur = []
        for h in hs:
            lo = min(h["sstart"], h["send"])
            if cur and lo - max(max(x["sstart"], x["send"]) for x in cur) > span:
                loci.append(cur); cur = []
            cur.append(h)
        if cur:
            loci.append(cur)
    out = []
    for group in loci:
        starts = [min(h["sstart"], h["send"]) for h in group]
        ends = [max(h["sstart"], h["send"]) for h in group]
        out.append({
            "contig": group[0]["contig"],
            "start": min(starts), "end": max(ends),
            "n_hsps": len(group),
            "total_bits": round(sum(h["bits"] for h in group), 1),
            "best_pident": max(h["pident"] for h in group),
            "best_qcov": max(h["qcov"] for h in group),
            "strand": "+" if sum(1 for h in group if h["send"] >= h["sstart"]) >= len(group) / 2 else "-",
        })
    return sorted(out, key=lambda l: -l["total_bits"])

def region_bounds(locus, flank=FLANK):
    return max(1, locus["start"] - flank), locus["end"] + flank
