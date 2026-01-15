document.addEventListener("DOMContentLoaded", async () => {
    const codigoMaquina = localStorage.getItem("maquinaSeleccionada");
    const titulo = document.querySelector("#subtitulo-maquina span");
    const cuerpoTabla = document.getElementById("tabla-cuerpo-historial");

    if (codigoMaquina) {
        titulo.textContent = codigoMaquina;
        try {
            const response = await fetch(`/home/mantenimiento/listar/${codigoMaquina}`);
            const mantenimientos = await response.json();

            if (mantenimientos.length === 0) {
                cuerpoTabla.innerHTML = "<tr><td colspan='5' style='text-align:center;'>No hay registros para este equipo.</td></tr>";
            } else {
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
        } catch (error) {
            console.error("Error al cargar historial:", error);
        }
    }

    // Botón Regresar
    document.getElementById("btn-volver-historial").addEventListener("click", () => {
        window.location.href = "/home/maquinas";
    });
});