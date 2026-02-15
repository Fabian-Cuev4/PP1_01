import { Routes, Route, Navigate } from 'react-router-dom'
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
      <Route path="/login" element={<Login />} />
      <Route path="/registro" element={<Register />} />
      <Route path="/inicio" element={<Inicio />} />
      <Route path="/maquinas" element={<Maquinas />} />
      <Route path="/reportes" element={<Reportes />} />
      <Route path="/agregar-maquina" element={<AgregarMaquina />} />
      <Route path="/actualizar-maquina" element={<ActualizarMaquina />} />
      <Route path="/mantenimiento" element={<Mantenimiento />} />
      <Route path="/historial" element={<Historial />} />
      <Route path="/" element={<Navigate to="/login" replace />} />
    </Routes>
  )
}

export default App
