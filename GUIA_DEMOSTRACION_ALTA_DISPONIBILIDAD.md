# 🚀 GUÍA DE DEMOSTRACIÓN - ALTA DISPONIBILIDAD SIGLAB

## 📋 RESUMEN DE LA INFRAESTRUCTURA

Esta implementación demuestra **Alta Disponibilidad** con:
- **1 Nginx Load Balancer** (Puerto 8080) - Punto único de entrada
- **2 Servidores API** (api_back_1, api_back_2) - Balanceo de carga
- **2 Bases de Datos Compartidas** (MySQL + MongoDB) - Archivador central
- **Dashboard VTS** (Puerto 8084) - Monitoreo visual en tiempo real

## 🌐 **PUERTOS DE ACCESO**

### **APLICACIÓN PRINCIPAL (Frontend + Load Balancer)**
```
http://localhost:8080
```
- Punto de entrada único para todos los usuarios
- Load Balancer automático entre APIs
- Sticky Sessions activadas

### **DASHBOARD DE MONITOREO VTS**
```
http://localhost:8084/dashboard
```
- Métricas en tiempo real
- Tráfico en PORCENTAJES (%)
- Estados UP/DOWN con colores

### **SERVIDORES API (Acceso Directo)**
```
API Servidor 1: http://localhost:18001
API Servidor 2: http://localhost:18002
```
- Para pruebas individuales
- Logs de identificación
- Conexión a bases de datos compartidas

### **BASES DE DATOS (Acceso Directo)**
```
MySQL: localhost:13306
MongoDB: localhost:27018
```
- Archivador central compartido
- Persistencia de datos
- Acceso para administración

---

## 🎯 DINÁMICA DE LA DEMOSTRACIÓN (PASO A PASO)

### 1. INICIO DEL SISTEMA
```bash
# Levantar toda la infraestructura
docker-compose up --build

# Verificar que todos los contenedores estén activos
docker ps
```

**ESPERADO VER:**
- ✅ `mysql_siglab` (Base de datos central)
- ✅ `mongo_siglab` (Base de datos central)  
- ✅ `api_back_1` (Servidor API 1)
- ✅ `api_back_2` (Servidor API 2)
- ✅ `nginx_balancer_siglab` (Load Balancer + Frontend)

### 2. VERIFICACIÓN DE CONEXIONES
```bash
# Ver logs de los servidores API para confirmar conexión a bases de datos
docker logs api_back_1
docker logs api_back_2
```

**ESPERADO VER EN LOGS:**
```
Petición recibida en API Servidor 1 - GET /api/login
Conectado exitosamente al archivador central (MySQL/Mongo)
=== API Servidor 1 LISTO PARA RECIBIR PETICIONES ===
```

### 3. ACCESO A LA APLICACIÓN
```bash
# Acceder al frontend a través del Load Balancer
http://localhost:8080
```

**ESPERADO VER:**
- 🌐 Página de login del SIGLAB
- ✅ El sistema está funcionando a través del Load Balancer

### 4. MONITOREO EN TIEMPO REAL
```bash
# Abrir dashboard de monitoreo
http://localhost:8084/dashboard
```

**ESPERADO VER:**
- 📊 Métricas de tráfico en PORCENTAJES (%)
- 🟢 Estados UP/DOWN con colores visuales
- 📈 Distribución de carga entre api_back_1 y api_back_2

### 5. PRUEBA DE CARGA Y STICKY SESSIONS
```bash
# En múltiples pestañas del navegador, hacer peticiones simultáneas
# O usar curl para simular múltiples usuarios

curl http://localhost:8080/api/maquinas
curl http://localhost:8080/api/maquinas
curl http://localhost:8080/api/maquinas
```

**VERIFICAR EN LOGS:**
```bash
# Ver logs en tiempo real
docker logs -f api_back_1 &
docker logs -f api_back_2 &
```

**ESPERADO VER:**
- 📥 Las peticiones se distribuyen entre ambos servidores
- 🔄 Sticky Sessions mantienen al usuario en el mismo servidor

