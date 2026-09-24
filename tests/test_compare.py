from jellygen.compare import (gc_content, codon_usage, kmer_spectrum, cosine,
                              pairwise_signature_distance, DNA_REPAIR_GENES,
                              TELOMERASE_GENES, copy_number_signal)
from jellygen.ncbi import parse_fasta


def test_gene_lists_nonempty_disjoint():
    assert len(DNA_REPAIR_GENES) >= 10 and len(TELOMERASE_GENES) >= 5
    assert not set(DNA_REPAIR_GENES) & set(TELOMERASE_GENES)


def test_parse_fasta():
    txt = ">rec1 description\nACGT\nACGT\n>rec2\nTTTT\n"
    recs = parse_fasta(txt)
    assert recs == [("rec1 description", "ACGTACGT"), ("rec2", "TTTT")]


def test_gc_content():
    assert abs(gc_content("GGCC") - 1.0) < 1e-9
    assert abs(gc_content("ATAT") - 0.0) < 1e-9
    assert abs(gc_content("GGCCNN") - 1.0) < 1e-9


def test_kmer_cosine_self():
    sp = kmer_spectrum("ACGTACGTACGT", 3)
    assert abs(cosine(sp, sp) - 1.0) < 1e-9


def test_signature_distance_bounds():
    a = ["ACGT" * 50]
    b = ["ACGT" * 50]
    c = ["TTTT" * 50]
    assert abs(pairwise_signature_distance(a, b)) < 1e-9
    assert pairwise_signature_distance(a, c) > 0.5


def test_codon_usage_sums_to_one():
    cu = codon_usage("ATGAAATTT" * 10)
    assert abs(sum(cu.values()) - 1.0) < 1e-9


def test_copy_number_signal():
    recs = [("TERT isoform 1 [Turritopsis dohrnii]", "ACGT"),
            ("TERT isoform 2 [Turritopsis dohrnii]", "ACGT"),
            ("unrelated", "ACGT")]
    assert copy_number_signal(recs, "tert") == 2
