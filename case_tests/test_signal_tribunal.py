from conftest import CONTRACT

SOURCES = ['https://primary.example/event/42', 'https://wire.example/event/42']
QUESTION = 'Did the independently recorded event 42 finish with a passing result?'


def web_mocks(vm, primary='Certified event 42 outcome: YES.', primary_status=200, include_appeal=False):
    vm.mock_web(r'primary\.example', {'status': primary_status, 'body': primary})
    vm.mock_web(r'wire\.example', {'status': 200, 'body': 'Wire archive: event 42 ended YES.'})
    if include_appeal:
        vm.mock_web(r'appeal\.example', {'status': 200, 'body': 'Independent appeal record also reports YES.'})


def decision_mocks(vm, answer='YES', findings='["FINAL_RECORD","TWO_SOURCE_MATCH"]', valid=None):
    vm.mock_llm(r'.*SignalTribunal resolver.*', '{"answer":"' + answer + '","finding_codes":' + findings + '}')
    if valid is not None:
        vm.mock_llm(r'.*SignalTribunal verifier.*', '{"valid":' + valid + '}')


def mocks(vm, include_appeal=False):
    vm.strict_mocks = True; vm.check_pickling = True; web_mocks(vm, include_appeal=include_appeal); decision_mocks(vm)


def proposed(vm, deploy, window=600):
    vm.warp('2030-01-01T00:00:00+00:00'); contract = deploy(CONTRACT)
    contract.propose('st-42', QUESTION, ['YES', 'NO'], SOURCES, window); return contract


def test_delayed_assessment_gets_the_full_frozen_window(direct_vm, direct_deploy):
    contract = proposed(direct_vm, direct_deploy, 3600); mocks(direct_vm)
    assert contract.get_resolution('ST-42')['challengeEnd'] == 0
    direct_vm.warp('2030-01-21T00:00:00+00:00'); contract.assess('ST-42')
    result = contract.get_resolution('ST-42')
    assert result['state'] == 'PROVISIONAL' and result['challengeWindow'] == 3600 and result['challengeEnd'] == 1895187600


def test_provisional_challenge_and_final_ruling(direct_vm, direct_deploy):
    contract = proposed(direct_vm, direct_deploy); mocks(direct_vm, include_appeal=True); contract.assess('ST-42')
    contract.challenge('ST-42', 'https://appeal.example/event/42'); contract.finalize('ST-42'); state = contract.get_resolution('ST-42')
    assert state['state'] == 'FINAL' and state['answer'] == 'YES' and len(state['digests']) == 3 and state['challengeAuthority'] == 'appeal.example'


def test_empty_question_duplicate_sources_and_window_bounds_fail(direct_vm, direct_deploy):
    contract = direct_deploy(CONTRACT)
    with direct_vm.expect_revert('complete independent resolution required'):
        contract.propose('EMPTY', '   ', ['YES', 'NO'], SOURCES, 600)
    with direct_vm.expect_revert('complete independent resolution required'):
        contract.propose('HOST', QUESTION, ['YES', 'NO'], [SOURCES[0], 'https://primary.example/other'], 600)
    with direct_vm.expect_revert('complete independent resolution required'):
        contract.propose('SHORT', QUESTION, ['YES', 'NO'], SOURCES, 599)
    with direct_vm.expect_revert('complete independent resolution required'):
        contract.propose('LONG', QUESTION, ['YES', 'NO'], SOURCES, 604801)


def test_failed_retrieval_and_malformed_model_output_fail(direct_vm, direct_deploy):
    contract = proposed(direct_vm, direct_deploy); direct_vm.strict_mocks = True; direct_vm.mock_web(r'primary\.example', {'status': 503, 'body': 'unavailable'})
    with direct_vm.expect_revert('source unavailable'):
        contract.assess('ST-42')
    direct_vm.clear_mocks(); web_mocks(direct_vm); decision_mocks(direct_vm, findings='[]')
    with direct_vm.expect_revert('bounded ruling required'):
        contract.assess('ST-42')


def test_validator_rejects_forged_output_disagreement_and_truthy_string(direct_vm, direct_deploy):
    contract = proposed(direct_vm, direct_deploy); mocks(direct_vm); result = contract._judge(contract.resolutions['ST-42']); direct_vm.mock_llm(r'.*SignalTribunal verifier.*', '{"valid":true}')
    assert direct_vm.run_validator(leader_result=result) is True
    forged = dict(result); forged['digests'] = list(reversed(result['digests'])); assert direct_vm.run_validator(leader_result=forged) is False
    direct_vm.clear_mocks(); web_mocks(direct_vm); direct_vm.mock_llm(r'.*SignalTribunal verifier.*', '{"valid":false}')
    assert direct_vm.run_validator(leader_result=result) is False
    direct_vm.clear_mocks(); web_mocks(direct_vm); direct_vm.mock_llm(r'.*SignalTribunal verifier.*', '{"valid":"true"}')
    assert direct_vm.run_validator(leader_result=result) is False


def test_mutable_original_source_divergence_is_terminal_and_explicit(direct_vm, direct_deploy):
    contract = proposed(direct_vm, direct_deploy); mocks(direct_vm); contract.assess('ST-42'); original = contract.get_resolution('ST-42')['digests']
    contract.challenge('ST-42', 'https://appeal.example/event/42')
    direct_vm.clear_mocks(); web_mocks(direct_vm, primary='MUTATED: event 42 now claims NO.', include_appeal=True); decision_mocks(direct_vm, answer='NO', findings='["SOURCE_CHANGED"]')
    contract.finalize('ST-42'); state = contract.get_resolution('ST-42')
    assert state['state'] == 'SOURCE_DIVERGED' and state['answer'] == 'YES' and state['digests'] == original and state['latestDigests'][:2] != original


def test_challenge_and_finalization_boundaries(direct_vm, direct_deploy):
    contract = proposed(direct_vm, direct_deploy); mocks(direct_vm); contract.assess('ST-42')
    with direct_vm.expect_revert('challenge window open'):
        contract.finalize('ST-42')
    with direct_vm.expect_revert('independent challenge host required'):
        contract.challenge('ST-42', 'https://primary.example/another')
    direct_vm.warp('2030-01-01T00:10:00+00:00'); contract.challenge('ST-42', 'https://appeal.example/event/42')
    with direct_vm.expect_revert('challenge window closed'):
        contract.challenge('ST-42', 'https://fourth.example/event/42')


def test_uncontested_case_finalizes_only_after_boundary(direct_vm, direct_deploy):
    contract = proposed(direct_vm, direct_deploy); mocks(direct_vm); contract.assess('ST-42')
    direct_vm.warp('2030-01-01T00:10:00+00:00')
    with direct_vm.expect_revert('challenge window open'):
        contract.finalize('ST-42')
    direct_vm.warp('2030-01-01T00:10:01+00:00'); contract.finalize('ST-42')
    assert contract.get_resolution('ST-42')['state'] == 'FINAL'
