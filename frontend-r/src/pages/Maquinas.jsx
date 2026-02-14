import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../utils/api'
import Modal from '../components/Modal'
import iconoUser from '../assets/img/icono_user.png'
import iconoMaquina from '../assets/img/icono_maquina.png'
import './Maquinas.css'

function Maquinas() {
  const navigate = useNavigate()
  const [maquinas, setMaquinas] = useState([])
  const [busqueda, setBusqueda] = useState('')
  const [loading, setLoading] = useState(true)
  const [modal, setModal] = useState({
    isVisible: false,
    title: 'Atención',
    message: '',
    icon: 'fa-exclamation-circle',
    iconColor: '#e74c3c',
    showCancel: false,
    onConfirm: null,
    confirmText: 'Entendido'
  })

  useEffect(() => {
    cargarMaquinas()
  }, [])

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

  const cargarMaquinas = async () => {
    try {
      setLoading(true)
      const data = await api.listarMaquinas()
      setMaquinas(data)
    } catch (error) {
      console.error('Error al cargar máquinas:', error)
      showModal('Error', 'Error al cargar las máquinas', 'fa-exclamation-circle', '#e74c3c')
    } finally {
      setLoading(false)
    }
  }

  const handleEliminar = async (codigo) => {
    const confirmEliminar = async () => {
      try {
        await api.eliminarMaquina(codigo)
        showModal('Eliminación Exitosa', 'Máquina eliminada exitosamente', 'fa-check-circle', '#27ae60')
        setTimeout(() => {
          hideModal()
          cargarMaquinas()
        }, 1500)
      } catch (error) {
        console.error('Error al eliminar máquina:', error)
        showModal('Error al Eliminar', 'Error al eliminar la máquina', 'fa-exclamation-circle', '#e74c3c')
      }
    }

    setModal({
      isVisible: true,
      title: 'Confirmar Eliminación',
      message: `¿Estás seguro de eliminar la máquina ${codigo}?`,
      icon: 'fa-trash-alt',
      iconColor: '#e67e22',
      showCancel: true,
      onConfirm: confirmEliminar,
      confirmText: 'Eliminar'
    })
  }

  const maquinasFiltradas = maquinas.filter(maquina => 
    maquina.codigo.toLowerCase().includes(busqueda.toLowerCase()) ||
    maquina.area.toLowerCase().includes(busqueda.toLowerCase()) ||
    maquina.tipo.toLowerCase().includes(busqueda.toLowerCase())
  )

  const getEstadoClass = (estado) => {
    switch (estado?.toLowerCase()) {
      case 'operativa': return 'status-operativa'
      case 'en mantenimiento': return 'status-mantenimiento'
      case 'fuera de servicio': return 'status-baja'
      default: return 'status-operativa'
    }
  }

  return (
    <div className="maquinas-container">
      <header className="main-header">
        <div className="user-profile">
          <div className="avatar">
            <img src={iconoUser} alt="Usuario" />
          </div>
        </div>
      </header>

      <main className="content">
        <div className="action-bar">
          <div className="left-actions">
            <button type="button" onClick={() => navigate('/pagina/agregar-maquina')} className="btn-create">Agregar Máquina</button>
            <button type="button" onClick={() => navigate('/pagina/reportes')} className="btn-create">Generar Reporte</button>
            <button type="button" onClick={() => navigate('/pagina/inicio')} className="btn-create">Regresar</button>
          </div>
          <div className="search-container">
            <input 
              type="text" 
              value={busqueda}
              onChange={(e) => setBusqueda(e.target.value)}
              placeholder="Buscar equipo..." 
            />
          </div>
        </div>

        <div id="contenedor-principal-maquinas">
          {loading ? (
            <div className="loading">Cargando máquinas...</div>
          ) : maquinasFiltradas.length === 0 ? (
            <div className="no-data">No se encontraron máquinas</div>
          ) : (
            maquinasFiltradas.map((maquina) => (
              <div key={maquina.codigo} className="detail-container">
                <div className="card-space">
                  <div className="card-icon">
                    <img src={iconoMaquina} alt="Máquina" />
                  </div>
                  <div className="card-info">
                    <h3>{maquina.codigo}</h3>
                    <p><strong>Tipo:</strong> {maquina.tipo}</p>
                    <p><strong>Área:</strong> {maquina.area}</p>
                    <p><strong>Estado:</strong> <span className={`status-badge ${getEstadoClass(maquina.estado)}`}>{maquina.estado}</span></p>
                  </div>
                </div>
                <div className="side-buttons">
                  <button 
                    type="button" 
                    onClick={() => navigate(`/pagina/historial?codigo=${maquina.codigo}`)} 
                    className="btn-action btn-yellow-history"
                  >
                    Historial
                  </button>
                  <button 
                    type="button" 
                    onClick={() => navigate(`/pagina/mantenimiento?codigo=${maquina.codigo}`)} 
                    className="btn-action btn-green"
                  >
                    Mantenimiento
                  </button>
                  <button 
                    type="button" 
                    onClick={() => navigate(`/pagina/actualizar-maquina?codigo=${maquina.codigo}`)} 
                    className="btn-action btn-blue-act"
                  >
                    Actualizar
                  </button>
                  <button 
                    type="button" 
                    onClick={() => handleEliminar(maquina.codigo)} 
                    className="btn-action btn-red"
                  >
                    Eliminar
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </main>

      <footer className="main-footer">
      </footer>

      <Modal
        isVisible={modal.isVisible}
        onClose={hideModal}
        title={modal.title}
        message={modal.message}
        icon={modal.icon}
        iconColor={modal.iconColor}
        showCancel={modal.showCancel}
        onConfirm={modal.onConfirm}
        confirmText={modal.confirmText}
      />
    </div>
  )
}

export default Maquinas
