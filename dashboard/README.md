# Dashboard de Monitoreo SIGLAB

Dashboard en tiempo real para monitorear las peticiones al endpoint `/api/maquinas/agregar` con balanceo de carga.

## Arquitectura

- **3 Backends**: pp1_01-backend-1, pp1_01-backend-2, pp1_01-backend-3
- **Nginx**: Balanceador con Weighted Round Robin (pesos: 3, 2, 3)
- **Dashboard**: Servidor aiohttp + WebSockets nativos
- **Frontend**: Chart.js para visualización en tiempo real

## Características

- Monitoreo en tiempo real de peticiones POST a `/api/maquinas/agregar`
- Visualización de distribución de carga entre backends
- Alertas visuales para errores (status no 2xx)
- Auto-reset después de 7 segundos de inactividad
- Reconexión automática de WebSocket

## Instrucciones de Despliegue

### 1. Limpieza de Redes Docker

Antes de desplegar, limpiar redes existentes para evitar el error "Resource is still in use":

```bash
# Detener todos los contenedores
docker-compose down --remove-orphans

# Eliminar redes no utilizadas
docker network prune -f

# Eliminar volúmenes si es necesario (cuidado: borra datos)
# docker volume prune -f

# Verificar redes limpias
docker network ls
```

### 2. Despliegue Completo

```bash
# Iniciar todos los servicios (incluyendo dashboard)
docker-compose --profile all up -d

# Verificar estado
docker-compose ps

# Ver logs del dashboard
docker-compose logs -f dashboard
```

### 3. Acceso al Dashboard

- **Dashboard Principal**: http://localhost:18081
- **WebSocket Nativo**: ws://localhost:8001/ws
- **Balanceador Nginx**: http://localhost:8888
- **Monitoreo Nginx**: http://localhost:8080/nginx_status

### 4. Pruebas de Carga

```bash
# Iniciar saturador k6
docker-compose --profile load-test up -d k6-saturator

# Ver logs de k6
docker-compose logs -f k6-saturator
```

## Explicación Técnica

### ¿Por qué WebSockets nativos en lugar de Socket.io?

**Problema con Socket.io:**
- Socket.io requiere protocol handshake específico
- Puede generar error "426 Upgrade Required" si el cliente no maneja correctamente el protocolo
- Añade overhead innecesario para monitoreo simple

**Solución con WebSockets nativos (aiohttp):**
- Protocolo estándar RFC 6455
- Sin dependencias adicionales en el cliente
- Conexión directa y eficiente
- Manejo simple de errores 404/426

### Verificación de Estado de Peticiones

El servidor dashboard:

1. **Lee logs de Nginx**: Monitorea `/var/log/nginx/balanceo_siglab.log`
2. **Parsea con regex**: Extrae `$upstream_addr` y `$status` de cada línea
3. **Mapea servidores**: Convierte direcciones IP:puerto a nombres legibles
4. **Detecta errores**: Status < 200 o >= 300 activan alertas visuales
5. **Broadcast en tiempo real**: Envía datos a todos los clientes conectados

### Formato de Log Personalizado

```nginx
log_format balanceo '$upstream_addr - $remote_user [$time_local] "$request" '
                   '$status $body_bytes_sent "$http_request_uri"';
```

- `$upstream_addr`: IP:puerto del backend que procesó la petición
- `$status`: Código HTTP de respuesta
- `$request_uri`: URI solicitado (filtra solo `/api/maquinas/agregar`)

## Estructura de Archivos

```
dashboard/
├── server.py          # Servidor aiohttp con WebSockets
├── index.html         # Frontend con Chart.js
├── requirements.txt   # Dependencias Python
├── Dockerfile        # Imagen Docker
└── README.md         # Esta documentación
```

## Flujo de Datos

1. Cliente → Nginx (8888) → Backend (8000)
2. Nginx escribe en `/var/log/nginx/balanceo_siglab.log`
3. Dashboard lee logs en tiempo real
4. Dashboard envía datos vía WebSocket a frontend
5. Frontend actualiza gráfico con Chart.js

## Troubleshooting

### Error "host not found"
- Verificar que los backends estén saludables antes de iniciar Nginx
- Usar `depends_on: condition: service_healthy` en docker-compose.yml

### Error "Upgrade Required" (426)
- El dashboard usa WebSockets nativos, no Socket.io
- Conectar a `ws://localhost:18081/ws` (no al puerto 8001)

### Dashboard no muestra datos
- Verificar que Nginx esté generando logs: `docker exec nginx_balancer tail -f /var/log/nginx/balanceo_siglab.log`
- Comprobar conexión WebSocket en consola del navegador
- Revisar logs del dashboard: `docker-compose logs dashboard`

### Redes Docker conflictivas
- Siempre ejecutar `docker network prune -f` antes de desplegar
- Verificar que no existan contenedores huérfanos: `docker ps -a`

## Monitoreo y Mantenimiento

### Verificar estado de servicios:
```bash
# Estado general
docker-compose ps

# Logs específicos
docker-compose logs -f nginx
docker-compose logs -f dashboard
docker-compose logs -f backend-1
```

### Reiniciar servicios específicos:
```bash
# Reiniciar solo el dashboard
docker-compose restart dashboard

# Reconstruir imagen del dashboard
docker-compose build --no-cache dashboard
docker-compose up -d dashboard
```

### Estadísticas en tiempo real:
- Acceder a http://localhost:18081 para ver el dashboard
- Las barras se ponen rojas si hay errores HTTP
- El gráfico se resetea automáticamente después de 7s sin actividad
