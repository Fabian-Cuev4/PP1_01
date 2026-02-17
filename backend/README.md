# Backend - API FastAPI Distribuida

## 📋 Descripción
API RESTful asíncrona construida con FastAPI para el sistema de gestión de laboratorios SIGLAB. Diseñada para arquitectura distribuida con load balancer y caché Redis.

## 🏗️ Arquitectura del Backend

```
┌─────────────────────────────────────────────────────────┐
│                    Backend Layer                        │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  Backend 1  │  │  Backend 2  │  │  Backend 3  │     │
│  │  :8000      │  │  :8000      │  │  :8000      │     │
│  │  FastAPI    │  │  FastAPI    │  │  FastAPI    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
    ┌─────────▼───┐ ┌──────▼──────┐ ┌───▼─────────┐
    │   MySQL     │ │   MongoDB   │ │    Redis    │
    │  (Persist)  │ │  (Logs)     │ │  (Cache)    │
    │   :13306    │ │   :27018    │ │    :6379    │
    └─────────────┘ └─────────────┘ └─────────────┘
```

## 🛠️ Stack Tecnológico

### Core
- **Python 3.11**: Lenguaje principal con tipado estático
- **FastAPI**: Framework web asíncrono de alto rendimiento
- **Uvicorn**: Servidor ASGI para producción
- **Pydantic**: Validación y serialización de datos

### Base de Datos
- **MySQL 8.0**: Datos estructurados (máquinas, usuarios)
- **MongoDB**: Datos NoSQL (mantenimientos, logs)
- **Redis**: Caché distribuida con TTL 60s

### Conectores
- **SQLAlchemy**: ORM asíncrono para MySQL
- **Motor**: Driver asíncrono para MongoDB
- **Redis-py**: Cliente Redis con connection pooling

## 📁 Estructura del Proyecto

```
backend/
├── app/
│   ├── daos/                    # Data Access Objects
│   │   ├── usuario_dao.py      # Acceso a datos de usuarios
│   │   ├── maquina_dao.py      # Acceso a datos de máquinas
│   │   └── mantenimiento_dao.py # Acceso a mantenimientos
│   ├── database/                # Configuración de bases de datos
│   │   ├── mysql.py            # Conexión y pool MySQL
│   │   ├── mongodb.py          # Conexión MongoDB
│   │   ├── redis.py            # Conexión Redis
│   │   └── database_manager.py # Orquestación de DBs
│   ├── dtos/                    # Data Transfer Objects
│   │   ├── usuario_dto.py      # DTOs de usuarios
│   │   ├── maquina_dto.py      # DTOs de máquinas
│   │   └── mantenimiento_dto.py # DTOs de mantenimientos
│   ├── routes/                  # Endpoints de la API
│   │   ├── auth.py             # Autenticación y usuarios
│   │   ├── maquina.py          # Gestión de máquinas
│   │   └── mantenimiento.py    # Gestión de mantenimientos
│   └── services/                # Lógica de negocio
│       ├── usuario_service.py  # Servicios de usuarios
│       ├── maquina_service.py  # Servicios de máquinas
│       └── mantenimiento_service.py # Servicios de mantenimientos
├── main.py                      # Entry point y configuración
├── requirements.txt             # Dependencias Python
├── Dockerfile                   # Imagen Docker
└── .dockerignore               # Exclusiones Docker
```

## 🚀 Endpoints de la API

### Autenticación (`/api/auth`)
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/register` - Registrar usuario
- `GET /api/auth/usuarios/activos` - Usuarios activos (cache Redis)

### Máquinas (`/api/maquinas`)
- `GET /api/maquinas/listar` - Listar todas las máquinas
- `POST /api/maquinas/agregar` - Agregar nueva máquina
- `GET /api/maquinas/buscar` - Buscar máquina por ID
- `PUT /api/maquinas/actualizar` - Actualizar máquina existente
- `DELETE /api/maquinas/eliminar` - Eliminar máquina
- `GET /api/maquinas/dashboard` - Datos para dashboard

### Mantenimientos (`/api/mantenimientos`)
- `GET /api/mantenimientos/historial/{codigo}` - Historial por máquina
- `POST /api/mantenimientos/agregar` - Agregar mantenimiento
- `GET /api/mantenimientos/informe` - Generar informe
- `GET /api/mantenimientos/todos` - Listar todos los mantenimientos

### Sistema (`/api/sistema`)
- `GET /api/sistema/health` - Health check del servicio
- `GET /api/sistema/metrics` - Métricas del sistema

## ⚙️ Configuración

### Variables de Entorno
```bash
# Configuración MySQL
MYSQL_HOST=mysql
MYSQL_USER=root
MYSQL_PASSWORD=Clubpengui1
MYSQL_DATABASE=proyecto_maquinas
MYSQL_PORT=3306

# Configuración MongoDB
MONGO_HOST=mongodb
MONGO_PORT=27017
MONGO_DATABASE=mantenimientos

# Configuración Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_TTL=60

# Configuración del Servidor
HOST=0.0.0.0
PORT=8000
SERVER_ID=1  # ID único para identificación en dashboard
```

### Configuración de Producción
```yaml
# docker-compose.yml
environment:
  - WORKERS=4
  - MAX_CONNECTIONS=100
  - TIMEOUT=30
  - KEEP_ALIVE=2
