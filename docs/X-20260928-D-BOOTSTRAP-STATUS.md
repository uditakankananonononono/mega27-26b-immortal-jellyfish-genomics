# Fresh-clone bootstrap status (arm D)

At locked-source commit 151d1bd, a clean /tmp clone needed an explicit fetch to obtain
current origin/main. It then fetched **three** Kyushu source files from the provider URL,
verified byte counts and SHA256 against the manifest, decompressed a fresh genome FASTA,
built a local nucleotide BLAST database, and ran a human-ATG5 tblastn smoke query.
One raw query hit was produced (Tur_r2.0_p0003.1). This is a narrow source-integrity
and execution demonstration, not recreation of all original loci or tables. The runner
accepts BLAST binaries as command-line paths (and now defaults to PATH), not a fixed
science workspace; installation/version pinning remains the caller's job. Full raw RNA
reads (~35.9 GB compressed for nine runs) and PacBio (~3.59 GB) do not fit the current
sandbox simultaneously. The full pipeline still hard-codes other workspace paths; its
`run` subcommand does not exist. Therefore the judge's end-to-end fresh-machine PASS is
**not met**, despite the successful smoke.

Primary source: https://mogt.agr.kyushu-u.ac.jp/turritopsis/download.html
Manifest: results/x-20260928-D-raw-manifest.json. Fresh smoke output and exact
source hashes: results/x-20260928-D-smoke.json. Raw genome and BLAST DB were not
committed to Git.
