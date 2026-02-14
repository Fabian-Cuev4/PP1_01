import { useNavigate } from 'react-router-dom'
import './AgregarMaquina.css'

function AgregarMaquina() {
  const navigate = useNavigate()

  const handleCancel = () => {
    navigate('/pagina/maquinas')
  }

  return (
    <div className="agregar-maquina-container">
      <div className="modal-overlay">
        <div className="modal-head">
          <h2 className="modal-content-head">Agregar Máquina</h2>

          <form className="form">
            <div className="form-content">
              <label>Tipo de Equipo:</label>
              <select id="tipo_equipo">
                <option value="">Selecciona</option>
                <option value="PC">Computadora</option>
                <option value="IMP">Impresora</option>
              </select>

              <div className="form-content">
                <label>Código del equipo</label>
                <input type="text" id="codigo" placeholder="Ingresa código" />
              </div>

              <div className="form-content">
                <label>Estado actual</label>
                <select id="estado_actual">
                  <option value="">Selecciona</option>
                  <option value="operativa">Operativa</option>
                  <option value="Fuera de servicio">Fuera de servicio</option>
                  <option value="dada de baja">Dada de baja</option>
                </select>
              </div>
            </div>

            <div className="form-content">
              <label>Área</label>
              <input type="text" id="area" placeholder="Ingresa el área" />
            </div>

            <div className="form-content">
              <label>Fecha de adquisición</label>
              <input type="date" id="fecha" />
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

export default AgregarMaquina
