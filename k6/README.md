# k6 - Testing de Carga y Rendimiento SIGLAB

## 📋 Descripción
Suite completa de pruebas de carga y rendimiento automatizadas con k6 para evaluar la escalabilidad, fiabilidad y rendimiento del sistema SIGLAB bajo diferentes condiciones de estrés.

## 🎯 Objetivos de Testing

- **Capacidad Máxima**: Determinar el límite de peticiones concurrentes
- **Rendimiento**: Medir tiempos de respuesta y throughput
- **Escalabilidad**: Validar comportamiento con múltiples usuarios
- **Resiliencia**: Probar recuperación bajo fallos
- **Balanceo**: Verificar distribución de carga entre backends

## 🏗️ Arquitectura de Testing

```
┌─────────────────────────────────────────────────────────┐
│                    Testing Layer                       │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │    k6 VU    │ │    k6 VU    │ │    k6 VU    │     │
│  │  (Client 1) │ │  (Client 2) │ │  (Client N) │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────┬───────────────────────────────────┘
                      │
              ┌───────▼───────┐
              │  Nginx LB     │
              │   :8888       │
              └───────┬───────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
│  Backend 1  │ │ Backend 2  │ │ Backend 3  │
│  :8000      │ │ :8000      │ │ :8000      │
└─────────────┘ └─────────────┘ └─────────────┘
```

## 🛠️ Stack Tecnológico

### Core Testing
- **k6**: Herramienta de testing de carga moderna
- **JavaScript ES6**: Scripts de prueba
- **Docker**: Ejecución aislada y reproducible

### Tipos de Pruebas
- **Load Testing**: Pruebas de saturación
- **Stress Testing**: Pruebas de estrés al límite
- **Spike Testing**: Pruebas de picos de carga
- **Soak Testing**: Pruebas de resistencia prolongada
- **Volume Testing**: Pruebas con grandes volúmenes de datos

## 📁 Estructura del Proyecto

```
k6/
├── scripts/                    # Scripts de prueba
│   ├── maquina-saturator.js   # Prueba de saturación de máquinas
│   ├── concurrent-users.js    # Prueba de usuarios concurrentes
│   ├── stress-test.js         # Prueba de estrés máximo
│   ├── spike-test.js          # Prueba de picos de carga
│   ├── soak-test.js           # Prueba de resistencia
│   └── volume-test.js         # Prueba de volumen
├── utils/                      # Utilidades de testing
│   ├── helpers.js             # Funciones helper
│   ├── checks.js              # Verificaciones personalizadas
│   └── metrics.js             # Colección de métricas
├── data/                       # Datos de prueba
│   ├── users.json             # Usuarios de prueba
│   ├── machines.json          # Datos de máquinas
│   └── payloads.json          # Payloads predefinidos
├── reports/                    # Reportes generados
│   ├── html/                  # Reportes HTML
│   ├── json/                  # Datos JSON
│   └── csv/                   # Datos CSV
├── Dockerfile                  # Imagen Docker k6
├── docker-compose.k6.yml       # Configuración específica
├── requirements.txt            # Dependencias Python (scripts auxiliares)
└── README.md                   # Esta documentación
```

## 🧪 Tipos de Pruebas Detalladas

### 1. Prueba de Saturación (maquina-saturator.js)

**Objetivo**: Medir capacidad máxima del endpoint `/api/maquinas/agregar`

