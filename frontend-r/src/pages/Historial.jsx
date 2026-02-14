import { useNavigate } from 'react-router-dom'
import './Historial.css'

function Historial() {
  const navigate = useNavigate()

  const handleBack = () => {
    navigate('/pagina/maquinas')
  }

  return (
    <div className="historial-container">
      <div className="overlay">
        <div className="modal-card">
          <div className="modal-header">
            <h2>Historial de Mantenimiento</h2>
            <p id="subtitulo-maquina">Equipo: <span>PC-LAB-001</span></p>
          </div>

          <div className="table-wrapper">
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
                <tr>
                  <td>10/02/2026</td>
                  <td>Preventivo</td>
                  <td>Juan Pérez</td>
                  <td>TechSupport S.A.</td>
                  <td>Limpieza interna y verificación de componentes</td>
                </tr>
                <tr>
                  <td>15/01/2026</td>
                  <td>Correctivo</td>
                  <td>María García</td>
                  <td>TechSupport S.A.</td>
                  <td>Reemplazo de memoria RAM dañada</td>
                </tr>
                <tr>
                  <td>20/12/2025</td>
                  <td>Preventivo</td>
                  <td>Carlos López</td>
                  <td>TechSupport S.A.</td>
                  <td>Actualización de software y antivirus</td>
                </tr>
                <tr>
                  <td>05/11/2025</td>
                  <td>Correctivo</td>
                  <td>Ana Martínez</td>
                  <td>TechSupport S.A.</td>
                  <td>Reparación de pantalla dañada</td>
                </tr>
              </tbody>
            </table>
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
