import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Modal from '../components/Modal'
import logo from '../assets/img/Logo.png'
import './Login.css'

function Login() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  })
  const [modal, setModal] = useState({
    isVisible: false,
    title: 'Atención',
    message: '',
    icon: 'fa-exclamation-circle',
    iconColor: '#e74c3c'
  })

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value
    })
  }

  const showModal = (title, message, icon = 'fa-exclamation-circle', iconColor = '#e74c3c') => {
    setModal({
      isVisible: true,
      title,
      message,
      icon,
      iconColor
    })
  }

  const hideModal = () => {
    setModal({
      ...modal,
      isVisible: false
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
        showModal('Error de Login', errorData.detail || 'Error en el login', 'fa-exclamation-circle', '#e74c3c')
      }
    } catch (error) {
      console.error('Error:', error)
      showModal('Error de Conexión', 'Error de conexión con el servidor', 'fa-wifi', '#e74c3c')
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="logo-section">
          <img src={logo} alt="SIGLAB Logo" className="logo" onError={(e) => {e.target.src='/vite.svg'}} />
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

      <Modal
        isVisible={modal.isVisible}
        onClose={hideModal}
        title={modal.title}
        message={modal.message}
        icon={modal.icon}
        iconColor={modal.iconColor}
      />
    </div>
  )
}

export default Login
