# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
from dataclasses import dataclass
import hashlib,json
from datetime import datetime, timezone

def cut(v,n=1000): return str(v).strip()[:n]
def key(v):
 x=cut(v,72).upper()
 if not x: raise gl.vm.UserError('[EXPECTED] resolution id required')
 return x
def url(v):
 s=cut(v,500); r=s[8:] if s.startswith('https://') else ''; h=r.split('/')[0].lower(); p=r[len(h):]
 if not h or '.' not in h or '@' in h or not p.startswith('/'): raise gl.vm.UserError('[EXPECTED] valid HTTPS source')
 return s,h
def parse(v):
 if isinstance(v,dict): return v
 s=str(v); a=s.find('{'); b=s.rfind('}')
 if a<0 or b<=a: raise gl.vm.UserError('[LLM_ERROR] invalid JSON')
 return json.loads(s[a:b+1])

@allow_storage
@dataclass
class Resolution:
 owner:Address; question:str; choices:str; sources:str; state:str; answer:str; findings:str; digests:str; challenge_end:u256; challenger:Address; challenge_source:str

class SignalTribunal(gl.Contract):
 resolutions:TreeMap[str,Resolution]
 def __init__(self): pass
 def _get(self,i):
  k=key(i)
  if k not in self.resolutions: raise gl.vm.UserError('[EXPECTED] resolution not found')
  return k,self.resolutions[k]
 def _judge(self,r,extra=''):
  sources=json.loads(r.sources)+([extra] if extra else [])
  def run():
   records=[]; digests=[]
   for index,link in enumerate(sources):
    raw=gl.nondet.web.get(link).body[:14000]; b=raw if isinstance(raw,bytes) else str(raw).encode(); digests.append(hashlib.sha256(b).hexdigest()); records.append({'source':index,'body':b.decode(errors='replace')})
   q='Resolve the question from the records. JSON only {"answer":"listed choice or INSUFFICIENT","finding_codes":[]}. QUESTION:'+r.question+' CHOICES:'+r.choices+' RECORDS:'+json.dumps(records)
   x=parse(gl.nondet.exec_prompt(q,response_format='json')); answer=cut(x.get('answer'),60).upper(); choices=json.loads(r.choices)
   if answer not in choices: answer='INSUFFICIENT'
   findings=sorted(set(cut(x,80).upper() for x in x.get('finding_codes',[])[:12] if cut(x,80)))
   return {'answer':answer,'findings':findings,'digests':digests}
  def valid(result):
   if not isinstance(result,gl.vm.Return): return False
   try:
    given=result.calldata; records=[]; digests=[]
    for index,link in enumerate(sources):
     raw=gl.nondet.web.get(link).body[:14000]; b=raw if isinstance(raw,bytes) else str(raw).encode(); digests.append(hashlib.sha256(b).hexdigest()); records.append({'source':index,'body':b.decode(errors='replace')})
    if given['digests']!=digests or given['answer'] not in json.loads(r.choices)+['INSUFFICIENT']: return False
    q='Verify the exact answer and every finding code from the records. JSON only {"valid":true}. QUESTION:'+r.question+' PROPOSAL:'+json.dumps({'answer':given['answer'],'findings':given['findings']})+' RECORDS:'+json.dumps(records)
    return bool(parse(gl.nondet.exec_prompt(q,response_format='json')).get('valid',False))
   except:return False
  return gl.vm.run_nondet_unsafe(run,valid)
 @gl.public.write
 def propose(self,i:str,question:str,choices:list[str],sources:list[str],challenge_seconds:u256)->None:
  k=key(i)
  if k in self.resolutions: raise gl.vm.UserError('[EXPECTED] duplicate resolution id')
  opts=sorted(set(cut(x,60).upper() for x in choices if cut(x,60))); links=[url(x) for x in sources]
  if len(opts)<2 or len(opts)>8 or len(links)!=2 or links[0][1]==links[1][1] or int(challenge_seconds)<60: raise gl.vm.UserError('[EXPECTED] complete independent resolution required')
  empty=Address('0x0000000000000000000000000000000000000000')
  self.resolutions[k]=Resolution(gl.message.sender_address,cut(question),json.dumps(opts),json.dumps([x[0] for x in links]),'PROPOSED','','[]','[]',u256(0),empty,'')
 @gl.public.write
 def assess(self,i:str,challenge_seconds:u256)->None:
  _,r=self._get(i)
  if r.state!='PROPOSED' or int(challenge_seconds)<60: raise gl.vm.UserError('[EXPECTED] assessment unavailable')
  x=self._judge(r); r.answer=x['answer']; r.findings=json.dumps(x['findings']); r.digests=json.dumps(x['digests']); r.challenge_end=u256(int(datetime.now(timezone.utc).timestamp())+int(challenge_seconds)); r.state='PROVISIONAL'
 @gl.public.write
 def challenge(self,i:str,conflicting_source:str)->None:
  _,r=self._get(i); link,host=url(conflicting_source)
  if r.state!='PROVISIONAL' or int(datetime.now(timezone.utc).timestamp())>int(r.challenge_end): raise gl.vm.UserError('[EXPECTED] challenge window closed')
  if host in [url(x)[1] for x in json.loads(r.sources)]: raise gl.vm.UserError('[EXPECTED] independent challenge host required')
  r.challenger=gl.message.sender_address; r.challenge_source=link; r.state='CHALLENGED'
 @gl.public.write
 def finalize(self,i:str)->None:
  _,r=self._get(i)
  if r.state=='PROVISIONAL':
   if int(datetime.now(timezone.utc).timestamp())<=int(r.challenge_end): raise gl.vm.UserError('[EXPECTED] challenge window open')
   r.state='FINAL'; return
  if r.state!='CHALLENGED': raise gl.vm.UserError('[EXPECTED] finalization unavailable')
  x=self._judge(r,r.challenge_source); r.answer=x['answer']; r.findings=json.dumps(x['findings']); r.digests=json.dumps(x['digests']); r.state='FINAL'
 @gl.public.view
 def get_resolution(self,i:str)->dict:
  k,r=self._get(i); return {'id':k,'owner':r.owner.as_hex,'question':r.question,'choices':json.loads(r.choices),'sources':json.loads(r.sources),'state':r.state,'answer':r.answer,'findings':json.loads(r.findings),'digests':json.loads(r.digests),'challengeEnd':int(r.challenge_end),'challenger':r.challenger.as_hex,'challengeSource':r.challenge_source}
