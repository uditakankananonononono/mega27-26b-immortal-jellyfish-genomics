"""Exploratory held-out top-20 family check; never upgrades a cluster to discovery."""
import gzip,json
from pathlib import Path
from Bio import SeqIO
p=Path('/tmp/jelly-A-work')
j=json.load(open('results/x-20260928-A-train-ranking.json'))
O=json.load(open(p/'holdout_O.json'));C=json.load(open(p/'holdout_C.json'))
ids={f'M{i:06d}':r.id for i,r in enumerate(SeqIO.parse(gzip.open('/tmp/jelly-HC.pep.fa.gz','rt'),'fasta'),1)}
rows=[]
for x in j['ranked'][:20]:
 mids=[ids[y] for y in x['members'] if y.startswith('M')]
 contigs={z.rsplit('.g',1)[0] for z in mids}
 o={v['id'] for v in O.get(x['rep'],[])};c={v['id'] for v in C.get(x['rep'],[])}
 rows.append({'rank':len(rows)+1,'rep':x['rep'],'M_proteins':x['M'],'R_proteins':x['R'],
 'M_distinct_contigs':len(contigs),'M_gene_models':mids,'strict_max_M':x['strict_subcluster_max_M'],
 'Oviedo_hits_to_train_representative':len(o),'Clytia_hits_to_train_representative':len(c),
 'BH_q_all_training_clusters':x['BH_q_all_clusters']})
out={'status':'NO_VALIDATED_EXPANSION','train_commit':'7a806e176155ff397e2f54b67f2cb954ad98b813','final_lock':'46698df1742df9135a6585d010f8827c54c492c1',
'primary_groups':j['primary_clusters'],'qualifying':j['qualifying_families'],'top20':rows,
'limitation':'DIAMOND hits to the frozen representative are not orthogroup assignments, not independent DNA locus validation. Some top clusters contain neighboring gene predictions on the same contig. All top-20 all-cluster BH q=1.0; annotation counts differ 2.5-fold and Fisher exchangeability is dubious. The locked empirical null plus independent structural gate was not met. Panel-free sweep is a real exploratory analysis, NOT a positive gene-family discovery.'}
assert all(x['BH_q_all_training_clusters']==1.0 for x in rows)
Path('results/x-20260928-A-holdout.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'top5':[{k:v for k,v in x.items() if k!='M_gene_models'} for x in rows[:5]]},indent=2))
