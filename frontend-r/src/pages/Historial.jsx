import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { api } from '../utils/api'
import './Historial.css'

function Historial() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const codigoMaquina = searchParams.get('codigo') || ''
  const [historial, setHistorial] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (codigoMaquina) {
      cargarHistorial()
    }
  }, [codigoMaquina])

  const cargarHistorial = async () => {
    try {
      setLoading(true)
      const data = await api.listarMantenimientos(codigoMaquina)
      setHistorial(data)
    } catch (error) {
      console.error('Error al cargar historial:', error)
      alert('Error al cargar el historial de mantenimientos')
    } finally {
      setLoading(false)
    }
  }

  const handleBack = () => {
    navigate('/pagina/maquinas')
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
    </div>
  )
}

export default Historial
