# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Argumento para URL da API (usado no build-time)
ARG NEXT_PUBLIC_API_URL=http://localhost:8001
ARG VITE_API_URL=http://localhost:8001
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Copiar arquivos de dependências
COPY package*.json ./

# Instalar dependências
RUN npm ci --legacy-peer-deps

# Copiar código fonte
COPY . .

# Build da aplicação Vite
RUN npm run build

# Stage 2: Production
FROM nginx:alpine AS runner

# Copiar arquivos buildados do Vite
COPY --from=builder /app/dist /usr/share/nginx/html

# Copiar configuração do nginx para SPA (react-router)
RUN echo 'server { \
    listen 80; \
    server_name _; \
    root /usr/share/nginx/html; \
    index index.html; \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

# Substituir variáveis de ambiente no index.html em runtime (se necessário)
# Isso permite mudar a API URL sem rebuild
CMD sh -c 'sed -i "s|NEXT_PUBLIC_API_URL_PLACEHOLDER|${NEXT_PUBLIC_API_URL:-http://localhost:8001}|g" /usr/share/nginx/html/index.html && nginx -g "daemon off;"'

