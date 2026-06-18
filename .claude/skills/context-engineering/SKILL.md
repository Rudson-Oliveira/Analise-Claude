---
name: context-engineering
description: Protocolo de engenharia de contexto do projeto Hospitalar Soluções em Saúde (memória N8N). Use SEMPRE ao iniciar/retomar uma sessão neste repositório, quando o usuário disser "leia o documento no GitHub Analise-Claude e continue", ao restaurar contexto, ou antes de gravar progresso. Reduz consumo de tokens carregando só a fonte da verdade (CONTEXTO.json) e evita reler README/checkpoints redundantes.
---

# Context Engineering — Analise-Claude

Skill de **economia de tokens** e **restauração rápida de contexto** para o repositório de memória do projeto da Hospitalar Soluções em Saúde (automação N8N Cloud + OpenRouter + Evolution API).

## Princípio central

**`CONTEXTO.json` é a ÚNICA fonte da verdade.** Tudo que importa para retomar o trabalho está lá, em formato compacto e máquina-legível. O `README.md` e os `CHECKPOINT_*.md` são derivados/históricos — **não os leia por padrão**.

## Protocolo de restauração (gatilho: "leia o documento... e continue")

Faça nesta ordem e PARE assim que tiver o suficiente:

1. **Leia apenas `CONTEXTO.json`.** Ele contém: meta/próximo_passo, variáveis N8N, status dos workflows, pendências e erros corrigidos.
2. Dê um resumo de **3–5 linhas**: onde paramos (`meta.proximo_passo`), pendências de prioridade ALTA e a `proxima_sessao.primeira_acao`.
3. **Não** abra `README.md`, `ANALISE_COMPLETA.md` nem `CHECKPOINT_*.md` — a menos que a tarefa atual precise de detalhe histórico específico que não está no JSON. Nesse caso, leia só o arquivo necessário, com `offset/limit`.

> Resultado: restauração em **1 leitura** em vez de 5+ arquivos. Economia típica de 70–85% dos tokens de abertura de sessão.

## Regras de economia de tokens (durante a sessão)

- **Leitura cirúrgica:** use `Grep`/`Glob` para localizar e leia trechos com `offset`/`limit`. Evite `Read` de arquivos inteiros grandes.
- **Não reimprima** blocos extensos (JSON inteiro, workflow N8N completo) na resposta. Cite o campo/linha e resuma.
- **Não re-derive** fatos já estabelecidos no `CONTEXTO.json`. Confie nele.
- **Delegue buscas amplas** a um subagente (Explore/general-purpose) quando precisar varrer muitos arquivos — você recebe só a conclusão, não os dumps.
- Para chamadas de IA dentro do N8N, prefira modelos econômicos já em uso (`gemini-2.5-flash`, `claude-haiku-4-5`) salvo quando a tarefa exigir mais capacidade.

## Rotina de atualização da memória (fim de sessão / ao gravar progresso)

1. Atualize **`CONTEXTO.json`** primeiro: incremente `meta.versao`, ajuste `meta.proximo_passo`, mova itens entre `pendencias_tecnicas`/`erros_corrigidos_historico`, e acrescente `conquistas_sessao_N`.
2. Mantenha o JSON **enxuto**: status curtos, sem prosa longa. É a fonte da verdade — não um diário.
3. Só atualize `README.md` se o usuário quiser uma versão humana; ele é espelho, não original.
4. **Evite duplicação**: um fato vive em um lugar. Se está no JSON, não repita no README com texto diferente.

## Anti-padrões (não faça)

- ❌ Ler README + 4 checkpoints "para garantir" no início.
- ❌ Colar o `CONTEXTO.json` inteiro na conversa.
- ❌ Criar mais um `CHECKPOINT_*.md` por sessão (infla o repo). Consolide no `CONTEXTO.json`.
- ❌ Repetir no README o que já está no JSON.

## Referência rápida do estado (ver CONTEXTO.json para o valor atual)

- **Próximo passo:** configurar `OPENAI_API_KEY` (Whisper) e `EVOLUTION_API_KEY` (menu WhatsApp).
- **Workflows-chave:** COCKPIT-07 (corrigido/ativo), COCKPIT-08 (cron 07h), WF-ORQUESTRADOR-DINAMICO.
- **Pendências ALTA:** as duas API keys acima.
