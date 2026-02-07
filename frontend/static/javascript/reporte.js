// Maneja generación de reportes de mantenimiento con búsqueda por código y polling en tiempo real
document.addEventListener("DOMContentLoaded", () => {
    const btnBuscar = document.getElementById("btn-buscar");
    const inputCodigo = document.getElementById("input-codigo");
    const tablaBody = document.getElementById("tabla-reporte");

    // Configuración de polling para reportes
    const TIEMPO_POLLING_MS = 2000;
    let pollingInterval = null;
    let ultimoCodigoBuscado = "";

    // Decide color del badge según tipo de mantenimiento
    const obtenerClaseBadgeTipo = (tipo) => {
        if (!tipo) return "badge";
        const t = tipo.toLowerCase();
        if (t.includes("preventivo")) return "badge badge-prev";
        if (t.includes("correctivo")) return "badge badge-corr";
        return "badge";
    };

    // Decide color del badge según estado de máquina
    const obtenerClaseBadgeEstado = (estado) => {
        if (!estado) return "badge";
        const e = estado.toLowerCase();

        if (e.includes("mantenimiento") || e.includes("revisión") || e.includes("fuera de servicio")) return "badge badge-maint";
        if (e.includes("operativa") || e.includes("bueno")) return "badge badge-ok";
        if (e.includes("baja") || e.includes("dañado") || e.includes("mal")) return "badge badge-baja";

        return "badge badge-maint";
    };

    // FUNCIÓN: Iniciar polling para reportes
    function iniciarPollingReportes(codigo = "") {
        // Detener polling anterior si existe
        if (pollingInterval) {
            clearInterval(pollingInterval);
        }
        
        // Guardar el código actual para comparar
        ultimoCodigoBuscado = codigo;
        
        // Iniciar nuevo polling
        pollingInterval = setInterval(() => {
            cargarDatos(codigo, true); // true = es polling
        }, TIEMPO_POLLING_MS);
        
        console.log(`Polling de reportes iniciado para código: "${codigo || 'todos'}"`);
    }

    // FUNCIÓN: Detener polling
    function detenerPolling() {
        if (pollingInterval) {
            clearInterval(pollingInterval);
            pollingInterval = null;
            console.log("Polling de reportes detenido");
        }
    }

    // pide los datos de reportes al backend (con o sin filtro de código)
    const cargarDatos = async (codigo = "", esPolling = false) => {
        try {
            // Solo mostrar "Cargando..." si no es polling
            if (!esPolling) {
                tablaBody.innerHTML = `<tr><td colspan="8" style="text-align:center;">Cargando...</td></tr>`;
            }

            const timestamp = new Date().getTime();
            // si hay código, lo envía como parámetro
            const url = codigo ?
                `/api/mantenimiento/informe-general?codigo=${encodeURIComponent(codigo.trim())}&_t=${timestamp}` :
                `/api/mantenimiento/informe-general?_t=${timestamp}`;

            const response = await fetch(url, {
                headers: { 'Cache-Control': 'no-cache, no-store, must-revalidate' }
            });

            if (!response.ok) {
                throw new Error("Error al obtener los datos de reportes");
            }

            const data = await response.json();

            if (!Array.isArray(data)) {
                throw new Error("Formato de datos incorrecto");
            }

            tablaBody.innerHTML = "";

            // si no se encontró nada, muestra mensaje personalizado
            if (data.length === 0) {
                tablaBody.innerHTML = `<tr><td colspan="8" style="text-align:center; color: #333; font-weight: bold;">Equipo no encontrado</td></tr>`;
                return;
            }

            let HTML_CONTENT = "";

            // recorre cada máquina y sus mantenimientos
            data.forEach(inf => {
                // si la máquina no tiene mantenimientos, muestra una fila básica
                if (!inf.mantenimientos || inf.mantenimientos.length === 0) {
                    HTML_CONTENT += `
                        <tr>
                            <td class="fw-bold">${inf.codigo || "N/A"}</td>
                            <td>${inf.area || "N/A"}</td>
                            <td>-</td>
                            <td>-</td>
                            <td>-</td>
                            <td><span class="${obtenerClaseBadgeEstado(inf.estado)}">${inf.estado || "N/A"}</span></td>
                            <td colspan="1" style="text-align:center; color:#999;">Sin mantenimientos</td>
                            <td><button class="btn-icon"><i class="fa-solid fa-eye"></i></button></td>
                        </tr>`;
                } else {
                    // si tiene mantenimientos, crea una fila por cada uno
                    inf.mantenimientos.forEach(m => {
                        const tipoTexto = m.tipo ? m.tipo.charAt(0).toUpperCase() + m.tipo.slice(1) : "N/A";

                        HTML_CONTENT += `
                            <tr>
                                <td class="fw-bold">${inf.codigo}</td>
                                <td>${inf.area}</td>
                                <td>${m.tecnico || "N/A"}</td>
                                <td>${m.fecha || "N/A"}</td>
                                <td><span class="${obtenerClaseBadgeTipo(m.tipo)}">${tipoTexto}</span></td>
                                <td><span class="${obtenerClaseBadgeEstado(inf.estado)}">${inf.estado}</span></td>
                                <td class="desc-cell">${m.observaciones || "Sin observaciones"}</td>
                                <td><button class="btn-icon" title="Ver detalle"><i class="fa-solid fa-eye"></i></button></td>
                            </tr>`;
                    });
                }
            });

            tablaBody.innerHTML = HTML_CONTENT;
        } catch (error) {
            console.error("Error al cargar datos:", error);
            tablaBody.innerHTML = `<tr><td colspan="8" style="text-align:center; color:red;">Error al cargar reportes.</td></tr>`;
        }
    };

    // maneja las teclas en el campo de búsqueda
    if (inputCodigo) {
        inputCodigo.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                const codigo = inputCodigo.value.trim();
                cargarDatos(codigo);
                iniciarPollingReportes(codigo); // Iniciar polling después de buscar
            } else if (e.key === "Escape") {
                e.preventDefault();
                inputCodigo.value = "";
                cargarDatos("");
                iniciarPollingReportes(""); // Iniciar polling para todos
            }
        });

        // si el usuario borra todo el texto, recarga la lista completa
        inputCodigo.addEventListener("input", () => {
            if (inputCodigo.value.trim() === "") {
                cargarDatos("");
                iniciarPollingReportes(""); // Iniciar polling para todos
            }
        });
    }

    // botón de buscar: filtra por código
    if (btnBuscar) {
        btnBuscar.addEventListener("click", (e) => {
            e.preventDefault();
            const codigo = inputCodigo ? inputCodigo.value.trim() : "";
            cargarDatos(codigo);
            iniciarPollingReportes(codigo); // Iniciar polling después de buscar
        });
    }

    // botón de regresar: vuelve a la lista de máquinas
    const btnReturn = document.getElementById("btn-return");
    if (btnReturn) {
        btnReturn.addEventListener("click", () => {
            detenerPolling(); // Detener polling al salir
            window.location.href = "/pagina/maquinas";
        });
    }

    // carga todos los datos al iniciar la página y empieza polling
    cargarDatos("").then(() => {
        iniciarPollingReportes(""); // Iniciar polling para todos los reportes
    });
});