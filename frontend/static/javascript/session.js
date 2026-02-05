// maneja el inicio de sesión de usuarios
document.addEventListener("DOMContentLoaded", () => {
    // Asegurar que el modal esté oculto al cargar
    const modal = document.getElementById("modal-notificacion");
    if (modal) {
        modal.classList.add("hidden");
        modal.classList.remove("show");
    }
    
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

                // si el login es exitoso, guarda el username y redirige
                if (response.ok) {
                    const data = await response.json();
                    // Guardar el username en localStorage para usarlo después
                    if (data.username) {
                        localStorage.setItem('username', data.username);
                    }
                    window.location.href = "http://localhost:8080/pagina/inicio";
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
            window.location.href = "http://localhost:8080/pagina/registro";
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
    console.log("mostrarModal llamado con:", titulo, mensaje);
    const modal = document.getElementById("modal-notificacion");
    const tituloElement = document.getElementById("modal-titulo");
    const mensajeElement = document.getElementById("modal-mensaje");

    console.log("Elementos encontrados:", {
        modal: !!modal,
        tituloElement: !!tituloElement,
        mensajeElement: !!mensajeElement
    });

    if (modal && tituloElement && mensajeElement) {
        tituloElement.textContent = titulo;
        mensajeElement.textContent = mensaje;
        
        console.log("Clases antes:", modal.className);
        // Mostrar el modal
        modal.classList.remove("hidden");
        modal.classList.add("show");
        console.log("Clases después:", modal.className);
        console.log("Estilos computados:", {
            display: window.getComputedStyle(modal).display,
            visibility: window.getComputedStyle(modal).visibility,
            opacity: window.getComputedStyle(modal).opacity,
            zIndex: window.getComputedStyle(modal).zIndex
        });
    } else {
        console.error("No se encontraron los elementos del modal");
    }
}

// función para ocultar el modal de notificación
function ocultarModal() {
    console.log("ocultarModal llamado");
    const modal = document.getElementById("modal-notificacion");
    if (modal) {
        console.log("Clases antes:", modal.className);
        // Ocultar el modal
        modal.classList.remove("show");
        modal.classList.add("hidden");
    }
}

// maneja el cierre de sesión
const btnLogout = document.getElementById("btn-logout-off");
if (btnLogout) {
    btnLogout.addEventListener("click", () => {
        // redirige al login (en un sistema real aquí se destruiría la sesión)
        window.location.href = "http://localhost:8080/pagina/login";
    });
}