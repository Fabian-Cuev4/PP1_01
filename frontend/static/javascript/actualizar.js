// Este archivo maneja la actualización de máquinas
// Solo permite cambiar el estado, el resto de campos están bloqueados

document.addEventListener("DOMContentLoaded", async () => {
    // Manejador del botón cancelar
    const btnCancelar = document.getElementById("btn-cancel-action");
    if (btnCancelar) {
        btnCancelar.addEventListener("click", () => {
            window.location.href = "http://localhost:18080/pagina/maquinas";
        });
    }

    // Obtener el código de la máquina desde la URL
    const urlParams = new URLSearchParams(window.location.search);
    const codigo = urlParams.get("codigo");

    if (!codigo) {
        // Si no hay código, volver a la lista
        window.location.href = "http://localhost:18080/pagina/maquinas";
        return;
    }

    // Buscar la máquina en el servidor
    try {
        const response = await fetch("/api/maquinas/listar");
        const maquinas = await response.json();
        const maquina = maquinas.find(m => m.codigo.toLowerCase() === codigo.toLowerCase());

        if (!maquina) {
            // Si no se encuentra, mostrar error y volver
            alert("No se encontró la máquina.");
            window.location.href = "http://localhost:18080/pagina/maquinas";
            return;
        }

        // Llenar el formulario con los datos de la máquina
        document.getElementById("tipo_equipo").value = maquina.tipo === "Computadora" ? "PC" : "IMP";
        document.getElementById("codigo").value = maquina.codigo;
        document.getElementById("estado_actual").value = maquina.estado;
        document.getElementById("area").value = maquina.area;
        document.getElementById("fecha").value = maquina.fecha;

        // Configurar el formulario para enviar la actualización
        const form = document.getElementById("form-actualizar");
        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            // Crear el modal si no existe (por si formulario.js no se cargó)
            if (!document.getElementById("validationModal")) {
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
            }

            const validationModal = document.getElementById("validationModal");
            const modalIcon = document.getElementById("modalIcon");
            const modalTitle = document.getElementById("modalTitle");
            const modalMessage = document.getElementById("modalMessage");
            const btnModalOk = document.getElementById("btnModalOk");

            // Función para mostrar el modal
            const mostrarModal = (tipo, titulo, mensaje, callback = null) => {
                let iconHtml = '';
                if (tipo === 'success') iconHtml = '<i class="fa-solid fa-circle-check icon-success"></i>';
                else if (tipo === 'error') iconHtml = '<i class="fa-solid fa-circle-xmark icon-error"></i>';
                else if (tipo === 'warning') iconHtml = '<i class="fa-solid fa-triangle-exclamation icon-warning"></i>';

                modalIcon.innerHTML = iconHtml;
                modalTitle.textContent = titulo;
                modalMessage.textContent = mensaje;
                validationModal.classList.add("active");

                btnModalOk.onclick = () => {
                    validationModal.classList.remove("active");
                    if (callback) callback();
                };
            };

            // Preparar los datos para actualizar
            const username = localStorage.getItem('username') || null;
            const datos = {
                codigo_equipo: maquina.codigo,
                tipo_equipo: maquina.tipo === "Computadora" ? "PC" : "IMP",
                estado_actual: document.getElementById("estado_actual").value,
                area: maquina.area,
                fecha: maquina.fecha,
                usuario: username
            };

            // Validar que se haya seleccionado un estado
            if (!datos.estado_actual) {
                mostrarModal('warning', 'Campo Requerido', 'Por favor, selecciona un estado.');
                return;
            }

            try {
                // Enviar la actualización al servidor
                const response = await fetch("/api/maquinas/actualizar", {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(datos)
                });

                if (response.ok) {
                    mostrarModal('success', '¡Actualización Exitosa!', 'El estado de la máquina ha sido actualizado correctamente.', () => {
                        window.location.href = "http://localhost:18080/pagina/maquinas";
                    });
                } else {
                    const error = await response.json();
                    mostrarModal('error', 'Error al Actualizar', error.detail || "No se pudo actualizar la máquina.");
                }
            } catch (error) {
                mostrarModal('error', 'Error de Conexión', 'No se pudo contactar con el servidor.');
            }
        });
    } catch (error) {
        alert("Error al cargar los datos de la máquina.");
        window.location.href = "http://localhost:18080/pagina/maquinas";
    }
});
