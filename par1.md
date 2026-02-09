## 📋 ¿Qué es SIGLAB?
SIGLAB es un sistema de gestión de laboratorios diseñado para administrar el inventario y mantenimiento de equipos de cómputo. Implementa una arquitectura por capas de alta disponibilidad con load balancer y actualizaciones en tiempo real con cache.

## 🛠️ Tecnologías y Herramientas
### Backend Stack
- *FastAPI*
- *MySQL*
- *MongoDB:*
- *Redis*
- *Docker:*
### Frontend Stack
- *HTML5/CSS3/JavaScript:*

## 🚀 Funcionalidades del Sistema
### Gestión de Usuarios
- *Registro de usuarios:* Creación de cuentas con autenticación
- *Inicio de sesión:* Validación de credenciales con sesiones seguras
- *Logout:* Cierre seguro de sesión

### Gestión de Equipos
- *Agregar máquina:* Registro de computadoras e impresoras con especificaciones
- *Listar máquinas:* Visualización de todos los equipos con filtros
- *Buscar máquina:* Búsqueda instantánea por código
- *Actualizar máquina:* Modificación del estado
### Sistema de Mantenimientos
- *Registrar mantenimiento:* Creación de intervenciones técnicas por máquina
- *Historial de mantenimientos:* Consulta de todas las intervenciones realizadas
- *Informes por máquina:* Reportes detallados de mantenimientos por equipo

### Monitoreo y Dashboard
- *Estado de servidores:* Monitoreo de 3 servidores API con Load Balancer
- *Estadísticas en tiempo real maquinas:* Totales por estado, tipo
### Autenticación y Seguridad
- *Login seguro:* Validación con bcrypt para contraseñas


---
## 📁 *Explicación Archivo por Archivo*
### 🏗️ *Backend - Python FastAPI*
#### *backend/main.py* - Punto de entrada principal de la API FastAPI que orquesta todos los módulos y endpoints del sistema.
#### *backend/app/routes/maquina.py* - Endpoints CRUD para gestión de máquinas con polling en tiempo real y búsqueda.
#### *backend/app/routes/mantenimiento.py* - Endpoints para registro, historial de mantenimientos y reporte con polling automático.
#### *backend/app/routes/auth.py* - Sistema de autenticación con login, registro y gestión de sesiones seguras.
#### *backend/app/services/maquina_service.py* - Lógica de negocio para máquinas con caché Redis y validaciones.
#### *backend/app/services/mantenimiento_service.py* - Lógica de negocio de mantenimientos con generación de informes complejos.
#### *backend/app/services/usuario_service.py* - Gestión de usuarios con autenticación bcrypt y validación de credenciales.
#### *backend/app/daos/maquina_dao.py* - Acceso a datos MySQL para operaciones CRUD de máquinas con cache optimizado.
#### *backend/app/daos/mantenimiento_dao.py* - Acceso a datos MongoDB para logs y MySQL para mantenimientos.
#### *backend/app/daos/usuario_dao.py* - Acceso a datos MySQL para autenticación y gestión de usuarios.
#### *backend/app/models/abstrac_factory/Maquina.py* - Clase base abstracta que define interfaz común para todos los tipos de máquinas.
#### *backend/app/dtos/informe_dto.py* - Data Transfer Object para formatear respuestas JSON de informes de mantenimiento y maquina
#### *backend/app/models/Computadora.py* - Implementación concreta para computadoras con atributos específicos (procesador, RAM, disco).
#### *backend/app/models/Impresora.py* - Implementación concreta para impresoras con atributos específicos (velocidad, tipo).
#### *backend/app/repositories/proyecto_repository.py* - Contenedor centralizado de todos los DAOs del sistema con instancia global compartida.
#### *backend/app/database/database_manager.py* - Gestor centralizado de conexiones a MySQL, MongoDB y Redis con pooling.
#### *backend/app/utils/encryption.py* - Utilidades de encriptación bcrypt para contraseñas y seguridad de datos.
#### *backend/app/database/mysql.py* - Conector MySQL con manejo de conexiones y reintentos automáticos.
#### *backend/app/database/mongodb.py* - Conector MongoDB para logs estructurados y auditoría del sistema.
#### *backend/app/database/redis.py* - Cliente Redis para caché distribuido con TTL y sincronización entre servidores.


