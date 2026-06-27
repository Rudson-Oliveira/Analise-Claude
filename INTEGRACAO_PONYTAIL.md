# Integração — Ponytail (modo "dev sênior preguiçoso")

> Plugin/skill open-source que força o agente de IA a entregar a solução **mais
> simples que funciona**: YAGNI, biblioteca padrão antes de código custom,
> recurso nativo antes de dependência, uma linha antes de cinquenta.

## 📌 O que é

- **Repo:** [github.com/DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)
- **Versão baixada:** v4.8.3 — **Licença:** MIT (livre/gratuita)
- **Site:** https://ponytail.dev
- **Lema:** *"He says nothing. He writes one line. It works."*
- **Compatível com 13 agentes** (Claude Code, Cursor, Copilot, Gemini CLI, Codex, Cline, Aider, OpenCode, Windsurf…).

## ✅ Como foi instalado neste projeto

Em vez de usar o marketplace (`/plugin install`), as **skills foram "vendoradas"**
direto em `.claude/skills/` — assim funcionam tanto no Claude Code Web quanto no
CLI, sem depender de Node/hooks externos.

```
.claude/skills/
├── ponytail/SKILL.md          # modo principal (lite | full | ultra)
├── ponytail-review/SKILL.md   # review focado em over-engineering (o que deletar)
├── ponytail-audit/SKILL.md    # auditoria do repo inteiro p/ bloat
├── ponytail-debt/SKILL.md     # coleta os comentários `ponytail:` num "ledger" de dívida
├── ponytail-gain/SKILL.md     # scoreboard de impacto (medianas do benchmark)
├── ponytail-help/SKILL.md     # cartão de referência dos comandos
├── PONYTAIL-LICENSE           # licença MIT original
└── PONYTAIL-SOURCE.txt        # origem/versão e o que NÃO foi copiado
```

> **Não foram copiados:** servidor MCP (`ponytail-mcp/`), hooks de auto-ativação
> (`hooks/`), benchmarks e configs dos outros 12 agentes — desnecessários aqui.
> Se quiser a **auto-ativação em toda sessão** (via hooks + Node), aí sim vale
> instalar pelo marketplace; veja abaixo.

## 🚀 Como usar

Invoque pelo nome da skill (ex.: `/ponytail`, `/ponytail-review`, `/ponytail-help`).
O modo principal tem 3 intensidades:

| Nível | Comportamento |
|---|---|
| `lite` | Constrói o que foi pedido, mas aponta a alternativa mais enxuta em 1 linha. |
| `full` *(padrão)* | "A escada" aplicada: stdlib/nativo primeiro, menor diff possível. |
| `ultra` | YAGNI extremista: entrega o one-liner e questiona o resto do requisito. |

Desligar: `stop ponytail` / `normal mode`.

## 🔄 Alternativa: instalar pelo marketplace (com auto-ativação)

Dois prompts **separados** no Claude Code (o README avisa que precisa ser assim):

```
/plugin marketplace add DietrichGebert/ponytail
```
```
/plugin install ponytail@ponytail
```

## ⚖️ Avaliação para o nosso contexto

Este repo é **memória/contexto** (sem código de aplicação pesado), então o ganho
direto do Ponytail aqui é **modesto** — ele brilha em repositórios com muito
código (ex.: os MCPs `context-mcp/` e `metricool-mcp/`, ou workflows gerados).
Como é MIT e leve, fica instalado como ferramenta opcional, sem custo.

> ⚠️ Os números de marketing do print ("80‑94% menos código · 47‑77% mais barato")
> são otimistas. As **medianas reais** do projeto são ~54% menos código e ~20%
> mais barato. Bom manter expectativa calibrada.
