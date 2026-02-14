import { useNavigate } from 'react-router-dom'
import './Maquinas.css'

function Maquinas() {
  const navigate = useNavigate()

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
            <input type="text" id="input-busqueda" placeholder="Buscar equipo..." />
          </div>
        </div>

        <div id="contenedor-principal-maquinas">
          <div className="detail-container">
            <div className="card-space">
              <div className="card-icon">
                <img src="/static/img/icono_maquina.png" alt="Máquina" />
              </div>
              <div className="card-info">
                <h3>PC-LAB-001</h3>
                <p><strong>Tipo:</strong> Computadora</p>
                <p><strong>Área:</strong> Laboratorio Principal</p>
                <p><strong>Estado:</strong> <span className="status-badge status-operativa">Operativa</span></p>
              </div>
            </div>
            <div className="side-buttons">
              <button type="button" onClick={() => navigate('/pagina/historial')} className="btn-action btn-yellow-history">Historial</button>
              <button type="button" onClick={() => navigate('/pagina/mantenimiento')} className="btn-action btn-green">Mantenimiento</button>
              <button type="button" onClick={() => navigate('/pagina/actualizar-maquina')} className="btn-action btn-blue-act">Actualizar</button>
            </div>
          </div>

          <div className="detail-container">
            <div className="card-space">
              <div className="card-icon">
                <img src="/static/img/icono_maquina.png" alt="Máquina" />
              </div>
              <div className="card-info">
                <h3>PC-LAB-002</h3>
                <p><strong>Tipo:</strong> Computadora</p>
                <p><strong>Área:</strong> Laboratorio Principal</p>
                <p><strong>Estado:</strong> <span className="status-badge status-mantenimiento">En mantenimiento</span></p>
              </div>
            </div>
            <div className="side-buttons">
              <button type="button" onClick={() => navigate('/pagina/historial')} className="btn-action btn-yellow-history">Historial</button>
              <button type="button" onClick={() => navigate('/pagina/mantenimiento')} className="btn-action btn-green">Mantenimiento</button>
              <button type="button" onClick={() => navigate('/pagina/actualizar-maquina')} className="btn-action btn-blue-act">Actualizar</button>
            </div>
          </div>

          <div className="detail-container">
            <div className="card-space">
              <div className="card-icon">
                <img src="/static/img/icono_maquina.png" alt="Máquina" />
              </div>
              <div className="card-info">
                <h3>IMP-LAB-001</h3>
                <p><strong>Tipo:</strong> Impresora</p>
                <p><strong>Área:</strong> Recepción</p>
                <p><strong>Estado:</strong> <span className="status-badge status-baja">Fuera de servicio</span></p>
              </div>
            </div>
            <div className="side-buttons">
              <button type="button" onClick={() => navigate('/pagina/historial')} className="btn-action btn-yellow-history">Historial</button>
              <button type="button" onClick={() => navigate('/pagina/mantenimiento')} className="btn-action btn-green">Mantenimiento</button>
              <button type="button" onClick={() => navigate('/pagina/actualizar-maquina')} className="btn-action btn-blue-act">Actualizar</button>
            </div>
          </div>
        </div>
      </main>

      <footer className="main-footer">
      </footer>
    </div>
  )
}

export default Maquinas
