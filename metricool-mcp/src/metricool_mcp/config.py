"""Configuração do servidor MCP do Metricool.

Todas as opções podem ser definidas por variáveis de ambiente. Apenas
``METRICOOL_USER_TOKEN`` e ``METRICOOL_USER_ID`` são obrigatórias para chamadas
autenticadas — os demais possuem defaults sensatos.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_BASE_URL = "https://app.metricool.com/api"


@dataclass(frozen=True)
class Settings:
    """Configuração imutável carregada do ambiente."""

    user_token: str | None
    user_id: str | None
    base_url: str = DEFAULT_BASE_URL
    timeout: float = 30.0
    max_retries: int = 3
    backoff_base: float = 0.5
    integration_source: str = "MCP"
    transport: str = "stdio"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            user_token=os.getenv("METRICOOL_USER_TOKEN"),
            user_id=os.getenv("METRICOOL_USER_ID"),
            base_url=os.getenv("METRICOOL_BASE_URL", DEFAULT_BASE_URL).rstrip("/"),
            timeout=_float_env("METRICOOL_TIMEOUT", 30.0),
            max_retries=_int_env("METRICOOL_MAX_RETRIES", 3),
            backoff_base=_float_env("METRICOOL_BACKOFF_BASE", 0.5),
            integration_source=os.getenv("METRICOOL_INTEGRATION_SOURCE", "MCP"),
            transport=os.getenv("METRICOOL_MCP_TRANSPORT", "stdio"),
        )

    @property
    def is_authenticated(self) -> bool:
        return bool(self.user_token and self.user_id)

    def missing_credentials(self) -> list[str]:
        missing: list[str] = []
        if not self.user_token:
            missing.append("METRICOOL_USER_TOKEN")
        if not self.user_id:
            missing.append("METRICOOL_USER_ID")
        return missing


def _int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _float_env(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return float(raw)
    except ValueError:
        return default
