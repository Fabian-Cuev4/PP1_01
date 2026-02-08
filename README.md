# SIGLAB - Sistema de Gestión de Laboratorios con Arquitectura de Alta Disponibilidad

Sistema web completo para gestionar máquinas (computadoras e impresoras) y sus mantenimientos en laboratorios, implementado con **alta disponibilidad**, **caché Redis** y **actualizaciones en tiempo real** mediante polling.

## 📋 Resumen del Sistema

Este sistema SIGLAB proporciona:
- **Gestión completa de máquinas**: Registro, actualización, eliminación de equipos
- **Historial de mantenimientos**: Consulta detallada de todos los mantenimientos
- **Alta disponibilidad**: Load balancer con múltiples servidores API
- **Caché inteligente**: Redis para optimizar rendimiento
- **Actualizaciones en tiempo real**: Polling automático cada 2 segundos
- **Monitoreo visual**: Dashboard de métricas en vivo

---

## 🏗️ Arquitectura Implementada

### Componentes de la Infraestructura

- **1 Nginx Load Balancer** (Puerto 8080) - Punto único de entrada
- **2 Servidores API Backend** (FastAPI + Python) - Balanceo de carga
- **1 Base de Datos MySQL** (Máquinas y Usuarios) - Archivador central
- **1 Base de Datos MongoDB** (Mantenimientos) - Archivador central
- **1 Redis Cache** (Caché y Polling en tiempo real)
- **1 Frontend** (HTML + CSS + JavaScript)
- **Dashboard VTS** (Puerto 8084) - Monitoreo visual en tiempo real

### Arquitectura de Cache y Polling

#### Gerente de Datos (DatabaseManager)
- `get_mysql_connection()` para los DAOs
- `get_redis()` para los Services
- `limpiar_cache_sistema()` que borra `cache:dashboard` y `cache:lista_maquinas`

#### Capa DAO (Datos)
- Solo usa el Gerente para pedir conexiones SQL
- No sabe que existe Redis

#### Capa Service (Cerebro)
- **Lectura**: Antes de ir al DAO, pide el cliente Redis al Gerente
- **Cache Hit**: Si hay datos en caché, devuelve los datos al Front
- **Cache Miss**: Si no hay, va al DAO y guarda en Redis
- **Escritura**: Invalida caché con `DatabaseManager.limpiar_cache_sistema()`
- **Failover**: Si Redis no está disponible, va directamente al DAO

#### Capa Router (Entrada)
- Recibe peticiones de Polling del Front-end
- Endpoints específicos para actualizaciones en tiempo real

---

## 🌐 Puertos de Acceso

### APLICACIÓN PRINCIPAL (Frontend + Load Balancer)
```
http://localhost:8080
```
- Punto de entrada único para todos los usuarios
- Load Balancer automático entre APIs
- Sticky Sessions activadas

### DASHBOARD DE MONITOREO VTS
```
http://localhost:8084/dashboard
```
- Métricas en tiempo real
- Tráfico en PORCENTAJES (%)
- Estados UP/DOWN con colores

### SERVIDORES API (Acceso Directo)
```
API Servidor 1: http://localhost:18001
API Servidor 2: http://localhost:18002
```
- Para pruebas individuales
- Logs de identificación
- Conexión a bases de datos compartidas

### BASES DE DATOS (Acceso Directo)
```
MySQL: localhost:13306
MongoDB: localhost:27018
Redis: localhost:6379
```
- Archivador central compartido
- Persistencia de datos
- Acceso para administración

---

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Docker Desktop instalado
- Docker Compose disponible

### Paso 1: Iniciar el Sistema Completo
```bash
# Clonar o navegar al proyecto
cd PP1_01

# Iniciar todos los servicios con Redis
docker-compose up -d --build

# Verificar que todos los servicios estén saludables
docker-compose ps
```

**ESPERADO VER:**
- `mysql_siglab` (Base de datos central)
- `mongo_siglab` (Base de datos central)  
- `redis_siglab` (Cache y polling)
- `api_back_1` (Servidor API 1)
- `api_back_2` (Servidor API 2)
- `nginx_balancer_siglab` (Load Balancer + Frontend)

### Paso 2: Verificar Conexiones
```bash
# Verificar Redis
docker exec redis_siglab redis-cli ping
# Debe responder: PONG

# Verificar MySQL
docker exec mysql_siglab mysqladmin ping -h localhost -u root -pClubpengui1

# Verificar MongoDB
docker exec mongo_siglab mongosh --eval "db.adminCommand('ping')"
```

