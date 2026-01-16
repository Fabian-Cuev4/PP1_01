# PP1_01 - Sistema de Inventario y Gestión de Mantenimiento de Equipos de Laboratorio

Proyecto dockerizado con FastAPI (backend), HTML/CSS/JS estático (frontend), MySQL y MongoDB.

## 📋 Requisitos Previos

Antes de comenzar, necesitas tener instalado en tu sistema:

### 1. Docker Desktop (Windows/Mac) o Docker Engine + Docker Compose (Linux)

#### Para Windows:
1. Descarga Docker Desktop desde: https://www.docker.com/products/docker-desktop
2. Ejecuta el instalador y sigue las instrucciones
3. Reinicia tu computadora si es necesario
4. Abre Docker Desktop y verifica que esté corriendo (deberías ver el ícono de Docker en la bandeja del sistema)

#### Para Linux (Ubuntu/Debian):
```bash
# Actualizar paquetes
sudo apt-get update

# Instalar Docker
sudo apt-get install -y docker.io docker-compose

# Agregar tu usuario al grupo docker (para no usar sudo)
sudo usermod -aG docker $USER

# Reiniciar sesión o ejecutar:
newgrp docker

# Verificar instalación
docker --version
docker-compose --version
```

#### Para Mac:
1. Descarga Docker Desktop desde: https://www.docker.com/products/docker-desktop
2. Arrastra Docker.app a la carpeta Applications
3. Abre Docker Desktop desde Applications
4. Verifica la instalación en terminal:
```bash
docker --version
docker-compose --version
```

### 2. Verificar que Docker esté funcionando

Abre una terminal (PowerShell en Windows, Terminal en Mac/Linux) y ejecuta:

```bash
docker --version
docker-compose --version
```

Deberías ver las versiones instaladas. Si aparece un error, asegúrate de que Docker Desktop esté corriendo.

## 🚀 Instalación y Configuración

### Paso 1: Clonar o Descargar el Proyecto

Si tienes el proyecto en Git:
```bash
git clone <url-del-repositorio>
cd PP1_01
```

O simplemente navega a la carpeta del proyecto si ya la tienes.

### Paso 2: Verificar la Estructura del Proyecto

Asegúrate de que tu proyecto tenga esta estructura:

```
PP1_01/
├── backend/
│   ├── app/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── static/
│   ├── templates/
│   ├── Dockerfile
│   └── nginx.conf
└── docker-compose.yml
```

### Paso 3: Verificar Puertos Disponibles

Antes de levantar los contenedores, verifica que estos puertos estén libres:

- **Puerto 80**: Para el frontend (Nginx)
- **Puerto 8000**: Para el backend (FastAPI)
- **Puerto 3306**: Para MySQL
- **Puerto 27017**: Para MongoDB

**En Windows:**
```powershell
netstat -ano | findstr :80
netstat -ano | findstr :8000
netstat -ano | findstr :3306
netstat -ano | findstr :27017
```

Si algún puerto está en uso, tendrás que:
- Detener el servicio que lo está usando, o
- Modificar los puertos en `docker-compose.yml`

**En Linux/Mac:**
```bash
lsof -i :80
lsof -i :8000
lsof -i :3306
lsof -i :27017
```

## 🐳 Levantar los Contenedores Docker

### Paso 1: Abrir Terminal en la Carpeta del Proyecto

Navega a la carpeta raíz del proyecto (donde está el archivo `docker-compose.yml`):

**Windows (PowerShell):**
```powershell
cd "D:\A A A UNIVERSIDAD\Arquitectura de Software\PP1_01\PP1_01"
```

**Linux/Mac:**
```bash
cd /ruta/al/proyecto/PP1_01
```

### Paso 2: Construir y Levantar los Contenedores

Ejecuta el siguiente comando para construir las imágenes y levantar todos los servicios:

```bash
docker-compose up -d
```

**¿Qué hace este comando?**
- `docker-compose up`: Levanta todos los servicios definidos en docker-compose.yml
- `-d`: Ejecuta en modo "detached" (en segundo plano), para que puedas seguir usando la terminal

**Primera vez que ejecutas esto:**
- Descargará las imágenes base (Python, Nginx, MySQL, MongoDB)
- Construirá las imágenes personalizadas del backend y frontend
- Creará los volúmenes para persistencia de datos
- Creará la red Docker para comunicación entre contenedores
- Esto puede tomar varios minutos la primera vez

### Paso 3: Verificar que los Contenedores Estén Corriendo

Ejecuta:

```bash
docker-compose ps
```

