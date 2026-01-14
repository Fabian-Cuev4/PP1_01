document.addEventListener("DOMContentLoaded", () => {
    const btnAgregar = document.getElementById("btn-create-machine");
    const btnAgregarMantenimiento = document.getElementById("btn-action-mant");
    const btnCrearReporte = document.getElementById("btn-action-report");

    if (btnAgregar) {
        btnAgregar.addEventListener("click", () => {
            window.location.href = "/home/maquinas/formulario";
        });
    }

    if (btnAgregarMantenimiento) {
        btnAgregarMantenimiento.addEventListener("click", () => {
            window.location.href = "/home/maquinas/formulario/mantenimiento";
        });
    }

    if (btnCrearReporte) {
        btnCrearReporte.addEventListener("click", () => {
            window.location.href = "/home/maquinas/reporte";
        });
    }
});