### 🎨 *Frontend - /JavaScript*
#### *frontend/static/javascript/reporte.js* - Generador de informes con exportación de datos.
#### *frontend/static/javascript/session.js* - Gestión de sesiones con cookies y rediccion.
#### *frontend/static/javascript/register.js* - Validación de registro de usuarios con confirmación de contraseñas.
#### *frontend/static/javascript/actualizar.js* - Sistema de actualización de estado de máquinas.
#### *frontend/static/javascript/ventana.js* - Control de redireccionamiento entre ventanas.
#### *frontend/static/javascript/formulario.js* - Manejo de formularios dinámicos con validación
#### *frontend/static/javascript/historial.js* - Gestión de historiales con polling automático
#### *frontend/static/javascript/mantenimiento.js* - Sistema de mantenimientos con polling cada 2 segundos
#### *frontend/static/javascript/dashboard.js* - Lógica principal del dashboard con polling cada 1 segundo y actualización automática.
---

## 🎭 *Patrones de Diseño Implementados*

### 🔍 *1. DAO (Data Access Object)*

*¿Qué es?*
Patrón que separa la lógica de acceso a datos de la lógica de negocio. Cada DAO se especializa en una tabla específica.

*¿Cómo funciona en SISLAB?*
- *maquina_dao.py* 
- *mantenimiento_dao.py* 
- *usuario_dao.py* 

*Pasos del flujo DAO:*
1. *Service solicita operación* → maquina_service.registrar_maquina()
2. *Service llama DAO* → self._maquina_dao.guardar(nueva_maquina)
3. *DAO obtiene conexión* → DatabaseManager.get_mysql_connection()
4. *DAO ejecuta SQL* → INSERT INTO maquinas VALUES (...)
5. *DAO retorna resultado* → True/False o datos consultados
6. *Service procesa resultado* → Invalida cache si fue escritura

*Ventajas:*
- *Separación clara* Cada DAO conoce solo su tabla
- *Reutilización* Mismo DAO para múltiples services


---

### 📦 *2. DTO (Data Transfer Object)*

*¿Qué es?*
Objeto que formatea y estructura datos para transferencia entre capas, evitando exponer modelos internos.

*¿Cómo funciona en SISLAB?*
- *informe_dto.py*
- *integrado en service* 

*Pasos del flujo DTO:*
1. *Service obtiene datos crudos* → MySQL + MongoDB
2. *Service llama DTO* → informe_dto.formatear(datos_mysql, datos_mongodb)
3. *DTO procesa y estructura* → Agrupa, calcula estadísticas, formatea fechas
4. *DTO crea objeto limpio* → {"status": "ok", "datos": [...], "estadisticas": {...}}
5. *API retorna DTO* → JSON perfecto para frontend
6. *Frontend consume DTO* → Datos listos para mostrar

*Ventajas:*
- *Consistencia:* Siempre misma estructura de respuesta
- *Seguridad:* No expone modelos internos de BD

---

### 🏛️ *3. ABC (Abstract Base Class)*

*¿Qué es?*
Clase base abstracta que define interfaz común para clases hijas, garantizando comportamiento consistente.

*¿Cómo funciona en SISLAB?*
- *Maquina.py* → Clase abstracta base para todos los tipos de máquinas
- *Computadora.py* → Hereda de Maquina, implementa atributos específicos
- *Impresora.py* → Hereda de Maquina, implementa atributos específicos

*Pasos del flujo ABC:*
1. *ABC define interfaz* → Métodos abstractos get_tipo(), get_atributos()
2. *Clases hijas heredan* → class Computadora(Maquina)
3. *Implementan métodos* → def get_tipo(): return "PC"
4. *Polimorfismo* → maquina.get_tipo() funciona para PC e IMP
5. *Service usa interfaz* → No sabe si es PC o IMP, solo llama métodos
6. *Runtime elige implementación* → Python ejecuta método correcto

*Ventajas:*
- *Extensibilidad:* Fácil agregar nuevos tipos (Servidor, Router, etc.)
- *Polimorfismo:* Código genérico funciona para todos los tipos

