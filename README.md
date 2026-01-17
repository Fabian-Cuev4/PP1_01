# 🏢 SIGLAB - Sistema de Gestión de Inventario y Mantenimiento de Laboratorios

**Sistema web profesional para la gestión integral de equipos de laboratorio y su historial de mantenimiento técnico.**

---

## 📑 Tabla de Contenidos

1. [Descripción del Proyecto](#-descripción-del-proyecto)
2. [Arquitectura del Sistema](#-arquitectura-del-sistema)
3. [Tecnologías y Dependencias](#-tecnologías-y-dependencias)
4. [Estructura del Proyecto](#-estructura-del-proyecto)
5. [Contenedores Docker](#-contenedores-docker)
6. [Instalación y Configuración](#-instalación-y-configuración)
7. [Problemas Resueltos](#-problemas-resueltos-durante-el-desarrollo)
8. [Comandos Útiles](#-comandos-útiles)

---

## 🎯 Descripción del Proyecto

**SIGLAB** es un sistema web completo diseñado para gestionar el inventario y mantenimientos de la **Universidad Central del Ecuador (UCE)**.

### Características Principales

- ✅ **Gestión de Inventario**: Registro y administración de equipos (PCs, Impresoras, etc.).
- ✅ **Historial de Mantenimiento**: Registro detallado de mantenimientos preventivos y correctivos, almacenados en **MongoDB** para flexibilidad.
- ✅ **Reportes Dinámicos**: Cruce de datos relacionales (MySQL) con no-relacionales (MongoDB) para generar informes consolidados.
- ✅ **Arquitectura Desacoplada**: Frontend estático servido por Nginx y Backend API REST puro en FastAPI.
- ✅ **Diseño Moderno**: Interfaz limpia y responsive (Vanilla JS + CSS).

---

## 🏗️ Arquitectura del Sistema

El sistema utiliza una **arquitectura basada en microservicios/contenedores** con una clara separación entre Cliente y Servidor.

### Diagrama de Flujo

```mermaid
graph TD
    User[Usuario (Navegador)] -->|HTTP Request| Frontend[Nginx (Puerto 18080)]
    Frontend -->|Sirve HTML/CSS/JS| User
    
    User -->|API Calls (AJAX/Fetch)| Frontend
    Frontend -->|Proxy Pass /api/*| Backend[FastAPI Backend (Puerto 18000)]
    
    Backend -->|CRUD Relacional| MySQL[(MySQL 8.0)]
    Backend -->|Historial No-SQL| MongoDB[(MongoDB)]
```

### Componentes

1.  **Frontend (Nginx + Static Files)**:
    -   Nginx actúa como servidor web y proxy reverso.
    -   Sirve archivos estáticos (`.html`, `.css`, `.js`) directamente.
    -   Redirige las peticiones `/api/*` al backend.
    -   Maneja el enrutamiento visual (URL Rewriting).

2.  **Backend (FastAPI)**:
    -   **API REST** pura (devuelve JSON, no HTML).
    -   Patrón **Controller-Service-DAO/Repository**.
    -   **Modelos**: Uso de Abstract Factory para instancias de equipos (Computadora, Impresora).

3.  **Persistencia Híbrida**:
    -   **MySQL**: Datos estructurales rígidos (Usuarios, Maquinas).
    -   **MongoDB**: Datos volátiles y de historial (Mantenimientos).

---

## 🛠️ Tecnologías y Dependencias

### Backend (Python 3.11+)
| Librería | Versión | Uso |
|:---|:---|:---|
| **FastAPI** | 0.104.1 | Framework principal de la API. |
| **Uvicorn** | 0.24.0 | Servidor ASGI. |
| **MySQL Connector** | 8.2.0 | Conexión a MySQL. |
| **PyMongo** | 4.6.0 | Conexión a MongoDB. |
| **Pydantic** | Core | Validación de datos. |

### Frontend
- **HTML5 / CSS3**: Diseño personalizado y responsivo.
- **JavaScript (Vanilla)**: Lógica del cliente, fetch a APIs, validaciones.
- **Nginx**: Servidor de producción y Proxy.

### Infraestructura
- **Docker**: Contenedorización de todos los servicios.
- **Docker Compose**: Orquestación de la red `siglab_network`.

---

## 📁 Estructura del Proyecto

La estructura ha sido organizada para separar responsabilidades claramente:

```
PP1_01/
│
├── backend/                          # 🐍 Backend (API REST)
│   ├── app/
│   │   ├── daos/                     # Data Access Objects (Acceso directo a BD)
│   │   ├── database/                 # Conexiones Singleton (MySQL/Mongo)
│   │   ├── dtos/                     # Data Transfer Objects
│   │   ├── models/                   # Modelos de Negocio
│   │   │   └── abstrac_factory/      # Patrón de creación de objetos
│   │   ├── routes/                   # Endpoints de la API
│   │   ├── repositories.py           # Repositorio (Abstracción sobre DAOs)
│   │   └── services.py               # Lógica de Negocio (Coordina DAOs y Modelos)
│   ├── main.py                       # Punto de entrada FastAPI
│   ├── requirements.txt              # Dependencias
│   └── Dockerfile                    # Configuración de imagen Backend
│
├── frontend/                         # 🎨 Frontend (Estático + Nginx)
│   ├── static/                       # Assets públicos
│   │   ├── css/                      # Estilos
│   │   ├── javascript/               # Lógica de cliente (AJAX, DOM)
│   │   └── img/                      # Imágenes
│   ├── templates/                    # Archivos HTML (Vistas)
│   ├── nginx.conf                    # Configuración del servidor web
│   └── Dockerfile                    # Configuración de imagen Frontend
│
├── docker-compose.yml                # Orquestador de servicios
└── SOLUCION_ERRORES.md               # Bitácora de problemas resueltos
```

---

## 🐳 Contenedores Docker

El proyecto corre sobre 4 contenedores orquestados:

| Servicio | Nombre Contenedor | Puerto Host | Puerto Interno | Descripción |
|:---|:---|:---|:---|:---|
| **Frontend** | `frontend_siglab` | **18080** | 80 | Servidor Web y Proxy. Punto de entrada del usuario. |
| **Backend** | `backend_siglab` | **18000** | 8000 | API REST. Procesa lógica y datos. |
| **MySQL** | `mysql_siglab` | **13306** | 3306 | BD Relacional (Tablas: maquinas, usuarios). |
| **MongoDB** | `mongo_siglab` | **27018** | 27017 | BD Documental (Colección: mantenimientos). |

---

## 🚀 Instalación y Configuración

Sigue estos pasos para desplegar el proyecto desde cero.

### 1. Requisitos
- Tener instalado **Docker Desktop** (Windows/Mac) o Docker Engine (Linux).

### 2. Clonar y Desplegar
```bash
# Entrar a la carpeta del proyecto
cd PP1_01

# Levantar los servicios (construye las imágenes si no existen)
docker-compose up -d --build
```

### 3. Verificar Despliegue
Ejecuta el siguiente comando para asegurarte que los 4 servicios están "Up" y "Healthy":
```bash
docker-compose ps
```

### 4. Acceder al Sistema
Abre tu navegador (Chrome/Edge/Firefox) y ve a:
👉 **[http://localhost:18080](http://localhost:18080)**

## 🔁 Cambios recientes (Separación Frontend / Backend)
- Hemos separado claramente el frontend del backend: **Nginx** sirve las páginas estáticas y actúa como proxy hacia la **API** (FastAPI).
- Rutas principales ahora son:
  - Páginas: `/pagina/*`  (ej. `/pagina/login`, `/pagina/maquinas`)
  - API REST: `/api/*` (ej. `POST /api/maquinas/agregar`, `GET /api/maquinas/listar`)
  - Estáticos: `/static/*` (CSS, JS, imágenes)
- Se eliminó el renderizado de plantillas desde FastAPI (se removió `views.py`) para evitar conflictos de rutas.
- Backend: FastAPI expone solo APIs y cuenta con `ProxyHeadersMiddleware` para respetar `X-Forwarded-*` y `TrustedHostMiddleware` para confiar en Nginx.
- Frontend: Nginx se configuró para preservar puerto (ej. `absolute_redirect off`, `port_in_redirect off`), servir páginas sin redirecciones HTTP y aplicar headers `no-cache` a `.js` para evitar problemas de caché. Además usamos versionado en los assets (`formulario.js?v=2.2`) para forzar recarga cuando es necesario.
- Puertos relevantes: frontend en **18080**, backend en **18000**, MySQL en **13306**, MongoDB en **27018**.
- Nota práctica: después de cambios en JS estático, limpia el caché del navegador (Ctrl+Shift+Suprimir) o incrementa el `?v=` del archivo para forzar la actualización.

---

## 🔧 Comandos Útiles

**Ver logs en tiempo real (Backend):**
```bash
docker-compose logs -f backend
```

**Ver logs en tiempo real (MySQL):**
```bash
docker-compose logs -f mysql
```

**Reiniciar servicios:**
```bash
docker-compose restart
```

**Apagar todo (Mantiene datos):**
```bash
docker-compose stop
```

**Eliminar todo (Borra contenedores y redes):**
```bash
docker-compose down
```

---

## 🐛 Problemas Resueltos Durante el Desarrollo

Consulta el archivo [SOLUCION_ERRORES.md](./SOLUCION_ERRORES.md) para ver detalles técnicos sobre:
1. **Healthchecks de MySQL**: Configuración de `start_period` para evitar fallos de inicio.
2. **Nginx Loops**: Configuración correcta de `proxy_pass` y `try_files`.
3. **Persistencia**: Uso de volúmenes Docker para no perder datos al reiniciar.