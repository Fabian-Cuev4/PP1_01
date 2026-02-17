# SIGLAB - Sistema de Gestión de Laboratorios

Sistema web distribuido para gestionar máquinas (computadoras e impresoras) y sus mantenimientos en laboratorios de la Universidad Central del Ecuador.

## 🚀 Características Principales

- **Gestión Completa**: Registro, seguimiento y mantenimiento de equipos
- **Arquitectura Distribuida**: 3 backends con load balancer Nginx
- **Monitoreo en Tiempo Real**: Dashboard con visualización de carga
- **Testing de Carga**: Pruebas automatizadas con k6
- **Base de Datos Híbrida**: MySQL + MongoDB para diferentes propósitos
- **Resiliente**: Failover automático y health checks

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Dashboard     │    │   k6 Testing    │
│   (React/Vite)  │    │   (WebSocket)   │    │   (Load Test)   │
│   :18080        │    │   :18081        │    │   (Headless)    │
└─────────┬───────┘    └─────────┬───────┘    └─────────────────┘
          │                      │                      
          │              ┌───────┴───────┐              
          │              │   Nginx       │              
          │              │ Load Balancer │              
          │              │     :8888     │              
          │              └───────┬───────┘              
          │                      │                      
          │        ┌─────────────┼─────────────┐        
          │        │             │             │        
          │  ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐  
          │  │ Backend 1 │ │ Backend 2 │ │ Backend 3 │  
          │  │ :8000     │ │ :8000     │ │ :8000     │  
          └──┤ (FastAPI) ├─┤ (FastAPI) ├─┤ (FastAPI) ├──
             └───────────┘ └───────────┘ └───────────┘
                   │             │             │
          ┌────────┴────────┐ ┌──┴────────────┴──┐
          │   MySQL         │ │   MongoDB        │
          │   :13306        │ │   :27018         │
          └─────────────────┘ └──────────────────┘
```

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.11**: Lenguaje principal
- **FastAPI**: Framework web asíncrono
- **MySQL**: Base de datos relacional (máquinas, usuarios)
- **MongoDB**: Base de datos NoSQL (mantenimientos, logs)
- **Redis**: Caché distribuida (TTL 60s)

### Frontend
- **React**: Framework JavaScript moderno
- **Vite**: Build tool rápido
- **TailwindCSS**: Framework de estilos
- **Chart.js**: Visualización de datos

### Infraestructura
- **Nginx**: Load balancer con 4 algoritmos
- **Docker**: Contenerización completa
- **Docker Compose**: Orquestación de servicios
- **k6**: Testing de carga y rendimiento

## 🚀 Inicio Rápido

### Requisitos Previos
- Docker Desktop instalado
- 4GB RAM mínima
- 10GB espacio en disco

### Ejecución del Sistema

```bash
# Clonar el repositorio
git clone <repository-url>
cd PP1_01

# Iniciar todos los servicios (producción)
docker-compose --profile all up -d

# Verificar estado
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f
```

### Acceso a los Servicios

- **Aplicación Principal**: http://localhost:18080
- **Dashboard de Monitoreo**: http://localhost:18081
- **API Balanceada**: http://localhost:8888
- **Health Check**: http://localhost:8888/health
- **Estadísticas Nginx**: http://localhost:8080/nginx_status

### Credenciales por Defecto
- **Usuario**: `admin`
- **Contraseña**: `admin123`

## 📊 Dashboard de Monitoreo

El sistema incluye un dashboard en tiempo real que muestra:

- **Distribución de Carga**: Visualización de peticiones por backend
- **Estado de Servidores**: Salud y disponibilidad
- **Métricas en Tiempo Real**: Requests por segundo, tasa de errores
- **Alertas Visuales**: Indicadores de problemas

Características del dashboard:
- Auto-reset después de 7s de inactividad
- Detección automática de nuevos servidores
- WebSocket para actualizaciones en vivo
- Integración con logs de Nginx

## ⚖️ Load Balancer

Nginx configura el balanceo de carga con múltiples algoritmos:

### Algoritmos Disponibles
1. **Round Robin**: Distribución equitativa (por defecto)
2. **Least Connections**: Servidor con menos conexiones activas
3. **IP Hash**: Mismo cliente siempre al mismo servidor
4. **Weighted Round Robin**: Distribución según capacidades

### Configuración Actual
- **Algoritmo**: Weighted Round Robin
- **Pesos**: Backend-1 (3), Backend-2 (2), Backend-3 (3)
- **Failover**: Detección automática de servidores caídos
- **Health Checks**: Verificación cada 30s

### Cambiar Algoritmo
```bash
# Editar configuración
vim nginx/nginx.conf

# Reiniciar Nginx
docker-compose restart nginx
```

## 🧪 Testing de Carga

Suite de pruebas automatizadas con k6:

```bash
# Ejecutar pruebas de saturación
docker-compose --profile load-test up --build k6-saturator

