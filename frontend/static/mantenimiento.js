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
        
        // Limpiamos el contenedor para evitar duplicados
        contenedor.innerHTML = "";

        if (maquinas.length === 0) {
            contenedor.innerHTML = "<p style='text-align:center; padding:20px;'>No se encontraron equipos registrados.</p>";
            return;
        }

        for (const m of maquinas) {
            // Valores por defecto si no hay mantenimiento
            let ultimo = { fecha: "---", tecnico: "---", nota: "Sin registros recientes." };
            
            try {
                const resM = await fetch(`/home/mantenimiento/listar/${m.codigo}`);
                if (resM.ok) {
                    const h = await resM.json();
                    if (h && h.length > 0) {
                        ultimo = { 
                            fecha: h[0].fecha, 
                            tecnico: h[0].tecnico, 
                            nota: h[0].observaciones || "Sin observaciones." 
                        };
                    }
                }
            } catch (e) { 
                console.warn("No se pudo obtener el historial de " + m.codigo); 
            }

            const claseEstado = obtenerClaseEstado(m.estado);

            // Generación de la estructura idéntica a tu diseño
            const tarjetaHTML = `
                <div class="detail-container">
                    <div class="card-space">
                        <div class="card-icon"></div>
                        <div class="card-info">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                <h3 style="font-size: 22px; color: #2c3e50;">${m.codigo}</h3>
                                <span class="status-badge ${claseEstado}">${m.estado}</span>
                            </div>
                            <div style="display: flex; gap: 30px;">
                                <div style="min-width: 200px;">
                                    <p style="margin-bottom: 8px;"><strong>Área:</strong> ${m.area}</p>
                                    <p><strong>Adquisición:</strong> ${m.fecha}</p>
                                </div>
                                <div style="flex: 1;">
                                    <p style="margin-bottom: 8px;"><strong>Último Mantenimiento:</strong> ${ultimo.fecha}</p>
                                    <p style="margin-bottom: 8px;"><strong>Responsable:</strong> ${ultimo.tecnico}</p>
                                    <div class="desc"><strong>Nota:</strong> ${ultimo.nota}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="side-buttons">
                        <button class="btn-action btn-red" onclick="confirmarEliminar('${m.codigo}')">Eliminar</button>
                        <button class="btn-action btn-green" onclick="actualizar('${m.codigo}')">Actualizar</button>
                        <button class="btn-action btn-blue-act" onclick="irAMantenimiento('${m.codigo}')">Mantenimiento</button>
                    </div>
                </div>
            `;
            contenedor.insertAdjacentHTML("beforeend", tarjetaHTML);
        }
    } catch (error) {
        console.error("Error crítico al cargar máquinas:", error);
        contenedor.innerHTML = "<p style='color:red;'>Error al conectar con el servidor.</p>";
    }
}

/**
 * Funciones de Acción
 */
function irAMantenimiento(codigo) {
    localStorage.setItem("maquinaSeleccionada", codigo);
    window.location.href = "/home/maquinas/formulario/mantenimiento";
}

function confirmarEliminar(codigo) {
    if (confirm(`¿Estás seguro de que deseas eliminar el equipo ${codigo}? Esta acción no se puede deshacer.`)) {
        // Aquí iría tu fetch para eliminar: fetch(`/home/maquinas/eliminar/${codigo}`, { method: 'DELETE' })
        console.log("Eliminando máquina:", codigo);
        // Al terminar, recargar: cargarMaquinas();
    }
}

/**
 * Función de filtrado para el buscador
 */
function filtrarMaquinas() {
    const termino = document.getElementById("input-busqueda").value.toLowerCase();
    const tarjetas = document.querySelectorAll(".detail-container");

    tarjetas.forEach(tarjeta => {
        const texto = tarjeta.innerText.toLowerCase();
        tarjeta.style.display = texto.includes(termino) ? "flex" : "none";
    });
}