// maneja la navegación entre las diferentes páginas de la aplicación
document.addEventListener("DOMContentLoaded", () => {
    // botón para ir a agregar una nueva máquina
    const btnAgregar = document.getElementById("btn-agregar-maquina");
    if (btnAgregar) {
        btnAgregar.addEventListener("click", () => {
            window.location.href = "/pagina/maquinas/agregar";
        });
    }

    // botón para ir a la página de reportes
    const btnReportes = document.getElementById("btn-reportes");
    if (btnReportes) {
        btnReportes.addEventListener("click", () => {
            window.location.href = "/pagina/maquinas/reportes";
        });
    }

    // botón para regresar a la lista de máquinas
    const btnRegresar = document.getElementById("btn-regresar");
    if (btnRegresar) {
        btnRegresar.addEventListener("click", () => {
            window.location.href = "/pagina/inicio";
        });
    }
});