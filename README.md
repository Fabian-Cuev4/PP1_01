# SIGLAB - Sistema de Gestión de Laboratorios

Sistema web para gestionar máquinas (computadoras e impresoras) y sus mantenimientos en laboratorios de la Universidad Central del Ecuador.

## ¿Qué hace este sistema?

Este sistema permite:
- **Registrar máquinas**: Agregar computadoras e impresoras al inventario
- **Ver historial**: Consultar todos los mantenimientos realizados a cada máquina
- **Agregar mantenimientos**: Registrar cuando se hace mantenimiento a una máquina
- **Actualizar estado**: Cambiar el estado de una máquina (operativa, fuera de servicio, etc.)
- **Eliminar máquinas**: Borrar máquinas y todos sus mantenimientos
- **Generar reportes**: Ver reportes completos de todas las máquinas y sus mantenimientos

## Tecnologías usadas

### Backend (Servidor)
- **Python 3.11**: Lenguaje de programación
- **FastAPI**: Framework para crear la API (interfaz de comunicación)
- **MySQL**: Base de datos para guardar máquinas y usuarios
- **MongoDB**: Base de datos para guardar los mantenimientos

### Frontend (Interfaz de usuario)
- **HTML**: Estructura de las páginas
- **CSS**: Estilos y diseño visual
- **JavaScript**: Lógica y comunicación con el servidor
- **Nginx**: Servidor web que muestra las páginas

## Cómo instalar y usar

### Requisitos
- Tener instalado **Docker Desktop** (Windows/Mac) o Docker (Linux)

### Pasos para iniciar

1. **Abrir la terminal** en la carpeta del proyecto

2. **Ejecutar este comando** para iniciar todos los servicios:
```bash
docker-compose up -d --build
```

3. **Esperar unos minutos** mientras se descargan e instalan todas las dependencias

4. **Abrir el navegador** y ir a: **http://localhost:18080**

5. **Iniciar sesión** con:
   - Usuario: `admin`
   - Contraseña: `admin123`

## Estructura del proyecto

```
PP1_01/
├── backend/              # Código del servidor (Python)
│   ├── app/
│   │   ├── daos/        # Acceso a las bases de datos
│   │   ├── database/    # Configuración de MySQL y MongoDB
│   │   ├── models/      # Modelos de datos (Máquina, Mantenimiento)
│   │   ├── routes/      # Rutas de la API (endpoints)
│   │   └── services.py  # Lógica de negocio
│   └── main.py         # Archivo principal que inicia el servidor
│
├── frontend/            # Código de la interfaz (HTML, CSS, JS)
│   ├── static/         # Archivos estáticos (CSS, JavaScript, imágenes)
│   ├── templates/      # Páginas HTML
│   └── nginx.conf      # Configuración del servidor web
│
└── docker-compose.yml  # Configuración de todos los servicios
```

## Cómo funciona

1. **El usuario** abre el navegador y va a `http://localhost:18080`
2. **Nginx** (servidor web) muestra la página de login
3. **El usuario** ingresa sus credenciales
4. **JavaScript** envía los datos al backend mediante una petición HTTP
5. **FastAPI** (backend) verifica las credenciales en MySQL
6. **Si es correcto**, el usuario puede ver y gestionar máquinas
7. **Al agregar una máquina**, se guarda en MySQL
8. **Al agregar un mantenimiento**, se guarda en MongoDB
9. **Los reportes** combinan datos de ambas bases de datos

## Guía rápida (preguntas comunes)

### 1) Flujo completo (de punta a punta)

Cuando el usuario hace una acción en la web, normalmente pasa esto:

1. **Frontend (JavaScript)** hace un `fetch("/api/..." )`
2. **Nginx (frontend)** recibe `/api/...` y lo reenvía al backend (reverse proxy)
3. **Routes (FastAPI)** recibe la petición y valida datos (Pydantic)
4. **Service (`services.py`)** aplica reglas y orquesta la operación
5. **DAO (`daos/*.py`)** guarda/lee datos en MySQL o MongoDB
6. **Database (`database/*.py`)** maneja la conexión/pool (encapsulado)

### 2) ¿Qué diferencia hay entre `factory.py` y `Maquina.py`?

