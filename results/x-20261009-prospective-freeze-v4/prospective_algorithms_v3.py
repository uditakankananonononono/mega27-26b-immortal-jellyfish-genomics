"""Deterministic pre-discovery test implementation. No Clytia alignment code."""
import hashlib,json

def pair(a,b):
    # Needleman-Wunsch score, diagonal/delete/insert tie priority.
    n,m=len(a),len(b);d=[[0]*(m+1) for _ in range(n+1)]
    for i in range(n+1):d[i][0]=-i
    for j in range(m+1):d[0][j]=-j
    for i in range(1,n+1):
        for j in range(1,m+1):d[i][j]=max(d[i-1][j-1]+(1 if a[i-1]==b[j-1] else -1),d[i-1][j]-1,d[i][j-1]-1)
    i,j=n,m;paired=identical=0
    while i or j:
        if i and j and d[i][j]==d[i-1][j-1]+(1 if a[i-1]==b[j-1] else -1):
            paired+=1;identical+=a[i-1]==b[j-1];i-=1;j-=1
        elif i and d[i][j]==d[i-1][j]-1:i-=1
        else:j-=1
    return {'paired':paired,'identical':identical,'longer':max(n,m),'duplicate':paired>0 and identical*10>=paired*9 and paired*5>=max(n,m)*4}

def cluster(records):
    ordered=sorted(records,key=lambda x:(x['label'],x['accession']));groups=[{i} for i in range(len(ordered))];edges=[]
    for i in range(len(ordered)):
        for j in range(i+1,len(ordered)):
            if pair(ordered[i]['sequence'],ordered[j]['sequence'])['duplicate']:
                edges.append([ordered[i]['label'],ordered[j]['label']]);a=next(g for g in groups if i in g);b=next(g for g in groups if j in g)
                if a is not b:a.update(b);groups.remove(b)
    return {'edges':edges,'components':[[ordered[i]['label'] for i in sorted(g)] for g in sorted(groups,key=min)],'retained':[ordered[min(g)]['label'] for g in sorted(groups,key=min)]}

def scramble(sequence,index):
    H=hashlib.sha256(sequence.encode('ascii')).hexdigest();counter=0;words=[];a=list(sequence)
    for k in range(len(a)-1,0,-1):
        bound=k+1;limit=2**64-(2**64%bound)
        while True:
            if not words:
                digest=hashlib.sha256(f'{H}:{index}:{counter}'.encode('ascii')).digest();counter+=1
                words=[int.from_bytes(digest[t:t+8],'big') for t in range(0,32,8)]
            w=words.pop(0)
            if w<limit:break
        j=w%bound;a[k],a[j]=a[j],a[k]
    return ''.join(a)

def realmatch(targets,pool):
    used=set();out=[]
    for t in sorted(targets,key=lambda t:t['label']):
        L=len(t['sequence']);c=[x for x in pool if x['accession'] not in used and 5*len(x['sequence'])>=4*L and 4*len(x['sequence'])<=5*L]
        c.sort(key=lambda x:(abs(len(x['sequence'])-L),x['accession']))
        chosen=c[0] if c else None
        if chosen:used.add(chosen['accession'])
        out.append({'label':t['label'],'null':chosen['accession'] if chosen else None})
    return out

def overlap(rows):
    # Inclusive coordinates, any >=1bp overlap on same contig. Connected components.
    rows=sorted(rows,key=lambda x:x['label']);groups=[{i} for i in range(len(rows))]
    for i,a in enumerate(rows):
        for j,b in enumerate(rows[i+1:],i+1):
            if a['contig']==b['contig'] and max(a['start'],b['start'])<=min(a['end'],b['end']):
                g=next(g for g in groups if i in g);h=next(g for g in groups if j in g)
                if g is not h:g.update(h);groups.remove(h)
    return [[rows[i]['label'] for i in sorted(g)] for g in sorted(groups,key=min)]

def vector(v):
    return {'cluster':cluster(v['records']),'scrambles':[scramble(x['sequence'],v['index']) for x in sorted(v['records'],key=lambda x:(x['label'],x['accession']))],'real_matches':realmatch(v['records'],v['pool']),'overlap':overlap(v['loci'])}

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode('ascii')
