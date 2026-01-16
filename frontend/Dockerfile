FROM nginx:alpine

# Copiar archivos estáticos
COPY static /usr/share/nginx/html/static
COPY templates /usr/share/nginx/html/templates

# Copiar configuración de nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
