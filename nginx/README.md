# Balanceador con Nginx ESPECÍFICO para Microservicio de Máquinas

## Configuración Implementada

He configurado nginx como balanceador de carga **ÚNICAMENTE** para el microservicio de máquinas con las siguientes características:

### 1. **Arquitectura Híbrida**
- **Microservicio Máquinas**: Balanceado con nginx (N servidores)
- **Resto de funcionalidades**: Directas al backend principal (sin balanceo)
- **Frontend**: Directo sin pasar por nginx para rutas no específicas

### 2. **Rutas Manejadas por Nginx (Balanceadas)**
```nginx
/api/maquinas/           # Todas las operaciones de máquinas
/api/maquinas/agregar     # POST crítico con configuración especial
```

### 3. **Rutas Directas (Sin Balanceo)**
```nginx
/                        # Frontend directo
/api/login               # Autenticación directa
/api/register            # Registro directo  
/api/mantenimiento/      # Mantenimiento directo
/api/                    # Cualquier otra ruta API directa
```

### 4. **Servidores Backend Configurados**

#### Para Balanceo (Máquinas):
- **backend1**: Servidor dedicado para balanceo de máquinas
- **backend2**: Servidor dedicado para balanceo de máquinas  
- **backend3**: Servidor dedicado para balanceo de máquinas

#### Para Resto de Funcionalidades:
- **backend**: Servidor principal para login, registro, mantenimiento, etc.

### 5. **Configuración Específica por Ruta**

#### Microservicio Máquinas (Balanceado):
- **Upstream**: `maquinas_backend` con 3+ servidores
- **Reintentos**: 3 intentos estándar, 5 para `/agregar`
- **Timeouts**: 3-10s (optimizados para operaciones críticas)
- **Health checks**: `max_fails=3 fail_timeout=30s`

#### Resto de Rutas (Directas):
- **Proxy directo**: `http://backend:8000`
- **Timeouts**: 30s estándar
- **Sin reintentos de balanceo**

### 6. **Ventajas de esta Arquitectura**

#### Especificidad:
- **Solo máquinas usa balanceo**: Donde más se necesita alta concurrencia
- **Resto sin complejidad**: Operaciones simples sin overhead de balanceo
- **Mantenimiento simple**: Solo un backend principal para la mayoría de funciones

#### Rendimiento:
- **Máquinas escalable**: Puede manejar alta carga de operaciones CRUD
- **Operaciones rápidas**: Login/registro sin latencia extra
- **Optimización por caso**: Timeouts diferentes por tipo de operación

### 7. **Escalabilidad**

#### Para agregar más servidores de máquinas:
1. Editar `nginx.conf` en sección `upstream maquinas_backend`
2. Agregar nuevos servicios `backend4`, `backend5`, etc. en docker-compose.yml
3. Las demás rutas no se ven afectadas

#### Ejemplo para 5 servidores de máquinas:
```nginx
upstream maquinas_backend {
    server backend1:8000 weight=1 max_fails=3 fail_timeout=30s;
    server backend2:8000 weight=1 max_fails=3 fail_timeout=30s;
    server backend3:8000 weight=1 max_fails=3 fail_timeout=30s;
    server backend4:8000 weight=1 max_fails=3 fail_timeout=30s;
    server backend5:8000 weight=1 max_fails=3 fail_timeout=30s;
}
```

### 8. **Uso y Comandos**

#### Iniciar arquitectura completa:
```bash
# Con balanceo para máquinas
docker-compose --profile multi-server up --build

# Sin balanceo (desarrollo)
docker-compose --profile single-server up --build
```

#### Verificar funcionamiento:
```bash
# Microservicio máquinas (balanceado)
curl -X POST http://localhost/api/maquinas/agregar \
  -H "Content-Type: application/json" \
  -d '{"codigo_equipo":"TEST","tipo_equipo":"test","estado_actual":"activo","area":"test","fecha":"2024-01-01"}'

# Otras rutas (directas)
curl http://localhost/api/login
curl http://localhost/api/mantenimiento/listar
```

#### Probar balanceo específico:
```bash
# Múltiples requests para ver distribución en máquinas
for i in {1..10}; do
  curl -X POST http://localhost/api/maquinas/agregar \
    -H "Content-Type: application/json" \
    -d '{"codigo_equipo":"TEST'$i'","tipo_equipo":"test","estado_actual":"activo","area":"test","fecha":"2024-01-01"}'
  sleep 0.1
done
```

### 9. **Monitoreo**
- **Puerto 80**: Balanceador principal
- **Puerto 8080**: Monitoreo de estado nginx
- **Health check**: `curl http://localhost/health`

### 10. **Resumen de Flujo**

```
Cliente → Nginx → [MÁQUINAS] backend1/backend2/backend3 (balanceado)
         → Nginx → [LOGIN] backend (directo)
         → Nginx → [MANTENIMIENTO] backend (directo)
         → Nginx → [FRONTEND] frontend (directo)
```

Esta arquitectura proporciona balanceo de carga **selectivo** donde más se necesita (máquinas) manteniendo la simplicidad para el resto de funcionalidades.
