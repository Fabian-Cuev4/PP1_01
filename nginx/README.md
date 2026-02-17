# Load Balancer Nginx - Configuración Avanzada

## 📋 Descripción
Load balancer de alto rendimiento con Nginx para distribuir carga entre múltiples backends FastAPI del sistema SIGLAB. Configurado con algoritmos de balanceo, health checks y monitoreo integrado.

## 🎯 Características Principales

- **4 Algoritmos de Balanceo**: Round Robin, Least Connections, IP Hash, Weighted
- **Health Checks**: Detección automática de servidores caídos
- **Failover**: Recuperación automática de servicios
- **Monitoreo**: Logs personalizados y estadísticas en tiempo real
- **SSL/TLS**: Terminación segura (futura)
- **Caching**: Optimización de respuestas estáticas

## 🏗️ Arquitectura del Load Balancer

```
┌─────────────────────────────────────────────────────────┐
│                    Internet / Clients                  │
└─────────────────────┬───────────────────────────────────┘
                      │
              ┌───────▼───────┐
              │   Nginx LB    │
              │   :8888       │
              │  :8080 (stats)│
              └───────┬───────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
│  Backend 1  │ │ Backend 2  │ │ Backend 3  │
│  :8000      │ │ :8000      │ │ :8000      │
│  FastAPI    │ │ FastAPI    │ │ FastAPI    │
└─────────────┘ └─────────────┘ └─────────────┘
```

## ⚙️ Configuración Principal

### 1. Estructura del Archivo

```nginx
# nginx.conf - Estructura completa
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    # Logging format personalizado para dashboard
    log_format balanceo_siglab '$upstream_addr - $remote_user [$time_local] '
                              '"$request" $status $body_bytes_sent '
                              '"$http_referer" "$http_user_agent"';
    
    # Configuración de rendimiento
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript;
    
    # Upstreams configurados
    include /etc/nginx/conf.d/*.conf;
}
```

### 2. Algoritmos de Balanceo Disponibles

```nginx
# ┌─────────────────────────────────────────────────────────┐
# │            SELECCIONAR UNO SOLO - DESCOMENTAR EL DESEADO   │
# └─────────────────────────────────────────────────────────┘

# 1. Round Robin (por defecto)
# upstream maquinas_backend {
#     server pp1_01-backend-1:8000 weight=1 max_fails=1 fail_timeout=5s;
#     server pp1_01-backend-2:8000 weight=1 max_fails=1 fail_timeout=5s;
#     server pp1_01-backend-3:8000 weight=1 max_fails=1 fail_timeout=5s;
#     keepalive 32;
# }

# 2. Least Connections
# upstream maquinas_backend {
#     least_conn;
#     server pp1_01-backend-1:8000 weight=1 max_fails=1 fail_timeout=5s;
#     server pp1_01-backend-2:8000 weight=1 max_fails=1 fail_timeout=5s;
#     server pp1_01-backend-3:8000 weight=1 max_fails=1 fail_timeout=5s;
#     keepalive 32;
# }

# 3. IP Hash
# upstream maquinas_backend {
#     ip_hash;
#     server pp1_01-backend-1:8000 weight=1 max_fails=1 fail_timeout=5s;
#     server pp1_01-backend-2:8000 weight=1 max_fails=1 fail_timeout=5s;
#     server pp1_01-backend-3:8000 weight=1 max_fails=1 fail_timeout=5s;
#     keepalive 32;
# }

# 4. Weighted Round Robin (ACTIVO)
upstream maquinas_backend {
    server pp1_01-backend-1:8000 weight=3 max_fails=1 fail_timeout=5s;
    server pp1_01-backend-2:8000 weight=2 max_fails=1 fail_timeout=5s;
    server pp1_01-backend-3:8000 weight=3 max_fails=1 fail_timeout=5s;
    keepalive 32;
}
```

### 3. Configuración del Servidor

