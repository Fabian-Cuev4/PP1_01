# EXPLICACIÓN: Usamos nginx estándar para load balancing
FROM nginx:alpine

# EXPLICACIÓN: Copiamos archivos estáticos y templates
COPY static /usr/share/nginx/html/static
COPY templates /usr/share/nginx/html/templates

# EXPLICACIÓN: Copiamos configuración con load balancer
COPY nginx.conf /etc/nginx/conf.d/default.conf

# EXPLICACIÓN: Exponemos puertos para aplicación y dashboard simple
EXPOSE 81 8083

# EXPLICACIÓN: Iniciamos nginx
CMD ["nginx", "-g", "daemon off;"]
