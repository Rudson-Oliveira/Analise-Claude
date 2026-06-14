import json

from analise_context_mcp.repo import Repo


def _make_repo(tmp_path):
    (tmp_path / "CONTEXTO.json").write_text(
        json.dumps(
            {
                "meta": {"versao": "4.0", "proximo_passo": "FASE 2"},
                "empresa": {"nome": "Hospitalar"},
                "pendencias_tecnicas": [{"item": "OPENAI_API_KEY", "prioridade": "ALTA"}],
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text("# Projeto\nCOCKPIT-07 migrado para OpenRouter\n", "utf-8")
    return Repo(tmp_path)


def test_list_documents(tmp_path):
    repo = _make_repo(tmp_path)
    names = {d["name"] for d in repo.list_documents()}
    assert names == {"CONTEXTO.json", "README.md"}


def test_summary_extracts_meta(tmp_path):
    repo = _make_repo(tmp_path)
    summary = repo.summary()
    assert summary["versao"] == "4.0"
    assert summary["proximo_passo"] == "FASE 2"
    assert summary["empresa"]["nome"] == "Hospitalar"


def test_search_finds_term_with_context(tmp_path):
    repo = _make_repo(tmp_path)
    res = repo.search("cockpit-07")
    assert res["count"] == 1
    assert res["hits"][0]["document"] == "README.md"
    assert "OpenRouter" in res["hits"][0]["snippet"]


def test_read_document_rejects_traversal(tmp_path):
    repo = _make_repo(tmp_path)
    assert "error" in repo.read_document("../secret.json")
    assert "error" in repo.read_document("nope.md")


def test_read_document_ok(tmp_path):
    repo = _make_repo(tmp_path)
    out = repo.read_document("README.md")
    assert "COCKPIT-07" in out["content"]


def test_pending_via_context(tmp_path):
    repo = _make_repo(tmp_path)
    ctx = repo.context_json()
    assert ctx["pendencias_tecnicas"][0]["item"] == "OPENAI_API_KEY"
