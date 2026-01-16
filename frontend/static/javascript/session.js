document.addEventListener("DOMContentLoaded", () => {
    const btnIngresar = document.getElementById("btn-signin-on");

    if (btnIngresar) {
        btnIngresar.addEventListener("click", async (e) => {
            e.preventDefault(); // Evita que el formulario se recargue solo

            // 1. Capturar los datos de los inputs
            const usuarioInput = document.getElementById("usuario");
            const passwordInput = document.getElementById("password");

            const datos = {
                username: usuarioInput.value,
                password: passwordInput.value
            };

            // 2. Validación básica en el navegador
            if (!datos.username || !datos.password) {
                alert("Por favor, ingresa usuario y contraseña.");
                return;
            }

            console.log("Enviando al backend:", datos);

            // 3. AQUÍ CONECTAREMOS CON PYTHON (FastAPI)
            // Por ahora, simulamos la conexión para que veas que funciona
            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(datos)
                });

                if (response.ok) {
                    const resultado = await response.json();
                    console.log("Login correcto:", resultado);
                    
                    window.location.href = "/templates/index_ventana2.html"; 
                } else {
                    alert("Usuario o contraseña incorrectos");
                }
            } catch (error) {
                console.error("Error:", error);
                alert("Error al conectar con el servidor");
            }
        });
    }
});

// Mantén tu lógica de logout tal cual, esa está bien para el botón de salir
document.addEventListener("DOMContentLoaded", () => {
    const btnSalir = document.getElementById("btn-logout-off");
    if (btnSalir) {
        btnSalir.addEventListener("click", () => {
            window.location.href = "/";
        });
    }
});