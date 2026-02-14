import { useNavigate } from 'react-router-dom'
import './Mantenimiento.css'

function Mantenimiento() {
  const navigate = useNavigate()

  const handleCancel = () => {
    navigate('/pagina/maquinas')
  }

  return (
    <div className="mantenimiento-container">
      <div className="modal-overlay">
        <div className="modal-content">
          <div className="modal-header">
            <h2 className="modal-title-main">Registro de mantenimiento</h2>
          </div>

          <form>
            <div className="form-group">
              <label>Empresa / Institución</label>
              <input type="text" id="mant-empresa" placeholder="Añade la empresa y especificar el cargo" />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Técnico Responsable</label>
                <input type="text" id="mant-tecnico" placeholder="Ingresa nombres completos" />
              </div>
              <div className="form-group">
                <label>Tipo de mantenimiento</label>
                <select id="mant-tipo">
                  <option value="">Selecciona</option>
                  <option value="preventivo">Preventivo</option>
                  <option value="correctivo">Correctivo</option>
                </select>
              </div>
            </div>

            <div className="form-group" style={{ width: '50%' }}>
              <label>Fecha de mantenimiento</label>
              <input type="date" id="mant-fecha" />
            </div>

            <div className="form-group">
              <label>Observaciones</label>
              <textarea id="mant-observaciones" placeholder="Ingresa un comentario" rows="3"></textarea>
            </div>

            <div className="form-group checkbox-group">
              <input type="checkbox" id="avanzadas" />
              <label htmlFor="avanzadas">Opciones avanzadas</label>
            </div>

            <div className="form-actions">
              <button type="button" className="btn-save">Guardar</button>
              <button type="button" onClick={handleCancel} className="btn-cancel">Cancelar</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default Mantenimiento
