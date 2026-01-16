document.addEventListener("DOMContentLoaded", () => {
    const btnBuscar = document.getElementById("btn-buscar");
    const inputCodigo = document.getElementById("input-codigo");
    const tablaBody = document.getElementById("tabla-reporte");

    // Función para obtener clase CSS del badge según tipo de mantenimiento
    const obtenerClaseBadgeTipo = (tipo) => {
        if (!tipo) return "badge";
        const t = tipo.toLowerCase();
        if (t.includes("preventivo")) return "badge badge-prev";
        if (t.includes("correctivo")) return "badge badge-corr";
        return "badge";
    };

    // Función para obtener clase CSS del badge según estado de máquina
    const obtenerClaseBadgeEstado = (estado) => {
        if (!estado) return "badge";
        const e = estado.toLowerCase();
        if (e.includes("operativa")) return "badge badge-ok";
        if (e.includes("mantenimiento")) return "badge badge-maint";
        if (e.includes("baja")) return "badge badge-baja";
        return "badge";
    };

    const cargarDatos = async (codigo = "") => {
        try {
            // Limpiar tabla y mostrar loading
            tablaBody.innerHTML = `<tr><td colspan="8" style="text-align:center;">Cargando...</td></tr>`;

            // Construir URL con parámetro codigo si existe
            const url = codigo ? 
                `/home/mantenimiento/informe-general?codigo=${encodeURIComponent(codigo.trim())}` : 
                `/home/mantenimiento/informe-general`;
            
            const response = await fetch(url);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || "Error al obtener los datos");
            }
            
            const data = await response.json();
            
            // Validar que data sea un array
            if (!Array.isArray(data)) {
                throw new Error("Formato de datos incorrecto");
            }

            // Limpiar tabla
            tablaBody.innerHTML = "";

            // Si no hay datos
            if (data.length === 0) {
                tablaBody.innerHTML = `
                    <tr>
                        <td colspan="8" style="text-align:center; color:#666;">
                            ${codigo ? `No se encontraron datos para la máquina "${codigo}"` : "No hay máquinas registradas"}
                        </td>
                    </tr>`;
                return;
            }

            // Procesar cada informe del DTO
            data.forEach(inf => {
                // Validar que el informe tenga la estructura correcta del DTO
                if (!inf.codigo || !inf.area || inf.mantenimientos === undefined) {
                    console.warn("Informe con estructura incorrecta:", inf);
                    return;
                }

                // Si la máquina no tiene mantenimientos
                if (!inf.mantenimientos || inf.mantenimientos.length === 0) {
                    tablaBody.innerHTML += `
                        <tr>
                            <td class="fw-bold">${inf.codigo || "N/A"}</td>
                            <td>${inf.area || "N/A"}</td>
                            <td>-</td>
                            <td>-</td>
                            <td>-</td>
                            <td><span class="${obtenerClaseBadgeEstado(inf.estado)}">${inf.estado || "N/A"}</span></td>
                            <td colspan="1" style="text-align:center; color:#999;">Sin mantenimientos registrados</td>
                            <td>
                                <button class="btn-icon" title="Ver detalles"><i class="fa-solid fa-eye"></i></button>
                            </td>
                        </tr>`;
                } else {
                    // Si tiene mantenimientos, mostrar cada uno
                    inf.mantenimientos.forEach(m => {
                        // Validar que el mantenimiento tenga los campos necesarios
                        const tecnico = m.tecnico || "N/A";
                        const fecha = m.fecha || "N/A";
                        const tipo = m.tipo || "N/A";
                        const observaciones = m.observaciones || "Sin observaciones";

                        tablaBody.innerHTML += `
                            <tr>
                                <td class="fw-bold">${inf.codigo}</td>
                                <td>${inf.area}</td>
                                <td>${tecnico}</td>
                                <td>${fecha}</td>
                                <td><span class="${obtenerClaseBadgeTipo(tipo)}">${tipo}</span></td>
                                <td><span class="${obtenerClaseBadgeEstado(inf.estado)}">${inf.estado}</span></td>
                                <td>${observaciones}</td>
                                <td>
                                    <button class="btn-icon" title="Ver detalles"><i class="fa-solid fa-eye"></i></button>
                                </td>
                            </tr>`;
                    });
                }
            });
        } catch (error) {
            console.error("Error al cargar datos:", error);
            tablaBody.innerHTML = `
                <tr>
                    <td colspan="8" style="text-align:center; color:red; padding:20px;">
                        <i class="fa-solid fa-exclamation-triangle"></i> ${error.message || "Error al cargar los datos"}
                    </td>
                </tr>`;
        }
    };

    // Event listener para el botón buscar
    if (btnBuscar) {
        btnBuscar.addEventListener("click", (e) => {
            e.preventDefault();
            const codigo = inputCodigo ? inputCodigo.value.trim() : "";
            cargarDatos(codigo);
        });
    }

    // Permitir búsqueda con Enter
    if (inputCodigo) {
        inputCodigo.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                if (btnBuscar) btnBuscar.click();
            }
        });

        // Recargar todos los datos cuando se borre el texto
        inputCodigo.addEventListener("input", (e) => {
            const valor = e.target.value.trim();
            if (valor === "") {
                // Si el campo está vacío, mostrar todos los resultados
                cargarDatos();
            }
        });
    }

    // Botón regresar
    const btnReturn = document.getElementById("btn-return");
    if (btnReturn) {
        btnReturn.addEventListener("click", () => {
            window.location.href = "/home/maquinas";
        });
    }

    // Cargar todos los datos al inicio
    cargarDatos();
});