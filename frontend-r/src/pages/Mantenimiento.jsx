import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { api } from '../utils/api'
import Modal from '../components/Modal'
import './Mantenimiento.css'

function Mantenimiento() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const codigoMaquina = searchParams.get('codigo') || ''
  const [formData, setFormData] = useState({
    codigo_maquina: codigoMaquina,
    empresa: '',
    tecnico: '',
    tipo: '',
    fecha: '',
    observaciones: '',
    usuario: ''
  })
  const [loading, setLoading] = useState(false)
  const [modal, setModal] = useState({
    isVisible: false,
    title: 'Atención',
    message: '',
    icon: 'fa-exclamation-circle',
    iconColor: '#e74c3c'
  })

  useEffect(() => {
    setFormData(prev => ({ ...prev, codigo_maquina: codigoMaquina }))
  }, [codigoMaquina])

  const handleChange = (e) => {
    const { id, value } = e.target
    const fieldName = id.replace('mant-', '')
    setFormData(prev => ({
      ...prev,
      [fieldName]: value
    }))
  }

  const showModal = (title, message, icon = 'fa-exclamation-circle', iconColor = '#e74c3c') => {
    setModal({
      isVisible: true,
      title,
      message,
      icon,
      iconColor
    })
  }

  const hideModal = () => {
    setModal({
      ...modal,
      isVisible: false
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!formData.empresa || !formData.tecnico || !formData.tipo || !formData.fecha) {
      showModal('Campos Requeridos', 'Por favor complete todos los campos requeridos', 'fa-exclamation-triangle', '#e74c3c')
      return
    }

    try {
      setLoading(true)
      await api.agregarMantenimiento(formData)
      showModal('Registro Exitoso', 'Mantenimiento registrado exitosamente', 'fa-check-circle', '#27ae60')
      setTimeout(() => {
        navigate('/pagina/maquinas')
      }, 2000)
    } catch (error) {
      console.error('Error al registrar mantenimiento:', error)
      showModal('Error al Registrar', error.detail || 'Error al registrar el mantenimiento', 'fa-exclamation-circle', '#e74c3c')
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = () => {
    navigate('/pagina/maquinas')
  }

  return (
    <div className="mantenimiento-container">
      <div className="modal-overlay">
        <div className="modal-content">
          <div className="modal-header">
            <h2 className="modal-title-main">Registro de mantenimiento</h2>
            <p>Código máquina: <strong>{codigoMaquina}</strong></p>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Empresa / Institución</label>
              <input 
                type="text" 
                id="mant-empresa" 
                placeholder="Añade la empresa y especificar el cargo"
                value={formData.empresa}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Técnico Responsable</label>
                <input 
                  type="text" 
                  id="mant-tecnico" 
                  placeholder="Ingresa nombres completos"
                  value={formData.tecnico}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Tipo de mantenimiento</label>
                <select 
                  id="mant-tipo" 
                  value={formData.tipo}
                  onChange={handleChange}
                  required
                >
                  <option value="">Selecciona</option>
                  <option value="preventivo">Preventivo</option>
                  <option value="correctivo">Correctivo</option>
                </select>
              </div>
            </div>

            <div className="form-group" style={{ width: '50%' }}>
              <label>Fecha de mantenimiento</label>
              <input 
                type="date" 
                id="mant-fecha"
                value={formData.fecha}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Observaciones</label>
              <textarea 
                id="mant-observaciones" 
                placeholder="Ingresa un comentario" 
                rows="3"
                value={formData.observaciones}
                onChange={handleChange}
              ></textarea>
            </div>

            <div className="form-group">
              <label>Usuario que registra</label>
              <input 
                type="text" 
                id="mant-usuario" 
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

      <Modal
        isVisible={modal.isVisible}
        onClose={hideModal}
        title={modal.title}
        message={modal.message}
        icon={modal.icon}
        iconColor={modal.iconColor}
      />
    </div>
  )
}

export default Mantenimiento
