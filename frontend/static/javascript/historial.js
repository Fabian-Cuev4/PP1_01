// Maneja visualización de historial de mantenimientos con polling en tiempo real
document.addEventListener("DOMContentLoaded", async () => {
    const btnVolver = document.getElementById("btn-volver-historial");
    if (btnVolver) {
        btnVolver.addEventListener("click", () => {
            detenerPolling();
            window.location.href = "/pagina/maquinas";
        });
    }

    const params = new URLSearchParams(window.location.search);
    const codigo = params.get("codigo");

    // Actualizar subtítulo
    const subtitulo = document.getElementById("subtitulo-maquina");
    if (subtitulo && codigo) {
        subtitulo.querySelector("span").textContent = codigo;
    }

    const tablaBody = document.getElementById("tabla-cuerpo-historial");

    if (!codigo) {
        if (tablaBody) {
            tablaBody.innerHTML = `<tr><td colspan="5" style="text-align:center; color:red;">No se especificó un código de máquina.</td></tr>`;
        }
        return;
    }

    // Configuración de polling para historial
    const TIEMPO_POLLING_MS = 2000;
    let pollingInterval = null;

    // Iniciar polling para historial
    function iniciarPollingHistorial() {
        if (pollingInterval) {
            clearInterval(pollingInterval);
        }
        
        pollingInterval = setInterval(() => {
            cargarHistorial(true);
            console.log(`🔄 Polling de historial activado para máquina: ${codigo} - ${new Date().toLocaleTimeString()}`);
        }, TIEMPO_POLLING_MS);
        
        console.log(`✅ Polling de historial iniciado para máquina: ${codigo}`);
    }

    // Detener polling
    function detenerPolling() {
        if (pollingInterval) {
            clearInterval(pollingInterval);
            pollingInterval = null;
            console.log("Polling de historial detenido");
        }
    }

    // FUNCIÓN: Actualizar el scroll dinámicamente según el contenido
    function actualizarScroll() {
        const tablaBody = document.getElementById("tabla-cuerpo-historial");
        if (!tablaBody) return;
        
        const scrollHeight = tablaBody.scrollHeight;
        const clientHeight = tablaBody.clientHeight;
        
        // Si el contenido es más alto que el contenedor, activar scroll
        if (scrollHeight > clientHeight) {
            console.log("📜 Activando scroll del historial - Contenido requiere scroll");
            tablaBody.style.overflowY = "auto";
        } else {
            console.log("📜 Desactivando scroll del historial - Contenido cabe en el contenedor");
            tablaBody.style.overflowY = "hidden";
        }
    }

    // FUNCIÓN: Cargar historial
    async function cargarHistorial(esPolling = false) {
        try {
            // Solo mostrar "Cargando..." si no es polling
            if (!esPolling) {
                tablaBody.innerHTML = `<tr><td colspan="5" style="text-align:center;">Cargando...</td></tr>`;
            }

            const timestamp = new Date().getTime();
            const response = await fetch(`/api/mantenimiento/listar/${encodeURIComponent(codigo)}?_t=${timestamp}`, {
                headers: { 'Cache-Control': 'no-cache' }
            });

            if (!response.ok) {
                throw new Error("Error al obtener el historial");
            }

            const data = await response.json();

            if (!Array.isArray(data) || data.length === 0) {
                tablaBody.innerHTML = `<tr><td colspan="5" style="text-align:center;">No hay mantenimientos registrados para este equipo.</td></tr>`;
                return;
            }

            tablaBody.innerHTML = "";
            data.forEach(m => {
                const tipoTexto = m.tipo ? m.tipo.charAt(0).toUpperCase() + m.tipo.slice(1) : "N/A";
                const fila = `
                    <tr>
                        <td>${m.fecha || "N/A"}</td>
                        <td>${tipoTexto}</td>
                        <td>${m.tecnico || "N/A"}</td>
                        <td>${m.empresa || "N/A"}</td>
                        <td>${m.observaciones || "Sin observaciones"}</td>
                    </tr>
                `;
                tablaBody.insertAdjacentHTML("beforeend", fila);
            });
            
            // Actualizar el scroll dinámicamente según el contenido
            actualizarScroll();

        } catch (error) {
            if (tablaBody) {
                tablaBody.innerHTML = `<tr><td colspan="5" style="text-align:center; color:red;">Error al cargar el historial.</td></tr>`;
            }
        }
    }

    // Cargar historial inicial y empezar polling
    await cargarHistorial();
    iniciarPollingHistorial();
});