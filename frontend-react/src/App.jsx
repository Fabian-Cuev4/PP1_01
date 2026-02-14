import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useEffect } from 'react'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Maquinas from './pages/Maquinas'
import AgregarMaquina from './pages/AgregarMaquina'
import Historial from './pages/Historial'
import './App.css'

function App() {
  useEffect(() => {
    // Add Font Awesome CDN
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
    document.head.appendChild(link)

    return () => {
      document.head.removeChild(link)
    }
  }, [])

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/pagina/login" element={<Login />} />
          <Route path="/pagina/registro" element={<Register />} />
          <Route path="/pagina/inicio" element={<Dashboard />} />
          <Route path="/pagina/maquinas" element={<Maquinas />} />
          <Route path="/pagina/agregar-maquina" element={<AgregarMaquina />} />
          <Route path="/pagina/historial" element={<Historial />} />
          <Route path="/" element={<Login />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
