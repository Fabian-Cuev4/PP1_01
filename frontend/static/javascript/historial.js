// maneja la visualización del historial de mantenimientos de una máquina específica
document.addEventListener("DOMContentLoaded", async () => {
    // obtiene el código de la máquina desde la URL
    const params = new URLSearchParams(window.location.search);
    const codigo = params.get("codigo");

    // actualiza el subtítulo con el código de la máquina
    const subtitulo = document.getElementById("subtitulo-maquina");
    if (subtitulo && codigo) {
        subtitulo.querySelector("span").textContent = codigo;
    }

    // captura el cuerpo de la tabla donde se mostrarán los datos
    const tablaBody = document.getElementById("tabla-cuerpo-historial");

    // si no hay código, muestra mensaje de error
    if (!codigo) {
        if (tablaBody) {
            tablaBody.innerHTML = `<tr><td colspan="5" style="text-align:center; color:red;">No se especificó un código de máquina.</td></tr>`;
        }
        return;
    }

    try {
        // pide al backend el historial de mantenimientos de esta máquina
        const timestamp = new Date().getTime();
        const response = await fetch(`/home/mantenimiento/listar/${encodeURIComponent(codigo)}?_t=${timestamp}`, {
            headers: { 'Cache-Control': 'no-cache' }
        });

        if (!response.ok) {
            throw new Error("Error al obtener el historial");
        }

        const data = await response.json();

        // si no hay datos, muestra mensaje
        if (!Array.isArray(data) || data.length === 0) {
            tablaBody.innerHTML = `<tr><td colspan="5" style="text-align:center;">No hay mantenimientos registrados para este equipo.</td></tr>`;
            return;
        }

        // limpia la tabla y construye las filas con los datos
        tablaBody.innerHTML = "";
        data.forEach(m => {
            // capitaliza la primera letra del tipo de mantenimiento
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

    } catch (error) {
        console.error("Error al cargar historial:", error);
        tablaBody.innerHTML = `<tr><td colspan="5" style="text-align:center; color:red;">Error al cargar el historial.</td></tr>`;
    }

    // botón de regresar: vuelve a la lista de máquinas
    const btnVolver = document.getElementById("btn-volver-historial");
    if (btnVolver) {
        btnVolver.addEventListener("click", () => {
            window.location.href = "/home/maquinas";
        });
    }
});