# Monitorear resultados
docker-compose logs -f k6-saturator
```

### Métricas Evaluadas
- **Throughput**: Requests por segundo
- **Latencia**: Tiempos de respuesta (P95 < 500ms)
- **Error Rate**: Tasa de fallos (< 0.1%)
- **Distribución**: Balanceo entre backends

## 📁 Estructura del Proyecto

```
PP1_01/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── daos/           # Data Access Objects
│   │   ├── database/       # Configuración DB
│   │   ├── dtos/           # Data Transfer Objects
│   │   ├── routes/         # Endpoints API
│   │   └── services/       # Lógica de negocio
│   ├── main.py             # Entry point
│   └── requirements.txt    # Dependencias
├── frontend/               # Aplicación React
│   ├── src/
│   │   ├── components/     # Componentes UI
│   │   ├── pages/          # Páginas principales
│   │   └── App.jsx         # App principal
│   ├── package.json        # Dependencias npm
│   └── vite.config.js      # Configuración Vite
├── dashboard/              # Dashboard monitoreo
│   ├── server.py           # Servidor WebSocket
│   ├── index.html          # Interfaz web
│   └── requirements.txt    # Dependencias Python
├── nginx/                  # Load balancer
│   ├── nginx.conf          # Configuración principal
│   └── Dockerfile          # Imagen Nginx
├── k6/                     # Testing de carga
│   ├── maquina-saturator.js # Script principal
│   └── Dockerfile          # Imagen k6
└── docker-compose.yml      # Orquestación completa
```

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# MySQL
MYSQL_HOST=mysql
MYSQL_USER=root
MYSQL_PASSWORD=Clubpengui1
MYSQL_DATABASE=proyecto_maquinas

# MongoDB
MONGO_HOST=mongodb
MONGO_PORT=27017
MONGO_DATABASE=mantenimientos

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
```

### Escalabilidad
```bash
# Escalar backends
docker-compose up --scale backend-1=2 --scale backend-2=2 --scale backend-3=2 -d

# Añadir nuevo backend
# 1. Editar nginx.conf para incluir nuevo servidor
# 2. Reiniciar nginx
docker-compose restart nginx
```

## 📈 Monitoreo y Logs

### Ver Logs Específicos
```bash
# Logs del load balancer
docker-compose logs -f nginx

# Logs de backends
docker-compose logs -f backend-1
docker-compose logs -f backend-2
docker-compose logs -f backend-3

# Logs del dashboard
docker-compose logs -f dashboard

# Logs de bases de datos
docker-compose logs -f mysql
docker-compose logs -f mongodb
```

### Métricas Importantes
- **Disponibilidad**: > 99.9%
- **Tiempo Respuesta**: P95 < 500ms
- **Tasa Error**: < 0.1%
- **Concurrencia**: 100+ usuarios simultáneos

## 🔄 Ciclo de Vida de Desarrollo

### Desarrollo Local
```bash
# Modo desarrollo con hot reload
docker-compose --profile all up --build

# Ver cambios en tiempo real
# Frontend: Hot reload automático
# Backend: Recarga automática con cambios
```

### Producción
```bash
# Despliegue producción
docker-compose --profile all up -d --build

# Verificación salud
curl http://localhost:8888/health
```

### Testing
```bash
# Tests unitarios (backend)
docker-compose exec backend-1 pytest

# Tests de carga
docker-compose --profile load-test up --build k6-saturator

# Tests E2E (futuro)
# npm run test:e2e
```

## 🚨 Troubleshooting

### Problemas Comunes

#### 1. "host not found" en Nginx
```bash
# Limpiar redes Docker
docker network prune -f

# Reiniciar servicios
docker-compose down
docker-compose --profile all up -d
```

#### 2. Dashboard no muestra datos
```bash
# Verificar logs de Nginx
docker exec nginx_balancer tail -f /var/log/nginx/balanceo_siglab.log

# Reiniciar dashboard
docker-compose restart dashboard
```

#### 3. Conexiones rechazadas
```bash
# Verificar puertos en uso
netstat -tulpn | grep :18080

# Reiniciar servicios específicos
docker-compose restart frontend
```

### Comandos de Mantenimiento
```bash
# Limpiar sistema completo
docker-compose down --volumes --remove-orphans
docker system prune -f

# Reconstruir imágenes
docker-compose build --no-cache

# Backup de datos
docker exec mysql_siglab mysqldump -u root -pClubpengui1 proyecto_maquinas > backup.sql
```

## 🤝 Contribución

### Flujo de Trabajo
1. Fork del repositorio
2. Crear rama feature/nombre-feature
3. Commits descriptivos
4. Pull request con pruebas

### Estándares de Código
- **Python**: PEP 8, type hints
- **JavaScript**: ESLint, Prettier
- **Docker**: Multi-stage builds
- **Documentación**: Markdown claro y actualizado

## 📝 Licencia

Proyecto desarrollado para la Universidad Central del Ecuador.
Departamento de Ingeniería de Sistemas.

## 📞 Soporte

Para problemas o consultas:
1. Verificar logs específicos del servicio
2. Reviar documentación de cada componente
3. Crear issue en el repositorio

---

**Versión**: 2.0.0  
**Última Actualización**: 2026  
**Arquitectura**: Microservicios con Load Balancer
