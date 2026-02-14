import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../utils/api'
import './AgregarMaquina.css'

function AgregarMaquina() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    tipo_equipo: '',
    codigo_equipo: '',
    estado_actual: '',
    area: '',
    fecha: '',
    usuario: ''
  })
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { id, value } = e.target
    setFormData(prev => ({
      ...prev,
      [id]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!formData.tipo_equipo || !formData.codigo_equipo || !formData.estado_actual || !formData.area || !formData.fecha) {
      alert('Por favor complete todos los campos requeridos')
      return
    }

    try {
      setLoading(true)
      await api.agregarMaquina(formData)
      alert('Máquina agregada exitosamente')
      navigate('/pagina/maquinas')
    } catch (error) {
      console.error('Error al agregar máquina:', error)
      alert(error.detail || 'Error al agregar la máquina')
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = () => {
    navigate('/pagina/maquinas')
  }

  return (
    <div className="agregar-maquina-container">
      <div className="modal-overlay">
        <div className="modal-head">
          <h2 className="modal-content-head">Agregar Máquina</h2>

          <form className="form" onSubmit={handleSubmit}>
            <div className="form-content">
              <label>Tipo de Equipo:</label>
              <select 
                id="tipo_equipo" 
                value={formData.tipo_equipo}
                onChange={handleChange}
                required
              >
                <option value="">Selecciona</option>
                <option value="PC">Computadora</option>
                <option value="IMP">Impresora</option>
              </select>

              <div className="form-content">
                <label>Código del equipo</label>
                <input 
                  type="text" 
                  id="codigo_equipo" 
                  placeholder="Ingresa código"
                  value={formData.codigo_equipo}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-content">
                <label>Estado actual</label>
                <select 
                  id="estado_actual" 
                  value={formData.estado_actual}
                  onChange={handleChange}
                  required
                >
                  <option value="">Selecciona</option>
                  <option value="operativa">Operativa</option>
                  <option value="en mantenimiento">En mantenimiento</option>
                  <option value="fuera de servicio">Fuera de servicio</option>
                </select>
              </div>
            </div>

            <div className="form-content">
              <label>Área</label>
              <input 
                type="text" 
                id="area" 
                placeholder="Ingresa el área"
                value={formData.area}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-content">
              <label>Fecha de adquisición</label>
              <input 
                type="date" 
                id="fecha"
                value={formData.fecha}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-content">
              <label>Usuario</label>
              <input 
                type="text" 
                id="usuario" 
                placeholder="Usuario que registra"
                value={formData.usuario}
                onChange={handleChange}
              />
            </div>

            <div className="form-actions">
              <button 
                type="submit" 
                className="btn-save"
                disabled={loading}
              >
                {loading ? 'Guardando...' : 'Guardar'}
              </button>
              <button type="button" onClick={handleCancel} className="btn-cancel">Cancelar</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default AgregarMaquina
