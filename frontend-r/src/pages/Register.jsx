import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './Register.css'

function Register() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    nombre_completo: '',
    username: '',
    password: '',
    'confirm-password': ''
  })

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value
    })
  }

  const handleRegister = async (e) => {
    e.preventDefault()
    
    if (formData.password !== formData['confirm-password']) {
      alert('Las contraseñas no coinciden')
      return
    }

    if (formData.password.length < 8) {
      alert('La contraseña debe tener mínimo 8 caracteres')
      return
    }

    try {
      const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          nombre_completo: formData.nombre_completo,
          username: formData.username,
          password: formData.password
        })
      })

      if (response.ok) {
        alert('Usuario registrado exitosamente')
        navigate('/pagina/login')
      } else {
        const errorData = await response.json()
        alert(errorData.detail || 'Error en el registro')
      }
    } catch (error) {
      console.error('Error:', error)
      alert('Error de conexión con el servidor')
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="logo-section">
          <img src="/static/img/Logo.png" alt="SIGLAB Logo" className="logo" />
        </div>

        <h2>Crear Cuenta</h2>
        <br />

        <form onSubmit={handleRegister}>
          <div className="input-user">
            <label htmlFor="nombre_completo">Nombre Completo</label>
            <div className="input-information">
              <input 
                type="text" 
                id="nombre_completo" 
                placeholder="Tu nombre y apellido"
                value={formData.nombre_completo}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="input-user">
            <label htmlFor="username">Usuario</label>
            <div className="input-information">
              <input 
                type="text" 
                id="username" 
                placeholder="Crea un nombre de usuario"
                value={formData.username}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="input-password">
            <label htmlFor="password">Contraseña</label>
            <div className="input-information">
              <input 
                type="password" 
                id="password" 
                placeholder="Mínimo 8 caracteres"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="input-password">
            <label htmlFor="confirm-password">Confirmar Contraseña</label>
            <div className="input-information">
              <input 
                type="password" 
                id="confirm-password" 
                placeholder="Repite tu contraseña"
                value={formData['confirm-password']}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <button type="submit" className="btn-signin">Registrarse</button>
        </form>

        <p className="footer-text">
          ¿Ya tienes cuenta? <a href="/pagina/login">Inicia sesión aquí</a>
        </p>
      </div>

      <div id="modal-notificacion" className="modal-overlay hidden">
        <div className="modal-content">
          <span className="modal-icon"><i className="fas fa-exclamation-circle"></i></span>
          <h3 id="modal-titulo">Atención</h3>
          <p id="modal-mensaje"></p>
          <button type="button" id="btn-modal-cerrar" className="btn-modal">Entendido</button>
        </div>
      </div>
    </div>
  )
}

export default Register
