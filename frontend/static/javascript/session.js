// =============================================================================
// SESIÓN SIGLAB - Manejo de Autenticación de Usuarios
// Autor: Estudiante de Programación Avanzada
// Propósito: Controlar el inicio de sesión, registro y cierre de sesión
// =============================================================================

document.addEventListener("DOMContentLoaded", () => {
    mostrarNombreUsuario();
    // Aseguramos que el modal esté oculto al cargar la página
    const modalNotificacion = document.getElementById("modal-notificacion");
    if (modalNotificacion) {
        modalNotificacion.classList.add("hidden");
        modalNotificacion.classList.remove("show");
    }
    
    // Referencias a los botones principales de la página de login
    const botonIniciarSesion = document.getElementById("btn-signin-on");
    const botonIrRegistro = document.getElementById("btn-register-redirect");

    // BOTÓN INICIAR SESIÓN: Valida credenciales y redirige según el tipo de usuario
    if (botonIniciarSesion) {
        botonIniciarSesion.addEventListener("click", async (evento) => {
            evento.preventDefault();

            // Capturar datos del formulario de login
            const nombreUsuario = document.getElementById("usuario").value;
            const contrasena = document.getElementById("password").value;

            // VALIDACIÓN: Verificar que los campos no estén vacíos
            if (!nombreUsuario || !contrasena) {
                mostrarModal("Campos incompletos", "Por favor, completa todos los campos.");
                return;
            }

            try {
                // AUTENTICACIÓN: Enviar credenciales al backend para validación
                const respuesta = await fetch("/api/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username: nombreUsuario, password: contrasena })
                });

                // ÉXITO: Procesar respuesta y redirigir según tipo de usuario
                if (respuesta.ok) {
                    const datosRespuesta = await respuesta.json();
                    // Usar el username devuelto por el servidor, o el enviado si no hay respuesta
                    const nombreUsuarioEfectivo = (datosRespuesta && datosRespuesta.username) ? datosRespuesta.username : nombreUsuario;
                    const nombreCompleto = (datosRespuesta && datosRespuesta.usuario) ? datosRespuesta.usuario : nombreUsuarioEfectivo;
                    
                    if (nombreUsuarioEfectivo === "admin") {
                        // USUARIO ADMIN: Guardar sesión y redirigir al dashboard
                        sessionStorage.setItem('is_admin', '1');
                        sessionStorage.setItem('username', nombreUsuarioEfectivo);
                        sessionStorage.setItem('nombre_completo', nombreCompleto);
                        window.location.href = "http://localhost:8080/pagina/dashboard";
                    } else {
                        // USUARIO NORMAL: Guardar sesión y redirigir a página principal
                        sessionStorage.setItem('is_admin', '0');
                        sessionStorage.setItem('username', nombreUsuarioEfectivo);
                        sessionStorage.setItem('nombre_completo', nombreCompleto);
                        window.location.href = "http://localhost:8080/pagina/inicio";
                    }
                } else {
                    // ERROR: Credenciales incorrectas
                    mostrarModal("Error de autenticación", "Usuario o contraseña incorrectos.");
                }
            } catch (error) {
                console.error("Error al iniciar sesión:", error);
                mostrarModal("Error de conexión", "Error de conexión con el servidor.");
            }
        });
    }

    // BOTÓN REGISTRARSE: Redirige a la página de registro de nuevos usuarios
    if (botonIrRegistro) {
        botonIrRegistro.addEventListener("click", () => {
            window.location.href = "http://localhost:8080/pagina/registro";
        });
    }

    // BOTÓN CERRAR MODAL: Cierra la notificación cuando el usuario hace clic
    const botonCerrarModal = document.getElementById("btn-modal-cerrar");
    if (botonCerrarModal) {
        botonCerrarModal.addEventListener("click", () => {
            ocultarModal();
        });
    }
});

// FUNCIÓN: Muestra el modal de notificación con título y mensaje
// Parámetros: titulo - Texto del encabezado, mensaje - Contenido del modal
function mostrarModal(titulo, mensaje) {
    console.log("mostrarModal llamado con:", titulo, mensaje);
    const modalNotificacion = document.getElementById("modal-notificacion");
    const elementoTitulo = document.getElementById("modal-titulo");
    const elementoMensaje = document.getElementById("modal-mensaje");

    console.log("Elementos encontrados:", {
        modalNotificacion: !!modalNotificacion,
        elementoTitulo: !!elementoTitulo,
        elementoMensaje: !!elementoMensaje
    });

    if (modalNotificacion && elementoTitulo && elementoMensaje) {
        elementoTitulo.textContent = titulo;
        elementoMensaje.textContent = mensaje;
        
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
    } else {
        console.error("No se encontraron los elementos del modal");
    }
}

// FUNCIÓN: Oculta el modal de notificación
function ocultarModal() {
    console.log("ocultarModal llamado");
    const modalNotificacion = document.getElementById("modal-notificacion");
    if (modalNotificacion) {
        console.log("Clases antes de ocultar:", modalNotificacion.className);
        // Ocultar el modal cambiando las clases CSS
        modalNotificacion.classList.remove("show");
        modalNotificacion.classList.add("hidden");
    }
}

// CIERRE DE SESIÓN: Maneja el logout del usuario
// Limpiamos cookies y sessionStorage para cerrar completamente la sesión
const botonCerrarSesion = document.getElementById("btn-logout-off");
if (botonCerrarSesion) {
    botonCerrarSesion.addEventListener("click", async () => {
        try {
            // Limpiar cookie de sesión en el backend
            await fetch("/sticky/logout", { method: "GET", cache: "no-store" });
        } catch (error) {
            console.error("No se pudo borrar cookie sticky:", error);
        }

        try {
            // Limpiar datos de sesión del frontend
            const nombreUsuario = sessionStorage.getItem('username');
            if (nombreUsuario) {
                // Eliminar flag de ping si existe
                sessionStorage.removeItem(`ping_${nombreUsuario}`);
            }
            // Eliminar datos de usuario y tipo de usuario
            sessionStorage.removeItem('is_admin');
            sessionStorage.removeItem('username');
            sessionStorage.removeItem('nombre_completo');
        } catch (error) {
            console.error("No se pudo limpiar storage:", error);
        }

        // Redirigir a la página de login
        window.location.href = "http://localhost:8080/pagina/login";
    });
}

// FUNCIÓN: Muestra el nombre del usuario en el header
function mostrarNombreUsuario() {
    const nombreUsuario = sessionStorage.getItem('nombre_completo');
    const elementoNombreUsuario = document.getElementById('nombre-completo');
    
    if (nombreUsuario && elementoNombreUsuario) {
        elementoNombreUsuario.textContent = nombreUsuario;
    }
}