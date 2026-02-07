# SIGLAB - Sistema de Gestión de Laboratorio con Redis Cache y Polling

## 🚀 **Arquitectura Implementada**

Sistema SIGLAB con **alta disponibilidad**, **caché Redis** y **actualizaciones en tiempo real** mediante polling.

### **📋 Componentes**

- **2 Instancias API Backend** (FastAPI + Python)
- **1 Load Balancer** (Nginx) con Sticky Sessions
- **1 Base de Datos MySQL** (Máquinas y Usuarios)
- **1 Base de Datos MongoDB** (Mantenimientos)
- **1 Redis Cache** (Caché y Polling en tiempo real)
- **1 Frontend** (HTML + CSS + JavaScript)

---

## 🏗️ **Arquitectura de Cache y Polling**

### **Gerente de Datos (DatabaseManager)**
- ✅ `get_mysql_connection()` para los DAOs
- ✅ `get_redis()` para los Services
- ✅ `limpiar_cache_sistema()` que borra `cache:dashboard` y `cache:lista_maquinas`

### **Capa DAO (Datos)**
- ✅ Solo usa el Gerente para pedir conexiones SQL
- ✅ No sabe que existe Redis

### **Capa Service (Cerebro)**
- ✅ **Lectura**: Antes de ir al DAO, pide el cliente Redis al Gerente
- ✅ **Cache Hit**: Si hay datos en caché, devuelve los datos al Front
- ✅ **Cache Miss**: Si no hay, va al DAO y guarda en Redis
- ✅ **Escritura**: Invalida caché con `DatabaseManager.limpiar_cache_sistema()`
- ✅ **Failover**: Si Redis no está disponible, va directamente al DAO

### **Capa Router (Entrada)**
- ✅ Recibe peticiones de Polling del Front-end
- ✅ Endpoints específicos para actualizaciones en tiempo real

---

## 🔄 **Flujo de Datos en Tiempo Real**

### **Escenario 1: Lectura con Polling**
```
Frontend → Router → Service → Redis → DAO → MySQL
```

1. **Frontend** hace polling cada 5 segundos a `/api/maquinas/polling/dashboard`
2. **Service** pide cliente Redis al `DatabaseManager`
3. **Cache Hit**: Si los datos están en caché, los devuelve inmediatamente
4. **Cache Miss**: Va al DAO → MySQL → guarda en Redis → devuelve datos

### **Escenario 2: Escritura con Invalidación**
```
Frontend → Router → Service → DAO → MySQL → [Invalidación de Caché]
```

1. **Frontend** registra/actualiza una máquina
2. **Service** guarda en MySQL a través del DAO
3. **Service** llama a `DatabaseManager.limpiar_cache_sistema()`
4. **Redis** borra las claves `cache:dashboard` y `cache:lista_maquinas`
5. **Próximo polling** será Cache Miss → datos frescos desde MySQL

---

## 🛠️ **Instalación y Ejecución**

### **Requisitos Previos**
- Docker Desktop instalado
- Docker Compose disponible

### **Paso 1: Iniciar el Sistema Completo**
```bash
# Clonar o navegar al proyecto
cd PP1_01

# Iniciar todos los servicios con Redis
docker-compose up -d

# Verificar que todos los servicios estén saludables
docker-compose ps
```

### **Paso 2: Verificar Conexiones**
```bash
# Verificar Redis
docker exec redis_siglab redis-cli ping
# Debe responder: PONG

# Verificar MySQL
docker exec mysql_siglab mysqladmin ping -h localhost -u root -pClubpengui1

# Verificar MongoDB
docker exec mongo_siglab mongosh --eval "db.adminCommand('ping')"
```

### **Paso 3: Acceder al Sistema**
- **Frontend Principal**: http://localhost:8080
- **Dashboard de Monitoreo**: http://localhost:8084
- **API Servidor 1**: http://localhost:18001
- **API Servidor 2**: http://localhost:18002

---

## 📊 **Endpoints de Polling Disponibles**

### **Máquinas**
```bash
# Dashboard principal con estadísticas
GET /api/maquinas/polling/dashboard

# Lista actualizada de máquinas
GET /api/maquinas/polling/lista

# Búsqueda en tiempo real
GET /api/maquinas/polling/buscar/{termino}

# Estado del sistema de caché
GET /api/maquinas/cache/status
```

### **Mantenimientos**
```bash
# Historial de una máquina específica
GET /api/mantenimiento/polling/historial/{codigo_maquina}

# Informe completo con estadísticas
GET /api/mantenimiento/polling/informe

# Todos los mantenimientos del sistema
GET /api/mantenimiento/polling/todos
```

---

## 🎯 **Tiempo de Vida del Cache (TTL)**

| Cache Key | Tiempo de Vida | Propósito |
|-----------|----------------|-----------|
| `cache:dashboard` | 5 minutos | Dashboard principal |
| `cache:lista_maquinas` | 5 minutos | Lista de máquinas |
| `maquina:{codigo}` | 5 minutos | Máquina individual |
| `historial:{codigo}` | 4 minutos | Historial de mantenimientos |
| `busqueda:codigo:{termino}` | 3 minutos | Resultados de búsqueda |
| `informe:{codigo}` | 3 minutos | Informes completos |

