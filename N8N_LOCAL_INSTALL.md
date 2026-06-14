# N8N Local — Guia de Instalação (Modelo Híbrido)

> **Objetivo:** Rodar um N8N self-hosted (grátis) para desenvolvimento, testes e
> workflows pesados, **mantendo o N8N Cloud no plano básico** para produção.
> Integrado ao `WF-ORQUESTRADOR-DINAMICO` (via `AGENTE_LOCAL`) e ao **n8n-mcp**
> para construção de workflows por conversa com o Claude.
>
> **Empresa:** Hospitalar Soluções em Saúde | **Cloud atual:** https://rudsonoliveira2323.app.n8n.cloud

---

## 1. Por que híbrido?

| Camada | Onde roda | Para quê |
|---|---|---|
| **Produção** | N8N Cloud (plano básico) | Webhooks sempre-online: COCKPIT-07 (WhatsApp/Email/Notion), COCKPIT-08 (cron 07h), COCKPIT-05 (polling Notion→WhatsApp) |
| **Dev / Testes** | N8N Local (Docker) | Construir e testar workflows **sem gastar execuções** do plano Cloud |
| **Workflows pesados** | N8N Local | Whisper (transcrição de áudio), scraping (telegram-inema), processamento em lote |
| **Dados sensíveis** | N8N Local | Fluxos que você não quer trafegando na nuvem |

O roteamento entre Cloud e Local já está previsto na sua arquitetura: o
`WF-ORQUESTRADOR-DINAMICO` lê o `staticData` com o `AGENTE_LOCAL` registrado, e o
`WF-MCC-SET-URL` atualiza a URL do agente local (que muda a cada sessão do túnel).

**Economia estimada:** o plano Cloud Starter custa ~€20-24/mês (~R$130-150). No
híbrido você mantém só o básico; no 100% local a economia é total (só infra).

---

## 2. Pré-requisitos comuns

- **Docker** + **Docker Compose** instalados
- Uma **N8N_API_KEY** gerada em cada instância (Settings → API → Create API Key)
- (Para receber webhooks externos) um **túnel**: Cloudflare Tunnel (recomendado) ou ngrok

---

## 3. Opção A — Rodar no seu PC/Notebook

**Melhor para:** dev e testes. Custo de infra **R$ 0**.
**Contrapartida:** webhooks só funcionam com o PC ligado e o túnel ativo.

### 3.1. Docker Compose

Crie uma pasta `n8n-local/` e dentro dela o arquivo `docker-compose.yml`:

```yaml
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    container_name: n8n-local
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - NODE_ENV=production
      - GENERIC_TIMEZONE=America/Sao_Paulo
      - TZ=America/Sao_Paulo
      # Habilita a API pública (necessária para o n8n-mcp e para a API REST)
      - N8N_PUBLIC_API_DISABLED=false
      # Persistência de criptografia das credenciais (NÃO perca esta chave)
      - N8N_ENCRYPTION_KEY=troque-por-uma-chave-aleatoria-longa
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  n8n_data:
```

### 3.2. Subir

```bash
cd n8n-local
docker compose up -d
docker compose logs -f n8n   # acompanhar a inicialização
```

Acesse **http://localhost:5678**, crie o usuário owner e gere a **API Key** em
Settings → n8n API.

### 3.3. Túnel para webhooks (Cloudflare Tunnel — grátis e estável)

Para WhatsApp/Evolution API e outros webhooks chegarem ao seu PC:

```bash
# Instale o cloudflared, depois:
cloudflared tunnel --url http://localhost:5678
```

Isso devolve uma URL pública (ex.: `https://algo.trycloudflare.com`). Configure
o N8N para usá-la como base de webhook adicionando ao `environment`:

```yaml
      - WEBHOOK_URL=https://algo.trycloudflare.com/
      - N8N_EDITOR_BASE_URL=https://algo.trycloudflare.com/
```

> Para domínio fixo (não muda a cada reinício), crie um *named tunnel* no painel
> da Cloudflare apontando para um subdomínio seu. Alternativa rápida: `ngrok http 5678`.

#### Túnel: grátis vs pago (só relevante no cenário PC)

> **No cenário VPS não há túnel** — a máquina já tem IP/domínio público. Esta
> comparação só vale para rodar no PC.

| Opção | Custo | URL fixa? | Observação |
|---|---|---|---|
| **ngrok Free** | R$ 0 | ❌ muda a cada reinício | Exige rodar `WF-MCC-SET-URL` toda sessão para re-registrar a URL no orquestrador |
| **ngrok Pay** | ~US$ 8-10/mês | ✅ domínio reservado | Setup simples, mas custo recorrente (contraria o objetivo de economia) |
| **Cloudflare Tunnel** ⭐ | R$ 0 | ✅ named tunnel | Entrega URL estável de graça; precisa apenas de um domínio (~R$ 40/ano) ou subdomínio |

