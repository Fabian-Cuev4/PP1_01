# Load Balancer Nginx - Configuración y Algoritmos

## Archivo de Configuración
`nginx.conf` - Configuración principal del load balancer

## Algoritmos Disponibles

### 1. Round Robin (por defecto)
- **Descripción**: Distribuye peticiones equitativamente en orden circular
- **Uso**: Ideal cuando todos los servidores tienen similar capacidad
- **Configuración**: Sin directiva especial (comportamiento por defecto)

### 2. Least Connections
- **Descripción**: Envía al servidor con menos conexiones activas
- **Uso**: Óptimo cuando las peticiones tienen diferentes duraciones
- **Configuración**: Directiva `least_conn`

### 3. Weighted Round Robin
- **Descripción**: Distribuye según pesos asignados a cada servidor
- **Uso**: Cuando los servidores tienen diferentes capacidades
- **Configuración**: Parámetro `weight` en cada servidor

## Configuración Actual

### Servidores Backend
- `pp1_01-backend-1:8000` - Réplica 1
- `pp1_01-backend-2:8000` - Réplica 2  
- `pp1_01-backend-3:8000` - Réplica 3

### Algoritmo Activo
**Weighted Round Robin** con pesos:
- Servidor 1: weight=3 (37.5% del tráfico)
- Servidor 2: weight=2 (25% del tráfico)
- Servidor 3: weight=3 (37.5% del tráfico)

## Cómo Cambiar de Algoritmo

1. Abre el archivo `nginx.conf`
2. Busca la sección `SELECCIONAR UNO SOLO - DESCOMENTAR EL DESEADO`
3. Comenta el upstream actual y descomenta el deseado:

```nginx
# Para activar Round Robin:
# upstream maquinas_backend {
#    server pp1_01-backend-1:8000 weight=1 max_fails=3 fail_timeout=5s;
#    server pp1_01-backend-2:8000 weight=1 max_fails=3 fail_timeout=5s;
#    server pp1_01-backend-3:8000 weight=1 max_fails=3 fail_timeout=5s;
#    keepalive 32;
# }

# Para activar Least Connections:
# upstream maquinas_backend {
#     least_conn;
#     server pp1_01-backend-1:8000 weight=1 max_fails=3 fail_timeout=5s;
#     server pp1_01-backend-2:8000 weight=1 max_fails=3 fail_timeout=5s;
#     server pp1_01-backend-3:8000 weight=1 max_fails=3 fail_timeout=5s;
#     keepalive 32;
# }

# Para activar Weighted Round Robin (actual):
upstream maquinas_backend {
    server pp1_01-backend-1:8000 weight=3 max_fails=3 fail_timeout=5s;
    server pp1_01-backend-2:8000 weight=2 max_fails=3 fail_timeout=5s;
    server pp1_01-backend-3:8000 weight=3 max_fails=3 fail_timeout=5s;
    keepalive 32;
}
```

## Aplicar Cambios

```bash
# Reiniciar nginx para aplicar cambios
docker restart nginx_balancer

# O usando docker-compose
docker-compose restart nginx
```

## Monitoreo

- **Health Check**: `GET http://localhost:8888/health`
- **Estadísticas Nginx**: `GET http://localhost:8080/nginx_status`
- **Logs de nginx**: `docker logs nginx_balancer -f`

## Configuración de Failover

- **max_fails=3**: Permite 3 fallos antes de marcar servidor como no disponible
- **fail_timeout=5s**: Servidor no disponible por 5 segundos después de fallos
- **Reintentos automáticos**: nginx envía tráfico a servidores disponibles

## Escalabilidad

### Para añadir más servidores:

1. **Escalar el servicio**:
   ```bash
   docker-compose up --scale backend=4 -d
   ```

2. **Agregar nuevo servidor al nginx.conf**:
   ```nginx
   upstream maquinas_backend {
       server pp1_01-backend-1:8000 weight=3 max_fails=3 fail_timeout=5s;
       server pp1_01-backend-2:8000 weight=2 max_fails=3 fail_timeout=5s;
       server pp1_01-backend-3:8000 weight=3 max_fails=3 fail_timeout=5s;
       server pp1_01-backend-4:8000 weight=2 max_fails=3 fail_timeout=5s;  # Nuevo
       keepalive 32;
   }
   ```

3. **Reiniciar nginx**:
   ```bash
   docker restart nginx_balancer
   ```

## Rutas Balanceadas

El load balancer solo balancea la ruta:
- `/api/maquinas/agregar` - Endpoint para agregar máquinas

## Arquitectura

```
Cliente → Nginx Load Balancer (puerto 8888)
    ↓
├── pp1_01-backend-1:8000
├── pp1_01-backend-2:8000
└── pp1_01-backend-3:8000
```

## Redes Docker

- **siglab_network**: Comunicación interna entre servicios
- **frontend_network**: Comunicación con frontend
- **nginx_balancer**: Actúa como gateway para tráfico externo

## Comparación de Algoritmos

| Algoritmo | Ventajas | Desventajas | Uso Recomendado |
|------------|------------|--------------|-------------------|
| Round Robin | Simple, equitativo | No considera carga | Servidores iguales |
| Least Connections | Balanceo inteligente | Requiere más cómputo | Cargas variables |
| Weighted | Control total | Configuración manual | Servidores diferentes |

## Optimización

### Parámetros de Rendimiento
- **keepalive 32**: Conexiones persistentes
- **max_fails 3**: Detección rápida de fallos
- **fail_timeout 5s**: Recuperación rápida
- **Timeouts agresivos**: 5-10s para microservicios

### Métricas Importantes
- **Request Rate**: Peticiones por segundo
- **Response Time**: Tiempo de respuesta promedio
- **Error Rate**: Porcentaje de fallos
- **Distribution**: Balanceo entre servidores
