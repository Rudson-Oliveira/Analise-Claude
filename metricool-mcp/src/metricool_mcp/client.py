"""Cliente HTTP assíncrono e resiliente para a API do Metricool.

Melhorias sobre o cliente do MCP oficial:

* **Erros estruturados** em vez de ``None`` silencioso — o agente recebe
  status HTTP e corpo da resposta, podendo reagir.
* **Retry com backoff exponencial** em erros transitórios (429 / 5xx / falhas
  de rede), respeitando o header ``Retry-After`` quando presente.
* **Injeção automática** de ``userId`` e ``integrationSource`` em toda chamada.
* **Connection pooling** via uma única instância de ``httpx.AsyncClient``.
"""

from __future__ import annotations

import asyncio
from typing import Any

import httpx

from .config import Settings

_RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class MetricoolError(Exception):
    """Erro de uma chamada à API do Metricool."""

    def __init__(self, message: str, *, status: int | None = None, detail: Any = None):
        super().__init__(message)
        self.message = message
        self.status = status
        self.detail = detail

    def as_dict(self) -> dict[str, Any]:
        return {"error": self.message, "status": self.status, "detail": self.detail}


class MetricoolClient:
    """Wrapper fino sobre ``httpx.AsyncClient`` com a semântica do Metricool."""

    def __init__(self, settings: Settings, *, http_client: httpx.AsyncClient | None = None):
        self.settings = settings
        self._client = http_client or httpx.AsyncClient(
            base_url=settings.base_url,
            timeout=settings.timeout,
            headers={"User-Agent": "metricool-mcp-swiss/1.0"},
        )

    # ----------------------------------------------------------------- helpers
    def _headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        headers = {
            "X-Mc-Auth": self.settings.user_token or "",
            "Accept": "application/json",
        }
        if extra:
            headers.update(extra)
        return headers

    def _merge_params(self, params: dict[str, Any] | None) -> dict[str, Any]:
        merged: dict[str, Any] = {
            "userId": self.settings.user_id,
            "integrationSource": self.settings.integration_source,
        }
        if params:
            # Remove chaves None para não enviar "?x=None".
            merged.update({k: v for k, v in params.items() if v is not None})
        return merged

    # ------------------------------------------------------------------- core
    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: Any = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """Executa uma requisição com retries. Levanta ``MetricoolError`` em falha."""
        if not self.settings.is_authenticated:
            raise MetricoolError(
                "Credenciais ausentes. Defina METRICOOL_USER_TOKEN e METRICOOL_USER_ID.",
                status=None,
                detail={"missing": self.settings.missing_credentials()},
            )

        url = path if path.startswith("http") else f"/{path.lstrip('/')}"
        merged_params = self._merge_params(params)
        merged_headers = self._headers(headers)
        last_exc: Exception | None = None

        for attempt in range(self.settings.max_retries + 1):
            try:
                response = await self._client.request(
                    method.upper(),
                    url,
                    params=merged_params,
                    json=json_body,
                    headers=merged_headers,
                )
            except httpx.TransportError as exc:  # rede instável, timeout, DNS...
                last_exc = exc
                if attempt < self.settings.max_retries:
                    await self._sleep_backoff(attempt)
                    continue
                raise MetricoolError(f"Falha de rede ao chamar {url}: {exc}") from exc

            if response.status_code in _RETRYABLE_STATUS and attempt < self.settings.max_retries:
                await self._sleep_backoff(attempt, response)
                continue

            if response.is_success:
                return _parse_body(response)

            raise MetricoolError(
                f"{method.upper()} {url} retornou HTTP {response.status_code}",
                status=response.status_code,
                detail=_parse_body(response),
            )

        # Só chega aqui se todos os retries de rede falharem.
        raise MetricoolError(f"Esgotaram as tentativas para {url}: {last_exc}")

    async def _sleep_backoff(self, attempt: int, response: httpx.Response | None = None) -> None:
        delay = self.settings.backoff_base * (2**attempt)
        if response is not None:
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                try:
                    delay = max(delay, float(retry_after))
                except ValueError:
                    pass
        await asyncio.sleep(delay)

    # ---------------------------------------------------------------- verbos
    async def get(self, path: str, **kwargs: Any) -> Any:
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs: Any) -> Any:
        return await self.request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs: Any) -> Any:
        return await self.request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> Any:
        return await self.request("DELETE", path, **kwargs)

    async def aclose(self) -> None:
        await self._client.aclose()


def _parse_body(response: httpx.Response) -> Any:
    """Tenta JSON; cai para texto bruto; ``None`` se vazio."""
    if not response.content:
        return None
    try:
        return response.json()
    except ValueError:
        return response.text


async def safe_call(coro: Any) -> Any:
    """Executa uma coroutine de cliente, convertendo erros em dict estruturado.

    Permite que as ferramentas MCP retornem feedback acionável ao agente em vez
    de estourar uma exceção crua.
    """
    try:
        return await coro
    except MetricoolError as exc:
        return exc.as_dict()
