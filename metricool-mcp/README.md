# metricool-mcp-swiss 🔧

**Canivete suíço MCP para o [Metricool](https://metricool.com).** Um servidor
[Model Context Protocol](https://modelcontextprotocol.io) que dá a agentes de IA
(Claude, etc.) acesso completo à API do Metricool: analytics de todas as redes,
campanhas de anúncios, concorrentes, agendamento/edição/exclusão de posts,
melhores horários e muito mais.

É um **superset compatível** do MCP oficial (`metricool/mcp-metricool`) — mantém
os mesmos nomes de ferramentas e adiciona melhorias de robustez e cobertura.

---

## ✨ Melhorias sobre o MCP oficial

| Área | Oficial | Este projeto |
|---|---|---|
| Erros | retorna `None` silencioso | **dict estruturado** com status HTTP e corpo |
| Rede | 1 tentativa | **retry com backoff exponencial** (429/5xx/falhas) + `Retry-After` |
| Conexões | novo `AsyncClient` por chamada | **pool único** reutilizado |
| Posts agendados | só criar/editar | **listar e excluir** também |
| Mídia | — | **`normalize_media_url`** (exigido antes de anexar mídia) |
| Marca | só listar | **`find_brand`** resolve nome → `blogId` |
| Cobertura | endpoints fixos | **`metricool_request`** chama qualquer endpoint |
| Diagnóstico | — | **`metricool_status`** valida credenciais e conectividade |
| Arquitetura | 1 arquivo de 940 linhas | **pacote modular** + testes |
| Transporte | stdio | **stdio / sse / streamable-http** |
| Extras | — | **resources** (`metricool://brands`) e **prompts** |

---

## 🧰 Ferramentas

**Marcas & diagnóstico:** `get_brands`, `find_brand`, `metricool_status`

**Analytics (orgânico):** `get_analytics` (unificada) + nomeadas:
`get_instagram_posts`, `get_instagram_reels`, `get_instagram_stories`,
`get_facebook_posts`, `get_facebook_reels`, `get_facebook_stories`,
`get_tiktok_videos`, `get_threads_posts`, `get_bluesky_posts`,
`get_linkedin_posts`, `get_pinterest_pins`, `get_youtube_videos`,
`get_x_posts`, `get_twitch_videos`

**Anúncios:** `get_ads_campaigns` (unificada), `get_facebookads_campaigns`,
`get_googleads_campaigns`, `get_tiktokads_campaigns`

**Concorrentes:** `get_competitors`

**Agendamento:** `schedule_post`, `update_scheduled_post`,
`get_scheduled_posts`, `delete_scheduled_post`, `get_best_time_to_post`

**Mídia:** `normalize_media_url`

**Genérica:** `metricool_request` (qualquer endpoint da API)

---

## 🚀 Instalação

```bash
cd metricool-mcp
pip install -e .          # ou: pip install -e ".[dev]" para rodar os testes
```

Requer Python ≥ 3.11.

## 🔑 Credenciais

Plano **Advanced** ou **Custom** do Metricool. Pegue o token em
*Configurações → API* e o `userId` na URL/conta.

```bash
export METRICOOL_USER_TOKEN="seu_token"
export METRICOOL_USER_ID="seu_user_id"
```

(Veja `.env.example` para todas as opções.)

## ▶️ Execução

```bash
metricool-mcp              # transporte stdio (padrão)
# ou
python -m metricool_mcp
```

### Configurar no Claude Desktop / Claude Code

```json
{
  "mcpServers": {
    "metricool": {
      "command": "metricool-mcp",
      "env": {
        "METRICOOL_USER_TOKEN": "seu_token",
        "METRICOOL_USER_ID": "seu_user_id"
      }
    }
  }
}
```

### Docker

```bash
docker build -t metricool-mcp-swiss .
docker run -i --rm \
  -e METRICOOL_USER_TOKEN=seu_token \
  -e METRICOOL_USER_ID=seu_user_id \
  metricool-mcp-swiss
```

### HTTP / SSE

```bash
METRICOOL_MCP_TRANSPORT=streamable-http metricool-mcp
```

---

## 🧪 Testes

```bash
pip install -e ".[dev]"
pytest -q
```

Os testes usam `httpx.MockTransport` — não fazem chamadas reais à API.

---

## 🗺️ Fluxo típico

1. `get_brands` (ou `find_brand "Hospitalar"`) → `blogId` + `timezone`.
2. Analytics, concorrentes ou melhores horários usando o `blogId`.
3. Para publicar: `normalize_media_url` em cada mídia → `schedule_post`.
4. Precisa de algo não coberto? `metricool_request("GET", "/v2/...", {...})`.

## 📋 Notas da API do Metricool

- Datas de entrada sempre `AAAA-MM-DD`; o servidor converte para o formato de
  cada endpoint (ISO com hora ou compacto `AAAAMMDD`).
- `userId` e `integrationSource=MCP` são injetados automaticamente.
- Concorrentes só em: Instagram, Facebook, Twitch, YouTube, Twitter (X), Bluesky.
- Datas de agendamento não podem estar no passado.

## ⚖️ Licença

MIT. Projeto independente, sem afiliação oficial com o Metricool.
