import csv,json,numpy as np
from pathlib import Path
root=Path(__file__).resolve().parent
for cohort,fn in [('sound','sound_life_all_olink.csv'),('aging','imm-of-aging_all_olink.csv')]:
 assays=set();kitmeta={};values={};lod={};duplicates=0
 with (root/fn).open(newline='') as f:
  for r in csv.DictReader(f):
   kit=r['sample.sampleKitGuid'];assay=r['olink.assay_id'];assays.add(assay)
   m=(r['subject.subjectGuid'],r['sample.visitName'],r['sample.subjectAgeAtDraw'],r['subject.biologicalSex'],r['subject.cmv'],r['olink.batch_id'])
   if kit in kitmeta and kitmeta[kit]!=m:raise AssertionError(('kit meta mismatch',kit,kitmeta[kit],m))
   kitmeta[kit]=m
   key=(kit,assay)
   if key in values:duplicates+=1
   npx=r['olink.NPX_norm'];lv=r['olink.LOD_norm']
   try: val=float(npx);ll=float(lv);val=val if val>=ll else float('nan')
   except ValueError:val=float('nan')
   values[key]=val
  assert not duplicates,duplicates
 ks=sorted(kitmeta);ass=sorted(assays);kidx={k:i for i,k in enumerate(ks)};aidx={a:i for i,a in enumerate(ass)}
 matrix=np.full((len(ks),len(ass)),np.nan,dtype=np.float32)
 for (kit,assay),v in values.items():matrix[kidx[kit],aidx[assay]]=v
 meta=[{'kit':k,'donor':kitmeta[k][0],'visit':kitmeta[k][1],'age':kitmeta[k][2],'sex':kitmeta[k][3],'cmv':kitmeta[k][4],'batch':kitmeta[k][5]} for k in ks]
 np.savez_compressed(root/(cohort+'_matrix.npz'),X=matrix,assays=np.array(ass),kits=np.array(ks))
 (root/(cohort+'_meta.json')).write_text(json.dumps(meta,indent=1))
 print(cohort,matrix.shape,'measured',np.isfinite(matrix).sum(),'missing',np.isnan(matrix).sum(),flush=True)
