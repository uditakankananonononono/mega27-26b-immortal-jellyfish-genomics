# 26b repository default-branch repair

```json
{
  "date": "2026-10-09",
  "decision": "Switch default master to main; preserve both branch histories and provenance-gap note.",
  "reason": "Default master presents obsolete 99-file lineage; current main has 1344 tracked files.",
  "correction": "52c4a91a itself adds only 12-line SOURCE_PROVENANCE_GAPS.md; not a deletion commit.",
  "before_default": "master",
  "after_default": "main",
  "main_before_after": "7267e2a0872bff312983f2dfba5cdf2c04f92be7",
  "master_before_after": "52c4a91a97f2f0ce3f2bdd4d77c044a032a092ab",
  "removed": [],
  "rewritten": [],
  "science_outputs_changed": false,
  "bundle_sha256": "9b332bd291898c8ce0a7cf8f40599ebd27a9333d12794494be48865088d69af2",
  "bundle_verification": "git bundle verify passed; complete history",
  "verification": "Live public API default and both branch SHA readbacks; repository-root screenshot inspected, showing main/7267e2a/112 commits.",
  "source": "https://github.com/uditakankananonononono/mega27-26b-immortal-jellyfish-genomics",
  "rights_holds": "Preserved. Documentation gap note is not clearance."
}
```
