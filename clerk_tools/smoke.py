import json,re,time
from pathlib import Path
from genlayer_py import create_account,create_client
from genlayer_py.chains import studionet
from genlayer_py.types import TransactionStatus
ROOT=Path(__file__).parents[1];CFG=(ROOT.parents[3]/'accounts.env').read_text()
def key():return re.search(r'^ACCOUNT_1_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)',CFG,re.M).group(1).strip()
d=json.loads((ROOT/'evidence/deployment.json').read_text());client=create_client(chain=studionet,account=create_account(account_private_key=key()));address=d['contract']
def send(fn,args):
 tx=client.write_contract(address=address,function_name=fn,args=args);print(fn,tx,flush=True);client.wait_for_transaction_receipt(transaction_hash=tx,status=TransactionStatus.FINALIZED,retries=180,interval=5000);info=client.get_transaction(transaction_hash=tx);receipts=(info.get('consensus_data') or {}).get('leader_receipt') or []
 if info.get('status_name')!='FINALIZED' or info.get('result_name')!='MAJORITY_AGREE' or not any(x.get('execution_result')=='SUCCESS' for x in receipts):raise RuntimeError({'tx':tx,'status':info.get('status_name'),'result':info.get('result_name'),'receipts':receipts})
 return tx
i='ST-'+str(int(time.time()))
sources=['https://www.rfc-editor.org/rfc/rfc9110.txt','https://datatracker.ietf.org/doc/html/rfc9110']
created=send('propose',[i,'Which application protocol is specified by RFC 9110?',['HTTP','SMTP'],sources,600])
assessed=send('assess',[i])
challenged=send('challenge',[i,'https://developer.mozilla.org/en-US/docs/Web/HTTP'])
finalized=send('finalize',[i])
state=client.read_contract(address=address,function_name='get_resolution',args=[i])
assert state['state']=='FINAL' and state['answer']=='HTTP' and len(state['digests'])==3
proof={'resolutionId':i,'transactions':{'propose':created,'assess':assessed,'challenge':challenged,'finalize':finalized},'state':state};(ROOT/'evidence/network-run.json').write_text(json.dumps(proof,indent=2));print(json.dumps(proof,indent=2))