**Recomendação:** não assinar o ngrok pago. Para URL fixa sem custo mensal, usar
**Cloudflare Tunnel** (named tunnel). Migrar para VPS elimina a necessidade de túnel.

### 3.4. Registrar a URL no orquestrador

Cada vez que o túnel sobe com URL nova, rode o `WF-MCC-SET-URL` (via Google
Sheets, como já está montado) para atualizar o `AGENTE_LOCAL` no
`WF-ORQUESTRADOR-DINAMICO`. Com domínio fixo isso vira passo único.

---

## 4. Opção B — Rodar numa VPS (24/7)

**Melhor para:** quando quiser migrar workflows de produção e cortar/reduzir o
Cloud. Fica online sempre, com domínio próprio e HTTPS.

**Custo típico:** Hetzner CX22 ~€4/mês (~R$25) · Contabo ~R$30 · Oracle Cloud
Free Tier = R$ 0 (ARM, generoso). Mais um domínio (~R$40/ano) se quiser HTTPS bonito.

### 4.1. Docker Compose com HTTPS automático (Caddy)

`docker-compose.yml` na VPS (substitua `n8n.seudominio.com.br`):

```yaml
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    container_name: n8n
    restart: unless-stopped
    environment:
      - N8N_HOST=n8n.seudominio.com.br
      - N8N_PROTOCOL=https
      - N8N_PORT=5678
      - NODE_ENV=production
      - WEBHOOK_URL=https://n8n.seudominio.com.br/
      - N8N_EDITOR_BASE_URL=https://n8n.seudominio.com.br/
      - GENERIC_TIMEZONE=America/Sao_Paulo
      - TZ=America/Sao_Paulo
      - N8N_PUBLIC_API_DISABLED=false
      - N8N_ENCRYPTION_KEY=troque-por-uma-chave-aleatoria-longa
    volumes:
      - n8n_data:/home/node/.n8n
    expose:
      - "5678"

  caddy:
    image: caddy:latest
    container_name: caddy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config

volumes:
  n8n_data:
  caddy_data:
  caddy_config:
```

