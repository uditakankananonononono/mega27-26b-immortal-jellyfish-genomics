"""Frozen top-20 similarity search in held-out whole predicted proteomes.
DIAMOND blastp is a low-memory substitute for MMseqs query-vs-proteome search;
its presence/absence is exploratory and not a cluster/orthology validation.
"""
import collections,json,subprocess
from pathlib import Path
from Bio import SeqIO
ROOT=Path('/tmp/jelly-A-work');BIN='/tmp/jelly-diamond/diamond'
train=json.load(open('results/x-20260928-A-train-ranking.json'))
reps=set(train['top20_frozen_reps'])
seq={r.id:r for r in SeqIO.parse(str(ROOT/'linprimary_rep_seq.fasta'),'fasta')}
assert reps<=set(seq)
with open(ROOT/'top20_rep.fasta','w') as f:SeqIO.write([seq[x] for x in train['top20_frozen_reps']],f,'fasta')
for label in ('O','C'):
 fasta={'O':'/tmp/jelly-rawrefs/tdoviedo.norm.fa','C':'/tmp/jelly-rawrefs/clytia.fa'}[label]
 db=str(ROOT/f'holdout_{label}.dmnd');out=str(ROOT/f'holdout_{label}.tsv')
 subprocess.run([BIN,'makedb','--in',fasta,'--db',db,'--threads','1'],check=True,stdout=subprocess.DEVNULL)
 cmd=[BIN,'blastp','--query',str(ROOT/'top20_rep.fasta'),'--db',db,'--out',out,'--threads','1','--id','30','--query-cover','70','--subject-cover','70','--max-target-seqs','200','--outfmt','6','qseqid','sseqid','pident','qcovhsp','scovhsp','evalue','bitscore']
 subprocess.run(cmd,check=True,stdout=open(str(ROOT/f'holdout_{label}.log'),'w'),stderr=subprocess.STDOUT,timeout=480)
 hits=collections.defaultdict(list)
 for line in open(out):
  q,t,p,qc,tc,e,b=line.rstrip().split('\t');hits[q].append({'id':t,'pident':float(p),'qcov':float(qc),'scov':float(tc),'evalue':float(e),'bits':float(b)})
 assert set(hits)<=reps
 print(label,'hit_counts',[(k,len(hits[k])) for k in train['top20_frozen_reps']])
 json.dump({k:v for k,v in sorted(hits.items())},open(str(ROOT/f'holdout_{label}.json'),'w'),indent=1)
