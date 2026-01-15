document.addEventListener("DOMContentLoaded", async () => {
    await cargarMaquinas();
});

function obtenerClaseEstado(estado) {
    const e = estado.toLowerCase();
    if (e.includes("operativa")) return "status-operativa";
    if (e.includes("mantenimiento")) return "status-mantenimiento";
    if (e.includes("baja")) return "status-baja";
    return "";
}

async function cargarMaquinas() {
    const contenedor = document.getElementById("contenedor-principal-maquinas");
    if (!contenedor) return;

    try {
        const response = await fetch("/home/maquinas/listar");
        const maquinas = await response.json();
        contenedor.innerHTML = "";

        for (const m of maquinas) {
            let ultimo = { fecha: "---", tecnico: "---", nota: "Sin registros." };
            
            try {
                const resM = await fetch(`/home/mantenimiento/listar/${m.codigo}`);
                const h = await resM.json();
                if (h && h.length > 0) {
                    ultimo = { fecha: h[0].fecha, tecnico: h[0].tecnico, nota: h[0].observaciones };
                }
            } catch (e) { console.log("Error fetch mantenimiento"); }

            const claseEstado = obtenerClaseEstado(m.estado);

            const tarjetaHTML = `
                <div class="detail-container">
                    <div class="card-space">
                        <div class="card-icon"></div>
                        <div class="card-info">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                                <h3 style="font-size: 26px; color: #2c3e50;">${m.codigo}</h3>
                                <span class="status-badge ${claseEstado}">${m.estado}</span>
                            </div>
                            <div style="display: flex; gap: 40px;">
                                <div style="flex: 1;">
                                    <p style="margin-bottom: 10px;"><strong>Área:</strong> ${m.area}</p>
                                    <p><strong>Adquisición:</strong> ${m.fecha}</p>
                                </div>
                                <div style="flex: 1;">
                                    <p style="margin-bottom: 10px;"><strong>Mantenimiento:</strong> ${ultimo.fecha}</p>
                                    <p style="margin-bottom: 10px;"><strong>Responsable:</strong> ${ultimo.tecnico}</p>
                                    <div class="desc"><strong>Nota:</strong> ${ultimo.nota}</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="side-buttons">
                        <button class="btn-action btn-red" onclick="eliminar('${m.codigo}')">Eliminar</button>
                        <button class="btn-action btn-green" onclick="actualizar('${m.codigo}')">Actualizar</button>
                        <button class="btn-action btn-blue-act" onclick="irAMantenimiento('${m.codigo}')">Mantenimiento</button>
                    </div>
                </div>
            `;
            contenedor.insertAdjacentHTML("beforeend", tarjetaHTML);
        }
    } catch (error) { console.error("Error al cargar máquinas:", error); }
}

function irAMantenimiento(codigo) {
    localStorage.setItem("maquinaSeleccionada", codigo);
    window.location.href = "/home/maquinas/formulario/mantenimiento";
}