```nginx
# Servidor principal de balanceo
server {
    listen 80;
    server_name _;
    
    # Logs de acceso para el dashboard
    access_log /var/log/nginx/balanceo_siglab.log balanceo_siglab;
    error_log /var/log/nginx/error.log;
    
    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
    
    # Balanceo para endpoint específico de máquinas
    location /api/maquinas/agregar {
        proxy_pass http://maquinas_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts optimizados
        proxy_connect_timeout 5s;
        proxy_send_timeout 10s;
        proxy_read_timeout 10s;
        
        # Headers de tracking
        add_header X-Upstream-Addr $upstream_addr always;
        add_header X-Upstream-Status $upstream_status always;
    }
    
    # Proxy para otros endpoints de API
    location /api/ {
        proxy_pass http://maquinas_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_connect_timeout 5s;
        proxy_send_timeout 10s;
        proxy_read_timeout 10s;
    }
    
    # Servidor de estadísticas
    location /nginx_status {
        stub_status on;
        access_log off;
        allow 172.0.0.0/8;  # Solo red interna
        deny all;
    }
}

# Servidor de estadísticas en puerto separado
server {
    listen 8080;
    server_name _;
    
    location /nginx_status {
        stub_status on;
        access_log off;
        allow all;  # Accesible para monitoreo
    }
    
    location / {
        return 200 "Nginx Statistics Server\n";
        add_header Content-Type text/plain;
    }
}
```

## 📊 Algoritmos de Balanceo

### 1. Round Robin (Distribución Equitativa)

**Descripción**: Distribuye peticiones en orden circular entre todos los servidores disponibles.

```nginx
upstream maquinas_backend {
    server pp1_01-backend-1:8000;
    server pp1_01-backend-2:8000;
    server pp1_01-backend-3:8000;
}
```

**Ventajas**:
- Simple y predecible
- Distribución equitativa
- Sin estado adicional

**Desventajas**:
- No considera carga real del servidor
- Sesiones pueden cambiar de servidor

**Uso recomendado**: Servidores con capacidad similar y peticiones de corta duración.

### 2. Least Connections (Menos Conexiones)

**Descripción**: Envía cada petición al servidor con menos conexiones activas.

```nginx
upstream maquinas_backend {
    least_conn;
    server pp1_01-backend-1:8000;
    server pp1_01-backend-2:8000;
    server pp1_01-backend-3:8000;
}
```

**Ventajas**:
- Balanceo inteligente basado en carga real
- Mejor para peticiones de duración variable

**Desventajas**:
- Requiere seguimiento de estado de conexiones
- Ligero overhead computacional

**Uso recomendado**: Peticiones con duración variable y diferentes costos de procesamiento.

### 3. IP Hash (Persistencia de Sesión)

**Descripción**: Mismo cliente (basado en IP) siempre va al mismo servidor.

```nginx
upstream maquinas_backend {
    ip_hash;
    server pp1_01-backend-1:8000;
    server pp1_01-backend-2:8000;
    server pp1_01-backend-3:8000;
}
```

**Ventajas**:
- Persistencia de sesión automática
- Cache local del servidor efectivo

**Desventajas**:
- Distribución desigual si hay pocos clientes
- Problemas con clientes detrás de NAT

**Uso recomendado**: Aplicaciones que requieren sticky sessions sin configuración adicional.

### 4. Weighted Round Robin (Ponderado)

**Descripción**: Distribución según pesos asignados a cada servidor.

```nginx
upstream maquinas_backend {
    server pp1_01-backend-1:8000 weight=3;  # 37.5% del tráfico
    server pp1_01-backend-2:8000 weight=2;  # 25% del tráfico
    server pp1_01-backend-3:8000 weight=3;  # 37.5% del tráfico
}
```

**Ventajas**:
- Control total sobre distribución
- Aprovecha diferentes capacidades

**Desventajas**:
- Configuración manual requerida
- No se adapta a cambios dinámicos

**Uso recomendado**: Servidores con diferentes capacidades de hardware.

## 🔧 Configuración Avanzada

### 1. Health Checks y Failover

