"""Synthetic input-contract tests. Never accepts/rebuilds a real DB."""
import pathlib,tempfile,json,hashlib,importlib.util
P=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('comparator',P/'compare_db_v4_19_2.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
root=pathlib.Path(tempfile.mkdtemp(prefix='route-b-fixtures-'));db=root/'db';db.mkdir()
# Override frozen source location/hash ONLY in this test module instance for synthetic bytes.
c.__file__=str(root/'comparator.py');a={'last-updated':'2026-10-09T16:58:00','dbname':'clytia','files':list(c.FIXED),'number-of-letters':420978673};old=root/c.OLD_NJS_FILENAME;old.write_text(json.dumps(a));oldbytes=old.read_bytes();binary=root/'binary';binary.write_bytes(b'fixture-binary');lockpath=root/'lock.json'
nin=bytearray(16836);nin[25:29]=bytes([0,0,0,27]);nin[29:56]=b'Oct 9, 2026  4:58 PM'+b'\x00'*7;nin=bytes(nin);(root/c.OLD_NIN_FILENAME).write_bytes(nin)
files=[{'file':n,'sha256':hashlib.sha256(nin if n=='clytia.nin' else b'fixture-index').hexdigest()} for n in c.FIXED]+[{'file':'clytia.njs','sha256':c.digest(old)},{'file':'makeblastdb','sha256':c.digest(binary)}]
for n in ['reference.fna','reference.fna.gz']:files.append({'file':n,'sha256':'a'*64,'md5':'b'*32})
for n in ['blast.tar.gz','tblastn']:files.append({'file':n,'sha256':'c'*64})
lock={'files':files};lockbytes=json.dumps(lock).encode();receipt={'fresh_download_verified':True,'compressed_md5':'b'*32,'compressed_sha256':'a'*64,'decompressed_md5':'b'*32,'decompressed_sha256':'a'*64,'bases':420978673,'scaffolds':1396};build={'argv':['./makeblastdb','-in','reference.fna','-dbtype','nucl','-parse_seqids','-blastdb_version','4','-out','clytia'],'exit':0,'stderr':'','stdout':'New DB title:  reference.fna\nSequence type: Nucleotide\nadded 1396 sequences'};cases=[]
def run(name,action=None):
 for x in db.iterdir():
  if x.is_dir() and not x.is_symlink():x.rmdir()
  else:x.unlink()
 for n in c.FIXED:(db/n).write_bytes(b'fixture-index')
 (root/c.OLD_NIN_FILENAME).write_bytes(nin)
 for_nin=bytearray(nin);for_nin[29:56]=b'Oct 9, 2026  5:00 PM'+b'\x00'*7;(db/'clytia.nin').write_bytes(for_nin)
 x=dict(a,last_updated=None);x.pop('last_updated');x['last-updated']='2026-10-09T17:00:00';(db/'clytia.njs').write_text(json.dumps(x));old.write_bytes(oldbytes);lockpath.write_bytes(lockbytes);c.LOCK_SHA256=c.digest(lockpath);binary.write_bytes(b'fixture-binary');br=json.loads(json.dumps(build));r=dict(receipt);complete='2026-10-09T17:10:00+05:30'
 if action:action(db,old,lockpath,br,r)
 out=c.check(lockpath,db,complete,binary,r,br);expect='PASS' if name=='valid' else 'HOLD';assert out['status']==expect,(name,out);cases.append({'case':name,'expected':expect,'actual':out['status'],'errors':out['errors']})
def editmeta(k,v):
 def f(d,o,l,b,r):x=json.loads((d/'clytia.njs').read_text());x[k]=v;(d/'clytia.njs').write_text(json.dumps(x))
 return f
def editlock(mode):
 def f(d,o,l,b,r):x=json.loads(l.read_text());x['files']=x['files'][:-1] if mode=='missing' else x['files']+[x['files'][0]];l.write_text(json.dumps(x))
 return f
run('valid');run('wrong-old-njs',lambda d,o,l,b,r:o.write_bytes(b'wrong'));run('lock-missing',editlock('missing'));run('lock-duplicate',editlock('duplicate'));run('component-changed',lambda d,o,l,b,r:(d/c.FIXED[0]).write_bytes(b'bad'));run('extra-file',lambda d,o,l,b,r:(d/'clytia.bad').write_bytes(b'x'));run('symlink',lambda d,o,l,b,r:((d/c.FIXED[0]).unlink(),(d/c.FIXED[0]).symlink_to(o)));run('directory',lambda d,o,l,b,r:((d/c.FIXED[0]).unlink(),(d/c.FIXED[0]).mkdir()));run('missing-file',lambda d,o,l,b,r:(d/c.FIXED[0]).unlink());run('before-window',editmeta('last-updated','2026-10-09T16:57:00'));run('after-window',editmeta('last-updated','2026-10-09T17:11:00'));run('invalid-time',editmeta('last-updated','bad'));run('extra-json-key',editmeta('extra',1));run('changed-path',editmeta('dbname','other'));run('wrong-argv',lambda d,o,l,b,r:b.update(argv=['wrong']));run('nonzero-build',lambda d,o,l,b,r:b.update(exit=1));run('bad-stdout',lambda d,o,l,b,r:b.update(stdout='wrong'));run('bad-ref',lambda d,o,l,b,r:r.update(bases=1));run('stderr',lambda d,o,l,b,r:b.update(stderr='warning'));run('binary-mismatch',lambda d,o,l,b,r:binary.write_bytes(b'wrong'))
def nin_edit(offset,data):
 def f(d,o,l,b,r):x=bytearray((d/'clytia.nin').read_bytes());x[offset:offset+len(data)]=data;(d/'clytia.nin').write_bytes(x)
 return f
run('nin-outside-mask',nin_edit(80,b'x'));run('nin-malformed',nin_edit(29,b'BAD'));run('nin-before-window',nin_edit(29,b'Oct 9, 2026  4:57 PM'));run('nin-after-window',nin_edit(29,b'Oct 9, 2026  5:11 PM'));run('nin-njs-disagree',nin_edit(29,b'Oct 9, 2026  5:05 PM'));run('nin-prefix',nin_edit(28,b'\x1a'));run('nin-shorter',lambda d,o,l,b,r:(d/'clytia.nin').write_bytes((d/'clytia.nin').read_bytes()[:-1]));run('nin-longer',lambda d,o,l,b,r:(d/'clytia.nin').write_bytes((d/'clytia.nin').read_bytes()+b'x'));run('nin-shifted-mask',nin_edit(28,b'Oct 9, 2026  5:00 PM'));run('nin-original-tampered',lambda d,o,l,b,r:(root/c.OLD_NIN_FILENAME).write_bytes(b'wrong'))
(P/'comparator-v4.19.2-synthetic-results.json').write_text(json.dumps({'status':'30 synthetic contracts only, production frozen hash never changed','synthetic_testing':'Loaded module copy overrides __file__ and expected lock hash only to use tiny synthetic fixtures; production source constants unchanged. Mutated lock fails frozen hash before structural validation. No real DB/rebuild/alignment.','production_comparator_sha256':hashlib.sha256((P/'compare_db_v4_19_2.py').read_bytes()).hexdigest(),'cases':cases},indent=2));print('30/30 expected synthetic outcomes')
