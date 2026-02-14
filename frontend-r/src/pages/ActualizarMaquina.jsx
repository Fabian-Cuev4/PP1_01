import { useNavigate } from 'react-router-dom'
import './ActualizarMaquina.css'

function ActualizarMaquina() {
  const navigate = useNavigate()

  const handleCancel = () => {
    navigate('/pagina/maquinas')
  }

  return (
    <div className="actualizar-maquina-container">
      <div className="modal-overlay">
        <div className="modal-head">
          <h2 className="modal-content-head">Actualizar Máquina</h2>

          <form className="form" id="form-actualizar">
            <div className="form-content">
              <label>Tipo de Equipo:</label>
              <select id="tipo_equipo" disabled>
                <option value="">Selecciona</option>
                <option value="PC">Computadora</option>
                <option value="IMP">Impresora</option>
              </select>

              <div className="form-content">
                <label>Código del equipo</label>
                <input type="text" id="codigo" placeholder="Ingresa código" disabled />
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
              <input type="text" id="area" placeholder="Ingresa el área" disabled />
            </div>

            <div className="form-content">
              <label>Fecha de adquisición</label>
              <input type="date" id="fecha" disabled />
            </div>

            <div className="form-actions">
              <button type="button" className="btn-save">Actualizar</button>
              <button type="button" onClick={handleCancel} className="btn-cancel">Cancelar</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default ActualizarMaquina