### Paso 3: Acceder al Sistema
- **Frontend Principal**: http://localhost:8080
- **Dashboard de Monitoreo**: http://localhost:8084/dashboard
- **API Servidor 1**: http://localhost:18001
- **API Servidor 2**: http://localhost:18002

### Paso 4: Iniciar Sesión
```bash
Usuario: admin
Contraseña: admin123
```

---

## 🔄 Flujo de Datos en Tiempo Real

### Escenario 1: Lectura con Polling
```
Frontend → Router → Service → Redis → DAO → MySQL
```

1. **Frontend** hace polling cada 2 segundos a `/api/maquinas/polling/dashboard`
2. **Service** pide cliente Redis al `DatabaseManager`
3. **Cache Hit**: Si los datos están en caché, los devuelve inmediatamente
4. **Cache Miss**: Va al DAO → MySQL → guarda en Redis → devuelve datos

### Escenario 2: Escritura con Invalidación
```
Frontend → Router → Service → DAO → MySQL → [Invalidación de Caché]
```

1. **Frontend** registra/actualiza una máquina
2. **Service** guarda en MySQL a través del DAO
3. **Service** llama a `DatabaseManager.limpiar_cache_sistema()`
4. **Redis** borra las claves `cache:dashboard` y `cache:lista_maquinas`
5. **Próximo polling** será Cache Miss → datos frescos desde MySQL

---

## 📊 Endpoints Disponibles

### Endpoints Principales (CRUD)
```bash
# Autenticación
POST /api/login
POST /api/register

# Máquinas
GET /api/maquinas/listar
POST /api/maquinas/agregar
PUT /api/maquinas/actualizar/{codigo}
DELETE /api/maquinas/eliminar/{codigo}

# Mantenimientos
GET /api/mantenimiento/listar/{codigo_maquina}
POST /api/mantenimiento/agregar
GET /api/mantenimiento/informe/{codigo_maquina}
```

### Endpoints de Polling (Tiempo Real)
```bash
# Máquinas
GET /api/maquinas/polling/dashboard     # Dashboard principal con estadísticas
GET /api/maquinas/polling/lista        # Lista actualizada de máquinas
GET /api/maquinas/polling/buscar/{termino}  # Búsqueda en tiempo real
GET /api/maquinas/cache/status         # Estado del sistema de caché

# Mantenimientos
GET /api/mantenimiento/polling/historial/{codigo_maquina}  # Historial específico
GET /api/mantenimiento/polling/informe                  # Informe completo
GET /api/mantenimiento/polling/todos                     # Todos los mantenimientos
```

---

## ⏱️ Tiempo de Vida del Cache (TTL)

| Cache Key | Tiempo de Vida | Propósito |
|-----------|----------------|-----------|
| `cache:dashboard` | 5 minutos | Dashboard principal |
| `cache:lista_maquinas` | 5 minutos | Lista de máquinas |
| `maquina:{codigo}` | 5 minutos | Máquina individual |
| `historial:{codigo}` | 4 minutos | Historial de mantenimientos |
| `busqueda:codigo:{termino}` | 3 minutos | Resultados de búsqueda |
| `informe:{codigo}` | 3 minutos | Informes completos |

---

## 🔧 Configuración de Redis

### Variables de Entorno
```bash
REDIS_HOST=redis          # Nombre del servicio Docker
REDIS_PORT=6379           # Puerto estándar de Redis
REDIS_DB=0                # Base de datos Redis
```

### Configuración en Docker
- **Memoria Máxima**: 256MB
- **Política de Evicción**: `allkeys-lru` (elimina las claves menos usadas)
- **Persistencia**: `appendonly yes` (guarda datos en disco)

---

## 🚨 Failover y Tolerancia a Fallos

### Si Redis no está disponible:
- **Services** detectan `redis_cliente is None`
- **Van directamente al DAO** sin detener la aplicación
- **Log informativo**: "Redis no disponible, yendo directamente a DAO"
- **La aplicación sigue funcionando** sin caché

### Si MySQL no está disponible:
- **DAOs** retornan `None` o listas vacías
- **Services** manejan errores gracefully
- **Routers** devuelven respuestas de error apropiadas

### Escenario de Caída de Servidor API

#### Simular Caída
```bash
# Matar el servidor API 1 para simular una caída
docker stop api_back_1

# Verificar que el servidor está caído
docker ps
```

