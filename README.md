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

4. **Abrir el navegador** y elegir una de estas opciones:
   - **Aplicación principal**: **http://localhost:8080** (Frontend)
   - **Load Balance API**: **http://localhost:81** (HAProxy Load Balancer)
   - **Dashboard de HAProxy**: **http://localhost:8404/stats** (Estadísticas)

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

1. **El usuario** abre el navegador y va a `http://localhost:8080`
2. **Nginx** (servidor web frontend) muestra la página de login
3. **El usuario** ingresa sus credenciales
4. **JavaScript** envía los datos mediante `fetch("/api/login")`
5. **Nginx** reenvía la petición a **HAProxy Load Balance** (puerto 81)
6. **HAProxy** distribuye la petición a **backend-1, backend-2, o backend-3** (round-robin)
7. **FastAPI** (backend) verifica las credenciales en **MySQL compartido**
8. **Si es correcto**, el usuario puede ver y gestionar máquinas
9. **Al agregar una máquina**, se guarda en **MySQL compartido**
10. **Al agregar un mantenimiento**, se guarda en **MongoDB compartido**
11. **Los reportes** combinan datos de ambas bases de datos compartidas

## Guía rápida (preguntas comunes)

### 1) Flujo completo (de punta a punta)

Cuando el usuario hace una acción en la web, normalmente pasa esto:

1. **Frontend (JavaScript)** hace un `fetch("/api/..." )`
2. **Nginx (frontend)** recibe `/api/...` y lo reenvía a **HAProxy Load Balance** (reverse proxy)
3. **HAProxy** distribuye la petición a **backend-1, backend-2, o backend-3** (round-robin)
4. **Routes (FastAPI)** recibe la petición y valida datos (Pydantic)
5. **Service (`services.py`)** aplica reglas y orquesta la operación
6. **DAO (`daos/*.py`)** guarda/lee datos en **MySQL compartido** o **MongoDB compartido**
7. **Database (`database/*.py`)** maneja la conexión/pool (encapsulado)

### 2) ¿Qué diferencia hay entre `factory.py` y `Maquina.py`?

- **`Maquina.py`** (clase base): define qué es una máquina (campos/estructura). Se hereda en `Computadora` e `Impresora`.
- **`factory.py`** (fábrica): decide qué clase crear (Computadora o Impresora) según el `tipo_equipo`.

Idea simple:
- `Maquina` = el “molde”
- `MaquinaFactory` = el “selector/constructor” que crea el objeto correcto

### 3) ¿Se encapsulan las bases de datos?

Sí, porque el proyecto NO abre conexiones en las rutas.

- **MySQL (compartido)**:
  - `app/database/mysql.py` encapsula conexión + pool + creación de tablas
  - Los 3 backends usan `MySQLConnection.conectar()` al mismo contenedor `mysql_siglab`
- **MongoDB (compartido)**:
  - `app/database/mongodb.py` encapsula cliente + reintentos + `conectar()`/`cerrar()`
  - Los 3 backends usan `MongoDB.conectar()` al mismo contenedor `mongo_siglab`
- **Orquestación**:
  - `app/database/database_manager.py` centraliza `inicializar()` y `cerrar()`
  - `main.py` lo llama en `startup`/`shutdown` en cada backend

### 4) ¿Qué es “reverse proxy” en este proyecto?

En `frontend/nginx.conf` existe:

- `location /api/ { proxy_pass http://haproxy-lb:81; }`

Esto significa:

- El navegador entra a **Frontend**: `http://localhost:8080`
- Cuando el frontend llama `/api/...`, **Nginx** reenvía esa petición al contenedor **HAProxy**
- **HAProxy** distribuye la petición entre **backend-1, backend-2, o backend-3**
- El navegador no necesita saber los puertos de los backends

### 5) ¿Para qué sirven los headers `X-Forwarded-*` y el `ProxyHeadersMiddleware`?

Nginx agrega headers como:

- `X-Forwarded-Proto` (http/https)
- `X-Forwarded-Host` y `X-Forwarded-Port` (host/puerto real)
- `X-Forwarded-For` (IP del cliente)

El `ProxyHeadersMiddleware` en `backend/main.py` sirve para que FastAPI use esa información “real” cuando el backend está detrás de Nginx y HAProxy.

Nota: para el CRUD básico normalmente no es obligatorio, pero es correcto tenerlo en este proyecto porque sí hay reverse proxy y Load Balance.

### 6) ¿Para qué sirve `Cache-Control: no-cache` en `/api/mantenimiento/listar/{codigo}`?

En algunos endpoints se envía:

- `Cache-Control: no-cache, no-store, must-revalidate`

Sirve para que el navegador NO muestre una respuesta vieja (cacheada) y siempre pida el historial actualizado.

### 7) ¿Cómo funciona el Load Balance con 3 servidores?

El sistema usa **HAProxy** para distribuir las peticiones entre 3 backends idénticos:

- **Round-robin**: Distribuye equitativamente (33.3% cada uno)
- **Health checks**: Verifica que los backends estén vivos
- **Failover**: Si un backend cae, los otros siguen funcionando
- **Dashboard**: `http://localhost:8404/stats` para ver estadísticas en tiempo real

## Apuntes (para ir agregando)

En esta sección puedes ir anotando dudas/respuestas del proyecto.

- Tema:
  - Explicación:

## Comandos útiles

**Ver los logs del sistema:**
```bash
docker-compose logs -f
```

**Ver logs de un servicio específico:**
```bash
docker-compose logs -f haproxy-lb    # Load Balancer
docker-compose logs -f backend-1       # Servidor 1
docker-compose logs -f backend-2       # Servidor 2
docker-compose logs -f backend-3       # Servidor 3
```

**Hacer caer un servidor (para demostración):**
```bash
docker stop backend_siglab_1    # Cae servidor 1
docker stop backend_siglab_2    # Cae servidor 2
docker stop backend_siglab_3    # Cae servidor 3
```

**Recuperar un servidor:**
```bash
docker start backend_siglab_1   # Recupera servidor 1
docker start backend_siglab_2   # Recupera servidor 2
docker start backend_siglab_3   # Recupera servidor 3
```

**Probar el Load Balance:**
```bash
curl http://localhost:81/api/maquinas/
```

**Ver dashboard de estadísticas:**
```bash
# Abre en navegador: http://localhost:8404/stats
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

- **8080**: Frontend (página web principal)
- **81**: Load Balance API (HAProxy - entrada principal)
- **8404**: Dashboard de HAProxy (estadísticas en tiempo real)
- **13306**: MySQL (base de datos)
- **27018**: MongoDB (base de datos)

### Notas importantes:
- **Puerto 81**: Es el puerto principal para hacer peticiones a la API
- **Dashboard 8404**: Muestra distribución entre los 3 servidores backend
- **Puedes hacer caer servidores** y ver cómo el sistema sigue funcionando

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
