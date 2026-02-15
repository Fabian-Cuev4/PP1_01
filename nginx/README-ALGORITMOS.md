# Algoritmos de Load Balancing para Nginx

Este archivo contiene 4 algoritmos de load balancing configurados para 3 servidores backend.

## Archivo de Configuración
`nginx-load-balancing-algorithms.conf`

## Algoritmos Disponibles

### 1. Round Robin (por defecto)
- **Descripción**: Distribuye las peticiones equitativamente entre todos los servidores
- **Uso**: Ideal cuando todos los servidores tienen similar capacidad
- **Configuración**: Sin directiva especial (comportamiento por defecto)

### 2. Least Connections
- **Descripción**: Envía cada nueva petición al servidor con menos conexiones activas
- **Uso**: Óptimo cuando las peticiones tienen diferentes duraciones
- **Configuración**: Directiva `least_conn`

### 3. IP Hash
- **Descripción**: Mismo cliente (IP) siempre va al mismo servidor
- **Uso**: Requerido para mantener sesiones persistentes sin sticky sessions
- **Configuración**: Directiva `ip_hash`

### 4. Weighted Round Robin
- **Descripción**: Distribución basada en pesos asignados a cada servidor
- **Uso**: Cuando los servidores tienen diferentes capacidades
- **Configuración**: Parámetro `weight` en cada servidor

## Cómo Cambiar de Algoritmo

1. Abre el archivo `nginx-load-balancing-algorithms.conf`
2. Busca la sección `SELECCIONAR EL ALGORITMO DESEADO`
3. Comenta la línea actual y descomenta la del algoritmo deseado:

```nginx
# Para usar Round Robin:
# set $backend_upstream "maquinas_backend_round_robin";

# Para usar Least Connections:
# set $backend_upstream "maquinas_backend_least_conn";

# Para usar IP Hash:
# set $backend_upstream "maquinas_backend_ip_hash";

# Para usar Weighted Round Robin:
set $backend_upstream "maquinas_backend_weighted";
```

## Configuración de Servidores

Los 3 servidores están configurados como:
- `backend:8000` - Servidor principal (Docker Compose)
- `backend_1:8000` - Réplica 1
- `backend_2:8000` - Réplica 2
- `backend_3:8000` - Réplica 3

## Pesos en Weighted Round Robin

- Servidor 1: weight=3 (30% del tráfico)
- Servidor 2: weight=2 (20% del tráfico)
- Servidor 3: weight=3 (30% del tráfico)
- Servidor 4: weight=2 (20% del tráfico)

## Monitoreo

- **Health Check**: `GET /health`
- **Status del Load Balancer**: `GET /lb-status`
- **Estadísticas Nginx**: `GET http://localhost:8080/nginx_status`

## Aplicar Cambios

```bash
# Recargar configuración de Nginx
nginx -s reload

# O reiniciar el contenedor
docker-compose restart nginx
```
