import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../utils/api'
import Modal from '../components/Modal'
import '../styles/Formularios.css'

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
  const [loading, setLoading] = useState(false)
  const [modal, setModal] = useState({
    isVisible: false,
    title: 'Atención',
    message: '',
    icon: 'fa-exclamation-circle',
    iconColor: '#e74c3c'
  })

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
    
    if (!formData.tipo_equipo || !formData.codigo_equipo || !formData.estado_actual || !formData.area || !formData.fecha) {
      showModal('Datos Incompletos', 'Por favor complete todos los campos para agregar la máquina', 'fa-exclamation-triangle', '#e74c3c')
      return
    }

    try {
      setLoading(true)
      await api.agregarMaquina(formData)
      showModal('Registro Exitoso', 'Máquina agregada exitosamente', 'fa-check-circle', '#27ae60')
      setTimeout(() => {
        navigate('/maquinas')
      }, 2000)
    } catch (error) {
      showModal('Error al Agregar', error.message || 'Error al agregar la máquina', 'fa-exclamation-circle', '#e74c3c')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="logo-section">
          <h2>Agregar Máquina</h2>
        </div>

        <form onSubmit={handleSubmit}>
          <div style={{display: 'flex', gap: '15px'}}>
            <div className="input-user" style={{flex: 1}}>
              <label htmlFor="tipo_equipo">Tipo de Equipo</label>
              <div className="input-information">
                <select 
                  id="tipo_equipo" 
                  value={formData.tipo_equipo}
                  onChange={handleChange}
                >
                  <option value="">Selecciona</option>
                  <option value="PC">Computadora</option>
                  <option value="IMP">Impresora</option>
                </select>
              </div>
            </div>

            <div className="input-user" style={{flex: 1}}>
              <label htmlFor="codigo_equipo">Código</label>
              <div className="input-information">
                <input 
                  type="text" 
                  id="codigo_equipo" 
                  placeholder="Ingresa código"
                  value={formData.codigo_equipo}
                  onChange={handleChange}
                />
              </div>
            </div>
          </div>

          <div style={{display: 'flex', gap: '15px'}}>
            <div className="input-user" style={{flex: 1}}>
              <label htmlFor="estado_actual">Estado</label>
              <div className="input-information">
                <select 
                  id="estado_actual" 
                  value={formData.estado_actual}
                  onChange={handleChange}
                >
                  <option value="">Selecciona</option>
                  <option value="operativa">Operativa</option>
                  <option value="en mantenimiento">En mantenimiento</option>
                  <option value="fuera de servicio">Fuera de servicio</option>
                </select>
              </div>
            </div>

            <div className="input-user" style={{flex: 1}}>
              <label htmlFor="area">Área</label>
              <div className="input-information">
                <input 
                  type="text" 
                  id="area" 
                  placeholder="Ingresa el área"
                  value={formData.area}
                  onChange={handleChange}
                />
              </div>
            </div>
          </div>

          <div className="input-user">
            <label htmlFor="fecha">Fecha de adquisición</label>
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
            <label htmlFor="usuario">Usuario que registra</label>
            <div className="input-information">
              <input 
                type="text" 
                id="usuario" 
                value={formData.usuario}
                disabled
                style={{cursor: 'not-allowed'}}
                placeholder="Usuario autenticado"
              />
            </div>
          </div>

          <div style={{display: 'flex', gap: '10px', marginTop: '20px'}}>
            <button type="submit" className="btn-signin" disabled={loading}>
              {loading ? 'Guardando...' : 'Guardar'}
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

export default AgregarMaquina
