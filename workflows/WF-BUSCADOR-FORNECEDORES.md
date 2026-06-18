# WF-BUSCADOR-FORNECEDORES-B2B

> Workflow n8n para buscar fornecedores de qualquer nicho no Brasil, com nome, telefone e site,
> normalizado por IA (OpenRouter) e com carimbo de conformidade LGPD em cada registro.
> Entregue como **JSON importável** — não foi publicado em produção.

## 📦 Origem
Implementação "limpa" da ideia vista nas imagens (agente "Buscador de Lista de Fornecedores").
Diferença em relação ao vídeo original: **não faz scraping agressivo de e-mail/telefone em massa**.
Usa fonte pública de estabelecimento (Google Places) e marca base legal + opt-out por registro.

## 🔧 Como importar
1. n8n Cloud → **Workflows** → **Import from File** → selecione `WF-BUSCADOR-FORNECEDORES.json`.
2. Reatribua as credenciais (Google Sheets OAuth2) no nó **Salvar Google Sheets**.
3. No nó **Salvar Google Sheets**, troque `COLE_O_ID_DA_PLANILHA_AQUI` pelo ID da sua planilha
   e garanta uma aba chamada `Fornecedores`.

## 🔑 Variáveis n8n necessárias
| Variável | Status no ecossistema | Uso |
|---|---|---|
| `OPENROUTER_API_KEY` | ✅ já configurada (sessão 31/05/2026) | Normalização/relevância via IA |
| `GOOGLE_MAPS_API_KEY` | 🔴 **NOVA — pendente** | Places Text Search + Place Details |

> A `GOOGLE_MAPS_API_KEY` precisa das APIs **Places API** habilitadas no Google Cloud.

## 🧭 Fluxo dos nós
1. **Entrada Formulario** — recebe `nicho` (obrigatório), `uf`, `limite`.
2. **Parametros** — monta a query de busca e o limite.
3. **Google Places Search** — busca estabelecimentos (dados públicos).
4. **Extrair Candidatos** — extrai nome, endereço, `place_id` (respeita o limite).
5. **Place Details** — telefone e site oficiais do estabelecimento.
6. **IA Relevancia OpenRouter** — pontua relevância 0..1 para o nicho (modelo `gemini-2.5-flash-preview`).
7. **Parse IA + Carimbo LGPD** — monta o registro final + metadados de conformidade.
8. **Filtro Relevante** — mantém apenas `relevancia >= 0.6`.
9. **Salvar Google Sheets** — append na planilha.
10. **Fim**.

> ⚠️ Lição reaproveitada da sessão 4 (COCKPIT-07): o corpo do nó OpenRouter usa
> `jsonBody = {{ JSON.stringify({...}) }}` (expressão única) para evitar o erro
> *JSON syntax error position 593* que ocorre quando se mistura `{{ }}` dentro de JSON cru.

## ⚖️ LGPD — decisões de design
- Coleta apenas **dados de pessoa jurídica publicamente disponíveis** (estabelecimento).
- O campo `email` fica **vazio por padrão** — Google Places não fornece e-mail, e não há raspagem
  automática de sites para extrair e-mails (respeita ToS e minimiza risco).
- Cada registro carrega `fonte`, `base_legal_lgpd`, `data_coleta` e `opt_out`.
- **Não usar para disparo em massa** sem base legal e mecanismo de descadastro ativo.

## 📊 Recomendação (0–5)
- Buscador de Fornecedores (esta versão limpa): **3/5** — útil para prospecção B2B cuidadosa.
- Versão "scraping agressivo" do vídeo original: **2/5** — risco LGPD/ToS.
