import sys,time,json,numpy as np
from pathlib import Path
from sklearn.metrics import roc_auc_score
import analyze as a
root=Path(__file__).resolve().parent
start=int(sys.argv[1]);end=int(sys.argv[2]);seed=20260929
rng=np.random.default_rng(seed)
# locked strata sex+CMV, if any class absent inside stratum fall back sex only
strata=a.sex*2+a.cmv
if any(len(set(a.y[strata==v]))<2 for v in np.unique(strata)):strata=a.sex
obs=json.load(open(root/'internal_first_pass.json'));p=np.empty(a.n)
for z in obs['results']:
 for i,v in zip(z['test_indices'],z['p0']):p[i]=v
observed=float(roc_auc_score(a.y,p))
cache={f:a.build_stability_cache(np.where(a.fold!=f)[0]) for f in range(5)}
for k in range(end):
 yp=a.y.copy()
 for v in np.unique(strata):
  ix=np.where(strata==v)[0];yp[ix]=rng.permutation(yp[ix])
 if k<start:continue
 t=time.time();prob=np.empty(a.n);fail=False
 for f in range(5):
  tr=np.where(a.fold!=f)[0];te=np.where(a.fold==f)[0]
  if len(np.unique(yp[tr]))<2:fail=True;break
  z,info=a.fold_fit(tr,te,labels=yp,cache=cache[f])
  if z is None:fail=True;break
  for i,v in zip(z['test_indices'],z['p0']):prob[i]=v
 # a failed null fit is conservative: score 0.5, not post-hoc a zero
 val=float(roc_auc_score(yp,prob)) if not fail else 0.5
 print(k,round(val,8),int(fail),round(time.time()-t,4),flush=True)
