import { useNavigate } from 'react-router-dom'
import '../styles/Inicio.css'

function Inicio() {
  const navigate = useNavigate()
  const username = localStorage.getItem('username')

  const handleLogout = () => {
    localStorage.removeItem('username')
    navigate("/pagina/login")
  }

  const handleMaquinasClick = () => {
    navigate("/pagina/maquinas")
  }

  return (
    <>
      <header className="main-header">
        <div className="user-profile">
          <div className="avatar">
            <img src="/img/icono_user.png" alt="Usuario" />
          </div>
        </div>
        <div className="logout-section">
          <button type="button" className="btn-logout" onClick={handleLogout}>
            Cerrar Sesión
            <img src="/img/icono_cerrar_sesion.png" alt="Cerrar Sesión" />
          </button>
        </div>
      </header>

      <main className="content">
        <div className="top-bar" style={{ height: '40px' }}></div>
        <h1 className="title">Tu espacio de trabajo</h1>
        
        <div className="cards-conta">
          <div className="card-target" onClick={handleMaquinasClick}>
            <div className="card-space">
              <div className="card-icon">
                <img src="/img/icono_maquina.png" alt="Máquinas" />
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
        <p> 2024 SIGLAB - Sistema de Gestión de Laboratorios</p>
      </footer>
    </>
  )
}

export default Inicio