```javascript
// scripts/maquina-saturator.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Métricas personalizadas
export let errorRate = new Rate('errors');

// Opciones de la prueba
export let options = {
    stages: [
        { duration: '2m', target: 10 },   // Ramp-up a 10 VUs
        { duration: '5m', target: 10 },   // Mantener 10 VUs
        { duration: '2m', target: 50 },   // Ramp-up a 50 VUs
        { duration: '5m', target: 50 },   // Mantener 50 VUs
        { duration: '2m', target: 100 },  // Ramp-up a 100 VUs
        { duration: '10m', target: 100 }, // Saturación sostenida
        { duration: '2m', target: 0 },    // Ramp-down
    ],
    thresholds: {
        http_req_duration: ['p(95)<500'],  // 95% de requests < 500ms
        http_req_failed: ['rate<0.1'],     // Tasa de error < 10%
        errors: ['rate<0.1'],
    },
};

// Datos de prueba
const MACHINE_TYPES = ['Computadora', 'Impresora', 'Scanner', 'Servidor'];
const STATUSES = ['Operativa', 'Mantenimiento', 'Fuera de Servicio'];
const LOCATIONS = ['Laboratorio A', 'Laboratorio B', 'Sala de Servidores', 'Oficina Principal'];

export default function () {
    // Generar datos aleatorios
    const machineData = {
        nombre: `Maquina-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        tipo: MACHINE_TYPES[Math.floor(Math.random() * MACHINE_TYPES.length)],
        estado: STATUSES[Math.floor(Math.random() * STATUSES.length)],
        ubicacion: LOCATIONS[Math.floor(Math.random() * LOCATIONS.length)],
        fecha_adquisicion: new Date().toISOString().split('T')[0],
        responsable: `Usuario-${Math.floor(Math.random() * 1000)}`,
    };

    const params = {
        headers: {
            'Content-Type': 'application/json',
            'User-Agent': 'k6-load-test/1.0',
        },
        timeout: '10s',
    };

    // Ejecutar request
    const response = http.post('http://nginx_balancer:80/api/maquinas/agregar', 
                              JSON.stringify(machineData), 
                              params);

    // Verificaciones
    const success = check(response, {
        'status es 201': (r) => r.status === 201,
        'tiempo de respuesta < 500ms': (r) => r.timings.duration < 500,
        'respuesta contiene ID': (r) => JSON.parse(r.body).id !== undefined,
        'content-type correcto': (r) => r.headers['Content-Type'].includes('application/json'),
    });

    errorRate.add(!success);

    // Pequeña pausa entre requests
    sleep(Math.random() * 2 + 1); // 1-3 segundos aleatorios
}

// Función de teardown
export function handleSummary(data) {
    console.log('=== RESUMEN DE PRUEBA DE SATURACIÓN ===');
    console.log(`Requests totales: ${data.metrics.http_reqs.count}`);
    console.log(`Tasa de error: ${(data.metrics.http_req_failed.rate * 100).toFixed(2)}%`);
    console.log(`Tiempo respuesta 95%: ${data.metrics.http_req_duration['p(95)']}ms`);
    console.log(`Throughput: ${data.metrics.http_reqs.rate.toFixed(2)} req/s`);
    
    return {
        'saturation_summary': {
            total_requests: data.metrics.http_reqs.count,
            error_rate: data.metrics.http_req_failed.rate,
            p95_response_time: data.metrics.http_req_duration['p(95)'],
            throughput: data.metrics.http_reqs.rate,
        }
    };
}
```

### 2. Prueba de Usuarios Concurrentes (concurrent-users.js)

**Objetivo**: Evaluar comportamiento con múltiples usuarios simultáneos

```javascript
// scripts/concurrent-users.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.1.0/index.js';

export let options = {
    stages: [
        { duration: '1m', target: 10 },   // 10 usuarios
        { duration: '2m', target: 25 },   // 25 usuarios
        { duration: '3m', target: 50 },   // 50 usuarios
        { duration: '5m', target: 100 },  // 100 usuarios
        { duration: '3m', target: 50 },   // Reducción a 50
        { duration: '2m', target: 25 },   // Reducción a 25
        { duration: '1m', target: 0 },    // Finalización
    ],
    thresholds: {
        http_req_duration: ['p(95)<1000'],
        http_req_failed: ['rate<0.05'],
    },
};

const BASE_URL = 'http://nginx_balancer:80/api';

