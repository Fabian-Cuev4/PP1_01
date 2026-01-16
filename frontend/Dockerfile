# Usamos nginx en versión alpine (ligera) como base para servir archivos web
FROM nginx:alpine

# Copiamos los archivos CSS, JS e imágenes al contenedor
COPY static /usr/share/nginx/html/static

# Copiamos las páginas HTML al contenedor
COPY templates /usr/share/nginx/html/templates

# Copiamos la configuración personalizada de nginx (rutas y proxy al backend)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponemos el puerto 80 para que nginx pueda recibir peticiones HTTP
EXPOSE 80

# Iniciamos nginx en primer plano (daemon off es necesario para que Docker no lo detenga)
CMD ["nginx", "-g", "daemon off;"]
