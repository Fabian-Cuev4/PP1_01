document.addEventListener("DOMContentLoaded", () => {
    const btnAgregar = document.getElementById("btn-create-machine");
    const btnAgregarMantenimiento = document.getElementById("btn-action-mant");
    const btnCrearReporte = document.getElementById("btn-action-report");
    const btnRegresar = document.getElementById("btn-return-action");


    if (btnAgregar) {
        btnAgregar.addEventListener("click", () => {
            window.location.href = "/home/maquinas/formulario";
        });
    }

    if (btnCrearReporte) {
        btnCrearReporte.addEventListener("click", () => {
            window.location.href = "/home/maquinas/reporte";
        });
    }

    if (btnRegresar) {
        btnRegresar.addEventListener("click", () => {
            window.location.href = "/home";
        });
    }
});