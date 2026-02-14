import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import '../styles/Maquinas.css'

function Maquinas() {
  const [maquinas, setMaquinas] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [modal, setModal] = useState({
    show: false,
    title: '',
    message: ''
  })
  const navigate = useNavigate()
  const username = localStorage.getItem('username')

  useEffect(() => {
    fetchMaquinas()
  }, [])

  const fetchMaquinas = async () => {
    try {
      const response = await fetch('/api/maquinas/listar')
      if (response.ok) {
        const data = await response.json()
        setMaquinas(data)
      } else {
        mostrarModal('Error', 'No se pudieron cargar las máquinas')
      }
    } catch (error) {
      console.error('Error al cargar máquinas:', error)
      mostrarModal('Error de conexión', 'No se pudo conectar con el servidor')
    } finally {
      setLoading(false)
    }
  }

  const mostrarModal = (titulo, mensaje) => {
    setModal({
      show: true,
      title: titulo,
      message: mensaje
    })
  }

  const ocultarModal = () => {
    setModal({
      ...modal,
      show: false
    })
  }

  const handleLogout = () => {
    localStorage.removeItem('username')
    navigate("/pagina/login")
  }

  const handleAgregarMaquina = () => {
    navigate("/pagina/agregar-maquina")
  }

  const handleGenerarReporte = () => {
    mostrarModal('Reportes', 'Función de reportes en desarrollo')
  }

  const handleRegresar = () => {
    navigate("/pagina/inicio")
  }

  const handleVerHistorial = (codigo) => {
    navigate(`/pagina/historial?codigo=${codigo}`)
  }

  const handleAgregarMantenimiento = (codigo) => {
    navigate(`/pagina/agregar-mantenimiento?codigo=${codigo}`)
  }

  const handleActualizarMaquina = (codigo) => {
    navigate(`/pagina/actualizar-maquina?codigo=${codigo}`)
  }

  const handleEliminarMaquina = (codigo) => {
    if (window.confirm(`¿Estás seguro de eliminar la máquina ${codigo}?`)) {
      // Lógica para eliminar máquina
      mostrarModal('Eliminado', `Máquina ${codigo} eliminada correctamente`)
    }
  }

  const getStatusClass = (estado) => {
    switch (estado) {
      case 'operativa':
        return 'status-operativa'
      case 'Fuera de servicio':
        return 'status-mantenimiento'
      case 'dada de baja':
        return 'status-baja'
      default:
        return 'status-operativa'
    }
  }

  const filteredMaquinas = maquinas.filter(maquina => 
    maquina.codigo_equipo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    maquina.tipo_equipo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (maquina.area && maquina.area.toLowerCase().includes(searchTerm.toLowerCase()))
  )

  if (loading) {
    return <div className="loading">Cargando máquinas...</div>
  }

  return (
    <div className="maquinas-container">
      <header className="main-header">
        <div className="user-profile">
          <div className="avatar">
            <img src="/img/icono_user.png" alt="Usuario" />
          </div>
          <span className="username">{username}</span>
        </div>
        <div className="logout-section">
          <button type="button" className="btn-logout" onClick={handleLogout}>
            Cerrar Sesión
            <img src="/img/icono_cerrar_sesion.png" alt="Cerrar Sesión" />
          </button>
        </div>
      </header>

      <main className="content">
        {/* Barra de acciones con botones y el buscador */}
        <div className="action-bar">
          <div className="left-actions">
            {/* Botón para ir a registrar una máquina nueva */}
            <button className="btn-create" onClick={handleAgregarMaquina}>
              Agregar Máquina
            </button>
            {/* Botón para ir a ver las estadísticas y reportes */}
            <button className="btn-create" onClick={handleGenerarReporte}>
              Generar Reporte
            </button>
            {/* Botón para volver al tablero de laboratorios (Ventana 1) */}
            <button className="btn-create" onClick={handleRegresar}>
              Regresar
            </button>
          </div>
          {/* Cuadro de texto para buscar máquinas por su nombre o código */}
          <div className="search-container">
            <input 
              type="text" 
              id="input-busqueda"
              placeholder="Buscar equipo..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>

        {/* En este contenedor es donde se dibujan todas las máquinas */}
        {filteredMaquinas.length === 0 ? (
          <div className="no-maquinas">
            <p>No hay máquinas registradas</p>
            <button onClick={handleAgregarMaquina} className="btn-create">
              Agregar primera máquina
            </button>
          </div>
        ) : (
          filteredMaquinas.map((maquina) => (
            <div key={maquina.codigo_equipo} className="detail-container">
              {/* Bloque principal de info de la máquina */}
              <div className="card-space">
                {/* Cuadrado muy oscuro a la izquierda de la tarjeta */}
                <div className="card-icon">
                  <img src="/img/icono_maquina.png" alt="Máquina" />
                </div>
                
                {/* Zona de textos de la máquina */}
                <div className="card-info">
                  <h3>{maquina.codigo_equipo}</h3>
                  <p><strong>Tipo:</strong> {maquina.tipo_equipo}</p>
                  <p><strong>Área:</strong> {maquina.area || 'No especificada'}</p>
                  <p><strong>Fecha:</strong> {maquina.fecha || 'No especificada'}</p>
                  
                  {/* Etiquetas de colores para el ESTADO */}
                  <span className={`status-badge ${getStatusClass(maquina.estado_actual)}`}>
                    {maquina.estado_actual}
                  </span>
                </div>
              </div>

              {/* La columna de acciones a la derecha de cada máquina */}
              <div className="side-buttons">
                <button className="btn-action btn-yellow-history" onClick={() => handleVerHistorial(maquina.codigo_equipo)}>
                  Historial
                </button>
                <button className="btn-action btn-blue-act" onClick={() => handleActualizarMaquina(maquina.codigo_equipo)}>
                  Actualizar
                </button>
                <button className="btn-action btn-green" onClick={() => handleAgregarMantenimiento(maquina.codigo_equipo)}>
                  Mantenimiento
                </button>
                <button className="btn-action btn-red" onClick={() => handleEliminarMaquina(maquina.codigo_equipo)}>
                  Eliminar
                </button>
              </div>
            </div>
          ))
        )}
      </main>

      {/* La parte de abajo de la página */}
      <footer className="main-footer">
      </footer>

      {modal.show && (
        <div className="modal-overlay">
          <div className="modal-card">
            <h3>{modal.title}</h3>
            <p>{modal.message}</p>
            <button onClick={ocultarModal} className="btn-modal-ok">
              Entendido
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default Maquinas
