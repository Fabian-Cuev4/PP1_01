// Maneja la visualización del historial de mantenimientos
document.addEventListener("DOMContentLoaded", async () => {
    const btnVolver = document.getElementById("btn-volver-historial");
    if (btnVolver) {
        btnVolver.addEventListener("click", () => {
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

    // Cargar historial
    try {
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

    } catch (error) {
        if (tablaBody) {
            tablaBody.innerHTML = `<tr><td colspan="5" style="text-align:center; color:red;">Error al cargar el historial.</td></tr>`;
        }
    }
});