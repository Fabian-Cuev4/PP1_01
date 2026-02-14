import { useNavigate } from 'react-router-dom'
import './Reportes.css'

function Reportes() {
  const navigate = useNavigate()

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
          <form className="filter-form">
            <div className="filter-group">
              <label><i className="fa-solid fa-desktop"></i> Máquina / ID</label>
              <input type="text" id="input-codigo" placeholder="Ej: PC-LAB-012" />
            </div>
            <div className="filter-actions">
              <button type="button" id="btn-buscar" className="btn-search">
                <i className="fa-solid fa-magnifying-glass"></i> Buscar
              </button>
            </div>
          </form>
        </div>

        <div className="table-container">
          <div className="table-responsive">
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
              <tbody id="tabla-reporte">
                <tr>
                  <td>PC-LAB-001</td>
                  <td>Laboratorio Principal</td>
                  <td>Juan Pérez</td>
                  <td>10/02/2026</td>
                  <td>Preventivo</td>
                  <td><span className="status-badge status-operativa">Completado</span></td>
                  <td>Limpieza interna y verificación de componentes</td>
                  <td><button type="button" className="btn-action-table">Ver</button></td>
                </tr>
                <tr>
                  <td>PC-LAB-002</td>
                  <td>Laboratorio Principal</td>
                  <td>María García</td>
                  <td>08/02/2026</td>
                  <td>Correctivo</td>
                  <td><span className="status-badge status-mantenimiento">En proceso</span></td>
                  <td>Reemplazo de disco duro dañado</td>
                  <td><button type="button" className="btn-action-table">Ver</button></td>
                </tr>
                <tr>
                  <td>IMP-LAB-001</td>
                  <td>Recepción</td>
                  <td>Carlos López</td>
                  <td>05/02/2026</td>
                  <td>Correctivo</td>
                  <td><span className="status-badge status-baja">Pendiente</span></td>
                  <td>Reparación de rodillo de alimentación</td>
                  <td><button type="button" className="btn-action-table">Ver</button></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  )
}

export default Reportes
