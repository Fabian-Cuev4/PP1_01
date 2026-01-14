document.addEventListener("DOMContentLoaded", () => {
    const btnRegresar = document.getElementById("btn-return");

    if (btnRegresar) {
        btnRegresar.addEventListener("click", () => {
            window.location.href = "/home/maquinas";
        });
    }
});