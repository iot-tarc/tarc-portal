import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Permitir requisições de origens cruzadas em desenvolvimento
  // Adicione aqui os IPs/hosts que precisam acessar o Next.js
  allowedDevOrigins: [
    "*",
    "10.13.22.191",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://10.13.22.191:3000",
  ],
  
  // Outras configurações úteis
  reactStrictMode: true,
  
  // Configuração para Docker (output standalone)
  output: "standalone",
};

export default nextConfig;
