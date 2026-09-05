from conftest import CONTRACT
SOURCES=['https://primary.example/event/42','https://wire.example/event/42']
def mocks(vm,answer='YES'):
 vm.strict_mocks=True;vm.check_pickling=True
 vm.mock_web(r'primary\.example',{'status':200,'body':'Certified event 42 outcome: YES.'});vm.mock_web(r'wire\.example',{'status':200,'body':'Wire archive: event 42 ended YES.'});vm.mock_web(r'appeal\.example',{'status':200,'body':'Independent appeal record also reports YES.'})
 vm.mock_llm(r'.*Resolve the question.*','{"answer":"'+answer+'","finding_codes":["FINAL_RECORD","TWO_SOURCE_MATCH"]}');vm.mock_llm(r'.*Verify the exact answer.*','{"valid":true}')
def test_provisional_challenge_and_final_ruling(direct_vm,direct_deploy):
 direct_vm.warp('2030-01-01T00:00:00+00:00');c=direct_deploy(CONTRACT);mocks(direct_vm);c.propose('st-42','Did event 42 pass?',['YES','NO'],SOURCES,600);c.assess('ST-42',600);assert c.get_resolution('ST-42')['state']=='PROVISIONAL';c.challenge('ST-42','https://appeal.example/event/42');c.finalize('ST-42');s=c.get_resolution('ST-42');assert s['state']=='FINAL' and s['answer']=='YES' and len(s['digests'])==3
def test_duplicate_sources_and_challenge_origin_rejected(direct_vm,direct_deploy):
 c=direct_deploy(CONTRACT)
 with direct_vm.expect_revert('independent resolution'):c.propose('A','Question?',['YES','NO'],[SOURCES[0],SOURCES[0]],600)
 c.propose('A','Question?',['YES','NO'],SOURCES,600)
 with direct_vm.expect_revert('duplicate resolution'):c.propose(' a ','Question?',['YES','NO'],SOURCES,600)
 mocks(direct_vm);c.assess('A',600)
 with direct_vm.expect_revert('independent challenge'):c.challenge('A','https://primary.example/other')
def test_forged_findings_or_digest_fail_validator(direct_vm,direct_deploy):
 c=direct_deploy(CONTRACT);mocks(direct_vm);c.propose('X','Did event 42 pass?',['YES','NO'],SOURCES,600);r=c.resolutions['X'];result=c._judge(r);assert direct_vm.run_validator(leader_result=result) is True;forged=dict(result);forged['digests']=list(reversed(result['digests']));assert direct_vm.run_validator(leader_result=forged) is False
