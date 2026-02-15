const API_BASE_URL = '/api';

export const api = {
  // Auth endpoints
  login: async (credentials) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials)
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`);
    }
    
    return response.json();
  },

  register: async (userData) => {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`);
    }
    
    return response.json();
  },

  // Máquinas endpoints
  listarMaquinas: async () => {
    const response = await fetch(`${API_BASE_URL}/maquinas/listar`);
    return response.json();
  },

  agregarMaquina: async (maquinaData) => {
    const response = await fetch(`${API_BASE_URL}/maquinas/agregar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(maquinaData)
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || 'Error al agregar la máquina');
    }
    return data;
  },

  actualizarMaquina: async (maquinaData) => {
    const response = await fetch(`${API_BASE_URL}/maquinas/actualizar`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(maquinaData)
    });
    return response.json();
  },

  eliminarMaquina: async (codigo) => {
    const response = await fetch(`${API_BASE_URL}/maquinas/eliminar/${codigo}`, {
      method: 'DELETE'
    });
    return response.json();
  },

  // Mantenimiento endpoints
  listarMantenimientos: async (codigo) => {
    const response = await fetch(`${API_BASE_URL}/mantenimiento/listar/${codigo}`);
    return response.json();
  },

  agregarMantenimiento: async (mantenimientoData) => {
    const response = await fetch(`${API_BASE_URL}/mantenimiento/agregar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(mantenimientoData)
    });
    return response.json();
  },

  informeGeneral: async (codigo = null) => {
    const url = codigo 
      ? `${API_BASE_URL}/mantenimiento/informe-general?codigo=${codigo}`
      : `${API_BASE_URL}/mantenimiento/informe-general`;
    const response = await fetch(url);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const error = new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`);
      error.status = response.status;
      throw error;
    }
    
    return response.json();
  }
};
