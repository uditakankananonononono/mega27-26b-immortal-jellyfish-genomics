"""Whole-proteome provisional cluster ranking, no holdout sequence read.
Reads the two frozen MMseqs train-only TSVs, never O or C. Annotation not used.
"""
import collections,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scipy.stats import fisher_exact
from jellyfish.xstats import bh_adjust
ROOT=Path('/tmp/jelly-A-work')
SIZES={'M':23314,'R':9324}
def groups(which):
 d=collections.defaultdict(list)
 for line in open(ROOT/f'{which}_cluster.tsv'):
  rep,member=line.strip().split('\t');assert member[0] in SIZES
  d[rep].append(member)
 assert sum(map(len,d.values()))==sum(SIZES.values())
 return d
p=groups('linprimary');q=groups('linstrict')
strict_members={member:frozenset(v) for v in q.values() for member in v}
rows=[]
for rep,v in p.items():
 m=sum(x.startswith('M') for x in v);r=len(v)-m
 if m<3 or r<1:continue
 ratio=(m/SIZES['M'])/(r/SIZES['R'])
 odds,pvalue=fisher_exact([[m,r],[SIZES['M']-m,SIZES['R']-r]],alternative='greater')
 rows.append({'rep':rep,'members':v,'M':m,'R':r,'corrected_ratio':ratio,'fisher_p':pvalue,
 'strict_subcluster_max_M':max(sum(x.startswith('M') for x in strict_members[x]) for x in v)})
# Correct across the full searched family universe, not only selected candidates.
allps=[]
for v in p.values():
 m=sum(x.startswith('M') for x in v);r=len(v)-m
 allps.append(fisher_exact([[m,r],[SIZES['M']-m,SIZES['R']-r]],alternative='greater')[1])
allq=bh_adjust(allps)
fullq=dict(zip(p,allq))
for x in rows:x['BH_q_all_clusters']=float(fullq[x['rep']])
rows.sort(key=lambda x:(-x['corrected_ratio'],-x['M'],x['rep']))
out={'lock_commit':'6e793f08cba33c71d95df6af6ff4bbf25ce76e54','method':'MMseqs2 easy-linclust low-memory operational deviation from easy-cluster; primary and strict thresholds unchanged','train_proteome_sizes':SIZES,'primary_clusters':len(p),'strict_clusters':len(q),'qualifying_families':len(rows),'ranked':rows,'top20_frozen_reps':[x['rep'] for x in rows[:20]],'caution':'Fisher/BH spans all primary clusters, but exchangeability is invalid when gene-prediction quality and proteome sizes differ markedly; q values are exploratory, not expansion validation. Clusters are not orthogroups.'}
Path('results/x-20260928-A-train-ranking.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'clusters':len(p),'qualifying':len(rows),'top20':[(x['rep'],x['M'],x['R'],round(x['corrected_ratio'],3)) for x in rows[:20]]},indent=2))
