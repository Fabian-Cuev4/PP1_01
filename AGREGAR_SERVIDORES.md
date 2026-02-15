# Guía para Escalar Backend con Réplicas Docker

## Configuración Actual (con Réplicas)

El sistema ahora usa **réplicas Docker** en lugar de múltiples servicios backend:

### **Ventajas de Réplicas:**
- ✅ **Más limpio**: Un solo servicio, múltiples contenedores
- ✅ **Escalabilidad dinámica**: Cambia el número de réplicas fácilmente
- ✅ **Balanceo automático**: Docker distribuye las peticiones
- ✅ **Menos configuración**: No necesitas editar nginx para cada réplica

---

## Para Cambiar el Número de Réplicas

### Método 1: Editar docker-compose.yml

Cambia el número en la sección `deploy.replicas`:

```yaml
backend:
  # ... (resto de configuración)
  deploy:
    replicas: 5  # Cambia este número (3, 5, 10, etc.)
    resources:
      limits:
        memory: 512M
      reservations:
        memory: 256M
```

### Método 2: Escalar Dinámicamente

```bash
# Escalar a 5 réplicas
docker-compose --profile multi-server up --scale backend=5

# Escalar a 10 réplicas
docker-compose --profile multi-server up --scale backend=10

# Reducir a 2 réplicas
docker-compose --profile multi-server up --scale backend=2
```

---

## Configuración Actual

### **docker-compose.yml:**
```yaml
backend:
  build:
    context: ./backend
    dockerfile: Dockerfile
  restart: always
  environment:
    MYSQL_HOST: mysql
    MYSQL_USER: root
    MYSQL_PASSWORD: Clubpengui1
    MYSQL_DATABASE: proyecto_maquinas
    MONGO_HOST: mongodb
    MONGO_PORT: 27017
    SERVER_ID: ${HOSTNAME}  # ID único automático
  volumes:
    - ./backend:/app
  depends_on:
    mysql:
      condition: service_healthy
    mongodb:
      condition: service_healthy
  networks:
    - siglab_network
  deploy:
    replicas: 3  # ← CAMBIA ESTE NÚMERO
    resources:
      limits:
        memory: 512M
      reservations:
        memory: 256M
  profiles:
    - multi-server
```

### **nginx.conf:**
```nginx
upstream maquinas_backend {
    # Docker balancea automáticamente las réplicas
    server backend:8000 weight=1 max_fails=3 fail_timeout=30s;
    
    keepalive 32;
}
```

---

## Ejemplos de Escalado

### **Para 5 Réplicas:**
```yaml
deploy:
  replicas: 5
```

```bash
# O dinámicamente:
docker-compose --profile multi-server up --scale backend=5
```

### **Para 10 Réplicas:**
```yaml
deploy:
  replicas: 10
```

```bash
# O dinámicamente:
docker-compose --profile multi-server up --scale backend=10
```

---

## Verificación y Monitoreo

### **Ver Réplicas Activas:**
```bash
# Ver todos los contenedores backend
docker ps | grep backend

# Ver detalles de las réplicas
docker-compose --profile multi-server ps backend
```

### **Probar Balanceo de Carga:**
```bash
# Múltiples requests para ver distribución
for i in {1..20}; do
  curl -X POST http://localhost/api/maquinas/agregar \
    -H "Content-Type: application/json" \
    -d '{"codigo_equipo":"TEST'$i'","tipo_equipo":"test","estado_actual":"activo","area":"test","fecha":"2024-01-01"}'
  sleep 0.1
done
```

### **Ver Logs de Réplicas:**
```bash
# Ver logs de todas las réplicas
docker-compose --profile multi-server logs -f backend

# Ver logs de una réplica específica
docker logs <container_id>
```

---

## Perfiles Disponibles

### **multi-server** (Producción con balanceo):
- mysql + mongodb + **backend (3+ réplicas)** + nginx + frontend
- Las máquinas van por nginx (balanceado)
- El resto va directo (sin nginx)

### **single-server** (Desarrollo):
- mysql + mongodb + **backend-single** + frontend
- Todo va directo sin nginx

---

## Recomendaciones

### **Para Desarrollo:**
```bash
docker-compose --profile single-server up --build
```

### **Para Producción (3 réplicas):**
```bash
docker-compose --profile multi-server up --build
```

### **Para Alta Carga (10 réplicas):**
```bash
docker-compose --profile multi-server up --scale backend=10
```

---

## Configuración Avanzada

### **Límites de Recursos por Réplica:**
```yaml
deploy:
  replicas: 5
  resources:
    limits:
      memory: 1G      # Máximo 1GB por réplica
      cpus: '0.5'      # Máximo 0.5 CPU por réplica
    reservations:
      memory: 512M     # Mínimo 512MB por réplica
      cpus: '0.25'     # Mínimo 0.25 CPU por réplica
```

### **Política de Reinicio:**
```yaml
deploy:
  replicas: 3
  restart_policy:
    condition: on-failure
    delay: 5s
    max_attempts: 3
```

---

## Resumen

Con réplicas Docker, el escalado es mucho más simple:

1. **Cambia `replicas: N`** en docker-compose.yml
2. **O usa `--scale backend=N`** dinámicamente
3. **Docker balancea automáticamente** entre las réplicas
4. **nginx apunta al servicio** `backend:8000`

¡Mucho más simple que múltiples servicios individuales!