#### Comportamiento Esperado
1. **En el Dashboard VTS** (http://localhost:8084/dashboard):
   - `api_back_1` cambia a estado **DOWN** (color rojo)
   - `api_back_2` muestra **100%** del tráfico
   - Los porcentajes se actualizan en tiempo real

2. **En la Aplicación** (http://localhost:8080):
   - La aplicación sigue funcionando normalmente
   - Todas las peticiones van automáticamente a `api_back_2`
   - Los usuarios no notan la caída

#### Recuperación Automática
```bash
# Levantar nuevamente el servidor caído
docker start api_back_1

# Observar el dashboard VTS
# El servidor volverá a estado UP y comenzará a recibir tráfico
```

---

## 📱 Frontend con Polling Automático

### Implementación JavaScript
El frontend incluye polling automático cada 2 segundos:

```javascript
// Polling automático implementado en mantenimiento.js
setInterval(async () => {
    await cargarMaquinasPolling();
}, 2000); // Cada 2 segundos
```

### Indicadores Visuales
- **Indicador verde**: "Actualizando automáticamente"
- **Indicador azul**: "Actualizado: HH:MM:SS"
- **Mensaje de error**: Si hay problemas de conexión

---

## 🎮 Ejemplos de Uso

### 1. Registrar una Máquina
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

### 2. Ver Dashboard en Tiempo Real
```bash
curl http://localhost:8080/api/maquinas/polling/dashboard
```

### 3. Buscar Máquinas
```bash
curl http://localhost:8080/api/maquinas/polling/buscar/PC
```

### 4. Agregar Mantenimiento
```bash
curl -X POST http://localhost:8080/api/mantenimiento/agregar \
  -H "Content-Type: application/json" \
  -d '{
    "codigo_maquina": "PC-001",
    "tipo": "Correctivo",
    "tecnico": "Juan Pérez",
    "empresa": "Tech Solutions",
    "observaciones": "Reparación de fuente de poder",
    "fecha": "2026-02-06",
    "usuario": "admin"
  }'
```

---

## 🔍 Monitoreo y Debugging

### Ver Logs de Redis
```bash
docker logs redis_siglab -f
```

### Ver Estado del Cache
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

### Ver Logs de las APIs
```bash
# API Servidor 1
docker logs api_back_1 -f

# API Servidor 2
docker logs api_back_2 -f

# Todos los servicios
docker-compose logs -f
```

### Ver Estado General del Sistema
```bash
docker-compose ps

# Ver métricas del Load Balancer
curl http://localhost:8084/status | jq

# Probar balanceo de carga
for i in {1..10}; do curl -s http://localhost:8080/api/maquinas | head -c 50; echo ""; done

# Simular estrés
ab -n 100 -c 10 http://localhost:8080/api/maquinas
```

---

## 🏆 Beneficios de la Arquitectura

### Performance
- **Cache Redis**: Reduce carga en MySQL hasta 90%
- **Polling eficiente**: Datos frescos sin recargar página
- **Respuesta rápida**: Cache Hit en milisegundos

### Disponibilidad
- **Load Balancer**: Distribuye carga entre 2 APIs
- **Failover automático**: Si Redis falla, sigue funcionando
- **Health checks**: Monitoreo constante de servicios

### Escalabilidad
- **Sticky Sessions**: Mantiene consistencia de usuario
- **Modular**: Fácil agregar más instancias API
- **Docker**: Despliegue simplificado

---

## 🛠️ Estructura del Proyecto

```
PP1_01/
├── backend/                    # Código del servidor (Python)
│   ├── app/
│   │   ├── daos/            # Acceso a las bases de datos
│   │   │   ├── maquina_dao.py
│   │   │   ├── mantenimiento_dao.py
│   │   │   └── usuario_dao.py
│   │   ├── database/        # Configuración de MySQL, MongoDB y Redis
│   │   │   ├── mysql.py
│   │   │   ├── mongodb.py
│   │   │   ├── redis.py
│   │   │   └── database_manager.py
│   │   ├── models/          # Modelos de datos (Pydantic)
│   │   │   ├── maquina.py
│   │   │   ├── mantenimiento.py
│   │   │   └── usuario.py
│   │   ├── routes/          # Rutas de la API (endpoints)
│   │   │   ├── auth.py
│   │   │   ├── maquina.py
│   │   │   ├── mantenimiento.py
│   │   │   └── usuarios.py
│   │   ├── services/        # Lógica de negocio
│   │   │   ├── maquina_service.py
│   │   │   ├── mantenimiento_service.py
│   │   │   └── usuario_service.py
│   │   └── utils/           # Utilidades varias
│   │       └── encryption.py
│   ├── main.py              # Archivo principal que inicia el servidor
│   ├── requirements.txt     # Dependencias Python
│   └── Dockerfile          # Configuración Docker
│
├── frontend/                # Código de la interfaz (HTML, CSS, JS)
│   ├── static/
│   │   ├── css/            # Estilos CSS
│   │   ├── javascript/     # Lógica JavaScript
│   │   └── img/           # Imágenes e iconos
│   ├── templates/          # Páginas HTML
│   │   ├── index_session.html
│   │   ├── index_dashboard.html
│   │   ├── index_formulario1.html
│   │   ├── index_actualizar.html
│   │   ├── index_ventana1.html
│   │   ├── index_ventana2.html
│   │   ├── index_historial.html
│   │   └── index_register.html
│   ├── nginx.conf         # Configuración del servidor web
│   └── Dockerfile         # Configuración Docker
│
├── docker-compose.yml      # Configuración de todos los servicios
├── README.md              # Este archivo
└── test_usuarios.html      # Página de pruebas
```

---

## 🔧 Patrones de Diseño Implementados

### 1. Factory Pattern
- **Ubicación**: `backend/app/models/factory.py`
- **Propósito**: Crear objetos de tipo máquina (Computadora o Impresora)
- **Uso**: `MaquinaFactory.crear_maquina(tipo_equipo, datos)`

### 2. DAO Pattern (Data Access Object)
- **Ubicación**: `backend/app/daos/`
- **Propósito**: Separar la lógica de acceso a datos
- **Componentes**: `MaquinaDAO`, `MantenimientoDAO`, `UsuarioDAO`

### 3. Service Layer Pattern
- **Ubicación**: `backend/app/services/`
- **Propósito**: Encapsular la lógica de negocio
- **Componentes**: `MaquinaService`, `MantenimientoService`, `UsuarioService`

### 4. Singleton Pattern (DatabaseManager)
- **Ubicación**: `backend/app/database/database_manager.py`
- **Propósito**: Gestionar conexiones centralizadas
- **Uso**: `DatabaseManager.get_mysql_connection()`, `DatabaseManager.get_redis()`

### 5. Repository Pattern (implícito)
- **Propósito**: Abstracción sobre el almacenamiento de datos
- **Implementación**: Los DAOs actúan como repositorios

---

## 🌐 Flujo Completo de una Petición

### Escenario: Registro de Nueva Máquina

1. **Frontend (JavaScript)**
   ```javascript
   fetch('/api/maquinas/agregar', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify(datosMaquina)
   })
   ```

2. **Nginx (Load Balancer)**
   - Recibe la petición en el puerto 8080
   - Reenvía a uno de los servidores API (balanceo de carga)
   - Mantiene sticky session si el usuario ya existe

3. **FastAPI (Router)**
   ```python
   @router.post("/agregar")
   async def agregar_maquina(maquina: MaquinaCreate):
       return maquina_service.crear_maquina(maquina)
   ```

4. **Service Layer**
   ```python
   def crear_maquina(self, maquina_data):
       # Validaciones de negocio
       if self.existe_codigo(maquina_data.codigo_equipo):
           raise ValueError("Código ya existe")
       
       # Usar Factory para crear objeto
       maquina = MaquinaFactory.crear_maquina(...)
       
       # Guardar mediante DAO
       resultado = maquina_dao.crear(maquina)
       
       # Invalidar caché
       DatabaseManager.limpiar_cache_sistema()
       
       return resultado
   ```

5. **DAO Layer**
   ```python
   def crear(self, maquina):
       connection = DatabaseManager.get_mysql_connection()
       cursor = connection.cursor()
       # Ejecutar INSERT SQL
       connection.commit()
       return maquina
   ```

6. **DatabaseManager**
   - Proporciona conexión MySQL desde el pool
   - Maneja reintentos y errores de conexión
   - Centraliza la configuración

7. **Respuesta**
   - DAO → Service → Router → Nginx → Frontend
   - Frontend actualiza la interfaz
   - Próximo polling refrescará los datos automáticamente

---

## 🚨 Solución de Problemas Comunes

### Problema: "No hay equipos registrados"
```bash
# Verificar que Redis esté funcionando
docker exec redis_siglab redis-cli ping

# Verificar que las APIs estén saludables
curl http://localhost:18001/api/health
curl http://localhost:18002/api/health

# Limpiar cache si es necesario
docker exec redis_siglab redis-cli FLUSHALL
```

### Problema: Los datos no se actualizan
```bash
# Verificar logs de las APIs
docker logs api_back_1 | grep "Cache"
docker logs api_back_2 | grep "Cache"

# Forzar invalidación de cache
curl http://localhost:8080/api/maquinas/cache/status
```

### Problema: Redis consume mucha memoria
```bash
# Ver uso de memoria
docker exec redis_siglab redis-cli INFO memory

# Limpiar cache si es necesario
docker exec redis_siglab redis-cli FLUSHALL
```

### Problema: Load Balancer no distribuye correctamente
```bash
# Ver configuración de Nginx
docker exec nginx_balancer_siglab nginx -t

# Reiniciar Nginx
docker restart nginx_balancer_siglab

# Ver logs del balanceador
docker logs nginx_balancer_siglab -f
```

---

## 📋 Comandos Útiles

### Gestión de Servicios
```bash
# Iniciar todos los servicios
docker-compose up -d --build

# Ver estado de los servicios
docker-compose ps

# Ver logs de todos los servicios
docker-compose logs -f

# Detener todos los servicios
docker-compose stop

# Eliminar todos los servicios y volúmenes
docker-compose down -v

# Reconstruir imágenes
docker-compose build --no-cache
```

### Gestión Individual de Contenedores
```bash
# Ver logs específicos
docker logs api_back_1 -f
docker logs api_back_2 -f
docker logs redis_siglab -f
docker logs mysql_siglab -f
docker logs mongo_siglab -f
docker logs nginx_balancer_siglab -f

# Acceder a contenedor
docker exec -it api_back_1 bash
docker exec -it redis_siglab redis-cli
docker exec -it mysql_siglab mysql -u root -pClubpengui1
```

### Monitoreo y Pruebas
```bash
# Probar endpoints directamente
curl http://localhost:8080/api/maquinas/listar
curl -X POST http://localhost:8080/api/login -H "Content-Type: application/json" -d '{"username":"admin","password":"admin123"}'

# Pruebas de carga
ab -n 100 -c 10 http://localhost:8080/api/maquinas

# Ver estado del sistema
curl http://localhost:8084/status | jq
```

---

## 🔐 Seguridad Considerada

### Autenticación
- **Encriptación de contraseñas**: bcrypt
- **Sesiones persistentes**: Sticky sessions
- **Tokens de sesión**: Gestión centralizada

### Base de Datos
- **MySQL**: Contraseña segura en variables de entorno
- **MongoDB**: Autenticación habilitada
- **Redis**: Sin exposición externa en producción

### Red
- **Nginx**: Reverse proxy oculta servidores backend
- **Docker**: Aislamiento de contenedores
- **Ports**: Solo exposición necesaria

---

## 📈 Métricas y Monitoreo

### Dashboard VTS (http://localhost:8084/dashboard)
- **Tráfico en porcentajes**: Distribución entre APIs
- **Estados UP/DOWN**: Salud de servidores
- **Tiempo real**: Actualizaciones automáticas

### Logs Estructurados
- **Identificación de servidor**: Cada petición logged
- **Eventos de sistema**: Inicio, caída, recuperación
- **Errores y warnings**: Trazabilidad completa

### Métricas de Rendimiento
- **Cache Hit Rate**: Eficiencia de Redis
- **Response Time**: Tiempos de respuesta
- **Throughput**: Peticiones por segundo

---

## 🎯 CONCLUSIÓN FINAL

Sistema SIGLAB implementado con arquitectura distribuida, load balancer y cache Redis. Dashboard optimizado mostrando estadísticas de máquinas con tipo pero sin área, polling en tiempo real (1s dashboard, 2s otros), y gestión completa de mantenimientos.

**Estado actual:**
- ✅ Load balancer funcional con 3 servidores
- ✅ Dashboard con estadísticas en tiempo real  
- ✅ Sistema de caché Redis sincronizado
- ✅ Código limpio y consistente sin inconsistencias

**Tecnologías clave:**
- FastAPI + MySQL + MongoDB + Redis
- JavaScript vanilla con polling
- Docker Compose para orquestación
- Arquitectura sin estado para escalabilidad

---

**🎉 SISTEMA COMPLETO Y FUNCIONAL 🎉**

*Última actualización: Febrero 2026*
*Versión: 2.0 - Arquitectura Distribuida*
