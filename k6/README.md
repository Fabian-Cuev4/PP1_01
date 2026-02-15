# Saturador k6 para microservicio de agregar máquina

## Descripción
Este directorio contiene el script k6 y configuración Docker para realizar pruebas de carga saturando el endpoint `/api/maquinas/agregar` del microservicio backend.

## Archivos
- `maquina-saturator.js`: Script k6 que agrega máquinas secuencialmente en grupos
- `Dockerfile`: Configuración para crear el contenedor del saturador

## Uso

### 1. Iniciar servicios base
```bash
docker-compose up -d
```

### 2. Ejecutar prueba de carga
```bash
docker-compose --profile load-test up k6-saturator --build
```

### 3. Ver resultados
La prueba mostrará progreso en consola y las máquinas agregadas estarán disponibles en:
- Base de datos MySQL
- Endpoint: `GET /api/maquinas/listar`

## Configuración de la prueba
- **Grupos**: 2 grupos de 20 máquinas cada uno
- **Duración total**: ~1 minuto 10 segundos
- **Endpoint**: POST /api/maquinas/agregar
- **Códigos**: Numeración secuencial TM-001, TM-002, etc.
- **Usuario**: admin (fijo para evitar autenticación)

## Variables configurables
Puedes modificar `maquina-saturator.js` para ajustar:
- `MACHINES_PER_GROUP`: Máquinas por grupo (default: 20)
- `PAUSE_BETWEEN_MACHINES`: Segundos entre máquinas (default: 1)
- `REST_BETWEEN_GROUPS`: Segundos de reposo entre grupos (default: 10)
- `TOTAL_GROUPS`: Número de grupos (default: 2)

## Características
- **Datos válidos**: Tipos PC/IMP, estados Operativo/Mantenimiento/Dañado
- **Sin autenticación**: Usuario admin fijo
- **Reintentos automáticos**: Manejo de errores de conexión
- **Numeración secuencial**: Códigos TM-001, TM-002, etc.

## Ejemplo de ejecución
```
Iniciando grupo 1 de 20 máquinas...
Grupo 1 - Máquina 1/20 - Status: 200
Grupo 1 - Máquina 2/20 - Status: 200
...
Reposo de 10 segundos...
Iniciando grupo 2 de 20 máquinas...
...
Prueba completada: 40 máquinas agregadas en total
```
