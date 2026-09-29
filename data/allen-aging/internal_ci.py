import json,sys,numpy as np
from sklearn.metrics import roc_auc_score
import analyze as a
j=json.load(open('data/allen-aging/internal_first_pass.json'));p0=np.full(a.n,np.nan);p7=p0.copy()
for z in j['results']:
 for i,x,y in zip(z['test_indices'],z['p0'],z['p7']):p0[i]=x;p7[i]=y
assert np.isfinite(p0).all() and np.isfinite(p7).all()
rng=np.random.default_rng(20260930);bs=[];d=[]
for _ in range(2000):
 idx=rng.integers(0,a.n,a.n)
 if len(set(a.y[idx]))<2:continue
 x=roc_auc_score(a.y[idx],p0[idx]);v=roc_auc_score(a.y[idx],p7[idx]);bs.append(x);d.append(v-x)
res={'baseline_auroc':roc_auc_score(a.y,p0),'day7_auroc':roc_auc_score(a.y,p7),'difference':roc_auc_score(a.y,p7)-roc_auc_score(a.y,p0),'baseline_95pct_donor_bootstrap':np.quantile(bs,[.025,.975]).tolist(),'difference_95pct_donor_bootstrap':np.quantile(d,[.025,.975]).tolist(),'bootstrap_count':len(bs)}
print(json.dumps(res,indent=2));open('data/allen-aging/internal_ci.json','w').write(json.dumps(res,indent=2)+'\n')