```nginx
upstream maquinas_backend {
    server pp1_01-backend-1:8000 weight=3 max_fails=1 fail_timeout=5s;
    server pp1_01-backend-2:8000 weight=2 max_fails=1 fail_timeout=5s;
    server pp1_01-backend-3:8000 weight=3 max_fails=1 fail_timeout=5s;
    
    # Backup server (solo se activa si todos fallan)
    server backup-server:8000 backup;
    
    keepalive 32;
    keepalive_requests 100;
    keepalive_timeout 60s;
}
```

**Parámetros**:
- `max_fails=1`: Número de fallos antes de marcar como no disponible
- `fail_timeout=5s`: Tiempo que el servidor permanece marcado como caído
- `backup`: Servidor de respaldo solo para emergencias

### 2. Timeouts y Optimización

```nginx
location /api/ {
    proxy_pass http://maquinas_backend;
    
    # Timeouts agresivos para microservicios
    proxy_connect_timeout 5s;
    proxy_send_timeout 10s;
    proxy_read_timeout 10s;
    
    # Buffering optimizado
    proxy_buffering on;
    proxy_buffer_size 4k;
    proxy_buffers 8 4k;
    proxy_busy_buffers_size 8k;
    
    # Reintentos configurados
    proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
    proxy_next_upstream_tries 2;
    proxy_next_upstream_timeout 5s;
}
```

### 3. Headers de Monitoreo

```nginx
location /api/ {
    # Headers estándar de proxy
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    
    # Headers de debugging y monitoreo
    add_header X-Upstream-Addr $upstream_addr always;
    add_header X-Upstream-Status $upstream_status always;
    add_header X-Upstream-Response-Time $upstream_response_time always;
    add_header X-Request-ID $request_id always;
    
    # Headers de seguridad
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

### 4. Logging Personalizado

```nginx
# Formato detallado para debugging
log_format detailed '$remote_addr - $remote_user [$time_local] '
                   '"$request" $status $body_bytes_sent '
                   '"$http_referer" "$http_user_agent" '
                   'rt=$request_time uct="$upstream_connect_time" '
                   'uht="$upstream_header_time" urt="$upstream_response_time" '
                   'us="$upstream_status" ua="$upstream_addr"';

# Formato para dashboard
log_format dashboard '$upstream_addr $status $request_time $request';

# Aplicar formatos
access_log /var/log/nginx/access.log detailed;
access_log /var/log/nginx/dashboard.log dashboard;
```

## 🚀 Despliegue y Configuración

### 1. Dockerfile Optimizado

```dockerfile
# Dockerfile
FROM nginx:alpine

# Copiar configuración personalizada
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/ /etc/nginx/conf.d/

# Crear directorios de logs
RUN mkdir -p /var/log/nginx

# Scripts de health check
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Exponer puertos
EXPOSE 80 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
```

### 2. Script de Entrada

```bash
#!/bin/sh
# docker-entrypoint.sh

set -e

# Esperar a que los backends estén disponibles
echo "Waiting for backends..."
for backend in pp1_01-backend-1 pp1_01-backend-2 pp1_01-backend-3; do
    until nc -z $backend 8000; do
        echo "Backend $backend is unavailable - sleeping"
        sleep 2
    done
    echo "Backend $backend is ready"
done

echo "All backends are ready - starting nginx..."

