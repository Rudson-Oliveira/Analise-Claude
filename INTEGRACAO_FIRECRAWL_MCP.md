# Integração — Firecrawl MCP + LOOP (Claude Code)

> **Status:** 🛠️ Instalado no `.mcp.json` / aguardando `FIRECRAWL_API_KEY` | **Data:** 20/06/2026
> **Decisão:** conectar via **servidor MCP oficial do Firecrawl** (uso pelo agente Claude) + rotina **LOOP**
> do Claude Code para monitoramento recorrente.

## 🎯 O que é

[Firecrawl](https://www.firecrawl.dev) é um serviço que transforma **sites/páginas web em dados prontos para LLM**
(Markdown limpo, HTML estruturado ou JSON). É o complemento web do MarkItDown:

| Ferramenta | Entrada | Função |
|---|---|---|
| **MarkItDown** | Arquivos (PDF/Word/Excel/imagem) | Arquivo → Markdown |
| **Firecrawl** | URLs / sites | Web → Markdown/JSON |

O **[firecrawl-mcp](https://github.com/firecrawl/firecrawl-mcp-server)** é o servidor MCP oficial que expõe essa
capacidade para clientes compatíveis (Claude Code / Claude Desktop).

### Principais ferramentas expostas pelo MCP

- `firecrawl_scrape(url)` — extrai uma única página em Markdown/HTML.
- `firecrawl_map(url)` — descobre todas as URLs de um site (sitemap rápido).
- `firecrawl_crawl(url)` — rastreia um site inteiro (múltiplas páginas).
- `firecrawl_search(query)` — busca na web + extrai conteúdo das melhores fontes.
- `firecrawl_extract(urls, schema)` — extração **estruturada** (JSON) guiada por schema/prompt.

## 🧩 Onde encaixa no nosso ecossistema

```
URL/site (ANVISA, licitações, concorrente, e-mail c/ link)
   → Firecrawl (scrape/extract) → Markdown/JSON limpo
   → OpenRouter (Claude) → triagem/resumo/alerta
```

Pontos naturais de uso na Hospitalar:

1. **COCKPIT-07 (Inbox):** quando chega um **link** (e não um anexo), o Firecrawl extrai o conteúdo antes da IA.
2. **Monitoramento regulatório:** acompanhar páginas da **ANVISA** / portais de **licitação** e avisar mudanças.
3. **Inteligência de concorrência:** capturar páginas de concorrentes e resumir novidades.
4. **Pesquisa rápida:** `firecrawl_search` para responder perguntas com fontes atualizadas.

> ⚠️ **Nota de arquitetura:** o `firecrawl-mcp` serve ao **agente Claude** (Claude Code/Desktop). Para um pipeline
> 100% automático **dentro do n8n Cloud**, use o **HTTP Request node** chamando direto a API REST do Firecrawl
> (`https://api.firecrawl.dev/v1/scrape`) — ver bloco abaixo. Os dois caminhos compartilham a mesma `FIRECRAWL_API_KEY`.

## ⚙️ Como configurar (Claude Code / Desktop)

### 1) Obter a API key

Crie a conta em https://www.firecrawl.dev → **Dashboard → API Keys** → copie a chave (`fc-...`).

### 2) Exportar a variável de ambiente (NUNCA commitar a chave)

```bash
export FIRECRAWL_API_KEY="fc-sua-chave-aqui"
```

### 3) Bloco MCP (já está no `.mcp.json` do repo)

> ✅ **Pronto no repo:** o **`.mcp.json`** na raiz já contém o servidor `firecrawl` abaixo. Basta exportar a
> `FIRECRAWL_API_KEY` no ambiente e abrir o Claude Code neste diretório (`npx` baixa o pacote na 1ª execução).

```json
{
  "mcpServers": {
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}"
      }
    }
  }
}
```

## 🔁 LOOP — monitoramento recorrente (Claude Code)

**LOOP** é a skill `/loop` do **Claude Code** (Anthropic) que executa um prompt/comando em **intervalos
recorrentes**. Combinada com o Firecrawl, vira um vigia automático de páginas.

### Como usar

```
/loop 6h Use o Firecrawl para coletar a página de notícias da ANVISA,
compare com a última coleta e, se houver novidade relevante para
home care / oxigenoterapia, gere um resumo curto em PT-BR.
```

- Sintaxe: `/loop <intervalo> <prompt ou /comando>` (ex.: `5m`, `1h`, `6h`, `24h`; padrão ~10m).
- Use para: vigiar ANVISA/licitações, checar concorrentes, ou **monitorar execuções n8n** periodicamente.
- Não é um pacote a instalar — é nativo do Claude Code; esta seção documenta o **padrão de uso** no projeto.

> 💡 Para automação contínua **sem o Claude aberto**, replicar a mesma ideia no n8n com um **Schedule Trigger**
> + HTTP Request (Firecrawl) — ver bloco n8n abaixo.

## 🔌 Alternativa n8n Cloud (HTTP Request node)

Para rodar dentro do n8n (sem depender do agente local):

- **Método:** `POST` → `https://api.firecrawl.dev/v1/scrape`
- **Auth:** Header `Authorization: Bearer {{ $env.FIRECRAWL_API_KEY }}` (cadastrar `FIRECRAWL_API_KEY` como
  variável n8n).
- **Body:** lembrar da lição do projeto — com expressões n8n `{{ }}`, usar **`specifyBody: "string"`** (nunca
  `"json"`, que quebra a validação).

Exemplo de body (string):

```json
{ "url": "https://www.gov.br/anvisa/pt-br/assuntos/noticias-anvisa", "formats": ["markdown"] }
```

## ✅ Workflow n8n criado — WF-MONITOR-ANVISA

Já existe no n8n Cloud (criado em 20/06/2026, **INATIVO** até cadastrar as variáveis):

- **Nome:** `WF-MONITOR-ANVISA-Firecrawl-WhatsApp` · **ID:** `lOWNpoAL4LM5j4AW`
- **Fluxo:** `Schedule 6h → Firecrawl Scrape (ANVISA) → Monta Prompt → OpenRouter (anthropic/claude-haiku-4-5) → IF "tem novidade?" → WhatsApp (Evolution)`
- **Lógica de novidade:** a IA responde `SEM_NOVIDADES` quando nada relevante/recente; o node IF só dispara o WhatsApp quando há novidade.
- **Destino do alerta:** WhatsApp `5535998352323` (Rudson), via Evolution `…railway.app/message/sendText/{instância}`.

### ⚙️ Para ativar (passos manuais no n8n — Settings → Variables)

Cadastrar como **Variables** do n8n (mesmo lugar do `OPENROUTER_API_KEY`):

| Variável | Valor |
|---|---|
| `FIRECRAWL_API_KEY` | a chave `fc-...` do Firecrawl |
| `EVOLUTION_API_KEY` | a apikey da sua Evolution API |
| `EVOLUTION_INSTANCE` | o nome da sua instância Evolution |
| `OPENROUTER_API_KEY` | (já existe) |

Depois: abrir o workflow → testar uma execução → **ativar**.

> ℹ️ O workflow referencia `{{ $vars.NOME }}`. Se no seu n8n as chaves globais forem lidas como `{{ $env.NOME }}`, é só avisar que eu troco.

## 🔒 Segurança

- A `FIRECRAWL_API_KEY` (`fc-...`) **nunca** entra no Git — só via variável de ambiente (`${FIRECRAWL_API_KEY}`)
  ou variável n8n.
- Respeitar `robots.txt`/Termos de Uso dos sites monitorados e a cota do plano Firecrawl.

## 📋 Próximos passos

1. Criar a conta Firecrawl e gerar a `FIRECRAWL_API_KEY`.
2. Exportar a variável e validar o MCP no Claude Code (testar `firecrawl_scrape` em uma URL real).
3. Definir as páginas-alvo de monitoramento (ANVISA, licitações, concorrentes) e montar o primeiro `/loop`.
4. Se justificar automação 24/7, cadastrar `FIRECRAWL_API_KEY` no n8n e montar o workflow Schedule + HTTP Request.
