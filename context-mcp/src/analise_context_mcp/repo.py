"""Leitura segura da memória do projeto (markdown + JSON) no repositório."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Extensões consideradas "documentos de memória".
_DOC_SUFFIXES = {".md", ".json"}
_MAX_BYTES = 1_000_000  # 1 MB de guarda por arquivo


@dataclass
class Repo:
    """Acesso somente-leitura aos documentos de memória sob ``root``."""

    root: Path

    # ------------------------------------------------------------------ docs
    def list_documents(self) -> list[dict[str, Any]]:
        docs = []
        for path in sorted(self.root.iterdir()):
            if path.is_file() and path.suffix.lower() in _DOC_SUFFIXES:
                docs.append(
                    {
                        "name": path.name,
                        "size_bytes": path.stat().st_size,
                        "type": path.suffix.lstrip("."),
                    }
                )
        return docs

    def _safe_path(self, name: str) -> Path | None:
        """Resolve ``name`` garantindo que fica dentro de ``root`` (anti-traversal)."""
        candidate = (self.root / name).resolve()
        try:
            candidate.relative_to(self.root)
        except ValueError:
            return None
        if candidate.is_file() and candidate.suffix.lower() in _DOC_SUFFIXES:
            return candidate
        return None

    def read_document(self, name: str) -> dict[str, Any]:
        path = self._safe_path(name)
        if path is None:
            return {"error": f"Documento não encontrado ou não permitido: {name!r}"}
        if path.stat().st_size > _MAX_BYTES:
            return {"error": f"Documento muito grande: {name} (> 1MB)"}
        text = path.read_text(encoding="utf-8", errors="replace")
        return {"name": name, "content": text}

    # ---------------------------------------------------------------- search
    def search(self, query: str, *, context_lines: int = 2, max_hits: int = 50) -> dict[str, Any]:
        q = query.casefold().strip()
        if not q:
            return {"query": query, "hits": [], "count": 0}
        hits: list[dict[str, Any]] = []
        for doc in self.list_documents():
            path = self.root / doc["name"]
            try:
                lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            for i, line in enumerate(lines):
                if q in line.casefold():
                    lo = max(0, i - context_lines)
                    hi = min(len(lines), i + context_lines + 1)
                    hits.append(
                        {
                            "document": doc["name"],
                            "line": i + 1,
                            "snippet": "\n".join(lines[lo:hi]).strip(),
                        }
                    )
                    if len(hits) >= max_hits:
                        return {"query": query, "hits": hits, "count": len(hits), "truncated": True}
        return {"query": query, "hits": hits, "count": len(hits)}

    # --------------------------------------------------------------- context
    def context_json(self) -> dict[str, Any]:
        path = self.root / "CONTEXTO.json"
        if not path.exists():
            return {"error": "CONTEXTO.json não encontrado", "root": str(self.root)}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return {"error": f"Falha ao ler CONTEXTO.json: {exc}"}

    def summary(self) -> dict[str, Any]:
        """Resumo estruturado e enxuto do estado atual do projeto."""
        ctx = self.context_json()
        if "error" in ctx:
            return {"root": str(self.root), **ctx, "documents": self.list_documents()}
        meta = ctx.get("meta", {})
        return {
            "root": str(self.root),
            "versao": meta.get("versao"),
            "data_analise": meta.get("data_analise"),
            "proximo_passo": meta.get("proximo_passo"),
            "empresa": ctx.get("empresa"),
            "plataformas": ctx.get("plataformas"),
            "pendencias_tecnicas": ctx.get("pendencias_tecnicas"),
            "estado_atual": ctx.get("estado_atual"),
            "documents": [d["name"] for d in self.list_documents()],
        }
