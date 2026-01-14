document.addEventListener("DOMContentLoaded", () => {
    const btnAgregar = document.getElementById("btn-create-machine");

    if (btnAgregar) {
        btnAgregar.addEventListener("click", () => {
            window.location.href = "/home/maquinas/formulario";
        });
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const btnAgregarMantenimiento = document.getElementById("btn-action-mant");

    if (btnAgregarMantenimiento) {
        btnAgregarMantenimiento.addEventListener("click", () => {
            window.location.href = "/home/maquinas/formulario/mantenimiento";
        });
    }
});