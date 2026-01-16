// maneja la lógica de los formularios de agregar máquina y agregar mantenimiento
document.addEventListener("DOMContentLoaded", () => {

    // crea el modal de avisos dinámicamente e inserta el HTML en la página
    const modalHTML = `
    <div id="validationModal" class="validation-modal-overlay">
        <div class="validation-card">
            <div id="modalIcon" class="modal-icon"></div>
            <h3 id="modalTitle" class="modal-title"></h3>
            <p id="modalMessage" class="modal-message"></p>
            <button id="btnModalOk" class="btn-modal-ok">Entendido</button>
        </div>
    </div>`;
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    // captura los elementos del modal para poder manipularlos
    const validationModal = document.getElementById("validationModal");
    const modalIcon = document.getElementById("modalIcon");
    const modalTitle = document.getElementById("modalTitle");
    const modalMessage = document.getElementById("modalMessage");
    const btnModalOk = document.getElementById("btnModalOk");

    // muestra el modal con el tipo (success/error/warning), título y mensaje
    const mostrarModal = (tipo, titulo, mensaje, callback = null) => {
        let iconHtml = '';
        if (tipo === 'success') iconHtml = '<i class="fa-solid fa-circle-check icon-success"></i>';
        else if (tipo === 'error') iconHtml = '<i class="fa-solid fa-circle-xmark icon-error"></i>';
        else if (tipo === 'warning') iconHtml = '<i class="fa-solid fa-triangle-exclamation icon-warning"></i>';

        modalIcon.innerHTML = iconHtml;
        modalTitle.textContent = titulo;
        modalMessage.textContent = mensaje;
        validationModal.classList.add("active");

        // cierra el modal al hacer clic en "entendido" y ejecuta callback si existe
        btnModalOk.onclick = () => {
            validationModal.classList.remove("active");
            if (callback) callback();
        };
    };

    // captura los botones y formularios de la página
    const btnCancelar = document.getElementById("btn-cancel-action");
    const formMaquina = document.querySelector(".form");
    const btnGuardarMant = document.querySelector(".btn-save");

    // botón cancelar: regresa a la lista de máquinas
    if (btnCancelar) {
        btnCancelar.addEventListener("click", () => {
            window.location.href = "/home/maquinas";
        });
    }

    // formulario de agregar máquina
    if (formMaquina) {
        formMaquina.addEventListener("submit", async (e) => {
            e.preventDefault(); // evita que la página se recargue

            // recopila los datos del formulario
            const datos = {
                tipo_equipo: document.getElementById("tipo_equipo").value,
                codigo_equipo: document.getElementById("codigo").value,
                estado_actual: document.getElementById("estado_actual").value,
                area: document.getElementById("area").value,
                fecha: document.getElementById("fecha").value
            };

            // valida que los campos obligatorios estén llenos
            if (!datos.tipo_equipo || !datos.codigo_equipo || !datos.estado_actual) {
                mostrarModal('warning', 'Campos Incompletos', 'Por favor, completa todos los campos obligatorios.');
                return;
            }

            try {
                // envía los datos al backend
                const response = await fetch("/home/maquinas/agregar", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(datos)
                });

                const resultado = await response.json();

                // si el servidor responde ok, muestra éxito y redirige
                if (response.ok) {
                    mostrarModal('success', '¡Registro Exitoso!', 'La máquina ha sido registrada correctamente.', () => {
                        window.location.href = "/home/maquinas?_refresh=" + new Date().getTime();
                    });
                } else {
                    // si hay error, muestra el mensaje
                    let msg = "No se pudo guardar la máquina.";
                    if (JSON.stringify(resultado).toLowerCase().includes("ya existe")) {
                        msg = `El código "${datos.codigo_equipo}" ya está en uso.`;
                    }
                    mostrarModal('error', 'Error al Guardar', msg);
                }
            } catch (error) {
                mostrarModal('error', 'Error de Conexión', 'No se pudo contactar con el servidor.');
            }
        });
    }

    // detecta si estamos en el formulario de mantenimiento
    const esFormularioMantenimiento = document.getElementById("mant-empresa") !== null;

    // formulario de agregar mantenimiento
    if (btnGuardarMant && esFormularioMantenimiento) {
        btnGuardarMant.addEventListener("click", async (e) => {
            e.preventDefault();

            // obtiene el código de la máquina desde la URL
            const urlParams = new URLSearchParams(window.location.search);
            const codigoVinculado = urlParams.get("codigo");

            if (!codigoVinculado) {
                mostrarModal('error', 'Error', 'No se ha seleccionado una máquina válida.');
                return;
            }

            // recopila los datos del mantenimiento
            const datosMant = {
                codigo_maquina: codigoVinculado,
                empresa: document.getElementById("mant-empresa").value,
                tecnico: document.getElementById("mant-tecnico").value,
                tipo: document.getElementById("mant-tipo").value,
                fecha: document.getElementById("mant-fecha").value,
                observaciones: document.getElementById("mant-observaciones").value
            };

            // valida campos obligatorios
            if (!datosMant.tecnico || !datosMant.fecha || !datosMant.tipo) {
                mostrarModal('warning', 'Faltan Datos', 'El técnico, la fecha y el tipo de mantenimiento son obligatorios.');
                return;
            }

            try {
                // envía el mantenimiento al backend
                const response = await fetch("/home/mantenimiento/agregar", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(datosMant)
                });

                // si se guardó correctamente, muestra éxito y redirige
                if (response.ok) {
                    mostrarModal('success', 'Mantenimiento Guardado', `Se registró el mantenimiento para ${codigoVinculado}.`, () => {
                        window.location.href = "/home/maquinas?_refresh=" + new Date().getTime();
                    });
                } else {
                    mostrarModal('error', 'Error', "No se pudo registrar el mantenimiento.");
                }
            } catch (error) {
                mostrarModal('error', 'Error Crítico', 'Falló la conexión con el servidor.');
            }
        });
    }
});