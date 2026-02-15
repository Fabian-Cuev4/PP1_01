# Backend - API FastAPI

## Descripción
API RESTful construida con FastAPI para gestionar el sistema de laboratorios SIGLAB.

## Tecnologías
- **Python 3.11**: Lenguaje principal
- **FastAPI**: Framework web moderno y rápido
- **MySQL**: Base de datos relacional para máquinas y usuarios
- **MongoDB**: Base de datos NoSQL para mantenimientos
- **Pydantic**: Validación de datos
- **SQLAlchemy**: ORM para MySQL
- **Motor**: Motor asíncrono para MongoDB

## Estructura del Proyecto

```
backend/
├── main.py              # Entry point y configuración principal
├── routes/              # Endpoints de la API
│   ├── auth.py         # Autenticación y usuarios
│   ├── maquina.py      # Gestión de máquinas
│   └── mantenimiento.py # Gestión de mantenimientos
├── services/            # Lógica de negocio
│   ├── usuario_service.py
│   ├── maquina_service.py
│   └── mantenimiento_service.py
├── models/              # Modelos de datos
│   ├── usuario.py
│   ├── maquina.py
│   └── mantenimiento.py
├── dao/                 # Data Access Objects
│   ├── usuario_dao.py
│   ├── maquina_dao.py
│   └── mantenimiento_dao.py
├── database/            # Configuración de bases de datos
│   ├── mysql.py
│   └── mongodb.py
└── requirements.txt      # Dependencias del proyecto
```

## Endpoints Principales

### Autenticación
- `POST /api/login` - Iniciar sesión
- `POST /api/register` - Registrar usuario

### Máquinas
- `GET /api/maquinas/listar` - Listar todas las máquinas
- `POST /api/maquinas/agregar` - Agregar nueva máquina
- `GET /api/maquinas/buscar` - Buscar máquina por ID
- `PUT /api/maquinas/actualizar` - Actualizar máquina
- `DELETE /api/maquinas/eliminar` - Eliminar máquina
- `GET /api/maquinas/dashboard` - Dashboard de máquinas

### Mantenimientos
- `GET /api/mantenimientos/historial` - Ver historial
- `POST /api/mantenimientos/agregar` - Agregar mantenimiento
- `GET /api/mantenimientos/informe` - Generar informe
- `GET /api/mantenimientos/todos` - Listar todos

## Variables de Entorno

```bash
# MySQL
MYSQL_HOST=mysql
MYSQL_USER=root
MYSQL_PASSWORD=Clubpengui1
MYSQL_DATABASE=proyecto_maquinas
MYSQL_PORT=3306

# MongoDB
MONGODB_HOST=mongodb
MONGODB_PORT=27017
MONGODB_DATABASE=mantenimientos

# API
HOST=0.0.0.0
PORT=8000
```

## Instalación y Ejecución

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar localmente
uvicorn main:app --host 0.0.0.0 --port 8000

# Ejecutar con Docker
docker build -t siglab-backend .
docker run -p 8000:8000 siglab-backend
```

## Configuración para Producción

- **Workers**: Configurar múltiples workers para alta concurrencia
- **Logging**: Implementar logging estructurado
- **Security**: Añadir middleware de seguridad
- **CORS**: Configurar orígenes permitidos

## Testing

```bash
# Ejecutar tests
pytest

# Ejecutar con cobertura
pytest --cov=.
```

## Deploy

El backend está diseñado para:
- **Docker**: Contenerización completa
- **Load Balancer**: Balanceo con Nginx
- **Escalabilidad**: Múltiples réplicas
- **High Availability**: Failover automático
