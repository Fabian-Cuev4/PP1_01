import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../styles/Login.css'

function Login() {
  const [formData, setFormData] = useState({
    usuario: '',
    password: ''
  })
  const [modal, setModal] = useState({
    show: false,
    title: '',
    message: ''
  })
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value
    })
  }

  const mostrarModal = (titulo, mensaje) => {
    setModal({
      show: true,
      title: titulo,
      message: mensaje
    })
  }

  const ocultarModal = () => {
    setModal({
      ...modal,
      show: false
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    // Obtener valores del DOM como en el original
    const usuario = document.getElementById('usuario').value
    const password = document.getElementById('password').value

    if (!usuario || !password) {
      mostrarModal("Campos incompletos", "Por favor, completa todos los campos.")
      return
    }

    try {
      const response = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          username: usuario, 
          password: password 
        })
      })

      if (response.ok) {
        const data = await response.json()
        if (data.username) {
          localStorage.setItem('username', data.username)
        }
        navigate("/pagina/inicio")
      } else {
        mostrarModal("Error de autenticación", "Usuario o contraseña incorrectos.")
      }
    } catch (error) {
      console.error("Error al iniciar sesión:", error)
      mostrarModal("Error de conexión", "Error de conexión con el servidor.")
    }
  }

  const handleLoginClick = () => {
    handleSubmit({ preventDefault: () => {} })
  }

  return (
    <>
      <div className="login-card">
        {/* Dibujo del logo del proyecto en la parte de arriba */}
        <div className="logo-section">
          <img src="/img/Logo.png" alt="SIGLAB Logo" className="logo" />
        </div>

        {/* El formulario donde se escriben los datos */}
        <form>
          {/* Contenedor para el nombre de usuario */}
          <div className="input-user">
            <label htmlFor="usuario">Usuario</label>
            <div className="input-information">
              <input 
                type="text" 
                id="usuario" 
                placeholder="Ingresar usuario"
              />
            </div>
          </div>
          
          {/* Contenedor para la clave secreta */}
          <div className="input-password">
            <label htmlFor="password">Contraseña</label>
            <div className="input-information">
              <input 
                type="password" 
                id="password" 
                placeholder="Ingresar contraseña"
              />
            </div>
          </div>
          
          {/* Botón azul que al darle clic intenta entrar al sistema */}
          <button type="button" className="btn-signin" onClick={handleLoginClick}>
            Iniciar sesión
          </button>
        </form>

        {/* Enlace para ir a la página de registro si no tienes cuenta */}
        <p className="footer-text">
          ¿No tienes cuenta? <a href="/pagina/registro" onClick={(e) => { e.preventDefault(); navigate("/pagina/registro"); }}>Registrarse</a>
        </p>
      </div>

      {/* Esta es la ventana flotante que sale solo cuando hay un aviso o error */}
      {modal.show && (
        <div className="modal-overlay show">
          <div className="modal-content">
            {/* Ícono de alerta que cambia de color según el aviso */}
            <span className="modal-icon">
              <i className="fas fa-exclamation-circle"></i>
            </span>
            <h3>{modal.title}</h3>
            <p>{modal.message}</p>
            {/* Botón para cerrar esta ventana flotante */}
            <button type="button" className="btn-modal" onClick={ocultarModal}>
              Entendido
            </button>
          </div>
        </div>
      )}
    </>
  )
}

export default Login