---

### ⚖️ *4. Load Balancer con Sticky Sessions*

*¿Qué es?*
Distribuidor de tráfico que reparte peticiones entre múltiples servidores, manteniendo sesión del usuario en mismo servidor.

*¿Cómo funciona en SISLAB?*
- *Nginx Load Balancer* → Distribuye entre 3 servidores API (18001, 18002, 18003)
- *Sticky Sessions* → Cookie SRV mantiene usuario en mismo servidor
- *Health Checks* → Detecta servidores caídos y los excluye automáticamente

*Código Nginx (Real):*
nginx
# Distribución 50/50 para nuevos usuarios
split_clients "${remote_addr}${request_id}" $new_srv {
    50% "s1";
    *   "s2";
}

# Mapeo de cookie a servidor
map $cookie_SRV $srv_route {
    default $cookie_SRV;
    ""      $new_srv;
}

# Upstream con 3 servidores API
upstream api_backend {
    hash $srv_route consistent;
    server api_back_1:8000 weight=1 max_fails=3 fail_timeout=30s;
    server api_back_2:8000 weight=1 max_fails=3 fail_timeout=30s;
    server api_back_3:8000 weight=1 max_fails=3 fail_timeout=30s;
}

# Sticky session con cookie SRV
location /api/ {
    add_header Set-Cookie "SRV=$srv_route; Max-Age=300; Path=/; HttpOnly; SameSite=Lax" always;
    proxy_pass http://api_backend;
}


*Pasos del flujo Load Balancer:*
1. *Usuario llega* → Nginx recibe petición en puerto 8080
2. *Verifica cookie SRV* → ¿Tiene cookie? Si no, asigna servidor aleatorio
3. *Asigna servidor* → split_clients distribuye 50% s1, 50% s2
4. *Crea cookie SRV* → Set-Cookie: SRV=s1; Max-Age=300 (5 minutos)
5. *Redirige a API* → proxy_pass http://api_backend al servidor asignado
6. *Hash consistente* → hash $srv_route consistent mantiene usuario en mismo servidor
7. *Health Check* → max_fails=3 fail_timeout=30s → Si falla 3 veces, excluye por 30s
8. *Siguientes peticiones* → Usan misma cookie SRV → mismo servidor

*Ventajas:*
- *Alta disponibilidad:* Si un servidor cae, otros siguen funcionando
- *Rendimiento:* Distribuye carga equitativamente
- *Sesiones persistentes:* Usuario no pierde sesión al cambiar requests
- *Escalabilidad:* Fácil agregar más servidores

---

### 🔄 *5. Polling en Tiempo Real*

*¿Qué es?*
Técnica de actualización automática donde el frontend solicita datos periódicamente al backend sin intervención del usuario.

*¿Cómo funciona en SISLAB?*
- *Polling automático* → Cada 1-2 segundos solicita datos actualizados
- *Headers especiales* → Cache-Control: no-cache evita caché del navegador
- *Endpoints optimizados* → Mismos endpoints sirven para polling y normal

*Configuración de Tiempos (Real):*
javascript
// frontend/static/javascript/polling-config.js
const POLLING_CONFIG = {
    dashboard: { interval: 1000, endpoint: '/api/dashboard/estadisticas' },      // 1 segundo
    mantenimientos: { interval: 2000, endpoint: '/api/mantenimientos/todos' },     // 2 segundos
    historial: { interval: 2000, endpoint: '/api/mantenimientos/historial' },    // 2 segundos
    busqueda: { interval: 1500, endpoint: '/api/maquinas/buscar/{termino}' }     // 1.5 segundos
};


*Headers Anti-Cache (Real):*
python
# Backend detecta polling y responde sin caché
response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
response.headers["Access-Control-Allow-Origin"] = "*"


*Pasos del flujo Polling:*
1. *Frontend inicia polling* → setInterval(request_data, 1000) cada 1 segundo
2. *Añade headers especiales* → Cache-Control: no-cache para evitar caché browser
3. *Backend detecta polling* → Revisa headers y responde sin caché local
4. *Backend consulta Redis* → Primero busca en caché (TTL 30s)
5. *Si no hay cache* → Consulta MySQL y guarda en Redis
6. *Retorna datos frescos* → Siempre datos actualizados, sin importar caché browser
7. *Frontend actualiza UI* → Reemplaza datos en tabla/dashboard sin refresh
8. *Repite ciclo* → Siguiente request en 1 segundo

