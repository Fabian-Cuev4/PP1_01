# Frontend - Aplicación React SIGLAB

## 📋 Descripción
Aplicación web moderna construida con React y Vite para el sistema de gestión de laboratorios SIGLAB. Interfaz responsiva y optimizada para alta usabilidad.

## 🎨 Características Principales

- **Diseño Moderno**: UI/UX intuitiva con TailwindCSS
- **Responsive**: Adaptativo a desktop, tablet y móvil
- **Componentes Reutilizables**: Arquitectura basada en componentes
- **Estado Global**: Gestión centralizada con Context API
- **Ruteo**: Navegación SPA con React Router
- **Formularios**: Validación y manejo de errores
- **Notificaciones**: Sistema de alertas y feedback
- **Gráficos**: Visualización de datos con Chart.js

## 🛠️ Stack Tecnológico

### Core Framework
- **React 18**: Framework JavaScript con hooks
- **Vite**: Build tool ultra rápido
- **JavaScript ES6+**: Sintaxis moderna

### Estilos y UI
- **TailwindCSS**: Framework CSS utility-first
- **Lucide React**: Iconos modernos
- **Headless UI**: Componentes accesibles
- **CSS Modules**: Estilos encapsulados

### Estado y Datos
- **React Context**: Estado global
- **React Query**: Caching y sincronización de servidor
- **Axios**: Cliente HTTP con interceptores
- **Formik**: Manejo de formularios

### Desarrollo y Build
- **ESLint**: Calidad de código
- **Prettier**: Formato consistente
- **TypeScript**: Tipado estático (opcional)
- **Vite PWA**: Soporte PWA

## 📁 Estructura del Proyecto

```
frontend/
├── public/                     # Archivos estáticos
│   ├── index.html             # Template HTML
│   ├── favicon.ico            # Favicon
│   └── manifest.json          # PWA manifest
├── src/
│   ├── components/            # Componentes UI
│   │   ├── common/           # Componentes genéricos
│   │   │   ├── Button.jsx    # Botón reutilizable
│   │   │   ├── Modal.jsx     # Modal genérico
│   │   │   ├── Table.jsx     # Tabla de datos
│   │   │   └── Alert.jsx     # Alertas y notificaciones
│   │   ├── forms/            # Componentes de formulario
│   │   │   ├── LoginForm.jsx # Formulario login
│   │   │   ├── MaquinaForm.jsx # Formulario máquina
│   │   │   └── MantenimientoForm.jsx # Formulario mantenimiento
│   │   └── layout/           # Componentes de layout
│   │       ├── Header.jsx    # Cabecera principal
│   │       ├── Sidebar.jsx   # Menú lateral
│   │       └── Footer.jsx    # Pie de página
│   ├── pages/                # Páginas principales
│   │   ├── Login.jsx         # Página de login
│   │   ├── Dashboard.jsx     # Dashboard principal
│   │   ├── Maquinas.jsx      # Gestión de máquinas
│   │   ├── Mantenimientos.jsx # Gestión de mantenimientos
│   │   ├── Reportes.jsx      # Reportes y estadísticas
│   │   └── Profile.jsx       # Perfil de usuario
│   ├── hooks/                # Hooks personalizados
│   │   ├── useAuth.js        # Hook de autenticación
│   │   ├── useApi.js         # Hook para llamadas API
│   │   ├── useLocalStorage.js # Hook para storage local
│   │   └── useDebounce.js    # Hook para debounce
│   ├── services/             # Servicios de API
│   │   ├── api.js            # Configuración Axios
│   │   ├── authService.js    # Servicio de autenticación
│   │   ├── maquinaService.js # Servicio de máquinas
│   │   └── mantenimientoService.js # Servicio de mantenimientos
│   ├── context/              # Context providers
│   │   ├── AuthContext.js    # Contexto de autenticación
│   │   ├── NotificationContext.js # Contexto de notificaciones
│   │   └── ThemeContext.js   # Contexto de tema
│   ├── utils/                # Utilidades
│   │   ├── constants.js      # Constantes de la app
│   │   ├── helpers.js        # Funciones helper
│   │   ├── validators.js     # Validaciones
│   │   └── formatters.js     # Formateo de datos
│   ├── styles/               # Estilos globales
│   │   ├── globals.css       # CSS global
│   │   ├── components.css    # Estilos componentes
│   │   └── variables.css     # Variables CSS
│   ├── assets/               # Assets estáticos
│   │   ├── images/           # Imágenes
│   │   ├── icons/            # Iconos
│   │   └── fonts/            # Fuentes
│   ├── App.jsx               # Componente principal
│   ├── main.jsx              # Entry point
│   └── index.css             # Estilos base
├── package.json              # Dependencias npm
├── vite.config.js            # Configuración Vite
├── tailwind.config.js        # Configuración Tailwind
├── eslint.config.js          # Configuración ESLint
├── .gitignore                # Exclusiones Git
├── Dockerfile                # Imagen Docker
└── README.md                 # Este archivo
```

