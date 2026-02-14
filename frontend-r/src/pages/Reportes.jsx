import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../utils/api'
import './Reportes.css'

function Reportes() {
  const navigate = useNavigate()
  const [reportes, setReportes] = useState([])
  const [busqueda, setBusqueda] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    cargarReportes()
  }, [])

  const cargarReportes = async () => {
    try {
      setLoading(true)
      const data = await api.informeGeneral()
      setReportes(data)
    } catch (error) {
      console.error('Error al cargar reportes:', error)
      alert('Error al cargar los reportes')
    } finally {
      setLoading(false)
    }
  }

  const handleBuscar = async () => {
    try {
      setLoading(true)
      const data = await api.informeGeneral(busqueda)
      setReportes(data)
    } catch (error) {
      console.error('Error al buscar reportes:', error)
      alert('Error al buscar reportes')
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleBuscar()
    }
  }

  const getEstadoClass = (estado) => {
    switch (estado?.toLowerCase()) {
      case 'operativa': return 'status-operativa'
      case 'en mantenimiento': return 'status-mantenimiento'
      case 'fuera de servicio': return 'status-baja'
      default: return 'status-operativa'
    }
  }
  return (
    <div className="reportes-container">
      <main className="content">
        <div className="page-header">
          <div className="header-text">
            <h1><i className="fa-solid fa-chart-pie"></i> Reporte de Mantenimientos</h1>
            <p>Genera consultas y exporta la información de los laboratorios.</p>
          </div>
          <button type="button" onClick={() => navigate('/pagina/maquinas')} className="btn-back">Regresar</button>
        </div>

        <div className="filter-card">
          <form className="filter-form" onSubmit={(e) => { e.preventDefault(); handleBuscar(); }}>
            <div className="filter-group">
              <label><i className="fa-solid fa-desktop"></i> Máquina / ID</label>
              <input 
                type="text" 
                value={busqueda}
                onChange={(e) => setBusqueda(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ej: PC-LAB-012" 
              />
            </div>
            <div className="filter-actions">
              <button type="submit" className="btn-search">
                <i className="fa-solid fa-magnifying-glass"></i> Buscar
              </button>
            </div>
          </form>
        </div>

        <div className="table-container">
          <div className="table-responsive">
            {loading ? (
              <div className="loading">Cargando reportes...</div>
            ) : reportes.length === 0 ? (
              <div className="no-data">No se encontraron reportes</div>
            ) : (
              <table className="report-table">
                <thead>
                  <tr>
                    <th>ID Equipo</th>
                    <th>Ubicación</th>
                    <th>Técnico</th>
                    <th>Fecha</th>
                    <th>Tipo</th>
                    <th>Estado</th>
                    <th>Descripción</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {reportes.map((reporte) => {
                    // Si hay mantenimientos, mostrar cada uno en una fila
                    if (reporte.mantenimientos && reporte.mantenimientos.length > 0) {
                      return reporte.mantenimientos.map((mantenimiento, index) => (
                        <tr key={`${reporte.codigo}-${index}`}>
                          <td>{reporte.codigo}</td>
                          <td>{reporte.area}</td>
                          <td>{mantenimiento.tecnico}</td>
                          <td>{mantenimiento.fecha}</td>
                          <td>{mantenimiento.tipo}</td>
                          <td><span className={`status-badge ${getEstadoClass(reporte.estado)}`}>{reporte.estado}</span></td>
                          <td>{mantenimiento.observaciones}</td>
                          <td>
                            <button 
                              type="button" 
                              className="btn-action-table"
                            >
                              Ver
                            </button>
                          </td>
                        </tr>
                      ))
                    } else {
                      // Si no hay mantenimientos, mostrar una sola fila
                      return (
                        <tr key={reporte.codigo}>
                          <td>{reporte.codigo}</td>
                          <td>{reporte.area}</td>
                          <td>-</td>
                          <td>-</td>
                          <td>-</td>
                          <td><span className={`status-badge ${getEstadoClass(reporte.estado)}`}>{reporte.estado}</span></td>
                          <td>Sin mantenimientos registrados</td>
                          <td>
                            <button 
                              type="button" 
                              className="btn-action-table"
                            >
                              Ver
                            </button>
                          </td>
                        </tr>
                      )
                    }
                  })}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}

export default Reportes
