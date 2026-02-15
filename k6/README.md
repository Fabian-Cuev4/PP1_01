# k6 - Testing de Carga y Rendimiento

## Descripción
Suite de pruebas de carga automatizadas con k6 para evaluar el rendimiento y escalabilidad del sistema SIGLAB.

## Tecnologías
- **k6**: Herramienta de testing de carga moderna
- **JavaScript ES6**: Scripts de prueba
- **Docker**: Ejecución en contenedores aislados

## Estructura del Proyecto

```
k6/
├── scripts/                # Scripts de prueba
│   ├── maquina-saturator.js    # Prueba de saturación de máquinas
│   ├── concurrent-users.js       # Prueba de usuarios concurrentes
│   └── stress-test.js          # Prueba de estrés
├── README.md               # Este archivo
└── Dockerfile             # Configuración de contenedor k6
```

## Tipos de Pruebas

### 1. Prueba de Saturación
**Archivo**: `maquina-saturator.js`
- **Objetivo**: Medir capacidad máxima del endpoint `/api/maquinas/agregar`
- **Duración**: 10 minutos
- **VUs**: 1 usuario virtual
- **Escenario**: Agregar 20 máquinas en grupos secuenciales

### 2. Prueba de Concurrencia
**Archivo**: `concurrent-users.js`
- **Objetivo**: Evaluar comportamiento con múltiples usuarios simultáneos
- **Duración**: 5 minutos
- **VUs**: 10-50 usuarios virtuales
- **Escenario**: Operaciones mixtas (listar, agregar, buscar)

### 3. Prueba de Estrés
**Archivo**: `stress-test.js`
- **Objetivo**: Encontrar puntos de ruptura del sistema
- **Duración**: Hasta fallo
- **VUs**: Incremental (10 → 100)
- **Escenario**: Pico de carga máxima

## Métricas Monitoreadas

### Principales
- **Requests/s**: Tasa de peticiones por segundo
- **Response Time**: Tiempo de respuesta promedio
- **Error Rate**: Porcentaje de peticiones fallidas
- **Throughput**: Cantidad total de datos transferidos

### Secundarias
- **P95 Response Time**: Percentil 95 de tiempo de respuesta
- **Connection Time**: Tiempo para establecer conexión
- **DNS Lookup Time**: Tiempo de resolución DNS

## Scripts de Prueba

### maquina-saturator.js
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    vus: 1,
    duration: '10m',
    thresholds: {
        http_req_duration: ['p(95)<500'],
        http_req_failed: ['rate<0.1'],
    },
};

export default function () {
    const payload = JSON.stringify({
        nombre: `Maquina-${Date.now()}`,
        tipo: 'Computadora',
        estado: 'Operativa',
        ubicacion: 'Laboratorio A'
    });

    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const res = http.post('http://nginx_balancer:80/api/maquinas/agregar', payload, params);
    
    check(res, {
        'status es 200': (r) => r.status === 200,
        'tiempo de respuesta < 500ms': (r) => r.timings.duration < 500,
    });

    sleep(1);
}
```

### concurrent-users.js
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    stages: [
        { duration: '2m', target: 10 },
        { duration: '2m', target: 25 },
        { duration: '2m', target: 50 },
        { duration: '2m', target: 25 },
        { duration: '2m', target: 10 },
    ],
    thresholds: {
        http_req_duration: ['p(95)<1000'],
        http_req_failed: ['rate<0.05'],
    },
};

export default function () {
    const responses = http.batch([
        ['GET', 'http://nginx_balancer:80/api/maquinas/listar'],
        ['GET', 'http://nginx_balancer:80/api/maquinas/buscar?id=1'],
        ['GET', 'http://nginx_balancer:80/api/mantenimientos/historial'],
    ]);

    responses.forEach((res) => {
        check(res, {
            'status es 200': (r) => r.status === 200,
        });
    });

    sleep(1);
}
```

## Configuración Docker

### Dockerfile
```dockerfile
FROM loadimpact/k6:latest

# Copiar scripts
COPY scripts/ /scripts/

# Directorio de trabajo
WORKDIR /scripts

# Comando por defecto
CMD ["run", "/scripts/maquina-saturator.js"]
```

### docker-compose.yml
```yaml
k6_saturator:
  build:
    context: ./k6
    dockerfile: Dockerfile
  container_name: k6_saturator
  environment:
    BASE_URL: http://nginx_balancer:80
  networks:
    - siglab_network
    - frontend_network
  profiles:
    - load-test
```

## Ejecución de Pruebas

### Prueba de Saturación
```bash
# Ejecutar prueba de máquinas
docker-compose --profile load-test up --build

# Monitorear en tiempo real
docker logs k6_saturator -f
```

### Pruebas Personalizadas
```bash
# Ejecutar script específico
docker run --rm -v $(pwd)/scripts:/scripts \
  loadimpact/k6 run /scripts/concurrent-users.js

# Con opciones personalizadas
k6 run --vus 20 --duration 5m script.js
```

## Análisis de Resultados

### Métricas Clave
```bash
# Resumen de ejecución
k6 run --summary-export=summary.json script.js

# Exportar a formato HTML
k6 run --out json=results.json script.js

# Integración con CI/CD
k6 run --junit test-results.xml script.js
```

### Interpretación de Resultados
- **< 100ms**: Excelente rendimiento
- **100-500ms**: Buen rendimiento
- **500-1000ms**: Rendimiento aceptable
- **> 1000ms**: Rendimiento pobre

## Umbrales de Rendimiento

### Objetivos del Sistema
- **Disponibilidad**: > 99.9%
- **Tiempo de respuesta**: P95 < 500ms
- **Tasa de error**: < 0.1%
- **Throughput**: > 100 req/s

### Load Balancer Testing
- **Distribución**: Verificar balanceo entre servidores
- **Failover**: Probar caída de servidores
- **Recuperación**: Medir tiempo de recuperación

## Integración CI/CD

### GitHub Actions
```yaml
name: Performance Tests
on: [push, pull_request]

jobs:
  k6-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run k6 test
        run: |
          docker-compose --profile load-test up --build
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: k6-results
          path: results/
```

## Monitoreo en Producción

### Dashboards
- **Grafana**: Visualización de métricas en tiempo real
- **K6 Cloud**: Análisis avanzado y comparación
- **ELK Stack**: Centralización de logs y métricas

### Alertas
- **SLA Violations**: Cuando se incumplen umbrales
- **Performance Degradation**: Caídas significativas
- **System Outages**: Fallos completos del servicio

## Best Practices

### Diseño de Pruebas
- **Realismo**: Simular patrones de uso reales
- **Gradualidad**: Incrementar carga progresivamente
- **Repetibilidad**: Ejecutar pruebas consistentes

### Análisis
- **Baseline**: Establecer línea base de rendimiento
- **Tendencias**: Identificar patrones a lo largo del tiempo
- **Comparación**: Medir contra versiones anteriores

### Optimización
- **Cuellos de Botella**: Identificar limitaciones
- **Escalabilidad**: Determinar puntos de escalado
- **Costo-Beneficio**: Balancear mejoras vs impacto
