# ARQUITECTURA GENERAL - SIGLAB

## 🏗️ DIAGRAMA DE FLUJO GENERAL

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Browser)                        │
├─────────────────────────────────────────────────────────────────┤
│  HTML Templates                                                  │
│  ├── index_dashboard.html    → Monitoreo de servidores         │
│  ├── index_formulario1.html  → Registro de máquinas            │
│  ├── index_historial.html    → Historial de mantenimientos     │
│  └── index_ventana*.html     → Interfaces varias               │
│                                                                 │
│  JavaScript (Capa de Presentación)                             │
│  ├── dashboard.js       → Health check + polling dashboard      │
│  ├── mantenimiento.js  → Gestión de máquinas (polling)         │
│  ├── formulario.js      → Formularios de CRUD                   │
│  ├── historial.js       → Historial con polling                 │
│  ├── reporte.js         → Reportes dinámicos                    │
│  ├── session.js         → Gestión de sesión                    │
│  └── (traffic_ping.js)  → ❌ Desactivado                       │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ HTTP Requests
                                    │
┌─────────────────────────────────────────────────────────────────┐
│                    LOAD BALANCER (Nginx)                        │
│  Distribuye peticiones a 3 servidores API                      │
│  ┌─────────┬─────────┬─────────┐                               │
│  │ API 1   │ API 2   │ API 3   │                               │
│  │ :8081   │ :8082   │ :8083   │                               │
│  └─────────┴─────────┴─────────┘                               │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                                    │
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                           │
├─────────────────────────────────────────────────────────────────┤
│  📁 MAIN.PY (Orquestador)                                       │
│  ├── Inicializa DatabaseManager                                 │
│  ├── Registra 3 routers principales                            │
│  │   ├── /api/maquinas/*     → maquina.py                      │
│  │   ├── /api/mantenimiento/* → mantenimiento.py               │
│  │   └── /api/login, /api/register → auth.py                   │
│  └── /api/health → Health check de servidor                    │
│                                                                 │
│  📁 ROUTES (Capa de Entrada)                                    │
│  ├── auth.py          → Login/Registro                          │
│  ├── maquina.py       → CRUD máquinas + polling endpoints       │
│  └── mantenimiento.py → CRUD mantenimientos + polling           │
│                                                                 │
│  📁 SERVICES (Capa de Negocio)                                 │
│  ├── usuario_service.py → Validación + encriptación           │
│  ├── maquina_service.py → Lógica de caché + validación          │
│  └── mantenimiento_service.py → Lógica de mantenimientos       │
│                                                                 │
│  📁 REPOSITORY (Contenedor de DAOs)                            │
│  └── proyecto_repository.py → Instancia global de DAOs         │
│                                                                 │
│  📁 DAOS (Capa de Datos)                                        │
│  ├── usuario_dao.py     → SQL puro usuarios                    │
│  ├── maquina_dao.py     → SQL puro máquinas                     │
│  └── mantenimiento_dao.py → SQL puro mantenimientos             │
│                                                                 │
│  📁 DATABASE_MANAGER (Gerente de Conexiones)                   │
│  ├── mysql.py      → Conexión MySQL (persistencia)             │
│  ├── mongodb.py     → Conexión MongoDB (logs)                   │
│  ├── redis.py       → Conexión Redis (caché distribuida)       │
│  └── database_manager.py → Centraliza todas las conexiones     │
│                                                                 │
│  📁 MODELS (Entidades)                                           │
│  ├── Computadora.py → Hereda de Maquina                         │
│  ├── Impresora.py  → Hereda de Maquina                         │
│  └── Mantenimiento.py → Modelo de mantenimiento                │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                                    │
┌─────────────────────────────────────────────────────────────────┐
│                    INFRAESTURA DE DATOS                          │
├─────────────────────────────────────────────────────────────────┤
│  🗄️  MYSQL (Base de Datos Principal)                            │
│  ├── Tabla: usuarios          → Autenticación                   │
│  ├── Tabla: maquinas          → Inventario de equipos           │
│  └── Tabla: mantenimientos    → Historial de mantenimientos     │
│                                                                 │
│  🍃 MONGODB (Logs y Auditoría)                                   │
│  └── Colección: logs          → Registro de eventos             │
│                                                                 │
│  ⚡ REDIS (Caché Distribuida)                                    │
│  ├── cache:dashboard       → Datos dashboard (TTL: 60s)        │
│  ├── cache:lista_maquinas  → Lista máquinas (TTL: 60s)         │
│  ├── informe:*             → Caché reportes                    │
│  ├── mantenimiento:*       → Caché mantenimientos              │
│  └── historial:*           → Caché historial                   │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 FLUJOS PRINCIPALES DE FUNCIONALIDADES

### 1. 🏠 MONITOREO DE SERVIDORES (Dashboard)
```
Browser → dashboard.js
    ↓
1. Verificar estado de servidores (health check):
   ├── /api1/api/health → Servidor 1
   ├── /api2/api/health → Servidor 2  
   └── /api3/api/health → Servidor 3
    ↓
2. Obtener datos de máquinas:
   → /api/maquinas/polling/dashboard
    ↓
3. Service busca caché Redis:
   ├── cache:dashboard ✓ → Devuelve datos
   └── cache:dashboard ✗ → Va a MySQL
       ↓
   DAO ejecuta: SELECT * FROM maquinas
       ↓
   Service guarda en Redis (TTL: 60s)
    ↓
4. UI actualiza:
   ├── Estado UP/DOWN de servidores
   ├── Estadísticas de máquinas
   └── Medidor de disponibilidad
```

### 2. 🔐 AUTENTICACIÓN (Login/Registro)
```
Browser → session.js + register.js
    ↓
POST /api/login o /api/register
    ↓
auth.py → usuario_service.py
    ↓
Service valida datos:
├── Login: Verifica usuario + contraseña
└── Registro: Encripta contraseña (bcrypt)
    ↓
usuario_dao.py → MySQL:
├── SELECT * FROM usuarios WHERE username=?
└── INSERT INTO usuarios VALUES (?,?,?)
    ↓
Respuesta:
├── ✅ {status: "ok", token: "..."}
└── ❌ {error: "Credenciales inválidas"}
```

### 3. 🖥️ GESTIÓN DE MÁQUINAS (CRUD + Polling)
```
Browser → mantenimiento.js (polling cada 2s)
    ↓
📝 CREAR MÁQUINA:
POST /api/maquinas/agregar
    ↓
maquina.py → maquina_service.py
    ↓
Service valida:
├── Código único
├── Tipo válido (PC/IMP)
└── Datos completos
    ↓
maquina_dao.py → MySQL:
INSERT INTO maquinas VALUES (?,?,?,?,?,?)
    ↓
Service limpia caché:
DatabaseManager.limpiar_cache_sistema()
    ↓
✅ {mensaje: "Máquina registrada"}

📋 LISTAR MÁQUINAS (con polling):
GET /api/maquinas/listar?polling=true
    ↓
Service busca caché Redis:
├── cache:lista_maquinas ✓ → Devuelve datos
└── cache:lista_maquinas ✗ → Va a MySQL
    ↓
DAO ejecuta: SELECT * FROM maquinas
    ↓
Service guarda en Redis (TTL: 60s)
    ↓
UI actualiza tabla en tiempo real
```

### 4. 🔧 MANTENIMIENTOS (Historial + Reportes)
```
Browser → historial.js + reporte.js
    ↓
📝 REGISTRAR MANTENIMIENTO:
POST /api/mantenimiento/registrar
    ↓
mantenimiento.py → mantenimiento_service.py
    ↓
Service valida y asocia a máquina
    ↓
mantenimiento_dao.py → MySQL:
INSERT INTO mantenimientos VALUES (?,?,?,?,?,?,?)
    ↓
Service limpia caché relacionada
    ↓
✅ {mensaje: "Mantenimiento registrado"}

📊 GENERAR REPORTE:
GET /api/mantenimiento/informe-general?polling=true
    ↓
Service busca caché: informe:general
├── ✓ → Devuelve datos cacheados
└── ✗ → Ejecuta query compleja en MySQL
    ↓
UI muestra tabla con filtros y exportación
```

### 5. ⚡ SISTEMA DE CACHÉ DISTRIBUIDA
```
ESCRITURA (Cualquier operación):
├── Service llama a DAO
├── DAO ejecuta SQL en MySQL
└── Service limpia TODA la caché:
    DatabaseManager.limpiar_cache_sistema()
    ├── cache:dashboard
    ├── cache:lista_maquinas
    ├── informe:*
    ├── mantenimiento:*
    └── historial:*

LECTURA (Polling y consultas):
├── Service pide Redis a DatabaseManager
├── Busca clave específica en caché
├── ✓ Cache Hit → Devuelve inmediato
└── ✗ Cache Miss → Va a MySQL
    ├── DAO ejecuta query
    ├── Service guarda resultado en Redis
    └── Devuelve datos
```

## 🎯 FUNCIONALIDADES PRINCIPALES POR CAPA

### FRONTEND (Capa de Presentación)
- **Dashboard**: Monitoreo en tiempo real de 3 servidores API
- **Formularios**: CRUD de máquinas y mantenimientos
- **Polling**: Actualización automática cada 1-2 segundos
- **Sesión**: Gestión de login/logout
- **Reportes**: Consultas dinámicas con exportación

### BACKEND (Capa de Negocio)
- **Routes**: Endpoints RESTful + polling endpoints
- **Services**: Validación, lógica de caché, coordinación
- **DAOs**: Acceso puro a SQL sin lógica de negocio
- **DatabaseManager**: Centralización de conexiones
- **Repository**: Contenedor global de DAOs

### INFRAESTURA
- **Load Balancer**: Distribución de carga entre 3 APIs
- **MySQL**: Persistencia de datos principal
- **MongoDB**: Logs y auditoría del sistema
- **Redis**: Caché distribuida con TTL de 60s
- **Health Checks**: Monitoreo de disponibilidad

## 🔄 CICLO DE VIDA COMPLETO

1. **Inicio**: 3 servidores API + Load Balancer
2. **Login**: Usuario se autentica → MySQL
3. **Dashboard**: Monitorea salud de servidores + datos en tiempo real
4. **Operaciones**: CRUD de máquinas/mantenimientos → MySQL + caché
5. **Polling**: Frontend actualiza cada 1-2s → Redis/MySQL
6. **Reportes**: Consultas dinámicas con caché inteligente
7. **Logs**: Todas las operaciones se registran en MongoDB

**Arquitectura escalable con alta disponibilidad, caché distribuida y monitoreo en tiempo real.**
