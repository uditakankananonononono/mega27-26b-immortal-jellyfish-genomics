"""Resume DRR267480 raw FASTQ in bounded byte ranges, promoting only full MD5 match.
No partial file is accepted as science input. Run once per bounded foreground batch.
"""
import argparse,hashlib,os,requests,time
P=argparse.ArgumentParser();P.add_argument('--chunks',type=int,default=2);P.add_argument('--size-mib',type=int,default=32);a=P.parse_args()
u='https://ftp.sra.ebi.ac.uk/vol1/fastq/DRR267/DRR267480/DRR267480_subreads.fastq.gz';p='/tmp/jelly-DRR267480.fastq.gz';want=3594233174;md5='8481187208c3a4892fea222346c02c46'
assert 0< a.chunks<=12 and 1<=a.size_mib<=64
for _ in range(a.chunks):
 st=os.path.getsize(p) if os.path.exists(p) else 0
 if st==want:break
 assert st<want
 en=min(want-1,st+a.size_mib*1048576-1)
 with requests.get(u,headers={'Range':f'bytes={st}-{en}'},stream=True,timeout=(10,90)) as r:
  assert r.status_code==206 and r.headers.get('Content-Range')==f'bytes {st}-{en}/{want}',(r.status_code,r.headers)
  n=0
  with open(p,'ab') as f:
   for part in r.iter_content(1048576):
    if part:f.write(part);n+=len(part)
 assert n==en-st+1,(n,en-st+1)
 print('checkpoint',en+1,'/',want,flush=True)
if os.path.getsize(p)==want:
 h=hashlib.md5()
 with open(p,'rb') as f:
  for x in iter(lambda:f.read(1048576),b''):h.update(x)
 print('complete-md5',h.hexdigest(),flush=True)
 assert h.hexdigest()==md5
