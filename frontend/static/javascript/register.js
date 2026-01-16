document.addEventListener("DOMContentLoaded", () => {
    const btnRegister = document.getElementById("btn-register");

    if (btnRegister) {
        btnRegister.addEventListener("click", async (e) => {
            e.preventDefault();

            // 1. Capturar los valores
            const nombre = document.getElementById("nombre").value;
            const usuario = document.getElementById("usuario").value;
            const password = document.getElementById("password").value;
            const confirm = document.getElementById("confirm-password").value;

            // 2. Validaciones básicas
            if (!nombre || !usuario || !password) {
                alert("Todos los campos son obligatorios.");
                return;
            }

            if (password !== confirm) {
                alert("Las contraseñas no coinciden.");
                return;
            }

            // Objeto listo para enviar al Backend
            const datosRegistro = {
                nombre_completo: nombre,
                username: usuario,
                password: password
            };

            console.log("Enviando registro...", datosRegistro);

            // 3. Enviar a Python (MySQL)
            try {
                const response = await fetch('/api/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(datosRegistro)
                });

                if (response.ok) {
                    alert("¡Cuenta creada con éxito! Ahora inicia sesión.");
                    // Redirigir al login
                    window.location.href = "/templates/index_session.html";
                } else {
                    const errorData = await response.json();
                    alert("Error: " + (errorData.detail || "No se pudo registrar"));
                }
            } catch (error) {
                console.error("Error de red:", error);
                alert("Error al conectar con el servidor.");
            }
        });
    }
});