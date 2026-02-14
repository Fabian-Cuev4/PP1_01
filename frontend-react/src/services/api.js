// Configuración base para llamadas a la API
const API_BASE_URL = import.meta.env.PROD ? '/api' : '/api'

// Configuración de headers por defecto
const defaultHeaders = {
  'Content-Type': 'application/json',
}

// Función helper para hacer peticiones fetch con manejo de errores
async function fetchAPI(url, options = {}) {
  const config = {
    headers: defaultHeaders,
    ...options,
  }

  try {
    const response = await fetch(`${API_BASE_URL}${url}`, config)
    
    // Si la respuesta no es ok, lanzar error con información
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`)
    }

    return await response.json()
  } catch (error) {
    console.error('Error en llamada API:', error)
    throw error
  }
}

// API de Autenticación
export const authAPI = {
  login: (credentials) => fetchAPI('/login', {
    method: 'POST',
    body: JSON.stringify(credentials)
  }),

  register: (userData) => fetchAPI('/register', {
    method: 'POST',
    body: JSON.stringify(userData)
  })
}

// API de Máquinas
export const maquinasAPI = {
  listar: () => fetchAPI('/maquinas/listar'),

  agregar: (maquinaData) => fetchAPI('/maquinas/agregar', {
    method: 'POST',
    body: JSON.stringify(maquinaData)
  }),

  buscar: (query) => fetchAPI(`/maquinas/buscar?q=${encodeURIComponent(query)}`),

  dashboard: () => fetchAPI('/maquinas/dashboard')
}

// API de Mantenimiento
export const mantenimientoAPI = {
  agregar: (mantenimientoData) => fetchAPI('/mantenimiento/agregar', {
    method: 'POST',
    body: JSON.stringify(mantenimientoData)
  }),

  historial: (codigoMaquina) => fetchAPI(`/mantenimiento/historial?codigo=${encodeURIComponent(codigoMaquina)}`),

  informe: (codigoMaquina) => fetchAPI(`/mantenimiento/informe?codigo=${encodeURIComponent(codigoMaquina)}`),

  todos: () => fetchAPI('/mantenimiento/todos')
}

// API de Usuarios
export const usuariosAPI = {
  activos: () => fetchAPI('/usuarios/activos')
}

export default {
  authAPI,
  maquinasAPI,
  mantenimientoAPI,
  usuariosAPI
}