export default function () {
    // Simular flujo de usuario real
    const flows = [
        flowListarMaquinas,
        flowBuscarMaquina,
        flowAgregarMaquina,
        flowListarMantenimientos,
    ];
    
    // Ejecutar flujo aleatorio
    const selectedFlow = flows[Math.floor(Math.random() * flows.length)];
    selectedFlow();
    
    sleep(randomIntBetween(1, 3));
}

function flowListarMaquinas() {
    const response = http.get(`${BASE_URL}/maquinas/listar`);
    check(response, {
        'listar máquinas - status 200': (r) => r.status === 200,
        'listar máquinas - respuesta array': (r) => {
            try {
                return Array.isArray(JSON.parse(r.body));
            } catch {
                return false;
            }
        },
    });
}

function flowBuscarMaquina() {
    const randomId = Math.floor(Math.random() * 100) + 1;
    const response = http.get(`${BASE_URL}/maquinas/buscar?id=${randomId}`);
    check(response, {
        'buscar máquina - status 200/404': (r) => r.status === 200 || r.status === 404,
    });
}

function flowAgregarMaquina() {
    const payload = {
        nombre: `Test-${Date.now()}`,
        tipo: 'Computadora',
        estado: 'Operativa',
        ubicacion: 'Lab Test',
    };
    
    const params = {
        headers: { 'Content-Type': 'application/json' },
    };
    
    const response = http.post(`${BASE_URL}/maquinas/agregar`, 
                              JSON.stringify(payload), 
                              params);
    check(response, {
        'agregar máquina - status 201': (r) => r.status === 201,
    });
}

function flowListarMantenimientos() {
    const randomId = Math.floor(Math.random() * 100) + 1;
    const response = http.get(`${BASE_URL}/mantenimientos/historial/${randomId}`);
    check(response, {
        'listar mantenimientos - status 200/404': (r) => r.status === 200 || r.status === 404,
    });
}
```

### 3. Prueba de Estrés (stress-test.js)

**Objetivo**: Encontrar puntos de ruptura del sistema

```javascript
// scripts/stress-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    stages: [
        { duration: '2m', target: 50 },   // Warm-up
        { duration: '5m', target: 100 },  // Carga moderada
        { duration: '5m', target: 200 },  // Carga alta
        { duration: '5m', target: 300 },  // Carga muy alta
        { duration: '5m', target: 400 },  // Carga extrema
        { duration: '5m', target: 500 },  // Límite del sistema
        { duration: '2m', target: 0 },    // Recuperación
    ],
    thresholds: {
        http_req_duration: ['p(95)<2000'],  // Más permisivo en estrés
        http_req_failed: ['rate<0.2'],     // Permitir más errores
    },
};

export default function () {
    const payload = {
        nombre: `StressTest-${Date.now()}-${__VU}`,
        tipo: 'Computadora',
        estado: 'Operativa',
        ubicacion: 'Stress Lab',
    };
    
    const params = {
        headers: { 'Content-Type': 'application/json' },
        timeout: '30s',  // Timeout más largo para estrés
    };
    
    const response = http.post('http://nginx_balancer:80/api/maquinas/agregar', 
                              JSON.stringify(payload), 
                              params);
    
    check(response, {
        'status es 201 o 500': (r) => r.status === 201 || r.status === 500,
        'respuesta recibida': (r) => r.body.length > 0,
        'tiempo de respuesta < 5s': (r) => r.timings.duration < 5000,
    });
    
    sleep(0.1); // Mínima pausa para máxima carga
}
```

### 4. Prueba de Picos (spike-test.js)

**Objetivo**: Simular picos súbitos de tráfico

```javascript
// scripts/spike-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    stages: [
        { duration: '2m', target: 10 },   // Nivel normal
        { duration: '10s', target: 200 }, // Pico súbito
        { duration: '1m', target: 200 },  // Mantener pico
        { duration: '10s', target: 10 },  // Caída súbita
        { duration: '2m', target: 10 },   // Recuperación
        { duration: '10s', target: 300 }, // Pico más alto
        { duration: '1m', target: 300 },  // Mantener pico
        { duration: '10s', target: 10 },  // Caída súbita
        { duration: '2m', target: 0 },    // Finalización
    ],
    thresholds: {
        http_req_duration: ['p(95)<1500'],
        http_req_failed: ['rate<0.15'],
    },
};