```

## 🔄 Flujo de Datos

### Request Lifecycle
1. **Cliente** → Nginx Load Balancer
2. **Nginx** → Backend específico (basado en algoritmo)
3. **Backend** → Redis (caché) si existe
4. **Backend** → MySQL/MongoDB si no hay caché
5. **Backend** → Redis (actualizar caché)
6. **Backend** → Respuesta al cliente

### Cache Strategy
- **TTL**: 60 segundos para sincronización entre réplicas
- **Invalidación**: Automática por tiempo
- **Patrón**: Cache-Aside con write-through

## 🚀 Despliegue

### Desarrollo Local
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar con recarga automática
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Con variables de entorno
export MYSQL_HOST=localhost && uvicorn main:app --reload
```

### Docker
```bash
# Construir imagen
docker build -t siglab-backend .

# Ejecutar contenedor
docker run -p 8000:8000 siglab-backend

# Con docker-compose
docker-compose up --build backend-1
```

### Producción
```bash
# Múltiples workers
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Con Gunicorn (alternativa)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🧪 Testing

### Tests Unitarios
```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=app --cov-report=html

# Tests específicos
pytest tests/test_auth.py -v
```

### Tests de Integración
```bash
# Tests de API
pytest tests/integration/test_api.py

# Tests de base de datos
pytest tests/integration/test_database.py
```

### Tests de Carga
```bash
# Con k6
docker-compose --profile load-test up k6-saturator

# Monitoring en tiempo real
docker-compose logs -f k6-saturator
```

## 📊 Monitoreo y Métricas

### Health Checks
```bash
# Salud del servicio
curl http://localhost:8000/api/sistema/health

# Métricas del sistema
curl http://localhost:8000/api/sistema/metrics
```

### Logs Estructurados
```python
# Configuración de logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
```

### Métricas Importantes
- **Response Time**: P95 < 500ms
- **Throughput**: > 100 req/s por instancia
- **Error Rate**: < 0.1%
- **Memory Usage**: < 512MB por contenedor

## 🔧 Optimización

### Base de Datos
- **Connection Pooling**: 10-20 conexiones por DB
- **Indexación**: Primary keys y foreign keys
- **Query Optimization**: SELECT específicos, no SELECT *

### Caché Redis
- **TTL Óptimo**: 60s para sincronización
- **Memory Management**: LRU eviction policy
- **Connection Pool**: 5-10 conexiones

### API Performance
- **Async/Await**: Para todas las operaciones I/O
- **Response Compression**: gzip para respuestas > 1KB
- **CORS**: Configurado para orígenes específicos

## 🚨 Troubleshooting

### Problemas Comunes

#### 1. Conexión a MySQL fallida
```bash
# Verificar conexión
docker exec -it mysql_siglab mysql -u root -p

# Revisar logs
docker-compose logs mysql
```

#### 2. Redis no responde
```bash
# Verificar Redis
docker exec -it redis redis-cli ping

# Limpiar caché
docker exec -it redis redis-cli FLUSHALL
```

#### 3. Alto uso de memoria
```bash
# Monitorear recursos
docker stats pp1_01-backend-1

# Reiniciar servicio
docker-compose restart backend-1
```

### Debug Mode
```bash
# Ejecutar con debug
uvicorn main:app --reload --log-level debug

# Ver logs detallados
docker-compose logs -f backend-1 | grep ERROR
```

## 🔒 Seguridad

### Autenticación
- **Hashing**: bcrypt para contraseñas
- **JWT**: Tokens con expiración
- **Session Management**: Redis para sesiones activas

### Validación
- **Input Validation**: Pydantic models
- **SQL Injection**: SQLAlchemy ORM protection
- **XSS Protection**: Headers de seguridad

### Headers de Seguridad
```python
# middleware.py
app.add_middleware(
    SecurityHeadersMiddleware,
    headers={
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block"
    }
)
```

## 📈 Escalabilidad

### Horizontal Scaling
```bash
# Escalar backends
docker-compose up --scale backend-1=2 --scale backend-2=2 --scale backend-3=2 -d

# Verificar distribución
docker-compose ps
```

### Vertical Scaling
```yaml
# docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 1G
    reservations:
      cpus: '0.5'
      memory: 512M
```

## 🔄 Ciclo de Vida de Desarrollo

### Git Workflow
```bash
# Feature branch
git checkout -b feature/nueva-funcionalidad

# Commits atómicos
git add .
git commit -m "feat: agregar endpoint de usuarios"

# Pull request con tests
git push origin feature/nueva-funcionalidad
```

### CI/CD Pipeline
```yaml
# .github/workflows/ci.yml
name: CI/CD Backend
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest --cov=app
      - name: Build Docker
        run: docker build -t siglab-backend .
```

## 📝 Mejores Prácticas

### Código
- **Type Hints**: Para todas las funciones
- **Docstrings**: Google style para documentación
- **Error Handling**: Excepciones específicas
- **Logging**: Estructurado y con niveles

### Performance
- **Async**: Para operaciones I/O
- **Connection Pooling**: Reutilizar conexiones
- **Batch Operations**: Múltiples registros en una transacción
- **Pagination**: Para listados grandes

### Seguridad
- **Principle of Least Privilege**: Mínimos permisos
- **Environment Variables**: Datos sensibles fuera del código
- **Regular Updates**: Dependencias actualizadas
- **Security Headers**: Headers HTTP de seguridad

---

**Versión**: 2.0.0  
**Estado**: Producción  
**Última Actualización**: 2026
