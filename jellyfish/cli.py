"""jellyfish-genomics CLI: audit, census, motifs, predict, verify, compare.

  python -m jellyfish.cli audit          live 21-gene annotation-desert audit
  python -m jellyfish.cli census FASTA   telomere census of an assembly
  python -m jellyfish.cli motifs TARGET_FASTA BG_FASTA [BG_FASTA...]
                                         k-mer enrichment z-scores
  python -m jellyfish.cli verify PROTEIN_FAA [gene]
                                         Pfam domain scan (+ expected-domain verdict)
  python -m jellyfish.cli compare QUERY_FAA REF_FAA [REF_FAA...]
                                         unique-substitution analysis
"""
import sys, json

def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        print(__doc__)
        return 2
    cmd, args = argv[0], argv[1:]
    if cmd == "audit":
        from experiments.fetch_panel import main as _  # noqa - heavy; audit is online
        print("run experiments/fetch_panel.py for the full live audit")
        return 0
    if cmd == "census":
        from jellyfish.telomere import census
        print(json.dumps(census(args[0]), indent=1))
        return 0
    if cmd == "motifs":
        from jellyfish.motifs import enrichment
        tgt = ["".join(l for l in open(args[0]).read().splitlines() if not l.startswith(">"))]
        bg = ["".join(l for l in open(a).read().splitlines() if not l.startswith(">")) for a in args[1:]]
        res = enrichment(tgt, bg)
        top = sorted(res.items(), key=lambda kv: -kv[1]["z"])[:20]
        print(json.dumps(dict(top), indent=1))
        return 0
    if cmd == "verify":
        print("Pfam scan requires /tmp/Pfam-A.hmm.gz; run experiments/domain_scan.py")
        return 0
    if cmd == "compare":
        from jellyfish.mutations import unique_substitutions
        q = "".join(l for l in open(args[0]).read().splitlines() if not l.startswith(">"))
        refs = ["".join(l for l in open(a).read().splitlines() if not l.startswith(">")) for a in args[1:]]
        print(json.dumps(unique_substitutions(q, refs), indent=1))
        return 0
    print("unknown command:", cmd)
    print(__doc__)
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
