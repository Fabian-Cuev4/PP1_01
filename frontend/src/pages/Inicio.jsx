import { useNavigate } from 'react-router-dom'
import { useEffect } from 'react'
import iconoUser from '../assets/img/icono_user.png'
import iconoCerrarSesion from '../assets/img/icono_cerrar_sesion.png'
import iconoMaquina from '../assets/img/icono_maquina.png'
import '../styles/Inicio.css'

function Inicio() {
  const navigate = useNavigate()

  useEffect(() => {
    if (!sessionStorage.getItem('token')) {
      navigate('/login')
    }
  }, [navigate])

  const handleLogout = () => {
    sessionStorage.removeItem('token')
    sessionStorage.removeItem('user')
    navigate('/login')
  }

  return (
    <div className="inicio-container">
      <header className="main-header">
        <div className="user-profile">
          <div className="avatar">
            <img src={iconoUser} alt="Usuario" />
          </div>
        </div>
        <div className="logout-section">
          <button type="button" onClick={handleLogout} className="btn-logout">
            Cerrar Sesión
            <img src={iconoCerrarSesion} alt="Cerrar" />
          </button>
        </div>
      </header>

      <main className="content">
        <div className="top-bar" style={{ height: '40px' }}>
        </div>

        <h1 className="title">Tu espacio de trabajo</h1>

        <div className="cards-conta">
          <div className="card-target" onClick={() => navigate('/maquinas')}>
            <div className="card-space">
              <div className="card-icon">
                <img src={iconoMaquina} alt="Máquinas" />
              </div>
              <div className="card-info">
                <h3>Gestión de Equipos</h3>
                <p>Administra todas las máquinas del laboratorio</p>
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
