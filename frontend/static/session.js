document.addEventListener("DOMContentLoaded", () => {
    const btnIngresar = document.getElementById("btn-signin-on");

    if (btnIngresar) {
        btnIngresar.addEventListener("click", () => {
            window.location.href = "/home";
        });
    }
});
document.addEventListener("DOMContentLoaded", () => {
    const btnSalir = document.getElementById("btn-logout-off");

    if (btnSalir) {
        btnSalir.addEventListener("click", () => {
            window.location.href = "/";
        });
    }
});

