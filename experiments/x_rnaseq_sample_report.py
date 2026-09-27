"""Descriptive 1% target-window RNA read counts, not differential expression.
States are read-only; one library per stage. Mate sums are read-end counts, not unique pairs.
"""
import collections,hashlib,json,math,os
from pathlib import Path
runs={'Medusa1':('SRR10967540',27349424,(2012337652,2443312337)),'Polyp1':('SRR10967543',20100588,(1461093996,1689171578)),'RevPolyp1':('SRR10967537',25857990,(1816084239,2265311832))}
meta=json.load(open('/tmp/xrnaseq_refmeta.json'))
assert len(meta['windows'])==37 and len(meta['targets'])==40
out={'method':'Exploratory, deterministic every-100th paired-read sample, target-window alignments, one library per stage; not DE','reference':'T. dohrnii GCA_027922465.2, 37 merged target-enriched windows for 40 named labels; 5kb flanks, locus capture +/-2kb','source':'ENA PRJNA603209','normalization':'per million MAPQ>=20 primary mapped read ends to the target-only reference; not genome-wide CPM or TPM','pair_deduplication':'NOT done; mate counts are read ends and must not be labeled unique fragments','limitations':['one library per stage selected; no replicate-based inference','no cyst stage','systematic 1% sample, low target counts','targeted reference inflates mapping proportions; ACTA1 dominates and may vary by stage','overlapping named labels (ATG5 and ATG5_locus2, PSEN1/PSEN2) count the same read twice if summed','locus +/-2kb captures genomic proximity rather than verified exons; counts do not independently prove transcription','ATG5 copy status remains unconfirmed by DNA depth'],'stages':{},'atg5_interpretation':'inconclusive'}
for stage,(acc,n_pairs,sizes) in runs.items():
 mates=[];counts=collections.Counter();mapped=0
 for mate,size in enumerate(sizes,1):
  fp=f'/tmp/xrnaseq_{acc}_{mate}.fastq.gz';sp=f'/tmp/xrnaseq_{acc}_{mate}.sample1pct.fastq.gz';st=f'/tmp/xrnaseq_{acc}_{mate}.state.json'
  j=json.load(open(st));assert j['eof'] and j['next_read']==math.ceil(n_pairs/100)==sum(c['read_end']-c['read_start'] for c in j['chunks'])
  assert len(j['chunks']) in (21,26,28)
  assert j['mapped_primary_mapq20']==sum(c['mapped'] for c in j['chunks'])
  assert os.path.getsize(fp)==size and Path(sp).stat().st_size==j['expected_bytes']
  with open(fp,'rb') as f:
   sha=hashlib.sha256()
   for block in iter(lambda:f.read(1024*1024),b''):sha.update(block)
   h=sha.hexdigest()
  mates.append({'mate':mate,'source_bytes':size,'source_sha256':h,'sampled_read_ends':j['next_read'],'mapped_primary_mapq20':j['mapped_primary_mapq20'],'chunks':len(j['chunks'])})
  mapped+=j['mapped_primary_mapq20'];counts.update(j['counts'])
 # No pair deduplication possible from accumulated marginal totals. Keep read-end units explicit.
 labels=sorted(meta['targets']);per={k:{'read_ends':counts[k],'per_million_target_mapped_read_ends':round(counts[k]/mapped*1e6,2) if mapped else None,'to_ACTA1_ratio':round(counts[k]/counts['ACTA1_housekeeping'],5) if counts['ACTA1_housekeeping'] else None,'sufficient_10_read_ends':counts[k]>=10} for k in labels}
 out['stages'][stage]={'run':acc,'original_pairs':n_pairs,'sampled_pairs':math.ceil(n_pairs/100),'mapped_target_primary_read_ends':mapped,'ACTA1_read_ends':counts['ACTA1_housekeeping'],'mates':mates,'targets':per}
print(json.dumps({'stages':{k:{'sampled_pairs':v['sampled_pairs'],'mapped_read_ends':v['mapped_target_primary_read_ends'],'ACTA1':v['ACTA1_read_ends'],'ATG5_loci':{g:v['targets'][g]['read_ends'] for g in ['ATG5_locus1','ATG5_locus2','ATG5_locus3']}} for k,v in out['stages'].items()}},indent=2))
Path('results/x-rnaseq-sample1pct.json').write_text(json.dumps(out,indent=2)+'\n')
