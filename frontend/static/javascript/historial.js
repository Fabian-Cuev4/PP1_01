document.addEventListener("DOMContentLoaded", async () => {
    // Obtener el código de la máquina desde los parámetros de la URL
    const urlParams = new URLSearchParams(window.location.search);
    const codigoMaquina = urlParams.get("codigo");
    const titulo = document.querySelector("#subtitulo-maquina span");
    const cuerpoTabla = document.getElementById("tabla-cuerpo-historial");

    if (codigoMaquina) {
        if (titulo) titulo.textContent = codigoMaquina;
        try {
            const response = await fetch(`/home/mantenimiento/listar/${codigoMaquina}`);
            const mantenimientos = await response.json();

            if (mantenimientos.length === 0) {
                if (cuerpoTabla) cuerpoTabla.innerHTML = "<tr><td colspan='5' style='text-align:center;'>No hay registros para este equipo.</td></tr>";
            } else {
                if (cuerpoTabla) {
                    cuerpoTabla.innerHTML = ""; // Limpiar antes de agregar
                    mantenimientos.forEach(m => {
                        const fila = `
                            <tr>
                                <td>${m.fecha}</td>
                                <td>${m.tipo}</td>
                                <td>${m.tecnico}</td>
                                <td>${m.empresa}</td>
                                <td>${m.observaciones}</td>
                            </tr>
                        `;
                        cuerpoTabla.innerHTML += fila;
                    });
                }
            }
        } catch (error) {
            console.error("Error al cargar historial:", error);
            if (cuerpoTabla) cuerpoTabla.innerHTML = "<tr><td colspan='5' style='text-align:center; color: red;'>Error al cargar el historial.</td></tr>";
        }
    } else {
        // Si no hay código, mostrar mensaje y redirigir
        if (titulo) titulo.textContent = "Máquina no especificada";
        if (cuerpoTabla) cuerpoTabla.innerHTML = "<tr><td colspan='5' style='text-align:center; color: red;'>Error: No se ha especificado una máquina. Redirigiendo...</td></tr>";
        setTimeout(() => {
            window.location.href = "/home/maquinas";
        }, 2000);
    }

    // Botón Regresar
    const btnVolver = document.getElementById("btn-volver-historial");
    if (btnVolver) {
        btnVolver.addEventListener("click", () => {
            window.location.href = "/home/maquinas";
        });
    }
});