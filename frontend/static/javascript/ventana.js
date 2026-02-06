// =============================================================================
// NAVEGACIÓN SIGLAB - Control de Navegación Entre Páginas
// Autor: Estudiante de Programación Avanzada
// Propósito: Manejar los botones de navegación de la aplicación
// =============================================================================

document.addEventListener("DOMContentLoaded", () => {
    // BOTÓN AGREGAR MÁQUINA: Navega al formulario de registro
    const botonAgregarMaquina = document.getElementById("btn-agregar-maquina");
    if (botonAgregarMaquina) {
        botonAgregarMaquina.addEventListener("click", () => {
            window.location.href = "/pagina/maquinas/agregar";
        });
    }

    // BOTÓN REPORTES: Navega a la página de reportes
    const botonVerReportes = document.getElementById("btn-reportes");
    if (botonVerReportes) {
        botonVerReportes.addEventListener("click", () => {
            window.location.href = "/pagina/maquinas/reportes";
        });
    }

    // BOTÓN REGRESAR: Vuelve a la página principal
    const botonRegresarInicio = document.getElementById("btn-regresar");
    if (botonRegresarInicio) {
        botonRegresarInicio.addEventListener("click", () => {
            window.location.href = "/pagina/inicio";
        });
    }
});