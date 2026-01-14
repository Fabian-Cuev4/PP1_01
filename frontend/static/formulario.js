document.addEventListener("DOMContentLoaded", () => {
    const btnCancelar = document.getElementById("btn-cancel-action");
    const formMaquina = document.querySelector(".form");

    // Lógica para Cancelar
    if (btnCancelar) {
        btnCancelar.addEventListener("click", () => {
            window.location.href = "/home/maquinas";
        });
    }

    // Lógica para Guardar (Enviar al Backend)
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
                    alert("✅ Máquina guardada: " + resultado.mensaje);
                    window.location.href = "/home/maquinas"; // Redirige a la lista
                } else {
                    alert("❌ Error: " + (resultado.detail || "No se pudo guardar"));
                }
            } catch (error) {
                console.error("Error en la petición:", error);
                alert("Hubo un error al conectar con el servidor.");
            }
        });
    }
});