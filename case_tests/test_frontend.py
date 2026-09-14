from pathlib import Path

ROOT = Path(__file__).parents[1]
DOCS = ROOT / 'docs'


def test_six_page_production_flow_is_present():
    for name in ('index.html', 'file.html', 'review.html', 'challenge.html', 'lookup.html', 'guide.html'):
        page = DOCS / name
        assert page.exists() and page.read_text(encoding='utf-8').strip()


def test_frontend_uses_frozen_window_contract_interface():
    app = (DOCS / 'app.js').read_text(encoding='utf-8')
    review = (DOCS / 'review.html').read_text(encoding='utf-8')
    filing = (DOCS / 'file.html').read_text(encoding='utf-8')
    assert "transact('assess',[id],id)" in app
    assert "transact('assess',[id,Number(value('window'))],id)" not in app
    assert 'Challenge window after assessment' not in review
    assert 'duration is immutable after filing' in filing


def test_frontend_waits_for_finalized_and_exposes_source_divergence():
    app = (DOCS / 'app.js').read_text(encoding='utf-8')
    assert "status:'FINALIZED'" in app
    assert "state==='SOURCE_DIVERGED'" in app
    assert 'Latest retrieval digests' in app


def test_editable_evidence_and_authority_warning_are_visible():
    filing = (DOCS / 'file.html').read_text(encoding='utf-8')
    assert 'id="source-a"' in filing and 'id="source-b"' in filing
    assert 'Hostname separation does not prove independent ownership.' in filing
