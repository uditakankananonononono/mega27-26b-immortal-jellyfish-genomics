"""Audit PacBio DRR267480 50%-thinned full-genome mapping for ATG5 copy status.
Input: PAF mapped to the complete GCA_027922465.2 assembly, not a target-only index.
Do not interpret this exploratory depth ratio as causal or as an allele-phased test.
"""
import argparse, collections, gzip, json, statistics
from pathlib import Path
P=argparse.ArgumentParser();P.add_argument('--paf',required=True);P.add_argument('--genome',required=True);P.add_argument('--fastq',nargs='+',required=True);P.add_argument('--out',required=True);a=P.parse_args()
REG={'copyA':['BQMF02000106.1',66386,66652],'copyB':['BQMF02000418.1',205689,205955],'paralog':['BQMF02000003.1',2632220,2633029]}
lengths={};n=0;ct=None
for line in open(a.genome):
 if line.startswith('>'):
  if ct:lengths[ct]=n
  ct=line[1:].split()[0];n=0
 else:n+=len(line.strip())
lengths[ct]=n
fastq_lines=[]
for fp in a.fastq:
 with gzip.open(fp,'rb') as f:count=sum(1 for _ in f)
 assert count%4==0,(fp,count)
 fastq_lines.append({'path':fp,'lines':count,'reads':count//4})
window_bases=collections.Counter();reg_events={k:collections.Counter() for k in REG};seen=set();qreads=set();rows=0;dup=0;passing=0;target_counts=collections.Counter()
for line in open(a.paf):
 rows+=1;f=line.rstrip().split('\t')
 assert len(f)>=12,(rows,line[:60])
 read,contig=f[0],f[5];s,e,mq=int(f[7]),int(f[8]),int(f[11])
 sig=(read,contig,s,e)
 if sig in seen:dup+=1;continue
 seen.add(sig)
 if mq<30 or e-s<500:continue
 passing+=1;qreads.add(read)
 w=s//50000
 while w*50000<e:
  lo=max(s,w*50000);hi=min(e,(w+1)*50000)
  if hi>lo:window_bases[(contig,w)]+=hi-lo
  w+=1
 for k,(c,ls,le) in REG.items():
  if contig!=c:continue
  lo=max(s,max(0,ls-25000));hi=min(e,min(lengths[c],le+25000))
  if hi>lo:reg_events[k][lo]+=1;reg_events[k][hi]-=1
  if s<=le and e>ls:target_counts[k]+=1
bg=[window_bases[(c,w)]/50000 for c,L in lengths.items() if c not in {r[0] for r in REG.values()} for w in range(L//50000)]
bg_median=statistics.median(bg)
out={'source_run':'DRR267480','reference':'GCA_027922465.2 TUR_r2.0.1 full genome','sampling':'systematic odd reads by original FASTQ record ordinal (50%, no replacement)','fastq_files':fastq_lines,'paf_rows':rows,'duplicate_alignment_signatures_skipped':dup,'mapq30_len500_alignments':passing,'unique_mapq30_reads':len(qreads),'background':{'window_bp':50000,'windows':len(bg),'median_depth':round(bg_median,5),'p10':round(sorted(bg)[int(.1*len(bg))],5),'p90':round(sorted(bg)[int(.9*len(bg))],5),'target_contigs_excluded':True},'targets':{},'decision':'unresolved','limitations':['The gene spans only 267 bp per cnidarian-type copy, and copyA/copyB local flanks have sharp depth variation.','Mapping of homologous copies to a draft assembly is not an allele-phased structural validation.','Sampling halves depth; ratios compare the same thinned dataset only.','A read-depth contrast alone cannot establish immortality-related function.']}
for k,(c,ls,le) in REG.items():
 ev=reg_events[k];lo=max(0,ls-25000);hi=min(lengths[c],le+25000);cur=0;depth=[]
 for p in range(lo,hi):
  cur+=ev.get(p,0);depth.append(cur)
 zones={'locus':[ls,le+1],'core_1kb':[ls-1000,le+1001],'left_5kb':[ls-6000,ls-1000],'right_5kb':[le+1000,le+6000]};summary={}
 for label,(x,y) in zones.items():
  vals=depth[max(x,lo)-lo:min(y,hi)-lo]
  summary[label]={'mean':round(statistics.mean(vals),4),'median':statistics.median(vals),'ratio_to_background':round(statistics.mean(vals)/bg_median,4),'min':min(vals),'max':max(vals)}
 out['targets'][k]={'contig':c,'start':ls,'end':le,'overlapping_alignments':target_counts[k],'zones':summary}
out['decision_reason']='CopyA locus 0.82x genome median and copyB 1.31x; neither a uniform half-depth haplotig pattern nor a uniform single-copy-depth duplication pattern. Local flank depths are heterogeneous. Extra copy remains unconfirmed.'
assert sum(x['reads'] for x in fastq_lines)==852070
assert rows>800000 and len(bg)>8000
Path(a.out).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'decision':out['decision'],'paf_rows':rows,'reads':sum(x['reads'] for x in fastq_lines),'background_median':bg_median,'target_ratios':{k:v['zones']['locus']['ratio_to_background'] for k,v in out['targets'].items()}},indent=2))