`Caddyfile` (HTTPS automático via Let's Encrypt):

```
n8n.seudominio.com.br {
    reverse_proxy n8n:5678
}
```

Aponte o DNS do subdomínio para o IP da VPS, abra as portas 80/443 e:

```bash
docker compose up -d
```

Pronto: `https://n8n.seudominio.com.br` com SSL automático e webhooks estáveis.
Não precisa de túnel.

### 4.2. Backup (importante no 100% local)

```bash
# Backup do volume de dados (workflows + credenciais criptografadas)
docker run --rm -v n8n_data:/data -v $(pwd):/backup alpine \
  tar czf /backup/n8n-backup-$(date +%F).tar.gz -C /data .
```

Guarde também a `N8N_ENCRYPTION_KEY` em local seguro — sem ela as credenciais
não são recuperáveis.

---

## 5. Comparativo rápido (PC vs VPS)

| Critério | PC/Notebook | VPS |
|---|---|---|
| Custo infra | R$ 0 | R$ 0–60/mês |
| Uptime | Só com PC ligado | 24/7 |
| Webhooks | Precisa de túnel | Domínio fixo + HTTPS |
| Ideal para | Dev/testes | Produção / cortar Cloud |
| Backup | Manual | Manual + snapshot do provedor |

**Recomendação para começar:** PC + Cloudflare Tunnel para validar o fluxo
híbrido sem gastar nada. Se funcionar bem, promova para VPS.

---

## 6. Integração com o n8n-mcp (czlonkowski/n8n-mcp)

O **n8n-mcp** dá ao Claude conhecimento completo dos nós do n8n (1.800+) **e**
conecta na API da sua instância para **criar, editar, validar e ativar
workflows** por conversa. Funciona igual para Cloud e Local — só muda a URL/key.

### 6.1. Via Docker (apontando para o N8N local)

```bash
docker run -i --rm \
  -e MCP_MODE=stdio \
  -e N8N_API_URL=http://host.docker.internal:5678 \
  -e N8N_API_KEY=SUA_API_KEY_DO_N8N_LOCAL \
  ghcr.io/czlonkowski/n8n-mcp:latest
```

### 6.2. Configuração no Claude Code / Claude Desktop

No `mcp` config (ex.: `claude_desktop_config.json` ou `.mcp.json`):

```json
{
  "mcpServers": {
    "n8n-local": {
      "command": "npx",
      "args": ["n8n-mcp"],
      "env": {
        "N8N_API_URL": "http://localhost:5678",
        "N8N_API_KEY": "SUA_API_KEY_DO_N8N_LOCAL"
      }
    },
    "n8n-cloud": {
      "command": "npx",
      "args": ["n8n-mcp"],
      "env": {
        "N8N_API_URL": "https://rudsonoliveira2323.app.n8n.cloud",
        "N8N_API_KEY": "SUA_API_KEY_DO_N8N_CLOUD"
      }
    }
  }
}
```

> Dois servidores MCP (um por instância) = posso construir/editar workflows tanto
> no Local quanto no Cloud na mesma conversa.

> **Não confundir:** o *n8n-mcp* (acima) é a ferramenta que o Claude usa para
> mexer no seu n8n. Já o nó nativo **"MCP Server Trigger"** dentro do n8n serve
> para o caminho inverso — expor um workflow seu como ferramenta para outros
> agentes de IA. São coisas diferentes.

---

## 7. Checklist de implantação

- [ ] Docker + Compose instalados
- [ ] `docker-compose.yml` criado (PC ou VPS)
- [ ] `N8N_ENCRYPTION_KEY` definida e guardada com segurança
- [ ] `docker compose up -d` e acesso ao editor
- [ ] API Key gerada (Settings → n8n API)
- [ ] Túnel (PC) ou domínio+HTTPS (VPS) configurado
- [ ] `WEBHOOK_URL` ajustada
- [ ] n8n-mcp conectado (local + cloud)
- [ ] `WF-MCC-SET-URL` rodado para registrar `AGENTE_LOCAL`
- [ ] Teste end-to-end via `WF-ORQUESTRADOR-DINAMICO`
- [ ] (VPS) rotina de backup do volume `n8n_data`

**Redundância / HA (seção 8):**
- [ ] Postgres no lugar do SQLite (`DB_TYPE=postgresdb`)
- [ ] 2 réplicas `cloudflared` para o mesmo named tunnel
- [ ] `restart: unless-stopped` + healthchecks em todos os serviços
- [ ] Public Hostnames por projeto no painel Cloudflare (multi-projeto)
- [ ] ngrok (perfil `dr`) com domínio reservado em standby
- [ ] Procedimento de failover testado (Cloudflare → ngrok + `WF-MCC-SET-URL`)
- [ ] Serviço de backup automático (dump diário + retenção 7 dias)
- [ ] `N8N_ENCRYPTION_KEY` e senha do Postgres guardadas fora do servidor

---

## 8. Arquitetura redundante multi-projeto (alta disponibilidade)

> **Princípio:** nenhum ponto único de falha. Dois caminhos de túnel
> **independentes** chegam ao mesmo n8n, a **URL canônica nunca muda**, e há
> failover automático onde dá e manual onde não dá. Serve para os vários
> projetos (n8n, Evolution, integrações de IA) atrás do mesmo domínio.

### 8.1. Camadas de redundância

| Camada | Papel | Redundância |
|---|---|---|
| **Cloudflare Tunnel (primário)** | URL canônica fixa de todos os projetos | **2+ réplicas do `cloudflared`** para o mesmo túnel → se um conector cai, o tráfego continua pelo outro (HA nativo da Cloudflare) |
| **ngrok (secundário/DR)** | Caminho de emergência + bancada de debug | Domínio reservado em standby; failover por troca de `WEBHOOK_URL` + `WF-MCC-SET-URL` |
| **VPS-hub (âncora)** | Mantém o domínio público estável | Independe da máquina de casa; alvo final de migração |
| **Dados** | Workflows + credenciais | Postgres + backup automático agendado |

A URL que os serviços externos (WhatsApp/Evolution/APIs de IA) apontam é sempre o
**hostname da Cloudflare** (ex.: `n8n.seudominio.com.br`) — estável para sempre.
O ngrok só entra se o caminho Cloudflare ficar indisponível.

### 8.2. Docker Compose redundante (PC ou VPS)

```yaml
services:
  # --- Banco de dados (melhoria: Postgres no lugar do SQLite) ---
  postgres:
    image: postgres:16-alpine
    container_name: n8n-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=troque-esta-senha
      - POSTGRES_DB=n8n
    volumes:
      - pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U n8n -d n8n"]
      interval: 10s
      timeout: 5s
      retries: 5

  # --- n8n ---
  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    container_name: n8n
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=troque-esta-senha
      - N8N_HOST=n8n.seudominio.com.br
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://n8n.seudominio.com.br/
      - N8N_EDITOR_BASE_URL=https://n8n.seudominio.com.br/
      - GENERIC_TIMEZONE=America/Sao_Paulo
      - TZ=America/Sao_Paulo
      - N8N_PUBLIC_API_DISABLED=false
      - N8N_ENCRYPTION_KEY=troque-por-uma-chave-aleatoria-longa
    volumes:
      - n8n_data:/home/node/.n8n
    expose:
      - "5678"
    healthcheck:
      test: ["CMD-SHELL", "wget -qO- http://localhost:5678/healthz || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3

  # --- Cloudflare Tunnel: réplica 1 (HA) ---
  cloudflared-1:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared-1
    restart: unless-stopped
    command: tunnel --no-autoupdate run --token ${CF_TUNNEL_TOKEN}
    depends_on:
      - n8n

  # --- Cloudflare Tunnel: réplica 2 (HA) ---
  cloudflared-2:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared-2
    restart: unless-stopped
    command: tunnel --no-autoupdate run --token ${CF_TUNNEL_TOKEN}
    depends_on:
      - n8n

  # --- ngrok: caminho secundário / DR (perfil opcional) ---
  ngrok:
    image: ngrok/ngrok:latest
    container_name: ngrok
    restart: unless-stopped
    profiles: ["dr"]            # sobe só quando ativado: docker compose --profile dr up -d
    command: http n8n:5678 --domain=${NGROK_DOMAIN}
    environment:
      - NGROK_AUTHTOKEN=${NGROK_AUTHTOKEN}
    depends_on:
      - n8n

volumes:
  n8n_data:
  pg_data:
```

Arquivo `.env` ao lado (nunca commitar):

```env
CF_TUNNEL_TOKEN=token-do-named-tunnel-da-cloudflare
NGROK_AUTHTOKEN=seu-authtoken-ngrok
NGROK_DOMAIN=seu-dominio-reservado.ngrok.app
```

**Por que isso é redundante:**
- **2 réplicas `cloudflared`** registram o mesmo túnel → a Cloudflare roteia para a
  saudável. Matar um container não derruba os webhooks.
- **`restart: unless-stopped`** em tudo → recuperação automática após crash/reboot.
- **Healthchecks** → o Docker sabe quando o n8n/Postgres estão de fato prontos.
- **Postgres** → muito mais resiliente que o SQLite default para uso intenso/concorrente.
- **ngrok em perfil `dr`** → fica pronto, mas só liga quando você precisar (debug ou
  queda do caminho Cloudflare), sem custo de recursos no dia a dia.

### 8.3. Multi-projeto (vários serviços, um domínio)

No painel da Cloudflare (Zero Trust → Tunnels → seu túnel → **Public Hostnames**),
adicione um hostname por projeto apontando para o serviço local correspondente:

| Hostname | Service (interno) |
|---|---|
| `n8n.seudominio.com.br` | `http://n8n:5678` |
| `evolution.seudominio.com.br` | `http://evolution:8080` |
| `ia.seudominio.com.br` | `http://outro-projeto:porta` |

Hostnames **ilimitados**, todos com HTTPS, **de graça**, pelas mesmas 2 réplicas.
Cada novo projeto = só mais uma linha de Public Hostname.

### 8.4. Failover para o ngrok (quando o caminho Cloudflare cai)

```bash
# 1. Sobe o ngrok (DR)
docker compose --profile dr up -d ngrok

# 2. Aponta o n8n para a URL do ngrok e reinicia
#    (edite WEBHOOK_URL/N8N_EDITOR_BASE_URL no compose para https://${NGROK_DOMAIN}/)
docker compose up -d n8n

# 3. Re-registra a URL no orquestrador (já existe no seu projeto)
#    Rode o WF-MCC-SET-URL para atualizar o AGENTE_LOCAL com a URL do ngrok
```

> Com **domínio reservado** no ngrok, a URL de DR também é fixa — então o
> `WF-MCC-SET-URL` vira um passo único, não por sessão.

### 8.5. Backup automático (melhoria)

Adicione um serviço de backup agendado (dump do Postgres + volume do n8n):

```yaml
  backup:
    image: postgres:16-alpine
    container_name: n8n-backup
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      - PGPASSWORD=troque-esta-senha
    volumes:
      - ./backups:/backups
    entrypoint: >
      sh -c 'while true; do
        pg_dump -h postgres -U n8n n8n | gzip > /backups/n8n-$(date +%F-%H%M).sql.gz;
        find /backups -name "n8n-*.sql.gz" -mtime +7 -delete;
        sleep 86400;
      done'
```

Guarde `N8N_ENCRYPTION_KEY` e a senha do Postgres fora do servidor — sem a chave,
as credenciais não são recuperáveis mesmo com o dump.

---

## 9. Próximos passos sugeridos

1. Subir N8N local no PC (Opção A) e validar com um workflow simples.
2. Mover o subfluxo de **áudio WhatsApp + Whisper** para o local (evita gastar
   execuções do Cloud e resolve a pendência `OPENAI_API_KEY` em ambiente de teste).
3. Conectar o n8n-mcp e construir/validar workflows por conversa.
4. Se estabilizar, avaliar VPS (Oracle Free Tier ou Hetzner) para 24/7.