- **`Maquina.py`** (clase base): define qué es una máquina (campos/estructura). Se hereda en `Computadora` e `Impresora`.
- **`factory.py`** (fábrica): decide qué clase crear (Computadora o Impresora) según el `tipo_equipo`.

Idea simple:
- `Maquina` = el “molde”
- `MaquinaFactory` = el “selector/constructor” que crea el objeto correcto

### 3) ¿Se encapsulan las bases de datos?

Sí, porque el proyecto NO abre conexiones en las rutas.

- **MySQL**:
  - `app/database/mysql.py` encapsula conexión + pool + creación de tablas
  - Los DAOs usan `MySQLConnection.conectar()`
- **MongoDB**:
  - `app/database/mongodb.py` encapsula cliente + reintentos + `conectar()`/`cerrar()`
  - `MantenimientoDAO` usa `MongoDB.conectar()`
- **Orquestación**:
  - `app/database/database_manager.py` centraliza `inicializar()` y `cerrar()`
  - `main.py` lo llama en `startup`/`shutdown`

### 4) ¿Qué es “reverse proxy” en este proyecto?

En `frontend/nginx.conf` existe:

- `location /api/ { proxy_pass http://backend:8000; }`

Esto significa:

- El navegador entra a **Frontend**: `http://localhost:18080`
- Cuando el frontend llama `/api/...`, **Nginx** reenvía esa petición al contenedor **backend**
- El navegador no necesita saber el puerto del backend

### 5) ¿Para qué sirven los headers `X-Forwarded-*` y el `ProxyHeadersMiddleware`?

Nginx agrega headers como:

- `X-Forwarded-Proto` (http/https)
- `X-Forwarded-Host` y `X-Forwarded-Port` (host/puerto real)
- `X-Forwarded-For` (IP del cliente)

El `ProxyHeadersMiddleware` en `backend/main.py` sirve para que FastAPI use esa información “real” cuando el backend está detrás de Nginx.

Nota: para el CRUD básico normalmente no es obligatorio, pero es correcto tenerlo en este proyecto porque sí hay reverse proxy.

### 6) ¿Para qué sirve `Cache-Control: no-cache` en `/api/mantenimiento/listar/{codigo}`?

En algunos endpoints se envía:

- `Cache-Control: no-cache, no-store, must-revalidate`

Sirve para que el navegador NO muestre una respuesta vieja (cacheada) y siempre pida el historial actualizado.

## Apuntes (para ir agregando)

En esta sección puedes ir anotando dudas/respuestas del proyecto.

- Tema:
  - Explicación:

## Comandos útiles

**Ver los logs del servidor:**
```bash
docker-compose logs -f backend
```

**Detener todos los servicios:**
```bash
docker-compose stop
```

**Iniciar los servicios de nuevo:**
```bash
docker-compose start
```

**Eliminar todo y empezar de cero:**
```bash
docker-compose down
```

## Usuarios por defecto

Al iniciar el sistema por primera vez, se crea automáticamente un usuario administrador:
- **Usuario**: `admin`
- **Contraseña**: `admin123`

## Puertos utilizados

- **18080**: Frontend (página web)
- **18000**: Backend (API)
- **13306**: MySQL (base de datos)
- **27018**: MongoDB (base de datos)

## Características principales

- ✅ **Encriptación de contraseñas**: Las contraseñas se guardan de forma segura usando bcrypt
- ✅ **Asociación de usuarios**: Cada máquina y mantenimiento está asociado al usuario que lo creó
- ✅ **Validaciones**: El sistema valida que los datos sean correctos antes de guardarlos
- ✅ **Manejo de errores**: Muestra mensajes claros cuando algo sale mal

## Notas importantes

- Si cambias código JavaScript, limpia la caché del navegador (Ctrl+Shift+Suprimir)
- Los datos se guardan en contenedores Docker, si los eliminas se pierden los datos
- Para desarrollo, puedes modificar los archivos y recargar la página

## Soporte

Si tienes problemas:
1. Revisa los logs con `docker-compose logs -f backend`
2. Verifica que todos los servicios estén corriendo con `docker-compose ps`
3. Reinicia los servicios con `docker-compose restart`
