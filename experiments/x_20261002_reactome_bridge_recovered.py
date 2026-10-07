# Recovered October 7 from October 2 execution records. No new run performed.
import requests,json,hashlib,time,math,random,collections,os
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'results/x-20261002-reactome';
if not (out/'snapshot-manifest.json').exists():raise SystemExit('Historical snapshots absent. Do not replace with current data; requires a new dated lock.')
original_manifest=json.load(open(out/'snapshot-manifest.json'))
for item in original_manifest['files']:
 name=item.get('filename') or item['url'].rsplit('/',1)[-1]
 fp=out/name
 if not fp.exists() or hashlib.sha256(fp.read_bytes()).hexdigest()!=item['sha256']:
  raise SystemExit('Historical source snapshot absent or hash mismatch; no current downloads allowed.')
t=time.monotonic();manifest=[];bytes_total=0
for name in ['NCBI2Reactome_All_Levels.txt','ReactomePathways.txt','ReactomePathwaysRelation.txt']:
 b=(out/name).read_bytes();bytes_total+=len(b)
 manifest.append({'url':'https://reactome.org/download/current/'+name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})

st=json.load(open(root/'results/x-stats.json'));panels={k:set(st['panels'][k])-{'APOE'} for k in ['B','C']};det={k:set(st['H1_panelB' if k=='B' else 'H2_panelC']['present'])-{'APOE'} for k in ['B','C']};maps={};unmapped=[]
for g in sorted(set.union(*panels.values())):
 u='https://rest.genenames.org/fetch/symbol/'+g
 fp=out/(g+'.json');b=fp.read_bytes();docs=json.loads(b)['response']['docs'];valid=[d for d in docs if d.get('status')=='Approved' and d.get('entrez_id')]
 if g=='GBA':
  u='https://rest.genenames.org/fetch/prev_symbol/GBA';b=(out/'GBA-prev_symbol.json').read_bytes();docs=json.loads(b)['response']['docs'];valid=[d for d in docs if d.get('symbol')=='GBA1' and d.get('status')=='Approved' and d.get('entrez_id')=='2629'];(out/'GBA-prev_symbol.json').write_bytes(b)
 bytes_total+=len(b);assert bytes_total<=105_000_000;manifest.append({'url':u,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})

 if len(valid)!=1:unmapped.append(g)
 else:maps[g]=valid[0]['entrez_id']
json.dump({'download_bytes':bytes_total,'files':manifest,'mapping':maps,'unmapped':unmapped,'panels':{k:sorted(v) for k,v in panels.items()},'detected':{k:sorted(v) for k,v in det.items()}},open(out/'snapshot-manifest.json','w'),indent=2)
if unmapped:raise SystemExit('Unresolved mapping: '+str(unmapped))
parents={l.split('\t')[0] for l in (out/'ReactomePathwaysRelation.txt').read_text().splitlines()};human={f[0] for l in (out/'ReactomePathways.txt').read_text().splitlines() if len(f:=l.split('\t'))>=3 and f[2]=='Homo sapiens'};leaf=human-parents;entrez_to_gene={v:k for k,v in maps.items()};membership=collections.defaultdict(set)
for l in (out/'NCBI2Reactome_All_Levels.txt').read_text().splitlines():
 f=l.split('\t')
 if len(f)>=6 and f[5]=='Homo sapiens' and f[4]=='TAS' and f[1] in leaf and f[0] in entrez_to_gene:membership[f[1]].add(entrez_to_gene[f[0]])
elig={p:gs for p,gs in membership.items() if len(gs)>=2};bridges={p:gs for p,gs in elig.items() if gs&panels['B'] and gs&panels['C']};assert bridges,'No eligible bridges'
degree={g:sum(g in gs for gs in elig.values()) for g in maps};bucket=lambda n:0 if n==0 else 1 if n==1 else 2 if n<=4 else 3
strata={};alloc=1
for k in panels:
 strata[k]=[]
 for b in range(4):
  gs=sorted(g for g in panels[k] if bucket(degree[g])==b);n=len(set(gs)&det[k]);strata[k].append((gs,n));alloc*=math.comb(len(gs),n)
json.dump({'eligible_leaf_pathways':len(elig),'bridge_denominator':len(bridges),'degrees':degree,'allocations':alloc,'strata':strata},open(out/'eligibility.json','w'),indent=2)
if alloc<100:raise SystemExit('Underpowered null allocations: '+str(alloc))
stat=lambda d:sum(bool(gs&d['B']) and bool(gs&d['C']) for gs in bridges.values())/len(bridges)
obs=stat(det);rng=random.Random(261002);vals=[]
for i in range(10000):
 d={k:set().union(*(set(rng.sample(gs,n)) for gs,n in strata[k])) for k in panels};vals.append(stat(d))
res={'observed_fraction':obs,'observed_numerator':round(obs*len(bridges)),'denominator':len(bridges),'null_mean':sum(vals)/len(vals),'difference':obs-sum(vals)/len(vals),'p_one_sided':(1+sum(x>=obs for x in vals))/10001,'permutations':10000,'seed':261002,'distinct_null_allocations':alloc,'coverage':{k:{'panel_genes':len(panels[k]),'approved_entrez_mapped':len(panels[k]&maps.keys()),'any_TAS_leaf_annotation':sum(any(g in gs for gs in membership.values()) for g in panels[k]),'eligible_annotation':sum(degree[g]>0 for g in panels[k]),'detected_genes':len(det[k])} for k in panels},'unmapped':unmapped,'elapsed_seconds':time.monotonic()-t,'download_bytes':bytes_total};res['supported']=res['p_one_sided']<.05 and res['difference']>0;json.dump(res,open(out/'result.json','w'),indent=2);print(json.dumps(res,indent=2))