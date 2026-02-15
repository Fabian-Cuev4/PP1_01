import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { api } from '../utils/api'
import Modal from '../components/Modal'
import '../styles/Historial.css'

function Historial() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const codigoMaquina = searchParams.get('codigo') || ''
  const [historial, setHistorial] = useState([])
  const [loading, setLoading] = useState(true)
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
      cargarHistorial()
    }
  }, [codigoMaquina, navigate])

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

  const cargarHistorial = async () => {
    try {
      setLoading(true)
      const data = await api.listarMantenimientos(codigoMaquina)
      setHistorial(data)
    } catch (error) {
      showModal('Error', 'Error al cargar el historial de mantenimientos', 'fa-exclamation-circle', '#e74c3c')
    } finally {
      setLoading(false)
    }
  }

  const handleBack = () => {
    navigate('/maquinas')
  }

  return (
    <div className="historial-container">
      <div className="overlay">
        <div className="modal-card">
          <div className="modal-header">
            <h2>Historial de Mantenimiento</h2>
            <p id="subtitulo-maquina">Equipo: <span>{codigoMaquina}</span></p>
          </div>

          <div className="table-wrapper">
            {loading ? (
              <div className="loading">Cargando historial...</div>
            ) : historial.length === 0 ? (
              <div className="no-data">No hay registros de mantenimiento para esta máquina</div>
            ) : (
              <table className="history-table">
                <thead>
                  <tr>
                    <th>Fecha</th>
                    <th>Tipo</th>
                    <th>Técnico</th>
                    <th>Empresa</th>
                    <th>Observaciones</th>
                  </tr>
                </thead>
                <tbody id="tabla-cuerpo-historial">
                  {historial.map((registro, index) => (
                    <tr key={registro._id || index}>
                      <td>{registro.fecha}</td>
                      <td>{registro.tipo}</td>
                      <td>{registro.tecnico}</td>
                      <td>{registro.empresa}</td>
                      <td>{registro.observaciones}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          <div className="modal-footer">
            <button type="button" onClick={handleBack} className="btn-back">Regresar</button>
          </div>
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

export default Historial