Deberías ver algo como:

```
NAME                STATUS          PORTS
backend_siglab      Up (healthy)     0.0.0.0:8000->8000/tcp
frontend_siglab     Up               0.0.0.0:80->80/tcp
mongo_siglab        Up (healthy)     0.0.0.0:27017->27017/tcp
mysql_siglab        Up (healthy)    0.0.0.0:3306->3306/tcp
```

Todos los contenedores deberían estar en estado "Up". Si alguno dice "Restarting" o "Exited", hay un problema.

### Paso 4: Ver los Logs (Opcional pero Recomendado)

Para ver qué está pasando en los contenedores:

```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f mysql
docker-compose logs -f mongodb
docker-compose logs -f frontend
```

**Busca estos mensajes en los logs del backend:**
- `¡ÉXITO! MySQL configurado (Máquinas y Usuarios) listo. :V`
- `¡Conexión a MongoDB establecida con éxito! :V`
- `Application startup complete.`

Si ves errores, anótalos para solucionarlos.

## 🌐 Acceder a la Aplicación

Una vez que todos los contenedores estén corriendo:

1. **Frontend (Interfaz Web):**
   - Abre tu navegador
   - Ve a: `http://localhost`
   - Deberías ver la página de login

2. **Backend API (Directo):**
   - Ve a: `http://localhost:8000`
   - Deberías ver la documentación de FastAPI (Swagger UI)
   - O ve a: `http://localhost:8000/docs` para la interfaz interactiva

3. **Credenciales por Defecto:**
   - Usuario: `admin`
   - Contraseña: `12345`

## 🔧 Comandos Útiles de Docker Compose

### Ver el Estado de los Contenedores
```bash
docker-compose ps
```

### Ver los Logs en Tiempo Real
```bash
docker-compose logs -f
```

### Detener los Contenedores (sin eliminar datos)
```bash
docker-compose stop
```

### Iniciar Contenedores Detenidos
```bash
docker-compose start
```

### Reiniciar un Contenedor Específico
```bash
docker-compose restart backend
```

### Detener y Eliminar Contenedores
```bash
docker-compose down
```

### Detener y Eliminar Contenedores + Volúmenes (⚠️ BORRA LOS DATOS)
```bash
docker-compose down -v
```

### Reconstruir las Imágenes (si cambiaste código)
```bash
docker-compose build
docker-compose up -d
```

O en un solo comando:
```bash
docker-compose up -d --build
```

### Entrar a un Contenedor (para debugging)
```bash
# Entrar al contenedor del backend
docker-compose exec backend bash

# Entrar al contenedor de MySQL
docker-compose exec mysql bash

# Entrar al contenedor de MongoDB
docker-compose exec mongodb bash
```

## 🗄️ Acceso a las Bases de Datos

### MySQL

**Desde tu máquina local:**
- Host: `localhost`
- Puerto: `3306`
- Usuario: `root`
- Contraseña: `Clubpengui1`
- Base de datos: `proyecto_maquinas`

**Desde dentro de un contenedor:**
- Host: `mysql` (nombre del servicio en docker-compose)
- Puerto: `3306`
- Usuario: `root`
- Contraseña: `Clubpengui1`

**Conectarse desde terminal:**
```bash
docker-compose exec mysql mysql -u root -pClubpengui1 proyecto_maquinas
```

### MongoDB

**Desde tu máquina local:**
- Host: `localhost`
- Puerto: `27017`
- Base de datos: `siglab_db`

**Desde dentro de un contenedor:**
- Host: `mongodb` (nombre del servicio)
- Puerto: `27017`

**Conectarse desde terminal:**
```bash
docker-compose exec mongodb mongosh siglab_db
```

## 🐛 Solución de Problemas Comunes

### Problema 1: "Port already in use" (Puerto ya en uso)

**Solución:**
1. Identifica qué programa está usando el puerto
2. Detén ese programa o cambia el puerto en `docker-compose.yml`

Ejemplo para cambiar el puerto del frontend a 8080:
```yaml
frontend:
  ports:
    - "8080:80"  # Cambia 80 por 8080
```

### Problema 2: Contenedor se reinicia constantemente (Restarting)

**Solución:**
1. Revisa los logs: `docker-compose logs nombre_contenedor`
2. Busca errores en los logs
3. Verifica que las variables de entorno estén correctas
4. Verifica que los archivos necesarios existan

### Problema 3: "Cannot connect to database"

**Solución:**
1. Verifica que MySQL/MongoDB estén en estado "healthy":
   ```bash
   docker-compose ps
   ```
