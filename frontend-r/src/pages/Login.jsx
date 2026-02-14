import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './Login.css'

function Login() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  })

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value
    })
  }

  const handleLogin = async (e) => {
    e.preventDefault()
    
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      })

      if (response.ok) {
        const data = await response.json()
        localStorage.setItem('token', data.token)
        localStorage.setItem('user', JSON.stringify(data.usuario))
        navigate('/pagina/inicio')
      } else {
        const errorData = await response.json()
        alert(errorData.detail || 'Error en el login')
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

        <form onSubmit={handleLogin}>
          <div className="input-user">
            <label htmlFor="username">Usuario</label>
            <div className="input-information">
              <input 
                type="text" 
                id="username" 
                placeholder="Ingresar usuario"
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
                placeholder="Ingresar contraseña"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <button type="submit" className="btn-signin">Iniciar sesión</button>
        </form>

        <p className="footer-text">
          ¿No tienes cuenta? <a href="/pagina/registro">Registrarse</a>
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

export default Login
