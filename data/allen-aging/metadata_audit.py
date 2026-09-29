import csv,json,collections,sys,hashlib
from pathlib import Path
root=Path(__file__).resolve().parent
result={}
for key,filename in [('sound_life','sound_life_all_olink.csv'),('immunobiology_aging','imm-of-aging_all_olink.csv')]:
 p=root/filename
 donors=set();visits=set();samples=set();specimens=set();assays=set();panels=set();batches=set();plates=set();paired=collections.defaultdict(set);by_donor=collections.defaultdict(set);age_by_donor=collections.defaultdict(set);sex_by_donor=collections.defaultdict(set);cmv_by_donor=collections.defaultdict(set);visit_counts=collections.Counter();assay_rows=collections.Counter();missing=collections.Counter();n=0
 with p.open(newline='') as fh:
  reader=csv.DictReader(fh);cols=reader.fieldnames
  for row in reader:
   n+=1
   donor=row.get('subject.subjectGuid','');sample=row.get('sample.sampleKitGuid','');specimen=row.get('specimen.specimenGuid','');assay=row.get('olink.assay_id','');visit=row.get('sample.visitName','');panel=row.get('olink.panel','');batch=row.get('olink.batch_id','');plate=row.get('olink.plate_id','')
   if donor:donors.add(donor)
   if sample:samples.add(sample)
   if specimen:specimens.add(specimen)
   if assay:assays.add(assay);assay_rows[assay]+=1
   if panel:panels.add(panel)
   if batch:batches.add(batch)
   if plate:plates.add(plate)
   if visit:visits.add(visit);visit_counts[visit]+=1
   if donor and sample:paired[sample].add(donor);by_donor[donor].add(sample)
   if donor and row.get('sample.subjectAgeAtDraw',''):age_by_donor[donor].add(row['sample.subjectAgeAtDraw'])
   if donor and row.get('subject.biologicalSex',''):sex_by_donor[donor].add(row['subject.biologicalSex'])
   if donor and row.get('subject.cmv',''):cmv_by_donor[donor].add(row['subject.cmv'])
   for c in ['olink.NPX_raw','olink.NPX_norm','olink.LOD_raw','olink.LOD_norm','subject.subjectGuid','sample.sampleKitGuid','sample.subjectAgeAtDraw','subject.biologicalSex','subject.cmv']:
    if row.get(c,'').strip().lower() in ('','na','nan','null','none'):missing[c]+=1
   if n%1000000==0:print(key,n,file=sys.stderr,flush=True)
 sha=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(8*1024*1024):sha.update(b)
 result[key]={'path':str(p.relative_to(root.parent.parent)),'byte_count':p.stat().st_size,'sha256':sha.hexdigest(),'rows':n,'columns':cols,'distinct_donors':len(donors),'distinct_sample_kits':len(samples),'distinct_specimens':len(specimens),'distinct_assays':len(assays),'panels':sorted(panels),'batch_count':len(batches),'plate_count':len(plates),'visits':sorted(visits),'visit_row_counts':dict(visit_counts),'donors_in_multiple_sample_kits':sum(len(v)>1 for v in by_donor.values()),'sample_kits_with_multiple_donor_ids':sum(len(v)>1 for v in paired.values()),'sample_kits_without_donor_id':len(samples)-len(paired),'donor_sample_counts':dict(collections.Counter(str(len(x)) for x in by_donor.values())),'donors_with_multiple_recorded_ages':sum(len(v)>1 for v in age_by_donor.values()),'donors_with_multiple_sexes':sum(len(v)>1 for v in sex_by_donor.values()),'donors_with_multiple_cmv_values':sum(len(v)>1 for v in cmv_by_donor.values()),'missing_field_row_counts':dict(missing),'assay_row_count_min_max':[min(assay_rows.values()),max(assay_rows.values())]}
(root/'metadata_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:{x:y for x,y in v.items() if x not in ('visits','visit_row_counts','panels','columns','donor_sample_counts')} for k,v in result.items()},indent=2))
