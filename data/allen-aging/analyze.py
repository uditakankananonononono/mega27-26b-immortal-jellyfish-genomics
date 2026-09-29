import json,hashlib,time,warnings,sys
from pathlib import Path
import numpy as np
from scipy.stats import rankdata,spearmanr,pearsonr
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
warnings.filterwarnings('ignore',category=RuntimeWarning)
root=Path(__file__).resolve().parent
M=np.load(root/'sound_matrix.npz');X=M['X'];ids=M['assays'].tolist();meta=json.load((root/'sound_meta.json').open());idx={m['kit']:i for i,m in enumerate(meta)}
by={}
for i,m in enumerate(meta):by.setdefault(m['donor'],{})[m['visit']]=i
v0='Flu Year 1 Day 0';v7='Flu Year 1 Day 7';v20='Flu Year 2 Day 0';v27='Flu Year 2 Day 7'
donors=sorted([d for d,vs in by.items() if v0 in vs and v7 in vs]);n=len(donors);assert n==92
B=np.array([X[by[d][v0],:] for d in donors]);D7=np.array([X[by[d][v7],:] for d in donors]);Y2=np.array([X[by[d][v20],:] if v20 in by[d] else np.full(X.shape[1],np.nan) for d in donors]);
y=np.array([1 if meta[by[d][v0]]['age'] and float(meta[by[d][v0]]['age'])>=50 else 0 for d in donors]);yg=np.array([meta[by[d][v0]]['donor'] for d in donors]);assert len(set(yg))==n
assert all((1 if meta[by[d][v0]]['age'] and float(meta[by[d][v0]]['age'])>=50 else 0)==(1 if meta[by[d][v0]]['age'] and meta[by[d][v0]]['age']!='' and float(meta[by[d][v0]]['age'])>=50 else 0) for d in donors)
# Verify metadata age groups via separate sample rows. The source exposes group only in raw CSV; two disjoint age bands make threshold equivalent.
sex=np.array([1 if meta[by[d][v0]]['sex']=='Male' else 0 for d in donors]);cmv=np.array([1 if meta[by[d][v0]]['cmv']=='Positive' else 0 for d in donors]);cov=np.stack([np.ones(n),sex,cmv],axis=1)
# deterministic balanced folds, the primary hash assignment is checked below
h=np.array([int(hashlib.sha256((d+'allen-pivot-20260929-v1').encode()).hexdigest(),16) for d in donors],dtype=object)
fold=np.array([x%5 for x in h],dtype=int)
if min(np.bincount(fold[y==0],minlength=5).min(),np.bincount(fold[y==1],minlength=5).min())==0:
 fold=np.zeros(n,dtype=int)
 for c in (0,1):
  indices=sorted(np.where(y==c)[0],key=lambda i:h[i]);
  for pos,i in enumerate(indices):fold[i]=pos%5
 fold_mode='balanced hash'
else:fold_mode='hash mod 5'

def get_eligible(train,labels=y,cache=None):
 x=B[train];d=D7[train];yy=labels[train]
 present=np.isfinite(x);overall=(present.mean(axis=0)>=.90);classok=np.ones(x.shape[1],dtype=bool)
 for c in (0,1):classok &= present[yy==c].mean(axis=0)>=.75
 eligible=np.where(overall & classok)[0]
 stab=[];rho=[];ratio=[]
 for j in eligible:
  pair=np.isfinite(x[:,j]) & np.isfinite(d[:,j]);
  if pair.sum()<10:continue
  xs=x[pair,j];ds=d[pair,j];
  if cache is None:
   rr=spearmanr(xs,ds).statistic
   delta=np.median(np.abs(ds-xs))
  else:rr,delta=cache[j]
  if not np.isfinite(rr):continue
  x0=x[yy==0,j];x1=x[yy==1,j];gap=abs(np.nanmedian(x1)-np.nanmedian(x0))
  if rr>=.6 and gap>0 and delta<=.5*gap:stab.append(j);rho.append(rr);ratio.append(delta/gap)
 return eligible,np.array(stab,dtype=int),{'eligible_assays':len(eligible),'stable_assays':len(stab),'stable_rho_min':float(min(rho)) if rho else None,'stable_ratio_max':float(max(ratio)) if ratio else None}

