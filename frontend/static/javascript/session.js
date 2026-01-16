// maneja el inicio de sesión de usuarios
document.addEventListener("DOMContentLoaded", () => {
    const btnLogin = document.getElementById("btn-signin-on");
    const btnRegister = document.getElementById("btn-register-redirect");

    // botón de login: valida credenciales y redirige al dashboard
    if (btnLogin) {
        btnLogin.addEventListener("click", async (e) => {
            e.preventDefault();

            // captura los datos del formulario
            const username = document.getElementById("usuario").value;
            const password = document.getElementById("password").value;

            // valida que los campos no estén vacíos
            if (!username || !password) {
                mostrarModal("Campos incompletos", "Por favor, completa todos los campos.");
                return;
            }

            try {
                // envía las credenciales al backend
                const response = await fetch("/api/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password })
                });

                // si el login es exitoso, redirige al dashboard
                if (response.ok) {
                    window.location.href = "/home";
                } else {
                    mostrarModal("Error de autenticación", "Usuario o contraseña incorrectos.");
                }
            } catch (error) {
                console.error("Error al iniciar sesión:", error);
                mostrarModal("Error de conexión", "Error de conexión con el servidor.");
            }
        });
    }

    // botón de registrarse: redirige a la página de registro
    if (btnRegister) {
        btnRegister.addEventListener("click", () => {
            window.location.href = "/register";
        });
    }

    // botón para cerrar el modal de notificación
    const btnCerrarModal = document.getElementById("btn-modal-cerrar");
    if (btnCerrarModal) {
        btnCerrarModal.addEventListener("click", () => {
            ocultarModal();
        });
    }
});

// función para mostrar el modal de notificación
function mostrarModal(titulo, mensaje) {
    const modal = document.getElementById("modal-notificacion");
    const tituloElement = document.getElementById("modal-titulo");
    const mensajeElement = document.getElementById("modal-mensaje");

    if (modal && tituloElement && mensajeElement) {
        tituloElement.textContent = titulo;
        mensajeElement.textContent = mensaje;
        modal.style.display = "flex";
    }
}

// función para ocultar el modal de notificación
function ocultarModal() {
    const modal = document.getElementById("modal-notificacion");
    if (modal) {
        modal.style.display = "none";
    }
}

// maneja el cierre de sesión
const btnLogout = document.getElementById("btn-logout-off");
if (btnLogout) {
    btnLogout.addEventListener("click", () => {
        // redirige al login (en un sistema real aquí se destruiría la sesión)
        window.location.href = "/";
    });
}