export default function () {
    const response = http.get('http://nginx_balancer:80/api/maquinas/listar');
    
    check(response, {
        'status 200 durante pico': (r) => r.status === 200,
        'tiempo respuesta aceptable': (r) => r.timings.duration < 1500,
    });
    
    sleep(1);
}
```

## 📊 Métricas y Monitoreo

### 1. Métricas Principales

```javascript
// utils/metrics.js
import { Rate, Trend, Counter } from 'k6/metrics';

// Métricas personalizadas
export let metrics = {
    // Tasa de errores personalizada
    customErrors: new Rate('custom_errors'),
    
    // Tiempos de respuesta por endpoint
    agregarMaquina: new Trend('agregar_maquina_duration'),
    listarMaquinas: new Trend('listar_maquinas_duration'),
    buscarMaquina: new Trend('buscar_maquina_duration'),
    
    // Contadores de operaciones
    totalOperations: new Counter('total_operations'),
    successfulOperations: new Counter('successful_operations'),
    
    // Métricas de negocio
    machinesCreated: new Counter('machines_created'),
    requestsPerSecond: new Rate('requests_per_second'),
};

// Función para registrar métricas
export function recordMetric(name, value, tags = {}) {
    if (metrics[name]) {
        metrics[name].add(value, tags);
    }
}
```

### 2. Checks Personalizados

```javascript
// utils/checks.js
import { check } from 'k6';

export const customChecks = {
    // Check para respuesta exitosa
    isSuccess: (response) => ({
        'status es 2xx': response.status >= 200 && response.status < 300,
        'cuerpo no vacío': response.body.length > 0,
        'content-type JSON': response.headers['Content-Type']?.includes('application/json'),
    }),
    
    // Check para performance
    isPerformant: (response, threshold = 500) => ({
        [`tiempo < ${threshold}ms`]: response.timings.duration < threshold,
        'conexión establecida': response.timings.connecting > 0,
        'tiempo DNS aceptable': response.timings.dns < 100,
    }),
    
    // Check para resiliencia
    isResilient: (response) => ({
        'no timeout': response.timings.duration < 30000,
        'respuesta recibida': response.status !== 0,
        'servidor disponible': response.status !== 503,
    }),
};

// Función para ejecutar checks y registrar métricas
export function executeChecks(response, checkType, threshold = 500) {
    let result;
    
    switch (checkType) {
        case 'success':
            result = check(response, customChecks.isSuccess);
            break;
        case 'performance':
            result = check(response, customChecks.isPerformant(response, threshold));
            break;
        case 'resilience':
            result = check(response, customChecks.isResilient(response));
            break;
        default:
            result = check(response, customChecks.isSuccess);
    }
    
    return result;
}
```

### 3. Helpers de Testing

```javascript
// utils/helpers.js
import { randomIntBetween, randomItem } from 'https://jslib.k6.io/k6-utils/1.1.0/index.js';

// Datos de prueba
export const TEST_DATA = {
    machineTypes: ['Computadora', 'Impresora', 'Scanner', 'Servidor', 'Router'],
    statuses: ['Operativa', 'Mantenimiento', 'Fuera de Servicio', 'En Reparación'],
    locations: [
        'Laboratorio A', 'Laboratorio B', 'Laboratorio C',
        'Sala de Servidores', 'Oficina Principal', 'Biblioteca'
    ],
    users: [
        'admin', 'usuario1', 'usuario2', 'tecnico1', 'tecnico2',
        'supervisor', 'gestor', 'analista', 'desarrollador', 'tester'
    ],
};

