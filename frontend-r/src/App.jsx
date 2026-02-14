import { Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Inicio from './pages/Inicio'
import Maquinas from './pages/Maquinas'
import Reportes from './pages/Reportes'
import AgregarMaquina from './pages/AgregarMaquina'
import ActualizarMaquina from './pages/ActualizarMaquina'
import Mantenimiento from './pages/Mantenimiento'
import Historial from './pages/Historial'

function App() {
  return (
    <Routes>
      <Route path="/pagina/login" element={<Login />} />
      <Route path="/pagina/registro" element={<Register />} />
      <Route path="/pagina/inicio" element={<Inicio />} />
      <Route path="/pagina/maquinas" element={<Maquinas />} />
      <Route path="/pagina/reportes" element={<Reportes />} />
      <Route path="/pagina/agregar-maquina" element={<AgregarMaquina />} />
      <Route path="/pagina/actualizar-maquina" element={<ActualizarMaquina />} />
      <Route path="/pagina/mantenimiento" element={<Mantenimiento />} />
      <Route path="/pagina/historial" element={<Historial />} />
      <Route path="*" element={<Login />} />
    </Routes>
  )
}

export default App
