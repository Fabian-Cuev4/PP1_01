import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Configuración Vite para desarrollo
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      // Auth endpoints - backend-simple
      '/api/auth/login': {
        target: 'http://backend-simple:8000',
        changeOrigin: true,
        secure: false
      },
      '/api/auth/register': {
        target: 'http://backend-simple:8000',
        changeOrigin: true,
        secure: false
      },
      // Máquinas endpoint agregar - nginx balancer
      '/api/maquinas/agregar': {
        target: 'http://nginx_balancer:80',
        changeOrigin: true,
        secure: false
      },
      // Máquinas endpoints - backend-simple
      '/api/maquinas/listar': {
        target: 'http://backend-simple:8000',
        changeOrigin: true,
        secure: false
      },
      '/api/maquinas/buscar': {
        target: 'http://backend-simple:8000',
        changeOrigin: true,
        secure: false
      },
      '/api/maquinas/actualizar': {
        target: 'http://backend-simple:8000',
        changeOrigin: true,
        secure: false
      },
      '/api/maquinas/eliminar': {
        target: 'http://backend-simple:8000',
        changeOrigin: true,
        secure: false
      },
      // Mantenimiento endpoints - backend-simple
      '/api/mantenimiento/agregar': {
        target: 'http://backend-simple:8000',
        changeOrigin: true,
        secure: false
      },
      '/api/mantenimiento/listar': {
        target: 'http://backend-simple:8000',
        changeOrigin: true,
        secure: false
      },
      '/api/mantenimiento/informe-general': {
        target: 'http://backend-simple:8000',
        changeOrigin: true,
        secure: false
      }
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets'
  }
})
