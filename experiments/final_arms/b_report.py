"""Locked ATG5 structural gate evaluation on complete-source whole-genome PAF stream."""
import collections,hashlib,json,re
from pathlib import Path
p=Path('/tmp/jelly-DRR267480.fastq.gz');assert p.stat().st_size==3594233174
h=hashlib.md5()
with open(p,'rb') as f:
 for x in iter(lambda:f.read(1048576),b''):h.update(x)
assert h.hexdigest()=='8481187208c3a4892fea222346c02c46'
j=json.load(open('/tmp/jelly-B-structural.state.json'))
assert j['next_ordinal']==j['total_reads']==1704140
assert j['index']=='whole GCA_027922465.2 map-pb k21 w40 single index'
REG={'copyA':('BQMF02000106.1',66386,66652),'copyB':('BQMF02000418.1',205689,205955)}
result={'source':'ENA DRR267480','source_url':'https://www.ebi.ac.uk/ena/portal/api/filereport?accession=DRR267480&result=read_run','fastq_bytes':p.stat().st_size,'fastq_md5':h.hexdigest(),'reads_processed':j['next_ordinal'],'mapper':'minimap2 2.28 map-pb, single full-genome index, k21 w40; global MAPQ','reference':'GCA_027922465.2 Tdohrnii 891 contigs, no target-only reference','targets':{},'decision':'UNRESOLVED','reason':'Frozen gate requires >=2 independent primary MAPQ>=30 long molecules each spanning 5kb unique left flank through locus to 5kb unique right flank for both copies. Neither copy has such an alignment. Ordinary locus-crossing reads and an inconclusive depth ratio do not distinguish haplotig from duplication.','limits':['PAF nearby rows preserve read IDs, target spans, mapq and primary/secondary flags, but no base-level unique-kmer anchor proof; zero coordinate-span pass is decisive under this gate.','Public FASTQ headers have generic DRR read ordinals, not ZMW identifiers; adjacent ordinals and near-identical spans cannot be presumed independent molecules.','Failure of this conservative gate does not disprove a real duplication or a biological effect.','The earlier split-index pilot was discarded before full replay because per-shard MAPQ is not global; only the single-index complete replay is scored.']}
for name,(c,s,e) in REG.items():
 a=[x for x in j['nearby_alignments'] if x[5]==c]
 primary=[x for x in a if 'tp:A:P' in x]
 cross=[x for x in primary if int(x[7])<s and int(x[8])>e]
 strict=[x for x in cross if int(x[7])<=s-5000 and int(x[8])>=e+5000 and int(x[11])>=30]
 assert not strict
 ids=[int(x[0].rsplit('.',1)[1]) for x in cross]
 blocks=[]
 for v in sorted(ids):
  if blocks and v==blocks[-1][-1]+1:blocks[-1].append(v)
  else:blocks.append([v])
 result['targets'][name]={'contig':c,'locus_1based':[s,e],'nearby_paf_rows':len(a),'primary_nearby_rows':len(primary),'primary_locus_crossing_rows':len(cross),'crossing_MAPQ':dict(collections.Counter(x[11] for x in cross)),'strict_5kb_both_flanks_MAPQ30':len(strict),'crossing_read_ordinal_blocks':[{'first':v[0],'last':v[-1],'n':len(v)} for v in blocks],'longest_crossing_alignment_bp':max((int(x[8])-int(x[7]) for x in cross),default=0),'crossing_PAF_subset':[x[:12]+[tag for tag in x[12:] if tag.startswith('tp:')] for x in cross]}
Path('results/x-20260928-B-structural.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:{a:v for a,v in x.items() if a!='crossing_PAF_subset'} for k,x in result['targets'].items()},indent=2));print(result['decision'])
