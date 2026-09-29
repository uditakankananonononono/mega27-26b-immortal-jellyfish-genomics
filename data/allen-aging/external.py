import json, numpy as np
from pathlib import Path
from scipy.stats import spearmanr,rankdata,t as tdist
from sklearn.linear_model import LogisticRegression
import analyze as a
root=Path(__file__).resolve().parent
assert json.load(open(root/'permutation_verdict.json'))['permutation_p']<.05
ci=json.load(open(root/'internal_ci.json'));assert ci['baseline_auroc']>=.7 and ci['difference']>=-.1
train=np.arange(a.n)
eligible,stable,info=a.get_eligible(train)
assert len(stable)>=2
cols,effects=a.select(train,stable,a.y)
print('final selected', [(a.ids[j],eff) for j,eff in zip(cols,effects)])
# alpha selection on all Sound Life baseline donors by training-only fourfold CV
from sklearn.model_selection import StratifiedKFold
best=(float('inf'),None)
for alpha in [.1,1,10]:
 losses=[]
 for it,iv in StratifiedKFold(n_splits=4,shuffle=True,random_state=20260929).split(train,a.y):
  aa=train[it];vv=train[iv];xt,xv,_,_,_=a.impute_scale(aa,vv,cols)
  model=LogisticRegression(C=1/alpha,max_iter=200,solver='liblinear').fit(xt,a.y[aa]);p=np.clip(model.predict_proba(xv)[:,1],1e-6,1-1e-6)
  losses.append(-np.mean(a.y[vv]*np.log(p)+(1-a.y[vv])*np.log(1-p)))
 if np.mean(losses)<best[0]:best=(float(np.mean(losses)),alpha)
alpha=best[1];xt,_,mu,sd,med=a.impute_scale(train,train,cols)
model=LogisticRegression(C=1/alpha,max_iter=200,solver='liblinear').fit(xt,a.y)
M=np.load(root/'aging_matrix.npz');X=M['X'];ids=M['assays'].tolist();meta=json.load((root/'aging_meta.json').open());assert len(meta)==229
jidx=[ids.index(a.ids[c]) for c in cols];Z=X[:,jidx].astype(float);missing=np.isnan(Z);Z=np.where(np.isfinite(Z),Z,med);score=model.decision_function((Z-mu)/sd)
age=np.array([float(m['age']) if m['age'].isdigit() else float('nan') for m in meta]);sex=np.array([1 if m['sex']=='Male' else 0 for m in meta]);cmv=np.array([1 if m['cmv']=='Positive' else 0 for m in meta]);batch=np.array([m['batch'] for m in meta]);valid=np.isfinite(age)&np.isfinite(score)
print('valid',sum(valid),'age censored',sum(~np.isfinite(age)),'missing per feature',missing.sum(axis=0),'batches',dict(zip(*np.unique(batch,return_counts=True))))
# prespecified rank-based partial association adjusting sex, CMV and batch; OLS rank of age and score residualized on covariates
batches=sorted(set(batch[valid]));C=np.column_stack([np.ones(sum(valid)),sex[valid],cmv[valid]]+[np.array(batch[valid]==b,dtype=float) for b in batches[1:]])
def partial(x,y):
 xr=rankdata(x);yr=rankdata(y);dx=xr-C@np.linalg.lstsq(C,xr,rcond=None)[0];dy=yr-C@np.linalg.lstsq(C,yr,rcond=None)[0]
 r=float(np.corrcoef(dx,dy)[0,1]);df=len(x)-C.shape[1]-1;t=r*np.sqrt(df/(1-r*r));p=float(tdist.sf(t,df)) # one-sided positive gate
 return {'partial_rank_r':r,'p_positive':p,'n':len(x),'df':df}
res=partial(age[valid],score[valid]);print('score',res,'unadjusted',spearmanr(age[valid],score[valid]))
# Each assay: compare adjusted external age correlation sign against signed development age effect.
from statsmodels.stats.multitest import multipletests
ass=[]
for k,(col,eff) in enumerate(zip(cols,effects)):
 x=X[:,jidx[k]].astype(float);mask=valid&np.isfinite(x);c=C if mask.sum()==valid.sum() else None
 # adjust covariate matrix for assay-specific nonmissing subset
 batchm=batch[mask];bs=sorted(set(batchm));C=np.column_stack([np.ones(sum(mask)),sex[mask],cmv[mask]]+[np.array(batchm==b,dtype=float) for b in bs[1:]])
 q=partial(age[mask],x[mask]);p_two=min(1,2*min(q['p_positive'],1-q['p_positive']));ass.append({'assay_id':a.ids[col],'development_selection_score':eff,'external_partial_r':q['partial_rank_r'],'p_two_sided':p_two,'n':q['n'],'direction_agrees':bool(np.sign(eff)==np.sign(q['partial_rank_r']))})
 _,qs,_,_=multipletests([z['p_two_sided'] for z in ass],method='fdr_bh')
for z,q in zip(ass,qs):z['q_bh_five']=float(q)
print('assays',ass)
# Save full crosswalk by IDs not symbols; no post-hoc retune.
out={'selected_assays':ass,'development_alpha':alpha,'coef':model.coef_[0].tolist(),'intercept':float(model.intercept_[0]),'sound_eligible_and_stable_counts':info,'external_score':res,'external_unadjusted_spearman':float(spearmanr(age[valid],score[valid]).statistic),'external_complete_age_donors':int(sum(valid)),'external_89plus_censored':int(sum(~np.isfinite(age))),'external_missing_selected_NPX':missing.sum(axis=0).tolist(),'external_npx_filled_from_sound_training_medians':True,'score_positive_gate':bool(res['partial_rank_r']>0 and res['p_positive']<.05),'four_of_five_direction_agreement':bool(sum(z['direction_agrees'] for z in ass)>=4),'four_of_five_agree_and_q_lt_05':bool(sum(z['direction_agrees'] and z['q_bh_five']<.05 for z in ass)>=4)}
(root/'external_verdict.json').write_text(json.dumps(out,indent=2)+'\n')