---

## 💥 ESCENARIO DE FALLA - DEMOSTRACIÓN DE ALTA DISPONIBILIDAD

### PASO CRÍTICO: SIMULAR CAÍDA DE SERVIDOR

```bash
# Matar el servidor API 1 para simular una caída
docker stop api_back_1

# Verificar que el servidor está caído
docker ps
```

### OBSERVAR EL COMPORTAMIENTO

#### 1. EN EL DASHBOARD VTS (http://localhost:8084/dashboard)
**ESPERADO VER INMEDIATAMENTE:**
- 🔴 `api_back_1` cambia a estado **DOWN** (color rojo)
- 🟢 `api_back_2` muestra **100%** del tráfico
- 📊 Los porcentajes se actualizan en tiempo real

#### 2. EN LA APLICACIÓN (http://localhost:8080)
**ESPERADO VER:**
- ✅ La aplicación sigue funcionando normalmente
- 🔄 Todas las peticiones van automáticamente a `api_back_2`
- 👤 Los usuarios no notan la caída

#### 3. EN LOS LOGS
```bash
# Ver logs del servidor sobreviviente
docker logs -f api_back_2
```

**ESPERADO VER:**
```
Petición recibida en API Servidor 2 - GET /api/maquinas
Petición recibida en API Servidor 2 - POST /api/login
```

### RECUPERACIÓN AUTOMÁTICA

```bash
# Levantar nuevamente el servidor caído
docker start api_back_1

# Observar el dashboard VTS
# El servidor volverá a estado UP y comenzará a recibir tráfico
```

**ESPERADO VER:**
- 🟢 `api_back_1` vuelve a estado **UP** (color verde)
- ⚖️ El tráfico se redistribuye automáticamente entre ambos servidores
- 🔄 El Load Balancer detecta la recuperación automáticamente

---

## 🎯 PUNTOS CLAVE PARA LA EXPOSICIÓN

### 1. ARQUITECTURA DE ALTA DISPONIBILIDAD
- **Un solo punto de entrada** (Nginx en puerto 8080)
- **Múltiples servidores backend** para distribución de carga
- **Bases de datos compartidas** como "archivador central"
- **Monitoreo visual** en tiempo real

### 2. RESILIENCIA AUTOMÁTICA
- **Detección automática** de caídas de servidores
- **Redirección transparente** del tráfico
- **Recuperación automática** sin intervención manual
- **Experiencia de usuario** ininterrumpida

### 3. MONITOREO VISUAL
- **Dashboard en tiempo real** (puerto 8084)
- **Métricas en porcentajes** para fácil comprensión
- **Estados visuales** (verde/rojo) para identificar problemas
- **Datos históricos** de rendimiento

### 4. LOGS DE SEGUIMIENTO
- **Identificación clara** del servidor que atiende cada petición
- **Conexiones a bases de datos** documentadas
- **Eventos de inicio/apagado** registrados

---

## 🔧 COMANDOS ÚTILES PARA LA DEMO

```bash
# Ver estado general del sistema
docker-compose ps

# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de servidores específicos
docker logs api_back_1 -f
docker logs api_back_2 -f

# Ver métricas del Load Balancer
curl http://localhost:8084/status | jq

# Probar balanceo de carga
for i in {1..10}; do curl -s http://localhost:8080/api/maquinas | head -c 50; echo ""; done

# Simular estrés
ab -n 100 -c 10 http://localhost:8080/api/maquinas

# Acceso directo a APIs (para pruebas)
curl http://localhost:18001/docs
curl http://localhost:18002/docs
```

---

## 🏆 CONCLUSIÓN

Esta implementación demuestra cómo un **solo Nginx** puede:
1. **Servir el frontend** a los usuarios (puerto 8080)
2. **Balancear la carga** entre múltiples APIs
3. **Monitorear la salud** del sistema en tiempo real (puerto 8084)
4. **Garantizar continuidad** del servicio ante fallos

**Resultado:** Un sistema robusto, escalable y resiliente listo para producción.
