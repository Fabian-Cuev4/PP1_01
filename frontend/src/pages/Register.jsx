import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Modal from '../components/Modal'
import logo from '../assets/img/Logo.png'
import '../styles/Formularios.css'

function Register() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    nombre_completo: '',
    username: '',
    password: '',
    'confirm-password': ''
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

  const handleRegister = async (e) => {
    e.preventDefault()
    
    if (!formData.nombre_completo || !formData.username || !formData.password || !formData['confirm-password']) {
      showModal('Datos Incompletos', 'Por favor complete todos los campos para registrarse', 'fa-exclamation-triangle', '#e74c3c')
      return
    }
    
    if (formData.password !== formData['confirm-password']) {
      showModal('Error de Validación', 'Las contraseñas no coinciden', 'fa-exclamation-triangle', '#e74c3c')
      return
    }

    if (formData.password.length < 8) {
      showModal('Error de Validación', 'La contraseña debe tener mínimo 8 caracteres', 'fa-exclamation-triangle', '#e74c3c')
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
        showModal('Registro Exitoso', 'Usuario registrado exitosamente', 'fa-check-circle', '#27ae60')
        setTimeout(() => {
          navigate('/login')
        }, 2000)
      } else {
        const errorData = await response.json()
        showModal('Error en el Registro', errorData.detail || 'Error en el registro', 'fa-exclamation-circle', '#e74c3c')
      }
    } catch (error) {
      showModal('Error de Conexión', 'Error de conexión con el servidor', 'fa-wifi', '#e74c3c')
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="logo-section">
          <img src={logo} alt="SIGLAB Logo" className="logo" onError={(e) => {e.target.src='/vite.svg'}} />
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
              />
            </div>
          </div>

          <button type="submit" className="btn-signin">Registrarse</button>
        </form>

        <p className="footer-text">
          ¿Ya tienes cuenta? <a href="/login">Inicia sesión aquí</a>
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

export default Register