2. Espera unos segundos más (las bases de datos tardan en iniciar)
3. Revisa los logs de las bases de datos:
   ```bash
   docker-compose logs mysql
   docker-compose logs mongodb
   ```

### Problema 4: Cambios en el código no se reflejan

**Solución:**
1. Los volúmenes están montados, así que los cambios deberían verse automáticamente
2. Si no, reinicia el contenedor:
   ```bash
   docker-compose restart backend
   ```
3. O reconstruye la imagen:
   ```bash
   docker-compose up -d --build backend
   ```

### Problema 5: "No space left on device"

**Solución:**
1. Limpia imágenes y contenedores no usados:
   ```bash
   docker system prune -a
   ```
2. Elimina volúmenes no usados (⚠️ cuidado, borra datos):
   ```bash
   docker volume prune
   ```

## 📁 Estructura del Proyecto

```
PP1_01/
├── backend/                 # Backend FastAPI
│   ├── app/
│   │   ├── daos/           # Data Access Objects
│   │   ├── database/       # Configuración de bases de datos
│   │   ├── models/         # Modelos de datos
│   │   ├── routes/         # Rutas de la API
│   │   └── services.py     # Lógica de negocio
│   ├── main.py             # Punto de entrada
│   ├── requirements.txt    # Dependencias Python
│   └── Dockerfile          # Imagen Docker del backend
│
├── frontend/               # Frontend estático
│   ├── static/
│   │   ├── css/           # Estilos
│   │   ├── javascript/    # Scripts JS
│   │   └── img/           # Imágenes
│   ├── templates/         # Plantillas HTML
│   ├── Dockerfile         # Imagen Docker del frontend
│   └── nginx.conf         # Configuración de Nginx
│
└── docker-compose.yml     # Orquestación de servicios
```

## 🔐 Variables de Entorno

Las variables de entorno están configuradas en `docker-compose.yml`. Si necesitas cambiarlas:

**MySQL:**
- `MYSQL_ROOT_PASSWORD`: Contraseña del root (por defecto: `Clubpengui1`)
- `MYSQL_DATABASE`: Nombre de la base de datos (por defecto: `proyecto_maquinas`)

**MongoDB:**
- Se conecta automáticamente, no requiere configuración adicional

**Backend:**
- `MYSQL_HOST`: Host de MySQL (por defecto: `mysql`)
- `MYSQL_USER`: Usuario de MySQL (por defecto: `root`)
- `MYSQL_PASSWORD`: Contraseña de MySQL
- `MYSQL_DATABASE`: Base de datos MySQL
- `MONGO_HOST`: Host de MongoDB (por defecto: `mongodb`)
- `MONGO_PORT`: Puerto de MongoDB (por defecto: `27017`)

## 📝 Notas Importantes

1. **Persistencia de Datos:** Los datos se guardan en volúmenes Docker. Si ejecutas `docker-compose down -v`, se eliminarán todos los datos.

2. **Red Docker:** Todos los contenedores están en la misma red (`siglab_network`) y se comunican usando los nombres de los servicios (mysql, mongodb, backend, frontend).

3. **Healthchecks:** MySQL y MongoDB tienen healthchecks configurados. El backend espera a que ambos estén "healthy" antes de iniciar.

4. **Reinicio Automático:** Todos los contenedores tienen `restart: always`, por lo que se reiniciarán automáticamente si se caen.

## 🆘 Obtener Ayuda

Si tienes problemas:

1. Revisa los logs: `docker-compose logs -f`
2. Verifica el estado: `docker-compose ps`
3. Consulta la documentación de Docker: https://docs.docker.com/
4. Consulta la documentación de Docker Compose: https://docs.docker.com/compose/

## ✅ Checklist de Verificación

Antes de considerar que todo está funcionando:

- [ ] Docker y Docker Compose están instalados
- [ ] Los puertos 80, 8000, 3306, 27017 están libres
- [ ] `docker-compose up -d` se ejecutó sin errores
- [ ] Todos los contenedores están en estado "Up"
- [ ] Puedo acceder a `http://localhost` en el navegador
- [ ] Puedo acceder a `http://localhost:8000/docs` (documentación de la API)
- [ ] Los logs del backend muestran "MySQL configurado" y "MongoDB establecida"
- [ ] Puedo hacer login con usuario `admin` y contraseña `12345`

---

**¡Listo!** Tu aplicación debería estar funcionando. Si encuentras algún problema, revisa la sección de "Solución de Problemas Comunes" arriba.
