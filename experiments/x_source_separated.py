import json,sys,hashlib
sys.path.insert(0,".")
from jellyfish.loci import cluster_loci
MB=100
def qdet(hs): return any(l["total_bits"]>=MB for l in cluster_loci(hs)) if hs else False
def score(raw,verified,labels):
    out={}
    for g in labels:
        hum=[h for k,v in raw.items() if k==f"human_{g}" for h in v]
        qs={k:v for k,v in raw.items() if k.split("_",1)[1]==g and k in verified}
        pooled=any(l["total_bits"]>=MB for l in cluster_loci([h for k,v in raw.items() if k.split("_",1)[1]==g for h in v]))
        cons_h=qdet(hum)
        cons_m=any(qdet(v) for v in qs.values())
        out[g]=dict(pooled=pooled,cons_human=cons_h,cons_multi=cons_m,n_verified_nonhuman=len([k for k in qs if not k.startswith("human_")]))
    return out
def H(c,s,e,b,q="q"): return dict(qseqid=q,contig=c,sstart=s,send=e,bits=b,pident=50,qcov=.5)
# fixtures
fx={"a":[H("c",1,100,60),H("c",200,300,60)],"b":[H("c",1,100,120)],"c":[H("c",1,100,60),H("d",1,100,60)]}
r=score({"x_G":[fx["a"][0]],"y_G":[fx["a"][1]]},{"x_G","y_G"},["G"]);assert r["G"]["pooled"] and not r["G"]["cons_multi"]
r=score({"x_G":fx["b"]},{"x_G"},["G"]);assert r["G"]["cons_multi"]
r=score({"x_G":fx["b"],"y_G":fx["b"]},{"x_G","y_G"},["G"]);assert r["G"]["cons_multi"]
r=score({"x_G":fx["c"]},{"x_G"},["G"]);assert not r["G"]["cons_multi"]
r=score({"x_G":[fx["a"][0]],"y_G":[fx["a"][0]]},{"x_G","y_G"},["G"]);assert not r["G"]["cons_multi"]
print("fixtures pass")
raw=json.load(open("results/x-tblastn-bc.json"))["Clytia"]
aud=json.load(open("results/x-20261007-query-provenance/nonhuman-audit.json"))
ver={r["key"] for r in aud if r["status"]=="verified_by_name"}
labels=sorted(json.load(open("data/xpanel_fixed/verify_report.json")).keys())
verified=ver|{k for k in raw if k.startswith("human_")}
res=score(raw,verified,labels)
n=len(labels);mh=sum(v["cons_human"] for v in res.values());mm=sum(v["cons_multi"] or v["cons_human"] for v in res.values())
gain=[g for g,v in res.items() if v["cons_multi"] and not v["cons_human"]]
orig=json.load(open("results/x-benchmark-recall.json"))["recovered_only_via_nonhuman"]
pooled_gain=[g for g,v in res.items() if v["pooled"] and not v["cons_human"]]
untest=[g for g,v in res.items() if v["n_verified_nonhuman"]==0]
out=dict(labels=n,cons_human=mh,cons_multi_union=mm,gain=gain,n_gain=len(gain),original_eight=orig,eight_remaining=[g for g in orig if g in gain],pooled_gain_in_this_run=pooled_gain,labels_zero_verified_nonhuman=untest,table=res,
 human_subset_ok=all(v["cons_human"]<=(v["cons_multi"] or v["cons_human"]) for v in res.values()),
 note="existing HSPs only; no replacement alignments; verification by header name")
json.dump(out,open("results/x-20261007-source-separated/outcome.json","w"),indent=1)
print({k:v for k,v in out.items() if k!="table"})
