// =============================================================================
// REGISTRO SIGLAB - Creación de Nuevas Cuentas de Usuario
// Autor: Estudiante de Programación Avanzada
// Propósito: Manejar el formulario de registro de nuevos usuarios
// =============================================================================

document.addEventListener("DOMContentLoaded", () => {
    // Aseguramos que el modal esté oculto al cargar la página
    const modalNotificacion = document.getElementById("modal-notificacion");
    if (modalNotificacion) {
        modalNotificacion.classList.add("hidden");
        modalNotificacion.classList.remove("show");
    }

    // Referencias a los elementos del formulario de registro
    const botonRegistrarse = document.getElementById("btn-register");
    const elementoMensajeModal = document.getElementById("modal-mensaje");
    const botonCerrarModal = document.getElementById("btn-modal-cerrar");
    const iconoModal = document.querySelector(".modal-icon i");

    // FUNCIÓN: Muestra el modal de notificación con mensaje y tipo
    // Parámetros: mensaje - Texto a mostrar, tipo - 'success' o 'error'
    function mostrarModalRegistro(mensaje, tipo = "error") {
        console.log("mostrarModal registro llamado con:", mensaje, tipo);
        elementoMensajeModal.textContent = mensaje;

        // Configurar ícono y color según el tipo de mensaje
        if (tipo === "success") {
            iconoModal.className = "fas fa-check-circle";
            iconoModal.parentElement.style.color = "#2ecc71";
        } else {
            iconoModal.className = "fas fa-exclamation-circle";
            iconoModal.parentElement.style.color = "#e74c3c";
        }

        console.log("Clases antes de mostrar:", modalNotificacion.className);
        // Mostrar el modal cambiando las clases CSS
        modalNotificacion.classList.remove("hidden");
        modalNotificacion.classList.add("show");
        console.log("Clases después de mostrar:", modalNotificacion.className);
        console.log("Estilos computados:", {
            display: window.getComputedStyle(modalNotificacion).display,
            visibility: window.getComputedStyle(modalNotificacion).visibility,
            opacity: window.getComputedStyle(modalNotificacion).opacity,
            zIndex: window.getComputedStyle(modalNotificacion).zIndex
        });
    }

    // BOTÓN CERRAR MODAL: Cierra la notificación cuando el usuario hace clic
    if (botonCerrarModal) {
        botonCerrarModal.addEventListener("click", () => {
            // Ocultar el modal cambiando las clases CSS
            modalNotificacion.classList.remove("show");
            modalNotificacion.classList.add("hidden");
        });
    }

    // BOTÓN REGISTRARSE: Maneja el envío del formulario de registro
    if (botonRegistrarse) {
        botonRegistrarse.addEventListener("click", async (evento) => {
            evento.preventDefault();

            // Capturar datos del formulario de registro
            const nombreCompleto = document.getElementById("nombre").value;
            const nombreUsuario = document.getElementById("usuario").value;
            const contrasena = document.getElementById("password").value;
            const confirmacionContrasena = document.getElementById("confirm-password").value;

            // VALIDACIÓN 1: Verificar que todos los campos estén llenos
            if (!nombreCompleto || !nombreUsuario || !contrasena) {
                mostrarModalRegistro("Todos los campos son obligatorios.");
                return;
            }

            // VALIDACIÓN 2: Verificar que las contraseñas coincidan
            if (contrasena !== confirmacionContrasena) {
                mostrarModalRegistro("Las contraseñas no coinciden. Por favor, verifica.");
                return;
            }

            // Preparar datos para enviar al backend
            const datosRegistro = {
                nombre_completo: nombreCompleto,
                username: nombreUsuario,
                password: contrasena
            };

            console.log("Enviando registro...", datosRegistro);

            try {
                // ENVIAR REGISTRO: Realizar la petición al backend
                const respuesta = await fetch('/api/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(datosRegistro)
                });

                // ÉXITO: Mostrar confirmación y redirigir al login
                if (respuesta.ok) {
                    mostrarModalRegistro("¡Cuenta creada con éxito!", "success");

                    // Configurar el botón de cerrar para redirigir automáticamente
                    botonCerrarModal.onclick = () => {
                        window.location.href = "http://localhost:8080/pagina/login";
                    };
                } else {
                    // ERROR: Analizar la respuesta del servidor y mostrar mensaje apropiado
                    const datosError = await respuesta.json();
                    let mensajeError = datosError.detail || "No se pudo completar el registro.";

                    // Mensaje específico para usuario duplicado
                    if (mensajeError.includes("ya existe")) {
                        mensajeError = "Ese nombre de usuario ya está en uso. Por favor, elige otro.";
                    }
                    mostrarModalRegistro(mensajeError);
                }
            } catch (error) {
                console.error("Error de red:", error);
                mostrarModalRegistro("Error crítico al conectar con el servidor.");
            }
        });
    }
});