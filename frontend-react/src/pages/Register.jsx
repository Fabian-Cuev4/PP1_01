import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../styles/Login.css'

function Register() {
  const [modal, setModal] = useState({
    show: false,
    title: '',
    message: ''
  })
  const navigate = useNavigate()

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
    const nombre = document.getElementById('nombre').value
    const usuario = document.getElementById('usuario').value
    const password = document.getElementById('password').value
    const confirmPassword = document.getElementById('confirm-password').value

    if (!nombre || !usuario || !password || !confirmPassword) {
      mostrarModal("Campos incompletos", "Por favor, completa todos los campos.")
      return
    }

    if (password !== confirmPassword) {
      mostrarModal("Contraseñas no coinciden", "Las contraseñas deben ser iguales.")
      return
    }

    if (password.length < 8) {
      mostrarModal("Contraseña muy corta", "La contraseña debe tener mínimo 8 caracteres.")
      return
    }

    try {
      const response = await fetch("/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          username: usuario, 
          password: password,
          nombre: nombre
        })
      })

      if (response.ok) {
        mostrarModal("Registro Exitoso", "Usuario registrado correctamente. Inicia sesión.", () => {
          navigate("/pagina/login")
        })
      } else {
        const errorData = await response.json()
        mostrarModal("Error de Registro", errorData.message || "No se pudo registrar el usuario.")
      }
    } catch (error) {
      console.error("Error al registrar:", error)
      mostrarModal("Error de conexión", "Error de conexión con el servidor.")
    }
  }

  const handleRegisterClick = () => {
    handleSubmit({ preventDefault: () => {} })
  }

  return (
    <>
      <div className="login-card register-compact">
        {/* Contenedor para la imagen del logo */}
        <div className="logo-section">
          <img src="/img/Logo.png" alt="SIGLAB Logo" className="logo" />
        </div>

        <h2>Crear Cuenta</h2>
        <br />

        <form>
          {/* Grupo para el nombre real de la persona */}
          <div className="input-user">
            <label htmlFor="nombre">Nombre Completo</label>
            <div className="input-information">
              <input 
                type="text" 
                id="nombre" 
                placeholder="Tu nombre y apellido"
              />
            </div>
          </div>

          {/* Grupo para elegir un nombre de usuario único */}
          <div className="input-user">
            <label htmlFor="usuario">Usuario</label>
            <div className="input-information">
              <input 
                type="text" 
                id="usuario" 
                placeholder="Crea un nombre de usuario"
              />
            </div>
          </div>

          {/* Grupo para escribir la contraseña */}
          <div className="input-password">
            <label htmlFor="password">Contraseña</label>
            <div className="input-information">
              <input 
                type="password" 
                id="password" 
                placeholder="Mínimo 8 caracteres"
              />
            </div>
          </div>

          {/* Grupo para repetir la contraseña y evitar errores */}
          <div className="input-password">
            <label htmlFor="confirm-password">Confirmar Contraseña</label>
            <div className="input-information">
              <input 
                type="password" 
                id="confirm-password" 
                placeholder="Repite tu contraseña"
              />
            </div>
          </div>

          {/* Botón que activa el proceso de guardado en la base de datos */}
          <button type="button" className="btn-signin" onClick={handleRegisterClick}>
            Registrarse
          </button>
        </form>

        {/* Texto para usuarios que ya tienen una cuenta */}
        <p className="footer-text">
          ¿Ya tienes cuenta? <a href="/pagina/login" onClick={(e) => { e.preventDefault(); navigate("/pagina/login"); }}>Inicia sesión aquí</a>
        </p>
      </div>

      {/* Ventana flotante que aparece para avisar si algo salió bien o mal */}
      {modal.show && (
        <div className="modal-overlay show">
          <div className="modal-content">
            {/* Ícono que advierte al usuario (!) */}
            <span className="modal-icon">
              <i className="fas fa-exclamation-circle"></i>
            </span>
            <h3>{modal.title}</h3>
            <p>{modal.message}</p>
            {/* Botón para cerrar esta notificación */}
            <button type="button" className="btn-modal" onClick={ocultarModal}>
              Entendido
            </button>
          </div>
        </div>
      )}
    </>
  )
}

export default Register
