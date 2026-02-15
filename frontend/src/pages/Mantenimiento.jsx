import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { api } from '../utils/api'
import Modal from '../components/Modal'
import '../styles/Formularios.css'

function Mantenimiento() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const codigoMaquina = searchParams.get('codigo') || ''
  const [formData, setFormData] = useState({
    empresa: '',
    tecnico: '',
    tipo: '',
    fecha: '',
    observaciones: '',
    codigo_maquina: codigoMaquina
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
    if (!sessionStorage.getItem('token')) {
      navigate('/login')
      return
    }
    const userData = sessionStorage.getItem('user')
    if (userData) {
      let usuario = ''
      try {
        usuario = JSON.parse(userData)
      } catch {
        usuario = userData.replace(/"/g, '')
      }
      if (typeof usuario === 'object') {
        usuario = usuario.nombre_completo || usuario.username || ''
      }
      setFormData(prev => ({...prev, usuario}))
    }
  }, [navigate])

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value
    })
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
    
    if (!formData.empresa || !formData.tecnico || !formData.tipo || !formData.fecha || !formData.observaciones) {
      showModal('Datos Incompletos', 'Por favor complete todos los campos para registrar el mantenimiento', 'fa-exclamation-triangle', '#e74c3c')
      return
    }

    try {
      setLoading(true)
      await api.agregarMantenimiento(formData)
      showModal('Registro Exitoso', 'Mantenimiento registrado exitosamente', 'fa-check-circle', '#27ae60')
      setTimeout(() => {
        navigate('/maquinas')
      }, 2000)
    } catch (error) {
      showModal('Error al Registrar', error.message || 'Error al registrar el mantenimiento', 'fa-exclamation-circle', '#e74c3c')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="logo-section">
          <h2>Registro de Mantenimiento</h2>
          <p style={{marginTop: '5px', color: '#666'}}>Código máquina: <strong>{codigoMaquina}</strong></p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="input-user">
            <label htmlFor="empresa">Empresa / Institución</label>
            <div className="input-information">
              <input 
                type="text" 
                id="empresa" 
                placeholder="Añade la empresa y especificar el cargo"
                value={formData.empresa}
                onChange={handleChange}
              />
            </div>
          </div>

          <div style={{display: 'flex', gap: '15px'}}>
            <div className="input-user" style={{flex: 1}}>
              <label htmlFor="tecnico">Técnico Responsable</label>
              <div className="input-information">
                <input 
                  type="text" 
                  id="tecnico" 
                  placeholder="Ingresa nombres"
                  value={formData.tecnico}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="input-user" style={{flex: 1}}>
              <label htmlFor="tipo">Tipo de mantenimiento</label>
              <div className="input-information">
                <select 
                  id="tipo"
                  value={formData.tipo}
                  onChange={handleChange}
                >
                  <option value="">Selecciona</option>
                  <option value="preventivo">Preventivo</option>
                  <option value="correctivo">Correctivo</option>
                </select>
              </div>
            </div>
          </div>

          <div className="input-user">
            <label htmlFor="fecha">Fecha de mantenimiento</label>
            <div className="input-information">
              <input 
                type="date" 
                id="fecha"
                value={formData.fecha}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="input-user">
            <label htmlFor="observaciones">Descripción del trabajo realizado</label>
            <div className="input-information">
              <textarea 
                id="observaciones" 
                placeholder="Describe detalladamente el trabajo realizado..."
                value={formData.observaciones}
                onChange={handleChange}
                style={{
                  width: '100%',
                  padding: '12px',
                  borderRadius: '8px',
                  border: '1px solid transparent',
                  backgroundColor: '#f1f3f5',
                  fontSize: '14px',
                  color: '#333',
                  outline: 'none',
                  minHeight: '100px',
                  resize: 'vertical'
                }}
              />
            </div>
          </div>

          <div style={{display: 'flex', gap: '10px', marginTop: '20px'}}>
            <button type="submit" className="btn-signin" disabled={loading}>
              {loading ? 'Registrando...' : 'Guardar'}
            </button>
            <button type="button" className="btn-signin" onClick={() => navigate('/maquinas')} style={{background: '#95a5a6'}}>
              Cancelar
            </button>
          </div>
        </form>
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
