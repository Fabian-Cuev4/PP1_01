import { useNavigate } from 'react-router-dom'
import './Login.css'

function Login() {
  const navigate = useNavigate()

  const handleLogin = () => {
    navigate('/pagina/inicio')
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="logo-section">
          <img src="/static/img/Logo.png" alt="SIGLAB Logo" className="logo" />
        </div>

        <form>
          <div className="input-user">
            <label htmlFor="usuario">Usuario</label>
            <div className="input-information">
              <input type="text" id="usuario" placeholder="Ingresar usuario" />
            </div>
          </div>

          <div className="input-password">
            <label htmlFor="password">Contraseña</label>
            <div className="input-information">
              <input type="password" id="password" placeholder="Ingresar contraseña" />
            </div>
          </div>

          <button type="button" onClick={handleLogin} className="btn-signin">Iniciar sesión</button>
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
