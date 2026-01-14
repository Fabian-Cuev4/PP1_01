document.addEventListener("DOMContentLoaded", () => {
    const btnCancelar = document.getElementById("btn-cancel-action");

    if (btnCancelar) {
        btnCancelar.addEventListener("click", () => {
            window.location.href = "/home/maquinas";
        });
    }
});