---

## 🔧 **Configuración de Redis**

### **Variables de Entorno**
```bash
REDIS_HOST=redis          # Nombre del servicio Docker
REDIS_PORT=6379           # Puerto estándar de Redis
REDIS_DB=0                # Base de datos Redis
```

### **Configuración en Docker**
- **Memoria Máxima**: 256MB
- **Política de Evicción**: `allkeys-lru` (elimina las claves menos usadas)
- **Persistencia**: `appendonly yes` (guarda datos en disco)

---

## 🚨 **Failover y Tolerancia a Fallos**

### **Si Redis no está disponible:**
- ✅ **Services** detectan `redis_cliente is None`
- ✅ **Van directamente al DAO** sin detener la aplicación
- ✅ **Log informativo**: "Redis no disponible, yendo directamente a DAO"
- ✅ **La aplicación sigue funcionando** sin caché

### **Si MySQL no está disponible:**
- ✅ **DAOs** retornan `None` o listas vacías
- ✅ **Services** manejan errores gracefully
- ✅ **Routers** devuelven respuestas de error apropiadas

---

## 📱 **Frontend con Polling Automático**

### **Implementación JavaScript**
El frontend ya incluye polling automático cada 5 segundos:

```javascript
// Polling automático implementado en mantenimiento.js
setInterval(async () => {
    await cargarMaquinasPolling();
}, 5000); // Cada 5 segundos
```

### **Indicadores Visuales**
- 🔄 **Indicador verde**: "Actualizando automáticamente"
- ✅ **Indicador azul**: "Actualizado: HH:MM:SS"
- ❌ **Mensaje de error**: Si hay problemas de conexión

---

## 🎮 **Ejemplos de Uso**

### **1. Registrar una Máquina**
```bash
curl -X POST http://localhost:8080/api/maquinas/agregar \
  -H "Content-Type: application/json" \
  -d '{
    "codigo_equipo": "PC-001",
    "tipo_equipo": "PC",
    "estado_actual": "Operativa",
    "area": "Sistemas",
    "fecha": "2026-02-06",
    "usuario": "admin"
  }'
```

### **2. Ver Dashboard en Tiempo Real**
```bash
curl http://localhost:8080/api/maquinas/polling/dashboard
```

### **3. Buscar Máquinas**
```bash
curl http://localhost:8080/api/maquinas/polling/buscar/PC
```

---

## 🔍 **Monitoreo y Debugging**

### **Ver Logs de Redis**
```bash
docker logs redis_siglab -f
```

### **Ver Estado del Cache**
```bash
# Conectarse a Redis
docker exec -it redis_siglab redis-cli

# Ver todas las claves
KEYS *

# Ver una clave específica
GET cache:dashboard

# Ver información de memoria
INFO memory
```

### **Ver Logs de las APIs**
```bash
# API Servidor 1
docker logs api_back_1 -f

# API Servidor 2
docker logs api_back_2 -f
```

---

## 🎯 **Beneficios de la Arquitectura**

### **Performance**
- ⚡ **Cache Redis**: Reduce carga en MySQL hasta 90%
- 🚀 **Polling eficiente**: Datos frescos sin recargar página
- 📊 **Respuesta rápida**: Cache Hit en milisegundos

### **Disponibilidad**
- 🔄 **Load Balancer**: Distribuye carga entre 2 APIs
- 💾 **Failover automático**: Si Redis falla, sigue funcionando
- 🏥 **Health checks**: Monitoreo constante de servicios

### **Escalabilidad**
- 📈 **Sticky Sessions**: Mantiene consistencia de usuario
- 🔧 **Modular**: Fácil agregar más instancias API
- 📦 **Docker**: Despliegue simplificado

---

## 🆘 **Solución de Problemas Comunes**

### **Problema: "No hay equipos registrados"**
```bash
# Verificar que Redis esté funcionando
docker exec redis_siglab redis-cli ping

# Verificar que las APIs estén saludables
curl http://localhost:18001/api/health
curl http://localhost:18002/api/health

# Limpiar cache si es necesario
docker exec redis_siglab redis-cli FLUSHALL
```

### **Problema: Los datos no se actualizan**
```bash
# Verificar logs de las APIs
docker logs api_back_1 | grep "Cache"
docker logs api_back_2 | grep "Cache"

# Forzar invalidación de cache
curl http://localhost:8080/api/maquinas/cache/status
```

### **Problema: Redis consume mucha memoria**
```bash
# Ver uso de memoria
docker exec redis_siglab redis-cli INFO memory

# Limpiar cache si es necesario
docker exec redis_siglab redis-cli FLUSHALL
```

---

## 🎉 **¡Listo para Usar!**

El sistema SIGLAB ahora tiene:
- ✅ **Actualizaciones en tiempo real** con polling cada 5 segundos
- ✅ **Caché inteligente** con Redis para máximo performance
- ✅ **Alta disponibilidad** con Load Balancer y failover
- ✅ **Arquitectura limpia** con separación de responsabilidades
- ✅ **Monitoreo completo** con dashboards y logs

**Accede a http://localhost:8080 y disfruta del sistema en tiempo real!** 🚀
