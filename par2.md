## ⚙️ Configuración de Infraestructura
### 🌐 Nginx Frontend (nginx.conf)
*Propósito:* Servir archivos estáticos del frontend y redirigir peticiones API al backend

*Configuración principal:*
nginx
# Puerto principal para usuarios
listen 81;

# Servir archivos estáticos
location / {
    root /usr/share/nginx/html;
    index index.html;
}

# Redirigir peticiones API a backend
location /api/ {
    proxy_pass http://api_backend;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}


*Explicación línea por línea:*
- *listen 81;*: Escucha peticiones en el puerto 81 interno del contenedor
- *location / {*: Bloque para manejar todas las peticiones a la raíz (/)
- *root /usr/share/nginx/html;*: Directorio base donde están los archivos HTML/CSS/JS
- *index index.html;*: Archivo por defecto cuando se accede a /
- *location /api/ {*: Bloque específico para peticiones que empiezan con /api/
- *proxy_pass http://api_backend;*: Redirige peticiones al grupo de servidores backend
- *proxy_set_header Host $host;*: Conserva el nombre del host original
- *proxy_set_header X-Real-IP $remote_addr;*: Pasa IP real del cliente al backend
- *proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;*: Cadena de IPs para traceo
- *proxy_set_header X-Forwarded-Proto $scheme;*: Mantiene protocolo HTTP/HTTPS original

*Funcionalidades:*
- *Servir HTML/CSS/JavaScript:* Archivos estáticos del frontend
- *Reverse Proxy:* Redirige /api/* a los servidores backend
- *Headers estándar:* Configuración básica de proxy

---

### 🐳 Dockerfile (Frontend)
*Propósito:* Crear imagen Docker para contenedor del frontend con Nginx

dockerfile
# Imagen base de Nginx
FROM nginx:alpine

# Copiar archivos estáticos
COPY static/ /usr/share/nginx/html/static/
COPY templates/ /usr/share/nginx/html/templates/

# Copiar configuración de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponer puerto
EXPOSE 81


*Componentes incluidos:*
- *Nginx Alpine:* Imagen ligera y optimizada
- *Archivos estáticos:* HTML, CSS, JavaScript del frontend
- *Configuración nginx.conf:* Reglas de enrutamiento
- *Puerto 81:* Puerto interno para el servicio

---

### 🐳 Dockerfile (Backend)
*Propósito:* Crear imagen Docker para contenedor de la API FastAPI

dockerfile
# Imagen base de Python
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Actualizar pip e instalar dependencias Python
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout=60 -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


*Explicación línea por línea:*
- *FROM python:3.11-slim*: Imagen base Python ligera
- *WORKDIR /app*: Directorio de trabajo dentro del contenedor
- *apt-get install gcc default-libmysqlclient-dev*: Dependencias para MySQL connector
- *pip install --upgrade pip*: Actualizar pip para mejor compatibilidad
- *COPY requirements.txt .*: Copiar archivo de dependencias
- *pip install -r requirements.txt*: Instalar paquetes Python (FastAPI, MySQL, Redis, etc.)
- *COPY . .*: Copiar todo el código del backend
- *EXPOSE 8000*: Puerto de la API FastAPI
- *CMD ["uvicorn"...]*: Comando para iniciar el servidor FastAPI

*Componentes incluidos:*
- *Python 3.11:* Runtime del backend
- *Dependencias sistema:* Compilador y librerías MySQL
- *Paquetes Python:* FastAPI, MySQL connector, Redis, MongoDB, etc.
- *Código aplicación:* Todo el backend (routes, services, daos, models)
- *Uvicorn:* Servidor ASGI para FastAPI

---

### 🐳 Docker Compose (docker-compose.yml)
*Propósito:* Orquestar (dirige y coordina) todos los servicios del sistema en contenedores

*Servicios principales:*
yaml
services:
  # Base de datos MySQL
  mysql:
    image: mysql:8.0                    # Usa imagen oficial MySQL versión 8.0
    container_name: mysql_siglab        # Nombre fijo del contenedor
    ports: ["13306:3306"]               # Mapea puerto 13306 local a 3306 del contenedor
    environment:                        # Variables de entorno para configuración
      MYSQL_ROOT_PASSWORD: Clubpengui1  # Contraseña del usuario root
      MYSQL_DATABASE: proyecto_maquinas # Nombre de la base de datos

  # Cache Redis
  redis:
    image: redis:7.2-alpine             # Imagen Redis ligera Alpine
    container_name: redis_siglab        # Nombre fijo del contenedor
    ports: ["16379:6379"]               # Mapea puerto 16379 local a 6379 del contenedor
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru  # Limita memoria a 256MB y elimina datos menos usados

  # 3 Servidores API Backend
  api_back_1:
    build: ./backend                     # Construye imagen desde Dockerfile del backend
    container_name: api_back_1          # Nombre fijo del contenedor
    ports: ["18001:8000"]               # Mapea puerto 18001 local a 8000 del contenedor
    environment:                         # Variables de entorno específicas del servidor
      API_SERVER_ID: "Servidor API 1"  # Identificador único para logs
      REDIS_HOST: redis                  # Nombre del servicio Redis para conexión
      MYSQL_HOST: mysql                  # Nombre del servicio MySQL para conexión

  api_back_2:
    build: ./backend                     # Construye imagen desde Dockerfile del backend
    container_name: api_back_2          # Nombre fijo del contenedor
    ports: ["18002:8000"]               # Mapea puerto 18002 local a 8000 del contenedor
    environment:
      API_SERVER_ID: "Servidor API 2"  # Identificador único para logs

  api_back_3:
    build: ./backend                     # Construye imagen desde Dockerfile del backend
    container_name: api_back_3          # Nombre fijo del contenedor
    ports: ["18003:8000"]               # Mapea puerto 18003 local a 8000 del contenedor
    environment:
      API_SERVER_ID: "Servidor API 3"  # Identificador único para logs

  # Load Balancer + Frontend
  nginx_balancer:
    build: ./frontend                    # Construye imagen desde Dockerfile del frontend
    container_name: nginx_balancer_siglab # Nombre fijo del contenedor
    ports: ["8080:81"]                  # Puerto principal para usuarios (8080 local a 81 contenedor)
    depends_on: [api_back_1, api_back_2, api_back_3]  # Espera a que APIs inicien primero


*Características clave:*
- *7 servicios totales:* 3 APIs + 3 bases de datos + 1 load balancer
- *Red interna:* Comunicación entre contenedores
- *Volúmenes persistentes:* Datos guardados en disco local

*Puertos de acceso:*
- *Frontend principal:* http://localhost:8080
- *API Server 1:* http://localhost:18001
- *API Server 2:* http://localhost:18002
- *API Server 3:* http://localhost:18003
- *MySQL:* localhost:13306
- *Redis:* localhost:16379























## 🔄 *Flujo de Arquitectura por Funcionalidad*

### 🖥️ *1. Agregar Máquina*

*Flujo en Tiempo Real:*
1. *Frontend:* formulario.js → Captura datos del formulario
2. *API:* maquina.py → POST /api/maquinas/agregar
3. *Service:* maquina_service.py → Validación y lógica de negocio
4. *DAO:* maquina_dao.py → Inserción en MySQL
5. *Cache:* redis.py → Invalida (borra informacion vieja) caché de máquinas
6. *Real-time:* dashboard.js → Polling detecta nuevo registro

*Código Clave:*
python
# backend/app/routes/maquina.py
@router.post("/agregar")
async def agregar_maquina(maquina: MaquinaCreate):
    # Validación y registro
    resultado, error = maquina_service.registrar_maquina(maquina.dict())
    return {"status": "ok", "mensaje": "Máquina agregada"}

# backend/app/services/maquina_service.py
def registrar_maquina(self, datos_dict):
    # 1. Validar datos
    codigo = datos_dict.get("codigo_equipo")
    if not codigo or codigo.strip() == "":
        return None, "El código de la máquina es obligatorio"
    
    # 2. Verificar que no exista
    maquina_existente = self._maquina_dao.buscar_por_codigo(codigo)
    if maquina_existente:
        return None, f"El código '{codigo}' ya existe"
    
    # 3. Crear objeto máquina según tipo
    if tipo == "PC":
        nueva_maquina = Computadora(codigo, estado, area, fecha_obj, usuario_str)
    elif tipo == "IMP":
        nueva_maquina = Impresora(codigo, estado, area, fecha_obj, usuario_str)
    
    # 4. Guardar en MySQL
    resultado = self._maquina_dao.guardar(nueva_maquina)
    
    if resultado:
        # 5. INVALIDAR cache del sistema (CÓDIGO REAL)
        DatabaseManager.limpiar_cache_sistema()
        return nueva_maquina, "Máquina registrada correctamente"


---









