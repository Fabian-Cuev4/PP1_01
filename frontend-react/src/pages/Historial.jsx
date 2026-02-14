import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import '../styles/Historial.css'

function Historial() {
  const [historial, setHistorial] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchParams] = useSearchParams()
  const codigoMaquina = searchParams.get('codigo')
  const navigate = useNavigate()

  useEffect(() => {
    if (codigoMaquina) {
      fetchHistorial()
    } else {
      navigate('/pagina/maquinas')
    }
  }, [codigoMaquina])

  const fetchHistorial = async () => {
    try {
      const response = await fetch(`/api/mantenimiento/historial?codigo=${codigoMaquina}`)
      if (response.ok) {
        const data = await response.json()
        setHistorial(data)
      } else {
        console.error('No se pudo cargar el historial')
      }
    } catch (error) {
      console.error('Error al cargar historial:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleVolver = () => {
    navigate('/pagina/maquinas')
  }

  const formatDate = (fechaString) => {
    if (!fechaString) return 'No especificada'
    const fecha = new Date(fechaString)
    return fecha.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  if (loading) {
    return (
      <div className="historial-container">
        <div className="loading">Cargando historial...</div>
      </div>
    )
  }

  return (
    <div className="historial-container">
      {/* Capa de fondo que ayuda a centrar la tabla en la pantalla */}
      <div className="overlay">
        {/* Caja blanca donde se muestra la información */}
        <div className="modal-card">
          {/* Encabezado de la ventana de historial */}
          <div className="modal-header">
            <h2>Historial de Mantenimiento</h2>
            {/* Aquí el JS pondrá el código de la máquina que estamos consultando */}
            <p>Equipo: <span>{codigoMaquina || '---'}</span></p>
          </div>

          {/* Contenedor para que la tabla tenga su propio estilo y márgenes */}
          <div className="table-wrapper">
            {/* Estructura de la tabla de datos */}
            <table className="history-table">
              <thead>
                {/* Títulos de las columnas de la tabla */}
                <tr>
                  <th>Fecha</th>
                  <th>Tipo</th>
                  <th>Técnico</th>
                  <th>Empresa</th>
                  <th>Observaciones</th>
                </tr>
              </thead>
              {/* Aquí el archivo 'historial.js' meterá las filas de datos reales */}
              <tbody>
                {historial.length === 0 ? (
                  <tr>
                    <td colSpan="5" style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
                      No hay registros de mantenimiento para esta máquina
                    </td>
                  </tr>
                ) : (
                  historial.map((registro, index) => (
                    <tr key={index}>
                      <td>{formatDate(registro.fecha)}</td>
                      <td>{registro.tipo || 'No especificado'}</td>
                      <td>{registro.tecnico || 'No especificado'}</td>
                      <td>{registro.empresa || 'No especificada'}</td>
                      <td>{registro.observaciones || 'Sin observaciones'}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          {/* Parte inferior de la ventana con botones */}
          <div className="modal-footer">
            {/* Botón para cerrar esta vista y volver a la lista anterior */}
            <button onClick={handleVolver} className="btn-back">
              Regresar
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Historial
