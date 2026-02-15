# Frontend - Interfaz Web SIGLAB

## Descripción
Interfaz web moderna y responsiva para el sistema de gestión de laboratorios SIGLAB.

## Tecnologías
- **HTML5**: Estructura semántica y accesible
- **CSS3**: Estilos modernos con Flexbox/Grid
- **JavaScript ES6+**: Lógica asíncrona y dinámica
- **Fetch API**: Comunicación con el backend
- **Responsive Design**: Adaptativo a móviles y tablets

## Estructura del Proyecto

```
frontend/
├── index.html          # Página principal
├── styles.css         # Hoja de estilos principal
├── script.js          # Lógica JavaScript
└── README.md          # Este archivo
```

## Funcionalidades Principales

### Gestión de Máquinas
- **Listado**: Ver todas las máquinas del sistema
- **Búsqueda**: Filtrar máquinas por ID o nombre
- **Agregar**: Formulario para registrar nuevas máquinas
- **Editar**: Modificar datos de máquinas existentes
- **Eliminar**: Remover máquinas del inventario

### Gestión de Mantenimientos
- **Historial**: Ver todos los mantenimientos realizados
- **Registro**: Agregar nuevos mantenimientos
- **Filtros**: Buscar por máquina o fecha
- **Reportes**: Generar informes detallados

### Dashboard
- **Resumen**: Vista general del sistema
- **Estadísticas**: Métricas de uso y estado
- **Gráficos**: Visualización de datos
- **Alertas**: Notificaciones importantes

## Componentes UI

### Header
- **Navegación**: Menú principal del sistema
- **Usuario**: Información de sesión actual
- **Logout**: Cerrar sesión segura

### Main Content
- **Cards**: Tarjetas de información
- **Tables**: Tablas de datos ordenables
- **Forms**: Formularios validados
- **Modals**: Ventanas emergentes

### Footer
- **Información**: Datos de contacto
- **Versión**: Número de versión del sistema

## Estilos y Diseño

### CSS Architecture
```css
/* Variables CSS */
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    --success-color: #27ae60;
    --danger-color: #e74c3c;
    --warning-color: #f39c12;
}

/* Layout */
.container { max-width: 1200px; margin: 0 auto; }
.grid { display: grid; gap: 1rem; }
.flex { display: flex; justify-content: space-between; }
```

### Responsive Design
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## JavaScript Architecture

### Módulos Principales
```javascript
// API Service
class ApiService {
    async getMachines() { /* ... */ }
    async addMachine(data) { /* ... */ }
    async updateMachine(id, data) { /* ... */ }
}

// UI Controller
class UIController {
    showMachines(machines) { /* ... */ }
    showMessage(type, text) { /* ... */ }
    validateForm(formData) { /* ... */ }
}

// Event Handlers
document.addEventListener('DOMContentLoaded', () => {
    // Inicialización
});
```

## Integración con Backend

### Endpoints Utilizados
```javascript
// Base URL
const API_BASE = 'http://localhost:8888/api';

// Peticiones comunes
fetch(`${API_BASE}/maquinas/listar`)
fetch(`${API_BASE}/maquinas/agregar`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
})
```

## Manejo de Estados

### Loading States
- **Spinners**: Indicadores de carga
- **Skeletons**: Placeholders mientras carga
- **Progress Bars**: Barras de progreso

### Error Handling
- **Try-Catch**: Captura de errores
- **User Messages**: Notificaciones amigables
- **Fallbacks**: Comportamiento ante fallos

## Optimización

### Performance
- **Lazy Loading**: Carga bajo demanda
- **Debouncing**: Optimización de búsquedas
- **Caching**: Almacenamiento local temporal

### Accesibilidad
- **ARIA Labels**: Etiquetas para screen readers
- **Keyboard Navigation**: Navegación sin mouse
- **Contrast**: Cumplimiento WCAG

## Testing

### Pruebas Manuales
- **Cross-browser**: Chrome, Firefox, Safari, Edge
- **Responsive**: Diferentes tamaños de pantalla
- **Functionality**: Todos los flujos de usuario

### Automatización (futura)
- **Unit Tests**: Jest para JavaScript
- **E2E Tests**: Cypress para flujos completos
- **Visual Regression**: Percy para UI

## Deploy

### Configuración Nginx
```nginx
server {
    listen 18080;
    server_name localhost;
    
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

### Build Process
```bash
# Minificación CSS/JS
npm run build

# Optimización de imágenes
npm run optimize

# Deploy a producción
docker build -t siglab-frontend .
```

## Desarrollo

### Herramientas Recomendadas
- **VS Code**: Editor con extensiones web
- **Chrome DevTools**: Debugging y profiling
- **Postman**: Testing de API
- **Lighthouse**: Auditoría de rendimiento

### Convenciones
- **BEM**: Metodología CSS (Block__Element--Modifier)
- **ESLint**: Calidad de código JavaScript
- **Prettier**: Formato consistente
