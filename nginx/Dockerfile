# Configuración para Dockerfile de Nginx
FROM nginx:alpine

# Copiar configuración personalizada
COPY nginx.conf /etc/nginx/nginx.conf

# Exponer puertos
EXPOSE 80 8080

# Comando para iniciar nginx
CMD ["nginx", "-g", "daemon off;"]
