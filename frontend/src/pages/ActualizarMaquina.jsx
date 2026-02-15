import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { api } from '../utils/api'
import Modal from '../components/Modal'
import '../styles/Formularios.css'

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
    if (codigoMaquina) {
      cargarDatosMaquina()
    }
  }, [codigoMaquina, navigate])

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
        showModal('Máquina No Encontrada', 'La máquina solicitada no existe', 'fa-search', '#e74c3c')
        setTimeout(() => {
          navigate('/maquinas')
        }, 2000)
      }
    } catch (error) {
      showModal('Error', 'Error al cargar los datos de la máquina', 'fa-exclamation-circle', '#e74c3c')
      setTimeout(() => {
        navigate('/maquinas')
      }, 2000)
    } finally {
      setLoadingData(false)
    }
  }

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
    
    if (!formData.estado_actual) {
      showModal('Datos Incompletos', 'Por favor complete el campo de estado para actualizar la máquina', 'fa-exclamation-triangle', '#e74c3c')
      return
    }

    try {
      setLoading(true)
      await api.actualizarMaquina(formData)
      showModal('Actualización Exitosa', 'Máquina actualizada exitosamente', 'fa-check-circle', '#27ae60')
      setTimeout(() => {
        navigate('/maquinas')
      }, 2000)
    } catch (error) {
      showModal('Error al Actualizar', error.message || 'Error al actualizar la máquina', 'fa-exclamation-circle', '#e74c3c')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="logo-section">
          <h2>Actualizar Máquina</h2>
        </div>

        {loadingData ? (
          <div className="loading">Cargando datos...</div>
        ) : (
          <form onSubmit={handleSubmit}>
            <div style={{display: 'flex', gap: '15px'}}>
              <div className="input-user" style={{flex: 1}}>
                <label htmlFor="tipo_equipo">Tipo de Equipo</label>
                <div className="input-information">
                  <select 
                    id="tipo_equipo" 
                    value={formData.tipo_equipo}
                    disabled
                    style={{cursor: 'not-allowed'}}
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
                    disabled
                    style={{cursor: 'not-allowed'}}
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
                {loading ? 'Actualizando...' : 'Actualizar'}
              </button>
              <button type="button" className="btn-signin" onClick={() => navigate('/maquinas')} style={{background: '#95a5a6'}}>
                Cancelar
              </button>
            </div>
          </form>
        )}
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

export default ActualizarMaquina
