# SIGLAB - Frontend React

Aplicación frontend del Sistema de Gestión de Laboratorios (SIGLAB) migrada a React 19.2.0 con Vite 7.3.1.

## 🚀 Tecnologías

- **React 19.2.0** - Framework principal de UI
- **Vite 7.3.1** - Herramienta de build y desarrollo
- **React Router DOM 7.13.0** - Manejo de rutas
- **CSS3** - Estilos personalizados
- **Font Awesome** - Iconos

## 📁 Estructura del Proyecto

```
src/
├── components/          # Componentes reutilizables (futuro)
├── pages/              # Páginas principales
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── Dashboard.jsx
│   ├── Maquinas.jsx
│   ├── AgregarMaquina.jsx
│   └── Historial.jsx
├── services/           # Servicios API
│   └── api.js
├── styles/            # Estilos CSS
│   ├── Login.css
│   ├── Register.css
│   ├── Dashboard.css
│   ├── Maquinas.css
│   ├── AgregarMaquina.css
│   └── Historial.css
├── App.jsx            # Componente principal con rutas
└── main.jsx           # Punto de entrada
```

## 🛠️ Instalación y Desarrollo

### Prerrequisitos
- Node.js 18+
- npm o yarn

### Instalación
```bash
npm install
```

### Desarrollo
```bash
npm run dev
```
La aplicación se ejecutará en `http://localhost:5173`

### Build para Producción
```bash
npm run build
```

### Preview de Producción
```bash
npm run preview
```

## 🔧 Configuración

### Proxy de Desarrollo
El proyecto está configurado con un proxy en `vite.config.js` para redirigir las llamadas `/api` al backend en `http://localhost:18080`.

### Variables de Entorno
- `VITE_API_URL` - URL base de la API (opcional, por defecto usa `/api`)

## 📱 Funcionalidades

### 🔐 Autenticación
- Login de usuarios
- Registro de nuevos usuarios
- Gestión de sesiones con localStorage

### 🏠 Dashboard
- Vista principal del espacio de trabajo
- Navegación a gestión de máquinas
- Información del usuario y cierre de sesión

### 🖥️ Gestión de Máquinas
- Listado de máquinas con estados visuales
- Agregar nuevas máquinas
- Búsqueda y filtrado
- Estados: Operativa, Fuera de servicio, Dada de baja

### 🔧 Mantenimiento
- Historial de mantenimientos por máquina
- Agregar nuevos mantenimientos
- Informes técnicos

## 🎨 Estilos

El proyecto utiliza CSS3 con:
- Diseño responsive
- Animaciones y transiciones suaves
- Paleta de colores consistente
- Componentes modulares

## 🐳 Docker

### Build para Producción
```bash
docker build -t siglab-frontend .
```

### Ejecutar Contenedor
```bash
docker run -p 80:80 siglab-frontend
```

## 🔄 Integración con Backend

La aplicación se integra con el backend a través de los siguientes endpoints:

- `POST /api/login` - Autenticación
- `POST /api/register` - Registro
- `GET /api/maquinas/listar` - Listar máquinas
- `POST /api/maquinas/agregar` - Agregar máquina
- `GET /api/mantenimiento/historial` - Historial de mantenimientos
- `POST /api/mantenimiento/agregar` - Agregar mantenimiento

## 🌐 Navegación

La aplicación utiliza React Router con las siguientes rutas:

- `/pagina/login` - Login
- `/pagina/registro` - Registro
- `/pagina/inicio` - Dashboard principal
- `/pagina/maquinas` - Gestión de máquinas
- `/pagina/agregar-maquina` - Formulario agregar máquina
- `/pagina/historial` - Historial de mantenimientos

## 📱 Responsive Design

La aplicación está optimizada para:
- Desktop (1024px+)
- Tablet (768px - 1023px)
- Mobile (320px - 767px)

## 🔮 Futuras Mejoras

- [ ] Componentes reutilizables en `/components`
- [ ] Sistema de temas (dark/light mode)
- [ ] Internacionalización (i18n)
- [ ] Testing con Jest + React Testing Library
- [ ] TypeScript migration
- [ ] State management con Zustand/Redux

## 🤝 Contribución

1. Fork del proyecto
2. Crear feature branch
3. Commit changes
4. Push al branch
5. Crear Pull Request

## 📄 Licencia

MIT License - ver archivo LICENSE para detalles
