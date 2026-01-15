document.addEventListener("DOMContentLoaded", () => {
    const btnCancelar = document.getElementById("btn-cancel-action");
    const formMaquina = document.querySelector(".form");
    // Detectamos el botón de guardar del formulario de mantenimiento
    const btnGuardarMant = document.querySelector(".btn-save");

    // Lógica para Cancelar
    if (btnCancelar) {
        btnCancelar.addEventListener("click", () => {
            window.location.href = "/home/maquinas";
        });
    }

    // Lógica para guardar una maquina (Enviar al Backend)
    if (formMaquina) {
        formMaquina.addEventListener("submit", async (e) => {
            e.preventDefault(); // Evita que la página se recargue

            // Capturamos los datos del formulario
            const datos = {
                codigo_equipo: document.getElementById("codigo").value,
                // Capturamos el select (asegúrate que el <select> tenga id="estado_actual")
                estado_actual: document.getElementById("estado_actual") ? document.getElementById("estado_actual").value : "operativa",
                area: document.getElementById("area").value,
                fecha: document.getElementById("fecha").value
            };

            try {
                const response = await fetch("/home/maquinas/agregar", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(datos)
                });

                const resultado = await response.json();

                if (response.ok) {
                    alert("Máquina guardada: " + resultado.mensaje);
                    window.location.href = "/home/maquinas"; // Redirige a la lista
                } else {
                    alert("Error: " + (resultado.detail || "No se pudo guardar"));
                }
            } catch (error) {
                console.error("Error en la petición:", error);
                alert("Hubo un error al conectar con el servidor.");
            }
        });
    }

    // Lógica para guardar mantenimiento (Enviar al Backend)
    if (btnGuardarMant) {
        btnGuardarMant.addEventListener("click", async () => {
            // Recuperamos el codigo de maquina vinculado desde el localStorage
            const codigoVinculado = localStorage.getItem("maquinaSeleccionada");

            if (!codigoVinculado) {
                alert("Error: No se ha seleccionado una máquina para el mantenimiento.");
                return;
            }

            // Capturamos los datos del mantenimiento (asegúrate que los IDs coincidan con tu HTML)
            const datosMant = {
                codigo_maquina: codigoVinculado,
                empresa: document.getElementById("mant-empresa").value,
                tecnico: document.getElementById("mant-tecnico").value,
                tipo: document.getElementById("mant-tipo").value,
                fecha: document.getElementById("mant-fecha").value,
                observaciones: document.getElementById("mant-observaciones").value
            };

            try {
                // Ajustamos la ruta para que coincida con el APIRouter prefix="/home/mantenimiento"
                const response = await fetch("/home/mantenimiento/agregar", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(datosMant)
                });

                const resultado = await response.json();

                if (response.ok) {
                    alert("Mantenimiento guardado con éxito para la máquina: " + codigoVinculado);
                    window.location.href = "/home/maquinas"; // Redirige a la lista para ver cambios
                } else {
                    alert("Error: " + (resultado.detail || "No se pudo registrar el mantenimiento"));
                }
            } catch (error) {
                console.error("Error en la petición de mantenimiento:", error);
                alert("Hubo un error al conectar con el servidor.");
            }
        });
    }
});