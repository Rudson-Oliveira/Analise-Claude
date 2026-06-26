"""Configuração do MCP de contexto do projeto Análise-Claude."""

from __future__ import annotations

import os
from pathlib import Path

# Arquivos âncora que identificam a raiz do repositório de memória.
_ANCHORS = ("CONTEXTO.json", "README.md")


def find_root(explicit: str | None = None) -> Path:
    """Resolve a raiz do repositório de memória.

    Ordem: argumento explícito > env ANALISE_CLAUDE_ROOT > sobe a partir do
    pacote/cwd procurando os arquivos âncora > cwd.
    """
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit))
    env = os.getenv("ANALISE_CLAUDE_ROOT")
    if env:
        candidates.append(Path(env))

    for start in (Path(__file__).resolve(), Path.cwd().resolve()):
        for parent in [start, *start.parents]:
            if all((parent / a).exists() for a in _ANCHORS):
                candidates.append(parent)
                break

    for cand in candidates:
        cand = cand.expanduser().resolve()
        if cand.is_dir():
            return cand
    return Path.cwd().resolve()


def transport() -> str:
    t = os.getenv("ANALISE_MCP_TRANSPORT", "stdio").lower()
    return t if t in {"stdio", "sse", "streamable-http"} else "stdio"