// Generar máquina aleatoria
export function generateRandomMachine() {
    return {
        nombre: `Maquina-Test-${Date.now()}-${randomIntBetween(1000, 9999)}`,
        tipo: randomItem(TEST_DATA.machineTypes),
        estado: randomItem(TEST_DATA.statuses),
        ubicacion: randomItem(TEST_DATA.locations),
        fecha_adquisicion: new Date(Date.now() - randomIntBetween(0, 365 * 24 * 60 * 60 * 1000))
            .toISOString().split('T')[0],
        responsable: randomItem(TEST_DATA.users),
        descripcion: `Máquina de prueba generada automáticamente`,
        costo: randomIntBetween(100, 5000),
        marca: `Marca-${randomIntBetween(1, 10)}`,
        modelo: `Modelo-${randomIntBetween(100, 999)}`,
        numero_serie: `SN-${Date.now()}-${randomIntBetween(1000, 9999)}`,
    };
}

// Generar mantenimiento aleatorio
export function generateRandomMaintenance(machineId) {
    return {
        codigo_maquina: machineId,
        tipo_mantenimiento: randomItem(['Preventivo', 'Correctivo', 'Predictivo']),
        descripcion: `Mantenimiento de prueba para máquina ${machineId}`,
        costo: randomIntBetween(50, 1000),
        tecnico: randomItem(TEST_DATA.users),
        fecha_mantenimiento: new Date().toISOString().split('T')[0],
        proximo_mantenimiento: new Date(Date.now() + randomIntBetween(7, 90) * 24 * 60 * 60 * 1000)
            .toISOString().split('T')[0],
    };
}

// Espera aleatoria
export function randomSleep(min = 1, max = 3) {
    sleep(randomIntBetween(min, max));
}

// Retraso exponencial para reintentos
export function exponentialBackoff(attempt, baseDelay = 1000, maxDelay = 10000) {
    const delay = Math.min(baseDelay * Math.pow(2, attempt), maxDelay);
    sleep(delay / 1000);
    return delay;
}

// Validar respuesta JSON
export function isValidJSON(response) {
    try {
        JSON.parse(response.body);
        return true;
    } catch {
        return false;
    }
}
```

## 🚀 Ejecución de Pruebas

### 1. Configuración Docker

```dockerfile
# Dockerfile
FROM loadimpact/k6:latest

# Instalar utilidades adicionales
RUN apk add --no-cache curl jq

# Copiar scripts y utilidades
COPY scripts/ /scripts/
COPY utils/ /utils/
COPY data/ /data/

# Directorio de trabajo
WORKDIR /scripts

# Variables de entorno
ENV K6_PROMETHEUS_RW_SERVER_URL=http://prometheus:9090/api/v1/write
ENV K6_STATSD_ENABLE=true
ENV K6_STATSD_ADDR=statsd:8125

# Comando por defecto
CMD ["run", "/scripts/maquina-saturator.js"]
```

### 2. Docker Compose para Testing

```yaml
# docker-compose.k6.yml
version: '3.8'

services:
  k6-saturator:
    build:
      context: ./k6
      dockerfile: Dockerfile
    container_name: k6_saturator
    environment:
      - BASE_URL=http://nginx_balancer:80
      - K6_NO_CONNECTION_REUSE=true
      - K6_WEB_DASHBOARD=true
      - K6_WEB_DASHBOARD_PORT=5665
    networks:
      - siglab_network
      - frontend_network
    ports:
      - "5665:5665"  # k6 web dashboard
    volumes:
      - ./k6/reports:/reports
    profiles:
      - load-test
      - monitoring

  k6-concurrent:
    build:
      context: ./k6
      dockerfile: Dockerfile
    container_name: k6_concurrent
    command: ["run", "/scripts/concurrent-users.js"]
    environment:
      - BASE_URL=http://nginx_balancer:80
      - K6_PROMETHEUS_RW_SERVER_URL=http://prometheus:9090/api/v1/write
    networks:
      - siglab_network
      - frontend_network
    volumes:
      - ./k6/reports:/reports
    profiles:
      - concurrent-test

  # Servicios de monitoreo opcionales
  prometheus:
    image: prom/prometheus:latest
    container_name: k6_prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./k6/prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - siglab_network
    profiles:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    container_name: k6_grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - ./k6/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./k6/grafana/datasources:/etc/grafana/provisioning/datasources
    networks:
      - siglab_network
    profiles:
      - monitoring

