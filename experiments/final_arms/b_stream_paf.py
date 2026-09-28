"""Stream gzip PacBio reads through whole-genome minimap2 in bounded batches.
No raw SAM/PAF accumulation: retain only alignments near frozen ATG5 loci plus
read identities needed to audit secondary/supplementary hits. Checkpoint cursor
advances only after minimap2 exits successfully; a crash reruns at most one batch.
"""
import argparse,gzip,json,os,subprocess,tempfile
from pathlib import Path
P=argparse.ArgumentParser();P.add_argument('--batches',type=int,default=1);P.add_argument('--batch-reads',type=int,default=10000);P.add_argument('--index',default='/tmp/jelly-Tdohrnii-map-pb.mmi');P.add_argument('--fastq',default='/tmp/jelly-DRR267480.fastq.gz');P.add_argument('--state',default='/tmp/jelly-B-structural.state.json');a=P.parse_args()
assert 1<=a.batches<=20 and 1000<=a.batch_reads<=20000
assert Path(a.fastq).stat().st_size==3594233174,'not a complete source FASTQ'
REG={'A':('BQMF02000106.1',66386,66652),'B':('BQMF02000418.1',205689,205955)}
state_path=Path(a.state);state=json.load(open(state_path)) if state_path.exists() else {'next_ordinal':0,'batches':0,'total_reads':0,'nearby_alignments':[],'input':'DRR267480 full MD5 8481187208c3a4892fea222346c02c46','index':'whole GCA_027922465.2 map-pb k19 w20 I150M'}
for _ in range(a.batches):
 with gzip.open(a.fastq,'rt') as f:
  # Simplicity over speed: skip completed records; bounded 10k batches.
  for i in range(state['next_ordinal']*4):
   if not f.readline():raise AssertionError('cursor past EOF')
  tmp=Path('/tmp/jelly-B-batch.fastq')
  with open(tmp,'w') as out:
   n=0
   for i in range(a.batch_reads):
    lines=[f.readline() for _ in range(4)]
    if not lines[0]:break
    assert all(lines) and lines[0].startswith('@') and lines[2].startswith('+')
    out.writelines(lines);n+=1
 if n==0:break
 cmd=['/home/sandbox/jellyfish-expansion/tools_bin/minimap2-2.28_x64-linux/minimap2','-x','map-pb','-k','19','-w','20','-I','150M','-t','1','-K','10M',a.index,str(tmp)]
 with open('/tmp/jelly-B-batch.paf','w') as paf,open('/tmp/jelly-B-batch.log','w') as err:
  rc=subprocess.run(cmd,stdout=paf,stderr=err,timeout=600).returncode
 assert rc==0,(rc,Path('/tmp/jelly-B-batch.log').read_text()[-800:])
 relevant=[]
 for line in open('/tmp/jelly-B-batch.paf'):
  x=line.rstrip().split('\t');t=x[5];s,e=int(x[7]),int(x[8])
  if any(t==contig and e>start-25000 and s<end+25000 for contig,start,end in REG.values()):
   relevant.append(x[:12]+[tag for tag in x[12:] if tag.startswith(('tp:','s1:','s2:','NM:','cm:'))])
 state['nearby_alignments'].extend(relevant);state['next_ordinal']+=n;state['total_reads']+=n;state['batches']+=1
 temp=state_path.with_suffix('.json.tmp');temp.write_text(json.dumps(state)+'\n');temp.replace(state_path)
 print('checkpoint',state['next_ordinal'],'reads; new target-region PAF rows',len(relevant),'total',len(state['nearby_alignments']),flush=True)
 if n<a.batch_reads:break