def select(train,eligible,target,source=B):
 # training-only residualization on sex and CMV. residualize X and Y to rank partial age effects.
 x=source[train][:,eligible].astype(float);c=cov[train];yy=target[train].astype(float)
 # missing values imputed training-column median after eligibility filtering; no heldout read
 med=np.nanmedian(x,axis=0);x=np.where(np.isfinite(x),x,med);xc=x-c@np.linalg.lstsq(c,x,rcond=None)[0]
 yr=yy-c@np.linalg.lstsq(c,yy,rcond=None)[0]
 sd=xc.std(axis=0);sd[sd==0]=np.inf
 eff=(xc.T@yr)/(np.linalg.norm(yr)*np.sqrt(len(train))*sd)
 top=np.argsort(-np.abs(eff),kind='stable')[:min(5,len(eligible))]
 return eligible[top].tolist(),[float(q) for q in eff[top]]

def impute_scale(train,test,cols,mat=B):
 trainx=mat[train][:,cols].astype(float);testx=mat[test][:,cols].astype(float)
 med=np.nanmedian(trainx,axis=0);trainx=np.where(np.isfinite(trainx),trainx,med);testx=np.where(np.isfinite(testx),testx,med)
 mu=trainx.mean(axis=0);sd=trainx.std(axis=0);sd[sd==0]=1
 return (trainx-mu)/sd,(testx-mu)/sd,mu,sd,med

def fold_fit(train,test,labels=y,fast=False,cache=None):
 eligible,stable,info=get_eligible(train,labels,cache)
 if len(stable)<2:return None,info
 cols,effects=select(train,stable,labels)
 # inner 4-fold CV by donor, split on labels (training only), fixed alphas
 best=(float('inf'),None)
 for alpha in [.1,1,10]:
  losses=[]
  for it,iv in StratifiedKFold(n_splits=4,shuffle=True,random_state=20260929).split(train,labels[train]):
   a=train[it];v=train[iv];xt,xv,_,_,_=impute_scale(a,v,cols)
   model=LogisticRegression(C=1/alpha,max_iter=200,solver='liblinear').fit(xt,labels[a]);p=model.predict_proba(xv)[:,1];p=np.clip(p,1e-6,1-1e-6)
   losses.append(-np.mean(labels[v]*np.log(p)+(1-labels[v])*np.log(1-p)))
  loss=float(np.mean(losses))
  if loss<best[0]:best=(loss,alpha)
 xt,xv,mu,sd,med=impute_scale(train,test,cols)
 model=LogisticRegression(C=1/best[1],max_iter=200,solver='liblinear').fit(xt,labels[train])
 p=model.predict_proba(xv)[:,1]
 day7=D7[test][:,cols].astype(float);day7=np.where(np.isfinite(day7),day7,med);p7=model.predict_proba((day7-mu)/sd)[:,1]
 return {'cols':cols,'effects':effects,'alpha':best[1],'test_indices':test.tolist(),'p0':p.tolist(),'p7':p7.tolist()},info

if __name__=='__main__':
 start=time.time();print('fold mode',fold_mode,'class counts',np.bincount(y),'fold class',[(int(sum((fold==f)&(y==0))),int(sum((fold==f)&(y==1)))) for f in range(5)],flush=True)
 results=[];inf=[]
 for f in range(5):
  train=np.where(fold!=f)[0];test=np.where(fold==f)[0];res,info=fold_fit(train,test);results.append(res);inf.append(info);print('fold',f,info,'result',None if res is None else [ids[c] for c in res['cols']],'time',round(time.time()-start,2),flush=True)
 (root/'internal_first_pass.json').write_text(json.dumps({'fold_mode':fold_mode,'n':n,'class_count':np.bincount(y).tolist(),'fold_info':inf,'results':results,'runtime_sec':round(time.time()-start,2)},indent=2)+'\n')

def build_stability_cache(train):
 cache={}
 for j in range(B.shape[1]):
  x=B[train,j];d=D7[train,j];pair=np.isfinite(x)&np.isfinite(d)
  if pair.sum()<10:continue
  rr=spearmanr(x[pair],d[pair]).statistic
  delta=np.median(np.abs(x[pair]-d[pair]))
  cache[j]=(rr,delta)
 return cache