## 🚀 Componentes Principales

### 1. Sistema de Autenticación
```jsx
// components/forms/LoginForm.jsx
const LoginForm = () => {
  const { login } = useAuth();
  const [formData, setFormData] = useState({ email: '', password: '' });
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    await login(formData);
  };
  
  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Form fields */}
    </form>
  );
};
```

### 2. Gestión de Máquinas
```jsx
// pages/Maquinas.jsx
const Maquinas = () => {
  const { data: maquinas, loading, error } = useApi('/api/maquinas/listar');
  const { showNotification } = useNotification();
  
  const handleDelete = async (id) => {
    try {
      await maquinaService.delete(id);
      showNotification('Máquina eliminada', 'success');
    } catch (error) {
      showNotification('Error al eliminar', 'error');
    }
  };
  
  return (
    <div className="container mx-auto p-6">
      <MaquinaTable maquinas={maquinas} onDelete={handleDelete} />
    </div>
  );
};
```

### 3. Dashboard con Gráficos
```jsx
// pages/Dashboard.jsx
const Dashboard = () => {
  const { data: stats } = useApi('/api/maquinas/dashboard');
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <StatCard title="Total Máquinas" value={stats?.total} />
      <StatCard title="Operativas" value={stats?.operativas} />
      <StatCard title="En Mantenimiento" value={stats?.mantenimiento} />
      <ChartCard data={stats?.chartData} />
    </div>
  );
};
```

## 🎨 Sistema de Diseño

### Paleta de Colores
```css
/* tailwind.config.js */
theme: {
  extend: {
    colors: {
      primary: {
        50: '#eff6ff',
        500: '#3b82f6',
        600: '#2563eb',
        700: '#1d4ed8',
      },
      secondary: {
        50: '#f8fafc',
        500: '#64748b',
        600: '#475569',
        700: '#334155',
      },
      success: '#10b981',
      warning: '#f59e0b',
      error: '#ef4444',
    }
  }
}
```

### Componentes Base
```jsx
// components/common/Button.jsx
const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'md', 
  loading = false,
  ...props 
}) => {
  const baseClasses = 'font-medium rounded-lg transition-colors';
  const variantClasses = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
    danger: 'bg-red-600 text-white hover:bg-red-700',
  };
  
  return (
    <button 
      className={`${baseClasses} ${variantClasses[variant]}`}
      disabled={loading}
      {...props}
    >
      {loading ? <Spinner /> : children}
    </button>
  );
};
```

## 🔄 Estado y Manejo de Datos

### Context de Autenticación
```jsx
// context/AuthContext.js
const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  const login = async (credentials) => {
    const response = await authService.login(credentials);
    setUser(response.user);
    localStorage.setItem('token', response.token);
  };
  
  const logout = () => {
    setUser(null);
    localStorage.removeItem('token');
  };
  
  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
```

### Hook Personalizado para API
```jsx
// hooks/useApi.js
const useApi = (url, options = {}) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await api.get(url, options);
        setData(response.data);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [url]);
  
  return { data, loading, error };
};
```

## 🚀 Desarrollo

### Instalación y Ejecución
```bash
# Instalar dependencias
npm install

# Modo desarrollo
npm run dev

# Modo producción
npm run build
npm run preview

# Análisis de bundle
npm run build -- --analyze
```

### Variables de Entorno
```bash
# .env.development
VITE_API_URL=http://localhost:8888/api
VITE_WS_URL=ws://localhost:18081
VITE_APP_TITLE=SIGLAB - Desarrollo

# .env.production
VITE_API_URL=https://api.siglab.edu/api
VITE_WS_URL=wss://dashboard.siglab.edu
VITE_APP_TITLE=SIGLAB
```

### Configuración Vite
```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg}']
      }
    })
  ],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8888',
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          charts: ['chart.js', 'react-chartjs-2']
        }
      }
    }
  }
});
```

## 📱 Responsive Design

### Breakpoints
```css
/* Tailwind breakpoints */
sm: 640px   /* Small devices */
md: 768px   /* Medium devices */
lg: 1024px  /* Large devices */
xl: 1280px  /* Extra large */
2xl: 1536px /* 2X large */
```

### Ejemplo de Componente Responsivo
```jsx
const ResponsiveTable = ({ data }) => {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full">
        {/* Desktop view */}
        <thead className="hidden md:table-header-group">
          <tr>
            <th className="px-6 py-3">ID</th>
            <th className="px-6 py-3">Nombre</th>
            <th className="px-6 py-3">Estado</th>
            <th className="px-6 py-3">Acciones</th>
          </tr>
        </thead>
        
        {/* Mobile view */}
        <tbody className="block md:table-row-group">
          {data.map(item => (
            <tr key={item.id} className="block md:table-row">
              <td className="block md:table-cell px-6 py-4">
                <span className="font-semibold md:hidden">ID: </span>
                {item.id}
              </td>
              {/* More cells */}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
```

