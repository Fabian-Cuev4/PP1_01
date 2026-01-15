document.addEventListener("DOMContentLoaded", async () => {
    // Ejecuta la carga inicial de máquinas
    await cargarMaquinas();

    // Opcional: Escuchador para el buscador (si quieres que funcione ya)
    const buscador = document.getElementById("input-busqueda");
    if (buscador) {
        buscador.addEventListener("input", filtrarMaquinas);
    }
});

/**
 * Determina el color del badge según el texto del estado
 */
function obtenerClaseEstado(estado) {
    if (!estado) return "status-baja"; // Por defecto rojo si no hay estado
    const e = estado.toLowerCase();
    if (e.includes("operativa")) return "status-operativa";
    if (e.includes("mantenimiento")) return "status-mantenimiento";
    if (e.includes("baja")) return "status-baja";
    return "status-mantenimiento";
}

/**
 * Carga las máquinas desde el servidor y genera el HTML dinámico
 */
async function cargarMaquinas() {
    const contenedor = document.getElementById("contenedor-principal-maquinas");
    if (!contenedor) return;

    try {
        const response = await fetch("/home/maquinas/listar");
        const maquinas = await response.json();
        
        contenedor.innerHTML = ""; // Limpiamos contenedor

        if (maquinas.length === 0) {
            contenedor.innerHTML = "<p style='text-align:center; padding:20px;'>No hay equipos registrados.</p>";
            return;
        }

        for (const m of maquinas) {
            const claseEstado = obtenerClaseEstado(m.estado);

            // TARJETA MINIMALISTA: Solo datos base y los 4 botones
            const tarjetaHTML = `
                <div class="detail-container">
                    <div class="card-space">
                        <div class="card-icon"></div>
                        <div class="card-info">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                <h3 style="font-size: 22px; color: #2c3e50; margin: 0;">${m.codigo}</h3>
                                <span class="status-badge ${claseEstado}">${m.estado}</span>
                            </div>
                            <div style="display: flex; gap: 40px; font-size: 14px; color: #555;">
                                <p><strong>Área:</strong> ${m.area}</p>
                                <p><strong>Adquisición:</strong> ${m.fecha}</p>
                                <p><strong>Tipo máquina:</strong> ${m.tipo}</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="side-buttons">
                        <button class="btn-action btn-yellow-history" onclick="verHistorial('${m.codigo}')">Historial mantenimiento</button>
                        <button class="btn-action btn-blue-act" onclick="irAMantenimiento('${m.codigo}')">Mantenimiento</button>
                        <button class="btn-action btn-green" onclick="actualizar('${m.codigo}')">Actualizar</button>
                        <button class="btn-action btn-red" onclick="confirmarEliminar('${m.codigo}')">Eliminar</button>
                    </div>
                </div>
            `;
            contenedor.insertAdjacentHTML("beforeend", tarjetaHTML);
        }
    } catch (error) {
        console.error("Error al cargar máquinas:", error);
    }
}

// Nueva función para el botón Historial
function verHistorial(codigo) {
    localStorage.setItem("maquinaSeleccionada", codigo);
    window.location.href = "/home/maquinas/historial";
}

function irAMantenimiento(codigo) {
    window.location.href = "/home/maquinas/formulario/mantenimiento";
}