networks:
  siglab_network:
    external: true
  frontend_network:
    external: true
```

### 3. Comandos de Ejecución

```bash
# Prueba de saturación
docker-compose --profile load-test up --build k6-saturator

# Prueba de usuarios concurrentes
docker-compose --profile concurrent-test up --build k6-concurrent

# Prueba con monitoreo completo
docker-compose --profile monitoring up --build

# Ver resultados en tiempo real
docker logs k6_saturator -f

# Acceder a dashboards
# k6: http://localhost:5665
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)
```

### 4. Ejecución Local

```bash
# Instalar k6 localmente
# macOS: brew install k6
# Ubuntu: sudo apt-get update && sudo apt-get install k6
# Windows: choco install k6

# Ejecutar prueba simple
k6 run scripts/maquina-saturator.js

# Con variables de entorno
K6_WEB_DASHBOARD=true k6 run scripts/maquina-saturator.js

# Exportar resultados
k6 run --out json=results.json scripts/maquina-saturator.js
k6 run --out csv=results.csv scripts/maquina-saturator.js

# Ejecutar con opciones personalizadas
k6 run --vus 50 --duration 5m scripts/maquina-saturator.js
```

## 📈 Análisis de Resultados

### 1. Métricas Clave

| Métrica | Descripción | Umbral Aceptable | Umbral Crítico |
|---------|-------------|------------------|----------------|
| **Throughput** | Requests por segundo | > 50 req/s | < 20 req/s |
| **P95 Response Time** | 95% de requests | < 500ms | > 2000ms |
| **Error Rate** | Tasa de errores | < 1% | > 10% |
| **Max Response Time** | Tiempo máximo | < 2000ms | > 5000ms |
| **Connection Time** | Tiempo de conexión | < 100ms | > 500ms |

### 2. Reportes Automáticos

```javascript
// Función para generar reporte personalizado
export function handleSummary(data) {
    return {
        'performance_summary': {
            total_requests: data.metrics.http_reqs.count,
            failed_requests: data.metrics.http_req_failed.count,
            error_rate: data.metrics.http_req_failed.rate,
            avg_response_time: data.metrics.http_req_duration.avg,
            p95_response_time: data.metrics.http_req_duration['p(95)'],
            p99_response_time: data.metrics.http_req_duration['p(99)'],
            max_response_time: data.metrics.http_req_duration.max,
            throughput: data.metrics.http_reqs.rate,
        },
        'load_distribution': {
            vus_max: data.metrics.vus.max,
            vus_current: data.metrics.vus.value,
        },
        'data_transferred': {
            bytes_received: data.metrics.http_req_received.bytes,
            bytes_sent: data.metrics.http_req_sent.bytes,
        },
        'thresholds': {
            passed: data.thresholds.http_req_duration.passes,
            failed: data.thresholds.http_req_duration.fails,
        }
    };
}
```

### 3. Integración CI/CD

```yaml
# .github/workflows/load-testing.yml
name: Load Testing

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'  # Cada día a las 2 AM

