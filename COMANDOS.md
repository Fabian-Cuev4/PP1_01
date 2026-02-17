# Comandos Útiles - Proyecto PP1_01

## 🚀 **Iniciar Servicios**

### **Iniciar todos los servicios (Dashboard + Backends + Balanceador)**
```bash
docker-compose --profile all up
```
**Propósito**: Inicia todo el sistema de monitoreo y balanceo de carga

### **Iniciar solo backends y balanceador**
```bash
docker-compose up
```
**Propósito**: Inicia nginx y los 3 servidores backend (sin dashboard)

---

## 📊 **Pruebas de Carga (K6)**

### **Ejecutar pruebas de carga**
```bash
docker-compose --profile load-test up
```
**Propósito**: Inicia k6 para saturar el endpoint `/api/maquinas/agregar`

### **Ejecutar pruebas de carga con reconstrucción**
```bash
docker-compose --profile load-test up --build
```
**Propósito**: Reconstruye y ejecuta pruebas de carga (usar después de cambios en k6)

---

## 🛠 **Reconstruir Contenedores (Después de Cambios)**

### **Reconstruir contenedor específico**
```bash
docker-compose up --build nginx_balancer
```
**Propósito**: Reconstruye nginx después de cambios en `nginx.conf`

### **Reconstruir dashboard**
```bash
docker-compose up --build dashboard
```
**Propósito**: Reconstruye dashboard después de cambios en `server.py` o `index.html`

### **Reconstruir backend específico**
```bash
docker-compose up --build pp1_01-backend-1
```
**Propósito**: Reconstruye backend 1 después de cambios en el código

### **Reconstruir todos los servicios**
```bash
docker-compose up --build
```
**Propósito**: Reconstruye todos los contenedores después de cambios generales

---

## 🔄 **Reiniciar Servicios**

### **Reiniciar nginx**
```bash
docker-compose restart nginx
```
**Propósito**: Aplica cambios en la configuración de nginx

### **Reiniciar dashboard**
```bash
docker-compose restart dashboard
```
**Propósito**: Reinicia el dashboard sin reconstruir

### **Reiniciar backend específico**
```bash
docker-compose restart pp1_01-backend-2
```
**Propósito**: Reinicia un backend específico

---

## 🛑 **Detener Servicios**

### **Detener todos los servicios (contenedores permanecen)**
```bash
docker-compose stop
```
**Propósito**: Detiene todos los contenedores pero los mantiene creados

### **Detener servicio específico**
```bash
docker-compose stop pp1_01-backend-3
```
**Propósito**: Detiene un contenedor específico (útil para pruebas de caída)

---

## 🗑️ **Eliminar Servicios**

### **Detener y eliminar todos los contenedores**
```bash
docker-compose down
```
**Propósito**: Detiene y elimina todos los contenedores, redes y volúmenes

### **Eliminar todo (incluyendo imágenes y volúmenes)**
```bash
docker-compose down --volumes --rmi all
```
**Propósito**: Limpieza completa del sistema (borra todo)

### **Eliminar contenedor específico**
```bash
docker-compose stop pp1_01-backend-2 && docker-compose rm -f pp1_01-backend-2
```
**Propósito**: Elimina completamente un contenedor específico

---

## 📋 **Ver Estado y Logs**

### **Ver estado de todos los contenedores**
```bash
docker-compose ps
```
**Propósito**: Muestra el estado de todos los servicios

### **Ver logs de todos los servicios**
```bash
docker-compose logs
```
**Propósito**: Muestra logs en tiempo real de todos los contenedores

### **Ver logs de servicio específico**
```bash
docker-compose logs dashboard
```
**Propósito**: Muestra logs del dashboard (útil para debugging)

### **Ver logs de nginx**
```bash
docker-compose logs nginx_balancer
```
**Propósito**: Muestra logs de nginx y errores de balanceo

---

## 🔧 **Comandos de Mantenimiento**

### **Limpiar imágenes no usadas**
```bash
docker image prune -f
```
**Propósito**: Libera espacio eliminando imágenes Docker no utilizadas

### **Limpiar sistema completo**
```bash
docker system prune -a --volumes
```
**Propósito**: Limpieza profunda del sistema Docker

### **Ver uso de recursos**
```bash
docker stats
```
**Propósito**: Monitoriza consumo de CPU y memoria de contenedores

---

## 🎯 **Flujo de Trabajo Típico**

### **Desarrollo con cambios frecuentes**:
1. Hacer cambios en el código
2. `docker-compose up --build [servicio]`  # Reconstruir lo cambiado
3. `docker-compose restart nginx`          # Si hay cambios en nginx
4. Probar con `docker-compose --profile load-test up`

### **Pruebas de caída de servidor**:
1. `docker-compose stop pp1_01-backend-2`  # Simular caída
2. Observar dashboard en http://localhost:18081
3. `docker-compose start pp1_01-backend-2` # Revivir servidor

### **Limpieza completa**:
1. `docker-compose down --volumes --rmi all`
2. `docker system prune -a --volumes`

---

## 🌐 **Accesos Rápidos**

- **Dashboard**: http://localhost:18081
- **API Balanceador**: http://localhost:8888
- **Backend 1**: http://localhost:8001
- **Backend 2**: http://localhost:8002  
- **Backend 3**: http://localhost:8003
