"""Resume-safe targeted RNA-seq counts on a verified, complete gzipped FASTQ mate.
Run bounded chunks (default 10k reads) in foreground. The input stream is reopened
at the start for every chunk; cursor advances only after successful mapping and
atomic state write. When uncertain after interruption inspect state before rerun.
Exploratory one-run-per-stage descriptive counts, not differential-expression inference.
"""
import argparse,collections,gzip,json,os,subprocess,tempfile
from pathlib import Path
P=argparse.ArgumentParser();P.add_argument('--stage',required=True);P.add_argument('--mate',type=int,choices=[1,2],required=True);P.add_argument('--fastq',required=True);P.add_argument('--expected-bytes',type=int,required=True);P.add_argument('--reads-per-chunk',type=int,default=10000);a=P.parse_args()
meta=json.load(open('/tmp/xrnaseq_refmeta.json'));acc=meta['run_accessions'][a.stage]
assert Path(a.fastq).stat().st_size==a.expected_bytes,'download incomplete or unexpected size'
assert a.reads_per_chunk>0 and a.reads_per_chunk<=10000
statep=Path(f'/tmp/xrnaseq_{acc}_{a.mate}.state.json')
state=json.load(open(statep)) if statep.exists() else {'accession':acc,'stage':a.stage,'mate':a.mate,'expected_bytes':a.expected_bytes,'next_read':0,'mapped_primary_mapq20':0,'counts':{},'chunks':[],'eof':False}
assert state['expected_bytes']==a.expected_bytes and not state['eof']
start=state['next_read'];stop=start+a.reads_per_chunk
chunk='/tmp/xrnaseq_chunk.fastq'
with gzip.open(a.fastq,'rb') as f, open(chunk,'wb') as out:
 for i in range(start*4):
  assert f.readline(),f'FASTQ truncated before read {start}'
 lines=0
 for i in range(a.reads_per_chunk*4):
  line=f.readline()
  if not line:break
  out.write(line);lines+=1
 assert lines%4==0,('incomplete record',lines)
 eof=lines<a.reads_per_chunk*4
 assert lines>0,('no reads left at cursor',start)
assert Path(chunk).stat().st_size>0
# -K 10M bounds mapper memory. -x sr sets short-read preset for Illumina reads.
cmd=['/home/sandbox/jellyfish-expansion/tools_bin/minimap2-2.28_x64-linux/minimap2','-t','1','-K','10M','-x','sr','-c','--secondary=no','/tmp/xrnaseq_ref.mmi',chunk]
out=subprocess.run(cmd,capture_output=True,text=True,timeout=110)
assert out.returncode==0,('mapper failed',out.stderr[-1000:])
counts=collections.Counter(state['counts']); mapped=0;ref=meta['windows']
for line in out.stdout.splitlines():
 t=line.split('\t')
 if len(t)<12 or int(t[11])<20:continue
 if not any(x=='tp:A:P' for x in t[12:]):continue
 mapped+=1;wname=t[5];x,y=int(t[7]),int(t[8]);contig,ws,we,loci=ref[wname]
 for name,s,e in loci:
  if not (y < s-ws-2000 or x > e-ws+2000):counts[name]+=1
state['next_read']=start+lines//4;state['mapped_primary_mapq20']+=mapped;state['counts']=dict(counts)
state['chunks'].append({'read_start':start,'read_end':state['next_read'],'mapped':mapped})
state['eof']=eof
# temp+replace, no credit for partial mapper output
with open(str(statep)+'.tmp','w') as f:json.dump(state,f,indent=1)
os.replace(str(statep)+'.tmp',statep)
print(json.dumps({'stage':a.stage,'mate':a.mate,'read_start':start,'next_read':state['next_read'],'chunk_mapped':mapped,'total_mapped':state['mapped_primary_mapq20'],'eof':eof,'acta1':counts['ACTA1_housekeeping'],'atg5':{k:v for k,v in counts.items() if 'ATG5' in k}},indent=1),flush=True)