jobs:
  load-test:
    runs-on: ubuntu-latest
    
    services:
      nginx:
        image: nginx:alpine
        ports:
          - 8888:80
        options: >-
          --health-cmd "curl -f http://localhost/ || exit 1"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    
    - name: Setup k6
      run: |
        sudo gpg -k
        sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
        echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
        sudo apt-get update
        sudo apt-get install k6
    
    - name: Run load tests
      run: |
        k6 run --out json=results.json k6/scripts/maquina-saturator.js
    
    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: load-test-results
        path: results.json
    
    - name: Check thresholds
      run: |
        # Script para verificar umbrales
        python3 scripts/check_thresholds.py results.json
```

## 🔧 Configuración Avanzada

### 1. Variables de Entorno

```bash
# .env.k6
BASE_URL=http://nginx_balancer:80
API_VERSION=v1
TIMEOUT=30000
MAX_RETRIES=3
RETRY_DELAY=1000

# k6 específicas
K6_NO_CONNECTION_REUSE=true
K6_WEB_DASHBOARD=true
K6_WEB_DASHBOARD_PORT=5665
K6_PROMETHEUS_RW_SERVER_URL=http://prometheus:9090/api/v1/write
K6_STATSD_ENABLE=true
K6_STATSD_ADDR=statsd:8125

# Base de datos de prueba
MYSQL_HOST=mysql
MYSQL_USER=root
MYSQL_PASSWORD=Clubpengui1
MYSQL_DATABASE=proyecto_maquinas
```

### 2. Configuración Prometheus

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'k6'
    static_configs:
      - targets: ['k6:6565']
    metrics_path: /metrics
    scrape_interval: 5s

rule_files:
  - "k6_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
```

### 3. Dashboards Grafana

```json
{
  "dashboard": {
    "title": "k6 Load Testing Dashboard",
    "panels": [
      {
        "title": "Requests per Second",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(k6_http_reqs_total[5m])",
            "legendFormat": "{{method}} {{status}} {{url}}"
          }
        ]
      },
      {
        "title": "Response Time P95",
        "type": "graph",
        "targets": [
          {
            "expr": "k6_http_req_duration{quantile=\"0.95\"}",
            "legendFormat": "P95 Response Time"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "singlestat",
        "targets": [
          {
            "expr": "rate(k6_http_req_failed_total[5m]) / rate(k6_http_reqs_total[5m])",
            "legendFormat": "Error Rate"
          }
        ]
      }
    ]
  }
}
```

## 🚨 Troubleshooting

### Problemas Comunes

#### 1. "connection refused" o timeouts

```bash
# Verificar conectividad
docker exec k6_saturator curl -v http://nginx_balancer:80/health

# Revisar redes Docker
docker network ls
docker network inspect siglab_network

# Verificar que nginx esté corriendo
docker-compose ps nginx
```

#### 2. Alto uso de memoria en k6

```bash
# Limitar memoria del contenedor
docker-compose -f docker-compose.k6.yml up -d --memory=2g k6-saturator

# Reducir número de VUs
# Modificar script: stages: [{ duration: '5m', target: 20 }]  // En lugar de 100
```

#### 3. Resultados inconsistentes

```bash
# Asegurar cleanup entre pruebas
docker-compose down --volumes
docker system prune -f

# Usar misma configuración de red
docker-compose --profile load-test down
docker-compose --profile load-test up --build
```

### Debug Mode

```javascript
// Habilitar debug en scripts
export let options = {
    debug: true,  // Muestra información detallada
    throw: true,  // Detiene en errores
    // ... otras opciones
};

// Logging personalizado
export default function () {
    console.log(`VU: ${__VU}, Iteration: ${__ITER}`);
    
    const response = http.post(url, payload, params);
    console.log(`Response status: ${response.status}, duration: ${response.timings.duration}ms`);
    
    // Resto del test
}
```

## 📊 Optimización de Pruebas

### 1. Mejores Prácticas

- **Datos Realistas**: Usar datos que simulen uso real
- **Escalado Gradual**: Aumentar carga progresivamente
- **Métricas Relevantes**: Medir lo que importa para el negocio
- **Repetibilidad**: Ejecutar mismas condiciones múltiples veces
- **Limpieza**: Limpiar datos de prueba entre ejecuciones