*Tiempos de Polling:*
- *Dashboard:* 1000ms (1 segundo) → Estadísticas críticas
- *Mantenimientos:* 2000ms (2 segundos) → Datos menos críticos
- *Historial:* 2000ms (2 segundos) → Datos históricos
- *Búsqueda:* 1500ms (1.5 segundos) → Resultados de búsqueda

*Ventajas:*
- *Tiempo real:* Usuario ve cambios inmediatos
- *Sin refresh:* Experiencia fluida sin recargar página
- *Controlado:* Tiempos ajustados por criticidad de datos
- *Compatible:* Funciona en todos los navegadores

---

### 💾 *6. Cache Distribuido con TTL*

*¿Qué es?*
Sistema de almacenamiento temporal compartido entre múltiples servidores con tiempo de vida automático para sincronización.

*¿Cómo funciona en SISLAB?*
- *Redis centralizado* → Todos los 3 servidores comparten misma instancia Redis
- *TTL automático* → Los datos expiran solos para sincronización
- *Keys estructuradas* → Nomenclatura organizada para fácil gestión

*TTL y Conexión (Real):*
python
# backend/app/services/maquina_service.py
def listar_todas_las_maquinas(self):
    # 1. Obtener cliente Redis (compartido por 3 servidores)
    redis_cliente = DatabaseManager.get_redis()
    
    if redis_cliente is not None:
        # 2. Intentar obtener desde caché
        maquinas_cache = RedisConnection.obtener_cache("cache:lista_maquinas")
        
        if maquinas_cache is not None:
            return maquinas_cache, None  # CACHE HIT
    
    # 3. Cache MISS: consultar MySQL
    maquinas = self._maquina_dao.listar_todas()
    
    if maquinas and redis_cliente is not None:
        # 4. Guardar en caché con TTL 30 segundos
        RedisConnection.guardar_cache("cache:lista_maquinas", maquinas, tiempo_vida=30)
    
    return maquinas, None


*Keys de Cache (Reales):*
python
# Estructura de keys organizada
"cache:lista_maquinas"           # Lista general de máquinas
"cache:dashboard"               # Estadísticas del dashboard
"maquina:{codigo}"              # Máquina específica
"busqueda:codigo:{termino}"      # Resultados de búsqueda
"informe:{codigo}"              # Reportes específicos
"historial:{codigo}"            # Historial de mantenimientos
"mantenimiento:todos"           # Todos los mantenimientos


*Pasos del flujo Cache Distribuido:*
1. *Service solicita datos* → maquina_service.listar_todas_las_maquinas()
2. *Obtiene cliente Redis* → DatabaseManager.get_redis() (compartido por 3 servidores)
3. *Verifica cache* → RedisConnection.obtener_cache("cache:lista_maquinas")
4. *Si hay datos (CACHE HIT)* → Retorna datos de Redis inmediatos
5. *Si no hay datos (CACHE MISS)* → Consulta MySQL
6. *Guarda en Redis* → RedisConnection.guardar_cache(key, datos, tiempo_vida=30)
7. *TTL expira automáticamente* → Redis borra datos después de 30 segundos
8. *Sincronización entre servidores* → Los 3 servidores ven misma instancia Redis

*TTL y Sincronización:*
- *TTL 60 segundos* → Datos expiran solos para forzar actualización
- *3 servidores comparten Redis* → Todos ven mismos datos cacheados
- *Invalidación manual* → DatabaseManager.limpiar_cache_sistema() para cambios
- *Keys organizadas* → Fácil identificar y limpiar por patrón

*Ventajas:*
- *Rendimiento:* Respuestas en milisegundos vs segundos de MySQL
- *Sincronización:* Todos los servidores ven mismos datos
- *Escalabilidad:* Reduce carga en base de datos
- *Consistencia:* TTL garantiza datos frescos automáticamente









