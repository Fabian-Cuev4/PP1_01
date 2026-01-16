// maneja la lista de máquinas: carga, muestra y filtra las tarjetas de equipos
document.addEventListener("DOMContentLoaded", async () => {
    await cargarMaquinas(); // carga las máquinas al iniciar la página

    // activa el buscador para filtrar mientras se escribe
    const buscador = document.getElementById("input-busqueda");
    if (buscador) {
        buscador.addEventListener("input", filtrarMaquinas);

        // atajos de teclado: enter para confirmar, escape para limpiar
        buscador.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                filtrarMaquinas();
            } else if (e.key === "Escape") {
                buscador.value = "";
                filtrarMaquinas();
            }
        });
    }
});

// decide el color del badge según el estado de la máquina
function obtenerClaseEstado(estado) {
    if (!estado) return "status-baja";
    const e = estado.toLowerCase();
    if (e.includes("operativa")) return "status-operativa";
    if (e.includes("mantenimiento")) return "status-mantenimiento";
    if (e.includes("baja")) return "status-baja";
    return "status-mantenimiento";
}

// pide las máquinas al backend y las dibuja en pantalla
async function cargarMaquinas() {
    const contenedor = document.getElementById("contenedor-principal-maquinas");
    if (!contenedor) return;

    try {
        // pide la lista de máquinas al backend
        const timestamp = new Date().getTime();
        const response = await fetch(`/home/maquinas/listar?_t=${timestamp}`, {
            method: 'GET',
            headers: {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            }
        });

        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }

        const maquinas = await response.json();

        if (!Array.isArray(maquinas)) {
            console.error("Error: La respuesta no es un array:", maquinas);
            contenedor.innerHTML = "<p>Error al cargar las máquinas.</p>";
            return;
        }

        contenedor.innerHTML = "";

        // si no hay máquinas, muestra mensaje
        if (maquinas.length === 0) {
            contenedor.innerHTML = "<p style='text-align:center; padding:20px;'>No hay equipos registrados.</p>";
            return;
        }

        // crea una tarjeta por cada máquina
        for (const m of maquinas) {
            const claseEstado = obtenerClaseEstado(m.estado);

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
                    </div>
                </div>
            `;
            contenedor.insertAdjacentHTML("beforeend", tarjetaHTML);
        }
    } catch (error) {
        console.error("Error al cargar máquinas:", error);
    }
}

// redirige a la página de historial pasando el código de la máquina
function verHistorial(codigo) {
    window.location.href = `/home/maquinas/historial?codigo=${encodeURIComponent(codigo)}`;
}

// redirige al formulario de mantenimiento con el código pre-cargado
function irAMantenimiento(codigo) {
    window.location.href = `/home/maquinas/formulario/mantenimiento?codigo=${encodeURIComponent(codigo)}`;
}

// filtra las tarjetas según lo que el usuario escribe en el buscador
function filtrarMaquinas() {
    const input = document.getElementById("input-busqueda");
    if (!input) return;

    const filtro = input.value.toLowerCase().trim();
    const tarjetas = document.querySelectorAll(".detail-container");

    tarjetas.forEach(tarjeta => {
        const textoTarjeta = tarjeta.innerText.toLowerCase();

        // si el buscador está vacío, muestra todas las tarjetas
        if (filtro === "") {
            tarjeta.style.display = "flex";
            return;
        }

        // muestra u oculta según si el texto coincide
        if (textoTarjeta.includes(filtro)) {
            tarjeta.style.display = "flex";
        } else {
            tarjeta.style.display = "none";
        }
    });
}
