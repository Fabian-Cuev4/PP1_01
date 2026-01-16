// maneja el registro de nuevos usuarios en el sistema
document.addEventListener("DOMContentLoaded", () => {

    // captura los elementos de la página
    const btnRegister = document.getElementById("btn-register");
    const modal = document.getElementById("modal-notificacion");
    const modalMensaje = document.getElementById("modal-mensaje");
    const btnCerrarModal = document.getElementById("btn-modal-cerrar");
    const modalIcon = document.querySelector(".modal-icon i");

    // muestra el modal con un mensaje de éxito o error
    function mostrarModal(mensaje, tipo = "error") {
        modalMensaje.textContent = mensaje;

        if (tipo === "success") {
            modalIcon.className = "fas fa-check-circle";
            modalIcon.parentElement.style.color = "#2ecc71";
        } else {
            modalIcon.className = "fas fa-exclamation-circle";
            modalIcon.parentElement.style.color = "#e74c3c";
        }

        modal.style.display = "flex";
    }

    // cierra el modal al hacer clic en el botón
    if (btnCerrarModal) {
        btnCerrarModal.addEventListener("click", () => {
            modal.style.display = "none";
        });
    }

    // maneja el clic en el botón de registrarse
    if (btnRegister) {
        btnRegister.addEventListener("click", async (e) => {
            e.preventDefault();

            // captura los datos del formulario
            const nombre = document.getElementById("nombre").value;
            const usuario = document.getElementById("usuario").value;
            const password = document.getElementById("password").value;
            const confirm = document.getElementById("confirm-password").value;

            // valida que todos los campos estén llenos
            if (!nombre || !usuario || !password) {
                mostrarModal("Todos los campos son obligatorios.");
                return;
            }

            // valida que las contraseñas coincidan
            if (password !== confirm) {
                mostrarModal("Las contraseñas no coinciden. Por favor, verifica.");
                return;
            }

            // prepara los datos para enviar al backend
            const datosRegistro = {
                nombre_completo: nombre,
                username: usuario,
                password: password
            };

            console.log("Enviando registro...", datosRegistro);

            try {
                // envía la petición de registro al backend
                const response = await fetch('/api/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(datosRegistro)
                });

                // si el registro fue exitoso, muestra mensaje y redirige al login
                if (response.ok) {
                    mostrarModal("¡Cuenta creada con éxito!", "success");

                    btnCerrarModal.onclick = () => {
                        window.location.href = "/";
                    };
                } else {
                    // si hubo error, muestra el mensaje del servidor
                    const errorData = await response.json();
                    let msg = errorData.detail || "No se pudo completar el registro.";

                    if (msg.includes("ya existe")) {
                        msg = "Ese nombre de usuario ya está en uso. Por favor, elige otro.";
                    }
                    mostrarModal(msg);
                }
            } catch (error) {
                console.error("Error de red:", error);
                mostrarModal("Error crítico al conectar con el servidor.");
            }
        });
    }
});