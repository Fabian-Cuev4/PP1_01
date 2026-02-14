import { useNavigate } from 'react-router-dom'
import './Inicio.css'

function Inicio() {
  const navigate = useNavigate()

  const handleLogout = () => {
    navigate('/pagina/login')
  }

  return (
    <div className="inicio-container">
      <header className="main-header">
        <div className="user-profile">
          <div className="avatar">
            <img src="/static/img/icono_user.png" alt="Usuario" />
          </div>
        </div>
        <div className="logout-section">
          <button type="button" onClick={handleLogout} className="btn-logout">
            Cerrar Sesión
            <img src="/static/img/icono_cerrar_sesion.png" alt="Cerrar" />
          </button>
        </div>
      </header>

      <main className="content">
        <div className="top-bar" style={{ height: '40px' }}>
        </div>

        <h1 className="title">Tu espacio de trabajo</h1>

        <div className="cards-conta">
          <div className="card-target" onClick={() => navigate('/pagina/maquinas')}>
            <div className="card-space">
              <div className="card-icon">
                <img src="/static/img/icono_maquina.png" alt="Máquinas" />
              </div>
              <div className="card-info">
                <h3>Laboratorio de Redes</h3>
                <p><strong>Ubicación:</strong> Edificio A - Piso 2</p>
                <p><strong>Entidad:</strong> FICA - Ing. en Sistemas</p>
                <p><strong>N° Equipos:</strong> 5</p>
              </div>
            </div>
          </div>
        </div>
      </main>

      <footer className="main-footer">
      </footer>
    </div>
  )
}

export default Inicio
