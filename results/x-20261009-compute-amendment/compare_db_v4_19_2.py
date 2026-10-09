"""Pre-alignment byte/metadata check. No rebuilding or alignment performed."""
import pathlib,json,hashlib,datetime,argparse,sys,re
FIXED=('clytia.nhr','clytia.nin','clytia.nog','clytia.nsd','clytia.nsi','clytia.nsq')
OFFSET=datetime.timezone(datetime.timedelta(hours=5,minutes=30))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def timestamp(s):
    if not isinstance(s,str):raise ValueError('timestamp not string')
    t=datetime.datetime.fromisoformat(s)
    if 'T' not in s:raise ValueError('timestamp must have date and time')
    return t.replace(tzinfo=OFFSET) if t.tzinfo is None else t

LOCK_SHA256='ef052d846a3eacd6b2d5a1bbda5ad6e93f1ed40f984718c37c8a6a72b9d49372'
OLD_NJS_FILENAME='locked-original-clytia.njs'
OLD_NIN_FILENAME='locked-original-clytia.nin'
NIN_MASK_OFFSET=29
NIN_MASK_LENGTH=27
NIN_PREFIX_OFFSET=25
def check(lock_path,new,completed,binary,reference_receipt,build_receipt):
    out={'status':'HOLD','components':[],'errors':[]}
    try:
        if lock_path.is_symlink() or not lock_path.is_file():raise ValueError('lock not regular file')
        if digest(lock_path)!=LOCK_SHA256:raise ValueError('lock byte hash not frozen')
        lock=json.loads(lock_path.read_text())
        expected_files={'blast.tar.gz','clytia.nhr','clytia.nin','clytia.njs','clytia.nog','clytia.nsd','clytia.nsi','clytia.nsq','makeblastdb','reference.fna','reference.fna.gz','tblastn'}
        names=[x['file'] for x in lock['files']]
        if len(names)!=len(set(names)) or set(names)!=expected_files:raise ValueError('extra/missing/duplicate lock entries')
        pins={x['file']:x['sha256'] for x in lock['files']}
        if any(not isinstance(v,str) or len(v)!=64 or any(c not in '0123456789abcdef' for c in v) for v in pins.values()):raise ValueError('invalid hash')
        # Fixed adjacent metadata artifact, no executor-selected old-directory or path.
        old_njs=pathlib.Path(__file__).resolve().parent/OLD_NJS_FILENAME
        if old_njs.is_symlink() or not old_njs.is_file():raise ValueError('old njs not regular')
        if digest(old_njs)!=pins['clytia.njs']:raise ValueError('old njs hash mismatch before parse')
    except Exception as e:
        out['errors'].append('frozen inputs:'+str(e));return out
    required=set(FIXED)|{'clytia.njs'}
    for role,directory in [('rebuilt',new)]:
        try:
            entries=list(directory.iterdir())
            if {x.name for x in entries}!=required:raise ValueError('extra/missing component')
            for x in entries:
                if x.is_symlink() or not x.is_file():raise ValueError('nonregular component '+x.name)
                with x.open('rb') as f:f.read(1)
            out[role+'_file_set']='PASS'
        except Exception as e:out['errors'].append(role+' exact-file-set:'+str(e))
    expected_argv=['./makeblastdb','-in','reference.fna','-dbtype','nucl','-parse_seqids','-blastdb_version','4','-out','clytia']
    if build_receipt.get('argv')!=expected_argv or build_receipt.get('exit')!=0 or build_receipt.get('stderr')!='':out['errors'].append('build argv/exit/stderr mismatch')
    stdout=build_receipt.get('stdout')
    if not isinstance(stdout,str) or not all(x in stdout for x in ['New DB title:  reference.fna','Sequence type: Nucleotide','added 1396 sequences']):out['errors'].append('build stdout title/type/count mismatch')
    out['build_receipt']=build_receipt
    for name in FIXED:
        if name=='clytia.nin':continue
        try:
            got=digest(new/name);out['components'].append({'component':name,'sha256':got,'locked_sha256':pins[name],'status':'PASS' if got==pins[name] else 'FAIL'})
        except Exception as e:out['components'].append({'component':name,'status':'FAIL','error':str(e)})
    try:
        old_raw=digest(old_njs);new_raw=digest(new/'clytia.njs');a=json.loads(old_njs.read_text());b=json.loads((new/'clytia.njs').read_text());assert isinstance(a,dict) and isinstance(b,dict)
        diff=[k for k in sorted(set(a)|set(b)) if a.get(k)!=b.get(k) or (k in a)!=(k in b)]
        c=datetime.datetime.fromisoformat(completed);assert c.tzinfo is not None,'completion must have UTC offset';t=timestamp(b['last-updated']);low=timestamp('2026-10-09T16:58:00');window=low<=t<=c
        good=old_raw==pins['clytia.njs'] and set(a)==set(b) and all(k=='last-updated' for k in diff) and window
        # Locked timestamp must also parse, independently of rebuild time.
        timestamp(a['last-updated'])
        out['njs']={'status':'PASS' if good else 'FAIL','locked_raw_sha256':old_raw,'rebuilt_raw_sha256':new_raw,'locked_parsed':a,'rebuilt_parsed':b,'diff_fields':diff,'timestamp_window_pass':window,'lower_iso':low.isoformat(),'rebuild_completion_iso':c.isoformat(),'last_updated_iso':t.isoformat()}
    except Exception as e:out['njs']={'status':'FAIL','error':str(e)}
    try:
        old_nin=pathlib.Path(__file__).resolve().parent/OLD_NIN_FILENAME
        if old_nin.is_symlink() or not old_nin.is_file():raise ValueError('original nin missing/nonregular')
        original=old_nin.read_bytes();rebuilt=(new/'clytia.nin').read_bytes()
        if hashlib.sha256(original).hexdigest()!=pins['clytia.nin']:raise ValueError('original nin hash mismatch')
        out['nin_evidence']={'original_sha256':hashlib.sha256(original).hexdigest(),'rebuilt_sha256':hashlib.sha256(rebuilt).hexdigest(),'diff_offsets':[i for i,(a,b) in enumerate(zip(original,rebuilt)) if a!=b],'original_length':len(original),'rebuilt_length':len(rebuilt)}
        if len(original)!=16836 or len(rebuilt)!=16836:raise ValueError('nin length mismatch')
        for raw in [original,rebuilt]:
            if raw[NIN_PREFIX_OFFSET:NIN_PREFIX_OFFSET+4]!=bytes([0,0,0,27]):raise ValueError('nin length prefix not27')
        def nin_date(raw):
            text=raw[NIN_MASK_OFFSET:NIN_MASK_OFFSET+NIN_MASK_LENGTH].decode('ascii')
            # Date value plus trailing NUL/space padding occupies the fixed27byte region.
            value=text.split('\x00',1)[0]
            if text[len(value):] != '\x00'*(27-len(value)):raise ValueError('nin padding notNUL')
            match=re.fullmatch(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) ([1-9]|[12][0-9]|3[01]), ([0-9]{4})  ([1-9]|1[0-2]):([0-5][0-9]) (AM|PM)',value)
            if not match:raise ValueError('nin malformed date')
            months={m:i+1 for i,m in enumerate(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])}
            month,day,year,hour,minute,ampm=match.groups();hour=int(hour)%12+(12 if ampm=='PM' else 0)
            return text,datetime.datetime(int(year),months[month],int(day),hour,int(minute),tzinfo=OFFSET)
        original_text,original_time=nin_date(original);rebuilt_text,rebuilt_time=nin_date(rebuilt)
        differences=[i for i,(a,b) in enumerate(zip(original,rebuilt)) if a!=b]
        if any(not NIN_MASK_OFFSET<=i<NIN_MASK_OFFSET+NIN_MASK_LENGTH for i in differences):raise ValueError('nin diff outside exactmask')
        completion=datetime.datetime.fromisoformat(completed)
        if completion.tzinfo is None:raise ValueError('completion offset required')
        lower=timestamp('2026-10-09T16:58:00')
        if not lower<=rebuilt_time<=completion:raise ValueError('nin date outside window')
        rebuilt_njs_time=timestamp(out['njs']['rebuilt_parsed']['last-updated'])
        if abs((rebuilt_time-rebuilt_njs_time).total_seconds())>60:raise ValueError('nin/njs discrepancy greater than1minute')
        out['nin']={'status':'PASS','original_sha256':hashlib.sha256(original).hexdigest(),'rebuilt_sha256':hashlib.sha256(rebuilt).hexdigest(),'diff_offsets':differences,'mask_offset':NIN_MASK_OFFSET,'mask_length':NIN_MASK_LENGTH,'prefix_offset':NIN_PREFIX_OFFSET,'original_decoded':original_text,'rebuilt_decoded':rebuilt_text,'original_iso':original_time.isoformat(),'rebuilt_iso':rebuilt_time.isoformat(),'outside_mask_equal_bytes':16809,'njs_cross_consistency_pass':True}
    except Exception as e:out['nin']={'status':'FAIL','error':str(e)}
    try:
        got=digest(binary);assert got==pins['makeblastdb'];out['makeblastdb_sha256']=got
    except Exception as e:out['errors'].append('binary:'+str(e))
    expected={'compressed_md5':next(x['md5'] for x in lock['files'] if x['file']=='reference.fna.gz'),'compressed_sha256':pins['reference.fna.gz'],'decompressed_md5':next(x['md5'] for x in lock['files'] if x['file']=='reference.fna'),'decompressed_sha256':pins['reference.fna'],'bases':420978673,'scaffolds':1396}
    out['reference_receipt']=reference_receipt
    if any(reference_receipt.get(k)!=v for k,v in expected.items()) or reference_receipt.get('fresh_download_verified') is not True:out['errors'].append('fresh reference receipt mismatch')
    if not out['errors'] and all(x['status']=='PASS' for x in out['components']) and out['njs']['status']=='PASS' and out['nin']['status']=='PASS':out['status']='PASS'
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--lock',required=True);ap.add_argument('--rebuilt-db-dir',required=True);ap.add_argument('--rebuild-completion',required=True);ap.add_argument('--makeblastdb-binary',required=True);ap.add_argument('--fresh-reference-receipt',required=True);ap.add_argument('--build-receipt',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    result=check(pathlib.Path(a.lock),pathlib.Path(a.rebuilt_db_dir),a.rebuild_completion,pathlib.Path(a.makeblastdb_binary),json.load(open(a.fresh_reference_receipt)),json.load(open(a.build_receipt)));pathlib.Path(a.output).write_text(json.dumps(result,indent=2));print(result['status']);sys.exit(0 if result['status']=='PASS' else 2)