## 🧪 Testing

### Tests Unitarios con Vitest
```bash
# Ejecutar tests
npm run test

# Con cobertura
npm run test:coverage

# Watch mode
npm run test:watch
```

### Ejemplo de Test
```jsx
// components/__tests__/Button.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '../Button';

describe('Button', () => {
  test('renders correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });
  
  test('handles click events', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### Tests E2E con Playwright
```bash
# Ejecutar tests E2E
npm run test:e2e

# Generar reporte
npm run test:e2e -- --reporter=html
```

## 📊 Optimización

### Performance
- **Code Splitting**: División automática con React.lazy
- **Memoización**: React.memo y useMemo para componentes pesados
- **Virtual Scrolling**: Para listas grandes
- **Image Optimization**: Lazy loading y WebP format

### Bundle Size
```bash
# Analizar tamaño del bundle
npm run build -- --analyze

# Optimizar dependencias
npm uninstall unused-package
npm install --save-dev bundle-analyzer
```

### PWA Features
```javascript
// PWA manifest
{
  "name": "SIGLAB",
  "short_name": "SIGLAB",
  "description": "Sistema de Gestión de Laboratorios",
  "theme_color": "#3b82f6",
  "background_color": "#ffffff",
  "display": "standalone",
  "icons": [
    {
      "src": "icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ]
}
```

## 🚀 Despliegue

### Docker
```dockerfile
# Dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Producción
```bash
# Build para producción
npm run build

# Desplegar a servidor
rsync -av dist/ user@server:/var/www/html/

# Configurar Nginx
server {
    listen 80;
    server_name siglab.edu;
    root /var/www/html;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://backend:8000;
    }
}
```

## 🔧 Configuración Avanzada

### Internacionalización (i18n)
```jsx
// i18n setup
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      es: { translation: require('./locales/es.json') },
      en: { translation: require('./locales/en.json') }
    },
    lng: 'es',
    fallbackLng: 'es'
  });
```

### Tema Oscuro
```jsx
// context/ThemeContext.js
const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [darkMode, setDarkMode] = useState(false);
  
  const toggleTheme = () => {
    setDarkMode(!darkMode);
    document.documentElement.classList.toggle('dark');
  };
  
  return (
    <ThemeContext.Provider value={{ darkMode, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};
```

## 🚨 Troubleshooting

### Problemas Comunes

#### 1. Hot Reload no funciona
```bash
# Limpiar caché de Vite
npm run dev -- --force

# Reinstalar dependencias
rm -rf node_modules package-lock.json
npm install
```

#### 2. Errores de CORS
```javascript
// vite.config.js
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8888',
      changeOrigin: true,
      secure: false
    }
  }
}
```

#### 3. Build falla por memoria
```bash
# Aumentar límite de Node
export NODE_OPTIONS="--max-old-space-size=4096"

# Build con menos paralelismo
npm run build -- --max-parallel 1
```

## 📈 Métricas y Monitoreo

### Web Vitals
```jsx
// utils/webVitals.js
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

const sendToAnalytics = (metric) => {
  // Enviar métricas a servicio de análisis
  gtag('event', metric.name, {
    value: Math.round(metric.value),
    event_category: 'Web Vitals'
  });
};

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getFCP(sendToAnalytics);
getLCP(sendToAnalytics);
getTTFB(sendToAnalytics);
```

### Error Boundary
```jsx
// components/ErrorBoundary.jsx
class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  
  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900">Oops!</h1>
            <p className="mt-2 text-gray-600">Something went wrong.</p>
            <button 
              onClick={() => window.location.reload()}
              className="mt-4 px-4 py-2 bg-blue-600 text-white rounded"
            >
              Reload Page
            </button>
          </div>
        </div>
      );
    }
    
    return this.props.children;
  }
}
```

## 📝 Mejores Prácticas

### Código
- **Componentes Funcionales**: Usar hooks en lugar de clases
- **Component Purity**: Evitar side effects en render
- **PropTypes**: Validar props con TypeScript o PropTypes
- **Consistent Naming**: Convenciones claras para archivos y componentes

### Performance
- **React.memo**: Para componentes que no necesitan re-render
- **useCallback/useMemo**: Para funciones y cálculos pesados
- **Code Splitting**: Cargar componentes bajo demanda
- **Virtual Lists**: Para listas muy largas

### UX
- **Loading States**: Indicadores de carga claros
- **Error Handling**: Mensajes de error amigables
- **Form Validation**: Validación en tiempo real
- **Accessibility**: Atributos ARIA y navegación por teclado

---

**Versión**: 2.0.0  
**Framework**: React 18 + Vite  
**Estado**: Producción  
**Última Actualización**: 2026
