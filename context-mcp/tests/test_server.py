import asyncio
import json

from analise_context_mcp.server import create_server


def _seed(tmp_path):
    (tmp_path / "CONTEXTO.json").write_text(
        json.dumps({"meta": {"versao": "4.0"}, "pendencias_tecnicas": []}), "utf-8"
    )
    (tmp_path / "README.md").write_text("# Projeto Hospitalar\n", "utf-8")


def test_server_registers_tools_and_resources(tmp_path):
    _seed(tmp_path)
    mcp = create_server(str(tmp_path))

    tools = {t.name for t in asyncio.run(mcp.list_tools())}
    assert {
        "restaurar_contexto",
        "get_project_summary",
        "list_documents",
        "read_document",
        "search_context",
        "get_pending_tasks",
    } <= tools

    resources = {str(r.uri) for r in asyncio.run(mcp.list_resources())}
    assert "analise://contexto" in resources


def test_restaurar_contexto_returns_json(tmp_path):
    _seed(tmp_path)
    mcp = create_server(str(tmp_path))
    result = asyncio.run(mcp.call_tool("restaurar_contexto", {}))
    assert result is not None
