import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { api } from '../utils/api'
import './ActualizarMaquina.css'

function ActualizarMaquina() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const codigoMaquina = searchParams.get('codigo') || ''
  const [formData, setFormData] = useState({
    tipo_equipo: '',
    codigo_equipo: codigoMaquina,
    estado_actual: '',
    area: '',
    fecha: '',
    usuario: ''
  })
  const [loading, setLoading] = useState(false)
  const [loadingData, setLoadingData] = useState(true)

  useEffect(() => {
    if (codigoMaquina) {
      cargarDatosMaquina()
    }
  }, [codigoMaquina])

  const cargarDatosMaquina = async () => {
    try {
      setLoadingData(true)
      const maquinas = await api.listarMaquinas()
      const maquina = maquinas.find(m => m.codigo === codigoMaquina)
      
      if (maquina) {
        setFormData({
          tipo_equipo: maquina.tipo,
          codigo_equipo: maquina.codigo,
          estado_actual: maquina.estado,
          area: maquina.area,
          fecha: maquina.fecha,
          usuario: maquina.usuario || ''
        })
      } else {
        alert('Máquina no encontrada')
        navigate('/pagina/maquinas')
      }
    } catch (error) {
      console.error('Error al cargar máquina:', error)
      alert('Error al cargar los datos de la máquina')
      navigate('/pagina/maquinas')
    } finally {
      setLoadingData(false)
    }
  }

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
      await api.actualizarMaquina(formData)
      alert('Máquina actualizada exitosamente')
      navigate('/pagina/maquinas')
    } catch (error) {
      console.error('Error al actualizar máquina:', error)
      alert(error.detail || 'Error al actualizar la máquina')
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = () => {
    navigate('/pagina/maquinas')
  }

  return (
    <div className="actualizar-maquina-container">
      <div className="modal-overlay">
        <div className="modal-head">
          <h2 className="modal-content-head">Actualizar Máquina</h2>

          <form className="form" id="form-actualizar" onSubmit={handleSubmit}>
            {loadingData ? (
              <div className="loading">Cargando datos...</div>
            ) : (
              <>
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
                      disabled
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
                    {loading ? 'Actualizando...' : 'Actualizar'}
                  </button>
                  <button type="button" onClick={handleCancel} className="btn-cancel">Cancelar</button>
                </div>
              </>
            )}
          </form>
        </div>
      </div>
    </div>
  )
}

export default ActualizarMaquina
