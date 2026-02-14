import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../styles/AgregarMaquina.css'

function AgregarMaquina() {
  const [formData, setFormData] = useState({
    tipo_equipo: '',
    codigo: '',
    estado_actual: '',
    area: '',
    fecha: '',
    opcionesAvanzadas: false
  })
  const [modal, setModal] = useState({
    show: false,
    type: '',
    title: '',
    message: ''
  })
  const navigate = useNavigate()

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    })
  }

  const mostrarModal = (tipo, titulo, mensaje, callback = null) => {
    setModal({
      show: true,
      type: tipo,
      title: titulo,
      message: mensaje,
      callback: callback
    })
  }

  const ocultarModal = () => {
    if (modal.callback) {
      modal.callback()
    }
    setModal({
      ...modal,
      show: false,
      callback: null
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    const username = localStorage.getItem('username') || null
    const datos = {
      tipo_equipo: formData.tipo_equipo,
      codigo_equipo: formData.codigo,
      estado_actual: formData.estado_actual,
      area: formData.area,
      fecha: formData.fecha,
      usuario: username
    }

    if (!datos.tipo_equipo || !datos.codigo_equipo || !datos.estado_actual) {
      mostrarModal('warning', 'Campos Incompletos', 'Por favor, completa todos los campos obligatorios.')
      return
    }

    try {
      const response = await fetch("/api/maquinas/agregar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
      })

      const resultado = await response.json()

      if (response.ok) {
        mostrarModal('success', '¡Registro Exitoso!', 'La máquina ha sido registrada correctamente.', () => {
          navigate("/pagina/maquinas")
        })
      } else {
        let msg = "No se pudo guardar la máquina."
        if (JSON.stringify(resultado).toLowerCase().includes("ya existe")) {
          msg = `El código "${datos.codigo_equipo}" ya está en uso.`
        }
        mostrarModal('error', 'Error al Guardar', msg)
      }
    } catch (error) {
      mostrarModal('error', 'Error de Conexión', 'No se pudo contactar con el servidor.')
    }
  }

  const handleCancel = () => {
    navigate("/pagina/maquinas")
  }

  const getModalIcon = () => {
    switch (modal.type) {
      case 'success':
        return '✅'
      case 'error':
        return '❌'
      case 'warning':
        return '⚠️'
      default:
        return 'ℹ️'
    }
  }

  return (
    <div className="agregar-maquina-container">
      <div className="modal-overlay">
        <div className="modal-head">
          <h2 className="modal-content-head">Agregar Máquina</h2>
          
          <form className="form" onSubmit={handleSubmit}>
            <div className="form-content">
              <label>Tipo de Equipo:</label>
              <select 
                id="tipo_equipo" 
                name="tipo_equipo"
                value={formData.tipo_equipo}
                onChange={handleChange}
              >
                <option value="">Selecciona</option>
                <option value="PC">Computadora</option>
                <option value="IMP">Impresora</option>
              </select>
            </div>

            <div className="form-content">
              <label>Código del equipo</label>
              <input 
                type="text" 
                id="codigo" 
                name="codigo"
                value={formData.codigo}
                onChange={handleChange}
                placeholder="Ingresa código"
              />
            </div>

            <div className="form-content">
              <label>Estado actual</label>
              <select 
                id="estado_actual"
                name="estado_actual"
                value={formData.estado_actual}
                onChange={handleChange}
              >
                <option value="">Selecciona</option>
                <option value="operativa">Operativa</option>
                <option value="Fuera de servicio">Fuera de servicio</option>
                <option value="dada de baja">Dada de baja</option>
              </select>
            </div>

            <div className="form-content">
              <label>Área</label>
              <input 
                type="text" 
                id="area" 
                name="area"
                value={formData.area}
                onChange={handleChange}
                placeholder="Ingresa el área"
              />
            </div>

            <div className="form-content">
              <label>Fecha de adquisición</label>
              <input 
                type="date" 
                id="fecha"
                name="fecha"
                value={formData.fecha}
                onChange={handleChange}
              />
            </div>

            <div className="form-group checkbox-group">
              <input 
                type="checkbox" 
                id="avanzadas"
                name="opcionesAvanzadas"
                checked={formData.opcionesAvanzadas}
                onChange={handleChange}
              />
              <label htmlFor="avanzadas">Opciones avanzadas</label>
            </div>

            <div className="form-actions">
              <button type="submit" className="btn-save">Guardar</button>
              <button type="button" className="btn-cancel" onClick={handleCancel}>Cancelar</button>
            </div>
          </form>
        </div>
      </div>

      {modal.show && (
        <div className={`validation-modal-overlay ${modal.show ? 'active' : ''}`}>
          <div className="validation-card">
            <div className={`modal-icon icon-${modal.type}`}>
              {getModalIcon()}
            </div>
            <h3 className="modal-title">{modal.title}</h3>
            <p className="modal-message">{modal.message}</p>
            <button className="btn-modal-ok" onClick={ocultarModal}>Entendido</button>
          </div>
        </div>
      )}
    </div>
  )
}

export default AgregarMaquina
