// Control de navegación entre páginas de la aplicación

document.addEventListener("DOMContentLoaded", () => {
    // Botón agregar máquina: navega al formulario de registro
    const botonAgregarMaquina = document.getElementById("btn-agregar-maquina");
    if (botonAgregarMaquina) {
        botonAgregarMaquina.addEventListener("click", () => {
            window.location.href = "/pagina/maquinas/agregar";
        });
    }

    // Botón reportes: navega a página de reportes
    const botonVerReportes = document.getElementById("btn-reportes");
    if (botonVerReportes) {
        botonVerReportes.addEventListener("click", () => {
            window.location.href = "/pagina/maquinas/reportes";
        });
    }

    // Botón regresar: vuelve a página principal
    const botonRegresarInicio = document.getElementById("btn-regresar");
    if (botonRegresarInicio) {
        botonRegresarInicio.addEventListener("click", () => {
            window.location.href = "/pagina/inicio";
        });
    }
});