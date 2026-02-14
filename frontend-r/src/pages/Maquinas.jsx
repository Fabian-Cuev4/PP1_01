import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../utils/api'
import './Maquinas.css'

function Maquinas() {
  const navigate = useNavigate()
  const [maquinas, setMaquinas] = useState([])
  const [busqueda, setBusqueda] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    cargarMaquinas()
  }, [])

  const cargarMaquinas = async () => {
    try {
      setLoading(true)
      const data = await api.listarMaquinas()
      setMaquinas(data)
    } catch (error) {
      console.error('Error al cargar máquinas:', error)
      alert('Error al cargar las máquinas')
    } finally {
      setLoading(false)
    }
  }

  const handleEliminar = async (codigo) => {
    if (confirm(`¿Estás seguro de eliminar la máquina ${codigo}?`)) {
      try {
        await api.eliminarMaquina(codigo)
        alert('Máquina eliminada exitosamente')
        cargarMaquinas()
      } catch (error) {
        console.error('Error al eliminar máquina:', error)
        alert('Error al eliminar la máquina')
      }
    }
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
            <img src="/static/img/icono_user.png" alt="Usuario" />
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
                    <img src="/static/img/icono_maquina.png" alt="Máquina" />
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
    </div>
  )
}

export default Maquinas
