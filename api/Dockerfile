FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primeiro (para cache de layers)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação (nova estrutura MVC)
COPY alembic.ini .
COPY alembic/ alembic/
COPY models/ models/
COPY schemas/ schemas/
COPY services/ services/
COPY controllers/ controllers/
COPY database.py .
COPY main.py .
COPY entrypoint.sh .

# Tornar entrypoint executável
RUN chmod +x /app/entrypoint.sh

# Expor porta
EXPOSE 8000

# Comando para rodar migrações e iniciar aplicação
CMD ["/app/entrypoint.sh"]

