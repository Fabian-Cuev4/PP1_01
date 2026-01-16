document.addEventListener("DOMContentLoaded", () => {
    const btnCancelar = document.getElementById("btn-cancel-action");
    const formMaquina = document.querySelector(".form");
    const btnGuardarMant = document.querySelector(".btn-save");

    // 1. Lógica para Cancelar (Volver a la lista)
    if (btnCancelar) {
        btnCancelar.addEventListener("click", () => {
            window.location.href = "/home/maquinas";
        });
    }

    // 2. Lógica para GUARDAR MÁQUINA (Aquí estaba el error 422)
    if (formMaquina) {
        formMaquina.addEventListener("submit", async (e) => {
            e.preventDefault();

            // CAPTURA COMPLETA: Estos nombres deben ser IGUALES a tu MaquinaSchema en Python
            const datos = {
                tipo_equipo: document.getElementById("tipo_equipo").value,
                codigo_equipo: document.getElementById("codigo").value,
                estado_actual: document.getElementById("estado_actual").value,
                area: document.getElementById("area").value,
                fecha: document.getElementById("fecha").value
            };

            try {
                const response = await fetch("/home/maquinas/agregar", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(datos)
                });

                const resultado = await response.json();

                if (response.ok) {
                    alert("¡Éxito!: " + resultado.mensaje);
                    window.location.href = "/home/maquinas";
                } else {
                    console.error("Detalle del error 422:", resultado.detail);
                    alert("Error de validación: Revisa que todos los campos estén llenos.");
                }
            } catch (error) {
                console.error("Error en la petición:", error);
                alert("Error al conectar con el servidor.");
            }
        });
    }

    // 3. Lógica para GUARDAR MANTENIMIENTO
    // Solo ejecutar si estamos en la página de mantenimiento (tiene campos mant-*)
    const esFormularioMantenimiento = document.getElementById("mant-empresa") !== null;
    
    if (btnGuardarMant && esFormularioMantenimiento) {
        btnGuardarMant.addEventListener("click", async () => {
            // Obtener el código de la máquina desde los parámetros de la URL
            const urlParams = new URLSearchParams(window.location.search);
            const codigoVinculado = urlParams.get("codigo");

            if (!codigoVinculado) {
                alert("Error: No se ha seleccionado una máquina.");
                return;
            }

            // Aquí mandamos lo que el MantenimientoSchema necesita
            const datosMant = {
                codigo_maquina: codigoVinculado,
                empresa: document.getElementById("mant-empresa").value,
                tecnico: document.getElementById("mant-tecnico").value,
                tipo: document.getElementById("mant-tipo").value,
                fecha: document.getElementById("mant-fecha").value,
                observaciones: document.getElementById("mant-observaciones").value
            };

            try {
                const response = await fetch("/home/mantenimiento/agregar", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(datosMant)
                });

                const resultado = await response.json();

                if (response.ok) {
                    alert("Mantenimiento guardado para: " + codigoVinculado);
                    window.location.href = "/home/maquinas";
                } else {
                    alert("Error al registrar mantenimiento: " + (resultado.detail || "Error desconocido"));
                }
            } catch (error) {
                console.error("Error:", error);
            }
        });
    }
});