# Ejecutar nginx
exec nginx -g "daemon off;"
```

### 3. Integración con Docker Compose

```yaml
# docker-compose.yml
nginx:
  build:
    context: ./nginx
    dockerfile: Dockerfile
  container_name: nginx_balancer
  restart: always
  ports:
    - "8888:80"      # Balanceador principal
    - "8080:8080"   # Estadísticas
  depends_on:
    backend-1:
      condition: service_healthy
    backend-2:
      condition: service_healthy
    backend-3:
      condition: service_healthy
  volumes:
    - nginx_logs:/var/log/nginx  # Compartir logs con dashboard
  networks:
    - siglab_network
    - frontend_network
  healthcheck:
    test: ["CMD-SHELL", "curl -f http://localhost/health || exit 1"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 40s
```

## 📈 Monitoreo y Estadísticas

### 1. Stub Status Module

```bash
# Ver estadísticas básicas
curl http://localhost:8080/nginx_status

# Salida esperada:
Active connections: 2 
server accepts handled requests
 16630 16630 31070 
Reading: 0 Writing: 1 Waiting: 1 
```

**Métricas explicadas**:
- `Active connections`: Conexiones actualmente activas
- `accepts`: Conexiones aceptadas total
- `handled`: Conexiones manejadas exitosamente
- `requests**: Requests procesados total
- `Reading`: Leyendo header de request
- `Writing`: Escribiendo respuesta
- `Waiting`: Conexiones en keep-alive

### 2. Logs de Balanceo

```bash
# Ver logs de balanceo en tiempo real
docker exec nginx_balancer tail -f /var/log/nginx/balanceo_siglab.log

# Ejemplo de salida:
172.20.0.3:8000 - - [16/Feb/2026:18:30:45 +0000] "POST /api/maquinas/agregar HTTP/1.1" 200 156 "-" "Mozilla/5.0..."

# Parseo con awk para estadísticas
docker exec nginx_balancer awk '{print $1}' /var/log/nginx/balanceo_siglab.log | sort | uniq -c
```

### 3. Métricas Avanzadas

```bash
# Script de monitoreo
#!/bin/bash
# monitor_nginx.sh

echo "=== Nginx Load Balancer Metrics ==="
echo "Timestamp: $(date)"
echo

# Conexiones activas
echo "Active Connections:"
curl -s http://localhost:8080/nginx_status | grep "Active connections"

# Distribución de carga (últimos 100 requests)
echo
echo "Load Distribution (last 100 requests):"
docker exec nginx_balancer tail -100 /var/log/nginx/balanceo_siglab.log | \
    awk '{print $1}' | sort | uniq -c | sort -nr

# Tasa de errores
echo
echo "Error Rate (last 100 requests):"
total=$(docker exec nginx_balancer tail -100 /var/log/nginx/balanceo_siglab.log | wc -l)
errors=$(docker exec nginx_balancer tail -100 /var/log/nginx/balanceo_siglab.log | \
    awk '$9 >= 400 {print}' | wc -l)
echo "Errors: $errors/$total ($(( errors * 100 / total ))%)"

# Response times promedio
echo
echo "Average Response Time:"
docker exec nginx_balancer tail -100 /var/log/nginx/balanceo_siglab.log | \
    awk '{sum+=$NF; count++} END {print sum/count "s"}'
```

## 🔧 Gestión de Configuración

### 1. Cambiar Algoritmo de Balanceo

```bash
# Editar configuración
vim nginx/nginx.conf

# Comentar upstream actual y descomentar el deseado

# Reiniciar nginx
docker-compose restart nginx

# Verificar cambio
docker-compose logs nginx | grep "using method"
```

### 2. Añadir Nuevo Backend

```bash
# 1. Escalar servicio
docker-compose up --scale backend-4=1 -d

# 2. Actualizar nginx.conf
upstream maquinas_backend {
    server pp1_01-backend-1:8000 weight=3 max_fails=1 fail_timeout=5s;
    server pp1_01-backend-2:8000 weight=2 max_fails=1 fail_timeout=5s;
    server pp1_01-backend-3:8000 weight=3 max_fails=1 fail_timeout=5s;
    server pp1_01-backend-4:8000 weight=2 max_fails=1 fail_timeout=5s;  # Nuevo
    keepalive 32;
}

# 3. Recargar configuración
docker-compose exec nginx nginx -s reload
```

### 3. Configuración en caliente

```bash
# Verificar sintaxis
docker-compose exec nginx nginx -t

# Recargar sin reiniciar
docker-compose exec nginx nginx -s reload

# Reiniciar completamente
docker-compose restart nginx
```

## 🚨 Troubleshooting

### Problemas Comunes

#### 1. "host not found" en upstream

```bash
# Verificar resolución DNS
docker exec nginx_balancer nslookup pp1_01-backend-1

# Verificar conectividad
docker exec nginx_balancer nc -zv pp1_01-backend-1 8000

# Revisar logs de errores
docker-compose logs nginx | grep -i "host not found"
```

**Solución**: Asegurar que los backends están corriendo antes de iniciar nginx.

#### 2. 502 Bad Gateway

```bash
# Verificar salud de backends
curl http://localhost:8888/health

# Revisar logs de nginx
docker-compose logs nginx | grep "502"

# Verificar timeouts
docker exec nginx_balancer grep timeout /etc/nginx/nginx.conf
```

**Solución**: Ajustar timeouts o verificar salud de backends.

#### 3. Distribución desigual

```bash
# Ver distribución actual
docker exec nginx_balancer tail -1000 /var/log/nginx/balanceo_siglab.log | \
    awk '{print $1}' | sort | uniq -c

# Ver configuración de pesos
docker exec nginx_balancer grep -A 10 "upstream maquinas_backend" /etc/nginx/nginx.conf
```

**Solución**: Ajustar pesos o cambiar algoritmo de balanceo.

### Debug Mode

```nginx
# Configuración de debug
error_log /var/log/nginx/debug.log debug;

# Log de variables
location /debug {
    return 200 "upstream_addr=$upstream_addr upstream_status=$upstream_status";
}
```

## 📊 Optimización de Rendimiento

### 1. Parámetros de Rendimiento

```nginx
# Optimización para alta concurrencia
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 2048;
    use epoll;
    multi_accept on;
}

http {
    # Keep-alive optimizado
    keepalive_timeout 65;
    keepalive_requests 1000;
    
    # Buffering
    client_body_buffer_size 128k;
    client_max_body_size 10m;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 4k;
    
    # Timeouts optimizados
    client_body_timeout 12;
    client_header_timeout 12;
    send_timeout 10;
}
```

### 2. Caching

```nginx
# Proxy cache
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g 
                 inactive=60m use_temp_path=off;

server {
    location /api/maquinas/listar {
        proxy_cache api_cache;
        proxy_cache_valid 200 5m;
        proxy_cache_key "$scheme$request_method$host$request_uri";
        proxy_pass http://maquinas_backend;
    }
}
```

### 3. Rate Limiting

```nginx
# Limitar requests por IP
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

server {
    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        proxy_pass http://maquinas_backend;
    }
}
```

## 🔒 Seguridad

### 1. Headers de Seguridad

```nginx
add_header X-Frame-Options DENY always;
add_header X-Content-Type-Options nosniff always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'"; always;
```

### 2. Restricción de Acceso

```nginx
# Limitar acceso a estadísticas
location /nginx_status {
    stub_status on;
    allow 172.0.0.0/8;
    allow 127.0.0.1;
    deny all;
}

# Limitar métodos HTTP
if ($request_method !~ ^(GET|HEAD|POST|PUT|DELETE|OPTIONS)$ ) {
    return 405;
}
```

### 3. Prevención de Abuso

```nginx
# Limitar tamaño de request
client_max_body_size 10M;

# Limitar request rate
limit_req_zone $binary_remote_addr zone=general:10m rate=5r/s;

# Protección contra slowloris
client_body_timeout 12;
client_header_timeout 12;
```

## 🔄 Mejores Prácticas

### 1. Configuración
- **Mantenimiento**: Usar `nginx -s reload` para cambios en caliente
- **Testing**: Siempre verificar con `nginx -t` antes de aplicar
- **Backups**: Guardar versiones anteriores de configuración
- **Monitoreo**: Implementar alertas para 502/503/504

### 2. Rendimiento
- **Keep-alive**: Mantener conexiones abiertas cuando sea posible
- **Compression**: Habilitar gzip para respuestas > 1KB
- **Buffering**: Ajustar tamaños según carga de trabajo
- **Timeouts**: Configurar según latencia de backends

### 3. Seguridad
- **Principle of Least Privilege**: Exponer solo puertos necesarios
- **Regular Updates**: Mantener nginx actualizado
- **Network Segmentation**: Usar redes Docker separadas
- **Monitoring**: Detectar patrones anómalos de tráfico

---

**Versión**: 2.0.0  
**Estado**: Producción  
**Última Actualización**: 2026  
**Arquitectura**: High Availability Load Balancer
