import { useNavigate } from 'react-router-dom'
import './Register.css'

function Register() {
  const navigate = useNavigate()

  const handleRegister = () => {
    navigate('/pagina/login')
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="logo-section">
          <img src="/static/img/Logo.png" alt="SIGLAB Logo" className="logo" />
        </div>

        <h2>Crear Cuenta</h2>
        <br />

        <form>
          <div className="input-user">
            <label htmlFor="nombre">Nombre Completo</label>
            <div className="input-information">
              <input type="text" id="nombre" placeholder="Tu nombre y apellido" />
            </div>
          </div>

          <div className="input-user">
            <label htmlFor="usuario">Usuario</label>
            <div className="input-information">
              <input type="text" id="usuario" placeholder="Crea un nombre de usuario" />
            </div>
          </div>

          <div className="input-password">
            <label htmlFor="password">Contraseña</label>
            <div className="input-information">
              <input type="password" id="password" placeholder="Mínimo 8 caracteres" />
            </div>
          </div>

          <div className="input-password">
            <label htmlFor="confirm-password">Confirmar Contraseña</label>
            <div className="input-information">
              <input type="password" id="confirm-password" placeholder="Repite tu contraseña" />
            </div>
          </div>

          <button type="button" onClick={handleRegister} className="btn-signin">Registrarse</button>
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
