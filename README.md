# 🏢 SIGLAB - Sistema de Gestión de Inventario y Mantenimiento de Laboratorios

**Sistema web profesional para la gestión integral de equipos de laboratorio y su historial de mantenimiento técnico.**

---

## 📑 Tabla de Contenidos

1. [Descripción del Proyecto](#-descripción-del-proyecto)
2. [Arquitectura del Sistema](#-arquitectura-del-sistema)
3. [Tecnologías y Dependencias](#-tecnologías-y-dependencias)
4. [Estructura del Proyecto](#-estructura-del-proyecto)
5. [Flujo de Datos (Arquitectura de Capas)](#-flujo-de-datos-arquitectura-de-capas)
6. [Contenedores Docker](#-contenedores-docker)
7. [Instalación y Configuración](#-instalación-y-configuración)
8. [Problemas Resueltos](#-problemas-resueltos-durante-el-desarrollo)
9. [Comandos Útiles](#-comandos-útiles)
10. [Acceso a la Aplicación](#-acceso-a-la-aplicación)

---

## 🎯 Descripción del Proyecto

**SIGLAB** es un sistema web completo diseñado para la **Universidad Central del Ecuador (UCE)** que permite:

- ✅ **Gestión de Inventario**: Registro y administración de equipos de laboratorio (PCs, impresoras, etc.)
- ✅ **Historial de Mantenimiento**: Registro detallado de mantenimientos preventivos y correctivos
- ✅ **Reportes Dinámicos**: Generación de informes consolidados con búsqueda avanzada
- ✅ **Autenticación de Usuarios**: Sistema de login y registro seguro
- ✅ **Interfaz Moderna**: Diseño responsive y profesional con experiencia de usuario optimizada

### Características Principales

- 🔍 **Búsqueda Inteligente**: Búsqueda insensible a mayúsculas/minúsculas con filtrado en tiempo real
- 📊 **Reportes Consolidados**: Cruza datos de MySQL (equipos) con MongoDB (mantenimientos)
- 🎨 **Interfaz Premium**: Diseño moderno con animaciones suaves y colores profesionales
- 🐳 **Totalmente Dockerizado**: Fácil despliegue en cualquier sistema operativo
- 🔄 **Arquitectura de Capas**: Separación clara entre presentación, lógica de negocio y acceso a datos

---

## 🏗️ Arquitectura del Sistema

El sistema utiliza una **arquitectura de 3 capas** con **bases de datos híbridas** (relacional + NoSQL):

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                      │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Frontend (Nginx + HTML/CSS/JavaScript)            │     │
│  │  - Interfaz de usuario responsive                  │     │
│  │  - Validación de formularios                       │     │
│  │  - Comunicación con API REST                       │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/REST
┌─────────────────────────────────────────────────────────────┐
│                   CAPA DE LÓGICA DE NEGOCIO                  │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Backend (FastAPI + Python)                        │     │
│  │  ┌──────────────┐  ┌──────────────┐               │     │
│  │  │   Routes     │  │   Services   │               │     │
│  │  │  (API REST)  │→ │  (Business   │               │     │
│  │  │              │  │   Logic)     │               │     │
│  │  └──────────────┘  └──────────────┘               │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↕ SQL/NoSQL
┌─────────────────────────────────────────────────────────────┐
│                   CAPA DE ACCESO A DATOS                     │
│  ┌────────────────────────────────────────────────────┐     │
│  │  DAOs (Data Access Objects)                        │     │
│  │  ┌──────────────┐  ┌──────────────┐               │     │
│  │  │ MaquinaDAO   │  │Mantenimiento │               │     │
│  │  │              │  │    DAO       │               │     │
│  │  └──────────────┘  └──────────────┘               │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                   CAPA DE PERSISTENCIA                       │
│  ┌──────────────────┐         ┌──────────────────┐          │
│  │  MySQL 8.0       │         │  MongoDB Latest  │          │
│  │  (Relacional)    │         │  (NoSQL)         │          │
│  │  - Máquinas      │         │  - Mantenimientos│          │
│  │  - Usuarios      │         │  - Historial     │          │
│  └──────────────────┘         └──────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

### ¿Por qué Bases de Datos Híbridas?

- **MySQL**: Para datos estructurados y relacionales (inventario de equipos, usuarios)
- **MongoDB**: Para datos semi-estructurados y de rápido crecimiento (historial de mantenimientos)

---

## 🛠️ Tecnologías y Dependencias

### Backend (Python)

| Dependencia | Versión | Propósito |
|------------|---------|-----------|
| **FastAPI** | 0.104.1 | Framework web moderno y rápido para construir APIs REST |
| **Uvicorn** | 0.24.0 | Servidor ASGI de alto rendimiento para ejecutar FastAPI |
| **mysql-connector-python** | 8.2.0 | Driver oficial de MySQL para Python |
| **pymongo** | 4.6.0 | Driver oficial de MongoDB para Python |
| **Jinja2** | 3.1.2 | Motor de plantillas para renderizar HTML |
| **python-multipart** | 0.0.6 | Manejo de formularios multipart/form-data |

### Frontend

| Tecnología | Propósito |
|-----------|-----------|
| **HTML5** | Estructura semántica de las páginas |
| **CSS3** | Estilos modernos con animaciones y transiciones |
| **JavaScript (Vanilla)** | Lógica del cliente sin dependencias externas |
| **Font Awesome 6.4.0** | Iconografía profesional |
| **Nginx** | Servidor web de alto rendimiento |

### Bases de Datos

| Base de Datos | Versión | Uso |
|--------------|---------|-----|
| **MySQL** | 8.0 | Almacenamiento de equipos y usuarios |
| **MongoDB** | Latest | Almacenamiento de historial de mantenimientos |

### Infraestructura

| Herramienta | Versión | Propósito |
|------------|---------|-----------|
| **Docker** | 20.10+ | Contenedorización de servicios |
| **Docker Compose** | 2.0+ | Orquestación de contenedores |

---

## 📁 Estructura del Proyecto

```
PP1_01-javier/
│
├── backend/                          # 🐍 Backend FastAPI
│   ├── app/
│   │   ├── daos/                    # Data Access Objects (Capa de Datos)
│   │   │   ├── maquina_dao.py       # Operaciones CRUD para máquinas (MySQL)
│   │   │   ├── mantenimiento_dao.py # Operaciones CRUD para mantenimientos (MongoDB)
│   │   │   └── usuario_dao.py       # Operaciones CRUD para usuarios (MySQL)
│   │   │
│   │   ├── database/                # Configuración de Bases de Datos
│   │   │   ├── mysql.py             # Conexión y configuración de MySQL
│   │   │   └── mongodb.py           # Conexión y configuración de MongoDB
│   │   │
│   │   ├── models/                  # Modelos de Dominio (Patrón Abstract Factory)
│   │   │   ├── abstrac_factory/
│   │   │   │   └── Maquina.py       # Clase abstracta base
│   │   │   ├── Computadora.py       # Modelo concreto de PC
│   │   │   ├── Impresora.py         # Modelo concreto de Impresora
│   │   │   └── Mantenimiento.py     # Modelo de Mantenimiento
│   │   │
│   │   ├── routes/                  # Rutas de la API REST
│   │   │   ├── auth.py              # Endpoints de autenticación (login/register)
│   │   │   ├── maquina.py           # Endpoints de gestión de máquinas
│   │   │   ├── mantenimiento.py     # Endpoints de gestión de mantenimientos
│   │   │   └── views.py             # Rutas para servir plantillas HTML
│   │   │
│   │   ├── dtos/                    # Data Transfer Objects
│   │   │   └── informe_dto.py       # DTO para reportes consolidados
│   │   │
│   │   └── services.py              # Lógica de Negocio (Capa de Servicio)
│   │
│   ├── main.py                      # Punto de entrada de la aplicación
│   ├── requirements.txt             # Dependencias de Python
│   └── Dockerfile                   # Imagen Docker del backend
│
├── frontend/                        # 🎨 Frontend Estático
│   ├── static/
│   │   ├── css/                     # Hojas de estilo
│   │   │   ├── style_session.css    # Estilos de login/registro
│   │   │   ├── style_ventana1.css   # Estilos de página principal
│   │   │   ├── style_ventana2.css   # Estilos de lista de máquinas
│   │   │   ├── style_ventana3.css   # Estilos de reportes
│   │   │   ├── style_formulario1.css # Estilos de formulario de máquinas
│   │   │   ├── style_formulario2.css # Estilos de formulario de mantenimiento
│   │   │   └── style_historial.css  # Estilos de historial
│   │   │
│   │   ├── javascript/              # Scripts del cliente
│   │   │   ├── session.js           # Lógica de login/logout
│   │   │   ├── register.js          # Lógica de registro
│   │   │   ├── ventana.js           # Navegación entre páginas
│   │   │   ├── mantenimiento.js     # Gestión de lista de máquinas
│   │   │   ├── formulario.js        # Validación de formularios
│   │   │   ├── reporte.js           # Generación de reportes
│   │   │   └── historial.js         # Visualización de historial
│   │   │
│   │   └── img/                     # Recursos gráficos
│   │
│   ├── templates/                   # Plantillas HTML
│   │   ├── index_session.html       # Página de login
│   │   ├── index_register.html      # Página de registro
│   │   ├── index_ventana1.html      # Página principal (dashboard)
│   │   ├── index_ventana2.html      # Lista de máquinas
│   │   ├── index_ventana3.html      # Página de reportes
│   │   ├── index_formulario1.html   # Formulario de nueva máquina
│   │   ├── index_formulario2.html   # Formulario de mantenimiento
│   │   └── index_historial.html     # Historial de mantenimiento
│   │
│   ├── nginx.conf                   # Configuración de Nginx
│   └── Dockerfile                   # Imagen Docker del frontend
│
├── docker-compose.yml               # Orquestación de servicios
├── SOLUCION_ERRORES.md             # Documentación de problemas resueltos
└── README.md                        # Este archivo
```

---

## 🔄 Flujo de Datos (Arquitectura de Capas)

### Ejemplo: Registro de un Nuevo Mantenimiento

```
1. USUARIO (Navegador)
   │
   │ Completa formulario de mantenimiento
   │ Hace clic en "Guardar"
   ↓
2. FRONTEND (JavaScript - formulario.js)
   │
   │ Valida datos del formulario
   │ Construye objeto JSON
   │ Envía POST a /home/mantenimiento/agregar
   ↓
3. NGINX (Proxy Reverso)
   │
   │ Recibe petición en puerto 18080
   │ Reenvía a backend:8000/home/mantenimiento/agregar
   ↓
4. BACKEND - CAPA DE RUTAS (routes/mantenimiento.py)
   │
   │ @router.post("/agregar")
   │ Valida esquema con Pydantic (MantenimientoSchema)
   │ Llama a service.registrar_mantenimiento()
   ↓
5. BACKEND - CAPA DE SERVICIO (services.py)
   │
   │ def registrar_mantenimiento(datos_dict):
   │   - Busca la máquina en MySQL (usando MaquinaDAO)
   │   - Valida que la máquina exista
   │   - Crea objeto Mantenimiento
   │   - Llama a MantenimientoDAO.guardar()
   ↓
6. BACKEND - CAPA DE ACCESO A DATOS (daos/mantenimiento_dao.py)
   │
   │ def guardar(mantenimiento):
   │   - Convierte objeto a diccionario (to_dict())
   │   - Inserta en colección de MongoDB
   ↓
7. BASE DE DATOS (MongoDB)
   │
   │ Almacena documento en colección "mantenimientos"
   │ {
   │   "codigo_maquina": "PC1",
   │   "empresa": "TechService",
   │   "tecnico": "Juan Pérez",
   │   "tipo": "preventivo",
   │   "fecha": "2024-01-15",
   │   "observaciones": "Limpieza general"
   │ }
   ↓
8. RESPUESTA (Flujo inverso)
   │
   │ MongoDB → DAO → Service → Route → Nginx → Frontend → Usuario
   │ Mensaje: "Mantenimiento guardado exitosamente"
```

### Ejemplo: Generación de Reporte Consolidado

```
1. USUARIO
   │ Busca código de máquina: "PC1"
   ↓
2. FRONTEND (reporte.js)
   │ GET /home/mantenimiento/informe-general?codigo=PC1
   ↓
3. BACKEND - ROUTE (routes/mantenimiento.py)
   │ @router.get("/informe-general")
   │ Llama a service.obtener_informe_completo(codigo)
   ↓
4. BACKEND - SERVICE (services.py)
   │ def obtener_informe_completo(codigo):
   │   ┌─────────────────────────────────────┐
   │   │ 1. Obtiene TODAS las máquinas       │
   │   │    de MySQL (MaquinaDAO)            │
   │   │                                     │
   │   │ 2. Filtra en Python por código     │
   │   │    (búsqueda insensible)           │
   │   │                                     │
   │   │ 3. Obtiene TODOS los mantenimientos│
   │   │    de MongoDB (MantenimientoDAO)   │
   │   │                                     │
   │   │ 4. Crea mapa de mantenimientos     │
   │   │    agrupados por código            │
   │   │    (normalizado a minúsculas)      │
   │   │                                     │
   │   │ 5. Cruza datos:                    │
   │   │    - Por cada máquina filtrada     │
   │   │    - Busca sus mantenimientos      │
   │   │    - Crea InformeMaquinaDTO        │
   │   └─────────────────────────────────────┘
   ↓
5. BASES DE DATOS (Consultas en paralelo)
   │
   ├─→ MySQL: SELECT * FROM maquinas
   │   └─→ Retorna: [{codigo: "PC1", tipo: "PC", area: "Lab Redes", ...}]
   │
   └─→ MongoDB: db.mantenimientos.find()
       └─→ Retorna: [{codigo_maquina: "PC1", tecnico: "Juan", ...}, ...]
   ↓
6. BACKEND - SERVICE (Procesamiento)
   │
   │ Normaliza códigos a minúsculas
   │ Agrupa mantenimientos por código
   │ Construye lista de InformeMaquinaDTO
   ↓
7. RESPUESTA JSON
   │
   │ [
   │   {
   │     "codigo": "PC1",
   │     "tipo": "PC",
   │     "area": "Lab Redes",
   │     "estado": "Operativa",
   │     "mantenimientos": [
   │       {
   │         "tecnico": "Juan Pérez",
   │         "fecha": "2024-01-15",
   │         "tipo": "preventivo",
   │         "observaciones": "Limpieza general"
   │       }
   │     ]
   │   }
   │ ]
   ↓
8. FRONTEND (reporte.js)
   │
   │ Renderiza tabla HTML con los datos
   │ Muestra filas por cada mantenimiento
```

---

## 🐳 Contenedores Docker

El sistema utiliza **4 contenedores** orquestados con Docker Compose:

### 1. **mysql_siglab** (Base de Datos Relacional)

```yaml
Imagen: mysql:8.0
Puerto: 13306:3306
Volumen: mysql_data (persistencia)
Healthcheck: mysqladmin ping cada 30s
```

**Responsabilidades:**
- Almacenar inventario de máquinas
- Almacenar usuarios del sistema
- Validar códigos únicos de equipos

**Tablas:**
- `maquinas`: (id, codigo, tipo, estado, area, fecha)
- `usuarios`: (id, nombre_completo, username, password, rol)

### 2. **mongo_siglab** (Base de Datos NoSQL)

```yaml
Imagen: mongo:latest
Puerto: 27018:27017
Volumen: mongo_data (persistencia)
Healthcheck: mongosh ping cada 30s
```

**Responsabilidades:**
- Almacenar historial de mantenimientos
- Permitir crecimiento flexible de datos
- Consultas rápidas por código de máquina

**Colecciones:**
- `mantenimientos`: Documentos con historial técnico

### 3. **backend_siglab** (API REST)

```yaml
Imagen: Custom (Python 3.11 + FastAPI)
Puerto: 18000:8000
Depende de: mysql (healthy), mongodb (healthy)
```

**Responsabilidades:**
- Exponer API REST para el frontend
- Implementar lógica de negocio
- Validar datos con Pydantic
- Cruzar datos de ambas bases de datos
- Servir plantillas HTML con Jinja2

**Endpoints principales:**
- `POST /api/login` - Autenticación
- `POST /api/register` - Registro de usuarios
- `POST /home/maquinas/agregar` - Crear máquina
- `GET /home/maquinas/listar` - Listar máquinas
- `POST /home/mantenimiento/agregar` - Registrar mantenimiento
- `GET /home/mantenimiento/informe-general` - Generar reporte

### 4. **frontend_siglab** (Servidor Web)

```yaml
Imagen: Custom (Nginx)
Puerto: 18080:80
Depende de: backend
```

**Responsabilidades:**
- Servir archivos estáticos (CSS, JS, imágenes)
- Actuar como proxy reverso al backend
- Cachear recursos estáticos
- Manejar rutas de la aplicación

**Configuración de Nginx:**
```nginx
# Archivos estáticos servidos directamente
location /static/ {
    alias /usr/share/nginx/html/static/;
}

# Proxy a backend para APIs
location /api/ {
    proxy_pass http://backend:8000/api/;
}

location /home/ {
    proxy_pass http://backend:8000/home/;
}
```

### Red Docker

Todos los contenedores están conectados a la red `siglab_network` (tipo bridge):

```
┌─────────────────────────────────────────────┐
│         siglab_network (bridge)             │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │  mysql   │  │ mongodb  │  │ backend  │ │
│  │  :3306   │  │  :27017  │  │  :8000   │ │
│  └──────────┘  └──────────┘  └──────────┘ │
│       ↑             ↑             ↑        │
│       └─────────────┴─────────────┘        │
│                     ↑                      │
│              ┌──────────┐                  │
│              │ frontend │                  │
│              │   :80    │                  │
│              └──────────┘                  │
└─────────────────────────────────────────────┘
         ↑
    Puerto 18080 (Host)
```

---

## 🚀 Instalación y Configuración

### Requisitos Previos

1. **Docker Desktop** (Windows/Mac) o **Docker Engine + Docker Compose** (Linux)
   - Descargar: https://www.docker.com/products/docker-desktop
   - Versión mínima: Docker 20.10+, Docker Compose 2.0+

2. **Verificar instalación:**
   ```bash
   docker --version
   docker-compose --version
   ```

### Pasos de Instalación

#### 1. Clonar o Descargar el Proyecto

```bash
git clone <url-del-repositorio>
cd PP1_01-javier
```

#### 2. Verificar Puertos Disponibles

Los siguientes puertos deben estar libres:

| Puerto | Servicio | Comando de Verificación (Windows) |
|--------|----------|-----------------------------------|
| 18080 | Frontend | `netstat -ano \| findstr :18080` |
| 18000 | Backend | `netstat -ano \| findstr :18000` |
| 13306 | MySQL | `netstat -ano \| findstr :13306` |
| 27018 | MongoDB | `netstat -ano \| findstr :27018` |

**Nota:** Estos puertos están en rango alto (13000-18000) para evitar conflictos con servicios del sistema.

#### 3. Levantar los Contenedores

```bash
# Construir y levantar todos los servicios
docker-compose up -d --build

# Ver el progreso en tiempo real
docker-compose logs -f
```

**Primera ejecución:**
- Descargará imágenes base (~2-3 GB)
- Construirá imágenes personalizadas
- Inicializará bases de datos
- Tiempo estimado: 5-10 minutos

#### 4. Verificar Estado de los Contenedores

```bash
docker-compose ps
```

**Salida esperada:**
```
NAME                STATUS          PORTS
backend_siglab      Up (healthy)    0.0.0.0:18000->8000/tcp
frontend_siglab     Up              0.0.0.0:18080->80/tcp
mongo_siglab        Up (healthy)    0.0.0.0:27018->27017/tcp
mysql_siglab        Up (healthy)    0.0.0.0:13306->3306/tcp
```

#### 5. Verificar Logs del Backend

```bash
docker-compose logs backend | grep "ÉXITO"
```

**Mensajes esperados:**
- `¡ÉXITO! MySQL configurado (Máquinas y Usuarios) listo. :V`
- `¡Conexión a MongoDB establecida con éxito! :V`
- `Application startup complete.`

---

## 🐛 Problemas Resueltos Durante el Desarrollo

Durante el desarrollo del proyecto, se identificaron y resolvieron varios problemas críticos. Aquí se documentan los más importantes:

### 1. **Healthcheck de MySQL Fallaba al Inicio**

**Problema:**
```
dependency failed to start: container mysql_siglab is unhealthy
```

**Causa Raíz:**
- MySQL tarda 30-40 segundos en inicializarse completamente
- El healthcheck comenzaba inmediatamente, fallando antes de que MySQL estuviera listo

**Solución Implementada:**
```yaml
healthcheck:
  test: ["CMD-SHELL", "mysqladmin ping -h localhost -u root -p${MYSQL_ROOT_PASSWORD} || exit 1"]
  interval: 30s
  timeout: 10s
  retries: 10
  start_period: 40s  # ← CLAVE: Da 40 segundos antes de verificar
```

**Resultado:** MySQL ahora tiene tiempo suficiente para inicializar antes de que el healthcheck comience.

---

### 2. **Bucles Infinitos en Nginx**

**Problema:**
- La aplicación entraba en bucles de redirección infinitos
- Los archivos estáticos no se cargaban
- Error 500 en el navegador

**Causa Raíz:**
```nginx
# Configuración INCORRECTA (antes)
location / {
    proxy_pass http://backend:8000;  # ← Todo iba al backend, incluso CSS/JS
}
```

**Solución Implementada:**
```nginx
# Configuración CORRECTA (después)

# 1. Servir archivos estáticos DIRECTAMENTE desde Nginx
location /static/ {
    alias /usr/share/nginx/html/static/;
    try_files $uri =404;
}

# 2. Proxy con trailing slash correcto
location /api/ {
    proxy_pass http://backend:8000/api/;
    proxy_redirect off;  # ← Previene redirecciones infinitas
}

location /home/ {
    proxy_pass http://backend:8000/home/;
    proxy_redirect off;
}

# 3. Fallback inteligente
location / {
    try_files $uri $uri/ @backend;
}

location @backend {
    proxy_pass http://backend:8000;
}
```

**Resultado:** 
- ✅ Archivos estáticos servidos directamente (más rápido)
- ✅ No más bucles infinitos
- ✅ Rutas de API funcionan correctamente

---

### 3. **Conflictos de Puertos**

**Problema:**
- Puerto 80 requiere permisos de administrador en Windows
- Puerto 3306 ocupado por MySQL local
- Puerto 8000 ocupado por otros servicios

**Solución Implementada:**
```yaml
# Puertos cambiados a rango alto (13000-18000)
frontend:
  ports:
    - "18080:80"  # Antes: 80:80

backend:
  ports:
    - "18000:8000"  # Antes: 8000:8000

mysql:
  ports:
    - "13306:3306"  # Antes: 3306:3306

mongodb:
  ports:
    - "27018:27017"  # Antes: 27017:27017
```

**Resultado:**
- ✅ No requiere permisos de administrador
- ✅ Funciona en cualquier máquina sin conflictos
- ✅ Compatible con Windows, Linux y Mac

---

### 4. **Búsqueda de Reportes Inconsistente**

**Problema:**
- Al buscar "PC1" en reportes, se mostraba la máquina pero SIN mantenimientos
- En el listado general sí aparecían los mantenimientos
- Inconsistencia entre búsqueda filtrada y listado completo

**Causa Raíz:**
```python
# Código PROBLEMÁTICO (antes)
if codigo:
    maquinas_db = self._dao_maq.buscar_por_codigo_parcial(codigo)
    # ← Usaba método diferente que no cruzaba bien con MongoDB
```

**Solución Implementada:**
```python
# Código CORREGIDO (después)
def obtener_informe_completo(self, codigo=None):
    # 1. SIEMPRE obtener TODAS las máquinas (fuente única de verdad)
    todas_las_maquinas = self._dao_maq.listar_todas()
    
    # 2. Filtrar en Python (garantiza consistencia)
    if codigo:
        filtro = str(codigo).strip().lower()
        maquinas_db = [
            m for m in todas_las_maquinas 
            if filtro in str(m.get("codigo", "")).lower()
        ]
    else:
        maquinas_db = todas_las_maquinas
    
    # 3. Obtener TODOS los mantenimientos
    todos_mttos = self._dao_mtto.listar_todos() or []
    
    # 4. Crear mapa normalizado (clave en minúsculas)
    mttos_map = {}
    for mt in todos_mttos:
        raw_c = mt.get("codigo_maquina") or mt.get("codigo")
        if raw_c:
            key = str(raw_c).strip().lower()  # ← Normalización
            if key not in mttos_map:
                mttos_map[key] = []
            mttos_map[key].append(mt)
    
    # 5. Cruzar datos usando la misma lógica de normalización
    for maq in maquinas_db:
        k_maq = str(maq.get("codigo", "")).strip().lower()
        mttos_encontrados = mttos_map.get(k_maq, [])
        # ... construir DTO
```

**Resultado:**
- ✅ Búsqueda y listado usan la MISMA lógica
- ✅ Normalización consistente (minúsculas)
- ✅ Cruce de datos MySQL-MongoDB 100% confiable
- ✅ "PC1", "pc1", "Pc1" funcionan igual

---

### 5. **Conexiones Excesivas a MongoDB**

**Problema:**
- Healthchecks cada 10 segundos generaban muchas conexiones
- Logs saturados con mensajes de conexión
- Consumo innecesario de recursos

**Solución Implementada:**
```yaml
# Healthcheck optimizado
healthcheck:
  interval: 30s  # Antes: 10s (66% menos conexiones)
  retries: 3     # Antes: 5
```

```python
# Pool de conexiones en MongoDB
client = MongoClient(
    uri,
    maxPoolSize=10,      # Máximo 10 conexiones simultáneas
    minPoolSize=1,       # Mínimo 1 conexión activa
    maxIdleTimeMS=45000  # Cerrar conexiones inactivas después de 45s
)
```

**Resultado:**
- ✅ 66% menos conexiones de healthcheck
- ✅ Reutilización eficiente de conexiones
- ✅ Logs más limpios

---

### Resumen de Mejoras

| Aspecto | Antes | Después |
|---------|-------|---------|
| **Start Period MySQL** | ❌ 0s | ✅ 40s |
| **Bucles en Nginx** | ❌ Sí | ✅ No |
| **Puertos** | ❌ Conflictos | ✅ Rango alto |
| **Búsqueda de Reportes** | ❌ Inconsistente | ✅ 100% confiable |
| **Conexiones MongoDB** | ❌ Excesivas | ✅ Optimizadas (66% menos) |

Para más detalles, consulta [`SOLUCION_ERRORES.md`](./SOLUCION_ERRORES.md).

---

## 🔧 Comandos Útiles

### Gestión de Contenedores

```bash
# Ver estado de todos los contenedores
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f mysql

# Reiniciar un contenedor
docker-compose restart backend

# Detener todos los contenedores
docker-compose stop

# Iniciar contenedores detenidos
docker-compose start

# Detener y eliminar contenedores (mantiene datos)
docker-compose down

# Detener y eliminar contenedores + volúmenes (⚠️ BORRA DATOS)
docker-compose down -v

# Reconstruir imágenes
docker-compose build

# Reconstruir y levantar
docker-compose up -d --build
```

### Acceso a Contenedores

```bash
# Entrar al contenedor del backend
docker-compose exec backend bash

# Entrar a MySQL
docker-compose exec mysql bash
# Luego: mysql -u root -pClubpengui1 proyecto_maquinas

# Entrar a MongoDB
docker-compose exec mongodb bash
# Luego: mongosh siglab_db
```

### Debugging

```bash
# Ver healthcheck de MySQL
docker inspect mysql_siglab | grep -A 10 Health

# Verificar conectividad a MySQL
docker-compose exec mysql mysqladmin ping -h localhost -u root -pClubpengui1

# Ver uso de recursos
docker stats

# Limpiar sistema (liberar espacio)
docker system prune -a
```

### Bases de Datos

```bash
# Conectar a MySQL desde host
mysql -h localhost -P 13306 -u root -pClubpengui1 proyecto_maquinas

# Conectar a MongoDB desde host
mongosh mongodb://localhost:27018/siglab_db

# Backup de MySQL
docker-compose exec mysql mysqldump -u root -pClubpengui1 proyecto_maquinas > backup.sql

# Restaurar MySQL
docker-compose exec -T mysql mysql -u root -pClubpengui1 proyecto_maquinas < backup.sql
```

---

## 🌐 Acceso a la Aplicación

### URLs de Acceso

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Frontend** | http://localhost:18080 | Interfaz web principal |
| **Backend API** | http://localhost:18000 | API REST directa |
| **Documentación API** | http://localhost:18000/docs | Swagger UI interactivo |
| **MySQL** | localhost:13306 | Base de datos relacional |
| **MongoDB** | localhost:27018 | Base de datos NoSQL |

### Credenciales por Defecto
**Uusario por defecto para iniciar sesión:**
- Usuario: `admin`
- Contraseña: `12345`

**MySQL:**
- Usuario: `root`
- Contraseña: `Clubpengui1`
- Base de datos: `proyecto_maquinas`

**MongoDB:**
- Sin autenticación (desarrollo)
- Base de datos: `siglab_db`

---

## 📊 Flujo de Uso de la Aplicación

### 1. Registro de Usuario
```
1. Ir a http://localhost:18080
2. Clic en "Registrarse"
3. Completar formulario
4. Sistema valida y crea usuario en MySQL
5. Redirección automática al login
```

### 2. Inicio de Sesión
```
1. Ingresar credenciales
2. Backend valida contra MySQL
3. Redirección al dashboard
```

### 3. Gestión de Equipos
```
1. Dashboard → "Laboratorio de Redes"
2. Clic en "Agregar Máquina"
3. Completar formulario (código, tipo, área, estado)
4. Backend valida código único
5. Guarda en MySQL
6. Redirección a lista de máquinas
```

### 4. Registro de Mantenimiento
```
1. Lista de máquinas → Clic en "Mantenimiento"
2. Formulario pre-cargado con código de máquina
3. Completar datos técnicos
4. Backend valida que la máquina exista (MySQL)
5. Guarda mantenimiento en MongoDB
6. Redirección a lista
```

### 5. Generación de Reportes
```
1. Lista de máquinas → "Generar Reporte"
2. (Opcional) Buscar código específico
3. Backend cruza datos MySQL + MongoDB
4. Renderiza tabla con:
   - Datos de máquina (MySQL)
   - Historial de mantenimientos (MongoDB)
5. Búsqueda insensible a mayúsculas
```

---

## 🎓 Patrones de Diseño Implementados

### 1. **Abstract Factory** (Modelos)
```python
# Maquina.py (Clase abstracta)
class Maquina(ABC):
    @abstractmethod
    def tipo_equipo(self):
        pass

# Computadora.py (Implementación concreta)
class Computadora(Maquina):
    def tipo_equipo(self):
        return "PC"
```

### 2. **DAO (Data Access Object)**
```python
# Separación de lógica de acceso a datos
class MaquinaDAO:
    def guardar(self, maquina): ...
    def buscar_por_codigo(self, codigo): ...
    def listar_todas(self): ...
```

### 3. **DTO (Data Transfer Object)**
```python
# Transferencia estructurada de datos
class InformeMaquinaDTO:
    def __init__(self, codigo, tipo, area, estado, mantenimientos):
        self.codigo = codigo
        self.mantenimientos = mantenimientos
```

### 4. **Service Layer**
```python
# Lógica de negocio centralizada
class ProyectoService:
    def registrar_maquina(self, datos): ...
    def obtener_informe_completo(self, codigo): ...
```

---

## 📝 Notas Finales

### Persistencia de Datos
- Los datos se almacenan en volúmenes Docker (`mysql_data`, `mongo_data`)
- Sobreviven a reinicios de contenedores
- Solo se eliminan con `docker-compose down -v`

### Seguridad
- Contraseñas en variables de entorno (no hardcodeadas)
- Validación de datos con Pydantic
- Consultas parametrizadas (prevención de SQL injection)

### Escalabilidad
- Arquitectura de capas permite escalar componentes independientemente
- Bases de datos híbridas optimizan rendimiento
- Nginx puede servir múltiples instancias del backend

### Mantenimiento
- Código documentado con comentarios claros
- Estructura modular facilita modificaciones
- Logs detallados para debugging

---

## 🆘 Soporte y Contacto

Para problemas o preguntas:
1. Revisa [`SOLUCION_ERRORES.md`](./SOLUCION_ERRORES.md)
2. Verifica logs: `docker-compose logs -f`
3. Consulta documentación de Docker: https://docs.docker.com/

---

**Desarrollado con amor para la Universidad Central del Ecuador (UCE)**

**Tecnologías:** FastAPI • MySQL • MongoDB • Docker • Nginx • JavaScript

**Licencia:** MIT
