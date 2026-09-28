"""Bounded, environment-independent fresh-clone raw-source bootstrap and smoke.
It does not claim full reproduction. Downloads provider genome/GFF/peptides, hashes,
checks target contig identity, builds local BLAST DB, maps a fixed sample query.
"""
import argparse,gzip,hashlib,json,subprocess,urllib.request
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--workdir',required=True);p.add_argument('--tblastn',required=True);p.add_argument('--makeblastdb',required=True);p.add_argument('--query',default='data/xpanel_fixed/human_ATG5.faa');p.add_argument('--manifest',default='results/x-20260928-D-raw-manifest.json');a=p.parse_args()
w=Path(a.workdir).resolve();w.mkdir(parents=True,exist_ok=True)
m=json.load(open(a.manifest));actual={}
for key,src in m['sources'].items():
 path=w/src['filename'];expect=src['sha256'];size=src['bytes']
 if not path.exists() or path.stat().st_size!=size:
  temp=path.with_suffix(path.suffix+'.partial')
  with urllib.request.urlopen(src['url'],timeout=90) as resp,open(temp,'wb') as out:
   for chunk in iter(lambda:resp.read(1048576),b''):out.write(chunk)
  assert temp.stat().st_size==size,(key,temp.stat().st_size,size)
  temp.replace(path)
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
 assert h.hexdigest()==expect,(key,h.hexdigest(),expect)
 actual[key]={'bytes':size,'sha256':expect}
fa=w/'TUR_r2.0.1.fa'
with gzip.open(w/m['sources']['genome']['filename'],'rb') as f,open(fa,'wb') as out:
 for chunk in iter(lambda:f.read(1048576),b''):out.write(chunk)
subprocess.run([a.makeblastdb,'-in',str(fa),'-dbtype','nucl','-out',str(w/'TUR_db')],check=True,stdout=subprocess.DEVNULL)
q=Path(a.query).resolve();assert q.exists()
out=w/'ATG5_smoke.tsv'
with open(out,'w') as f:subprocess.run([a.tblastn,'-query',str(q),'-db',str(w/'TUR_db'),'-evalue','1e-5','-max_target_seqs','20','-outfmt','6 qseqid sseqid pident length evalue bitscore qstart qend sstart send qlen'],check=True,stdout=f)
rows=out.read_text().splitlines();assert rows
report={'mode':'source-verified raw bootstrap smoke, NOT full end-to-end reproduction','source_checks':actual,'ATG5_smoke_rows':len(rows),'target_accessions':sorted({r.split('\t')[1] for r in rows}),'limitations':['only one query and main assembly; no raw RNA or PacBio fetched','does not regenerate all ledgers, tables, figures or paper','full raw program still needs portable versioned dependencies, full datasets and higher disk/RAM']}
(w/'smoke_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
