# TARC - Plataforma IoT

Sistema de monitoramento e gerenciamento de dispositivos IoT.

## Estrutura do Projeto

- `api/` - Backend FastAPI (Python)
- `web/` - Frontend Next.js (React/TypeScript)
- `docker-compose.yml` - Orquestração de serviços

## Requisitos

- Docker
- Docker Compose

## Como Executar

### Desenvolvimento Local

1. Clone o repositório
2. Configure as variáveis de ambiente se necessário
3. Execute:
```bash
docker-compose up -d
```

### Build e Deploy

```bash
# Build de todos os serviços
docker-compose build

# Iniciar serviços
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down
```

## Serviços

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **PostgreSQL**: localhost:5432

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:

```bash
cp .env.example .env
```

### Variáveis Principais

- `NEXT_PUBLIC_API_URL`: URL da API que o frontend usa (padrão: `http://localhost:8000`)
  - Em desenvolvimento local: `http://localhost:8000`
  - Em produção: `http://seu-servidor:8000` ou `http://IP_DO_SERVIDOR:8000`
  
- `DATABASE_URL`: URL de conexão com o PostgreSQL
  - Formato: `postgresql://usuario:senha@host:porta/nome_do_banco`
  - Padrão no Docker: `postgresql://postgres:postgres@postgres:5432/tarc_db`

### Importante

- A variável `NEXT_PUBLIC_API_URL` é necessária porque o Next.js precisa dela em build-time
- No Docker, use `http://localhost:8000` se o frontend e API estiverem na mesma máquina
- Se estiverem em servidores diferentes, use o IP/hostname do servidor da API

## Comandos Úteis

```bash
# Rebuild apenas um serviço
docker-compose build api
docker-compose build web

# Restart um serviço
docker-compose restart api

# Ver logs de um serviço específico
docker-compose logs -f api
docker-compose logs -f web

# Executar comandos dentro de um container
docker-compose exec api bash
docker-compose exec web sh
```

## Produção

Para produção, ajuste:
1. Variáveis de ambiente no `docker-compose.yml`
2. Senhas do PostgreSQL
3. URLs da API no frontend
4. Configurações de rede/firewall conforme necessário