### 2. Optimización de Rendimiento

```javascript
// Reutilizar conexiones HTTP
export const options = {
    noConnectionReuse: false,  // Reutilizar conexiones
    noVUConnectionReuse: false,  // Reutilizar por VU
    discardResponseBodies: true,  // Descartar cuerpos de respuesta
    insecureSkipTLSVerify: true,  // Skip TLS verify para testing
    // ... otras opciones
};

// Batch requests para mayor throughput
import http from 'k6/http';

export default function () {
    const requests = [
        ['GET', `${BASE_URL}/maquinas/listar`],
        ['GET', `${BASE_URL}/maquinas/buscar?id=1`],
        ['GET', `${BASE_URL}/mantenimientos/historial/1`],
    ];
    
    const responses = http.batch(requests);
    
    // Procesar respuestas
    responses.forEach((response, index) => {
        check(response, {
            [`request ${index} successful`]: (r) => r.status < 400,
        });
    });
}
```

### 3. Paralelización

```bash
# Ejecutar múltiples pruebas en paralelo
k6 run script1.js &
k6 run script2.js &
k6 run script3.js &
wait

# O con diferentes perfiles
docker-compose --profile test1 up -d &
docker-compose --profile test2 up -d &
docker-compose --profile test3 up -d &
wait
```

## 🔄 Integración Continua

### 1. Pipeline Automatizado

```bash
#!/bin/bash
# scripts/run_load_tests.sh

set -e

echo "=== Iniciando Suite de Pruebas de Carga ==="

# Variables
TEST_ENV=${1:-staging}
REPORT_DIR="reports/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$REPORT_DIR"

# Función para ejecutar prueba
run_test() {
    local test_name=$1
    local script=$2
    local duration=$3
    
    echo "Ejecutando prueba: $test_name"
    
    k6 run \
        --out json="$REPORT_DIR/${test_name}.json" \
        --out csv="$REPORT_DIR/${test_name}.csv" \
        --summary-export="$REPORT_DIR/${test_name}_summary.json" \
        --duration "$duration" \
        "scripts/$script"
    
    echo "Prueba $test_name completada. Resultados en $REPORT_DIR"
}

# Ejecutar suite de pruebas
run_test "saturation" "maquina-saturator.js" "15m"
run_test "concurrent" "concurrent-users.js" "20m"
run_test "stress" "stress-test.js" "30m"

# Generar reporte consolidado
python3 scripts/generate_report.py "$REPORT_DIR"

echo "=== Suite de Pruebas Completada ==="
echo "Reporte consolidado: $REPORT_DIR/consolidated_report.html"
```

### 2. Análisis Automático

```python
# scripts/analyze_results.py
import json
import sys
from datetime import datetime

def analyze_results(results_file):
    with open(results_file, 'r') as f:
        data = json.load(f)
    
    metrics = data['metrics']
    
    analysis = {
        'timestamp': datetime.now().isoformat(),
        'performance': {
            'total_requests': metrics['http_reqs']['count'],
            'error_rate': metrics['http_req_failed']['rate'],
            'avg_response_time': metrics['http_req_duration']['avg'],
            'p95_response_time': metrics['http_req_duration']['p(95)'],
            'throughput': metrics['http_reqs']['rate'],
        },
        'status': 'PASS' if metrics['http_req_failed']['rate'] < 0.05 else 'FAIL',
    }
    
    return analysis

if __name__ == "__main__":
    results_file = sys.argv[1]
    analysis = analyze_results(results_file)
    
    print(json.dumps(analysis, indent=2))
    
    # Exit code para CI/CD
    sys.exit(0 if analysis['status'] == 'PASS' else 1)
```

---

**Versión**: 2.0.0  
**Estado**: Producción  
**Última Actualización**: 2026  
**Framework**: k6 Performance Testing
