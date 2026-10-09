"""Pre-alignment byte/metadata check. No rebuilding or alignment performed."""
import pathlib,json,hashlib,datetime,argparse,sys
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
        got=digest(binary);assert got==pins['makeblastdb'];out['makeblastdb_sha256']=got
    except Exception as e:out['errors'].append('binary:'+str(e))
    expected={'compressed_md5':next(x['md5'] for x in lock['files'] if x['file']=='reference.fna.gz'),'compressed_sha256':pins['reference.fna.gz'],'decompressed_md5':next(x['md5'] for x in lock['files'] if x['file']=='reference.fna'),'decompressed_sha256':pins['reference.fna'],'bases':420978673,'scaffolds':1396}
    out['reference_receipt']=reference_receipt
    if any(reference_receipt.get(k)!=v for k,v in expected.items()) or reference_receipt.get('fresh_download_verified') is not True:out['errors'].append('fresh reference receipt mismatch')
    if not out['errors'] and all(x['status']=='PASS' for x in out['components']) and out['njs']['status']=='PASS':out['status']='PASS'
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--lock',required=True);ap.add_argument('--rebuilt-db-dir',required=True);ap.add_argument('--rebuild-completion',required=True);ap.add_argument('--makeblastdb-binary',required=True);ap.add_argument('--fresh-reference-receipt',required=True);ap.add_argument('--build-receipt',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    result=check(pathlib.Path(a.lock),pathlib.Path(a.rebuilt_db_dir),a.rebuild_completion,pathlib.Path(a.makeblastdb_binary),json.load(open(a.fresh_reference_receipt)),json.load(open(a.build_receipt)));pathlib.Path(a.output).write_text(json.dumps(result,indent=2));print(result['status']);sys.exit(0 if result['status']=='PASS' else 2)
