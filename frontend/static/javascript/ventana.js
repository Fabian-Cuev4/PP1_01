// =============================================================================
// NAVEGACIÓN Y DASHBOARD VENTANA 1 - Control de Navegación y Contadores
// =============================================================================

document.addEventListener("DOMContentLoaded", () => {
    
    // --- 1. CONTROL DE NAVEGACIÓN (Lo que ya tenías) ---
    const botonAgregarMaquina = document.getElementById("btn-agregar-maquina");
    if (botonAgregarMaquina) {
        botonAgregarMaquina.addEventListener("click", () => {
            window.location.href = "/pagina/maquinas/agregar";
        });
    }

    const botonVerReportes = document.getElementById("btn-reportes");
    if (botonVerReportes) {
        botonVerReportes.addEventListener("click", () => {
            window.location.href = "/pagina/maquinas/reportes";
        });
    }

    const botonRegresarInicio = document.getElementById("btn-regresar");
    if (botonRegresarInicio) {
        botonRegresarInicio.addEventListener("click", () => {
            window.location.href = "/pagina/inicio";
        });
    }

    // --- 2. NUEVO: POLLING PARA ACTUALIZAR CONTADORES (Redis) ---
    // Solo ejecutamos esto si estamos en la página de inicio (Ventana 1)
    // Buscamos el elemento donde se muestra el número de equipos
    
    // NOTA: Primero necesitamos darle un ID a ese párrafo en el HTML.
    // Asumiremos que le pondrás id="contador-equipos-redes"
    const contadorRedes = document.getElementById("contador-equipos-redes");

    if (contadorRedes) {
        console.log("🟢 Iniciando Polling en Ventana 1...");
        
        // Función para pedir el total al backend
        const actualizarContador = async () => {
            try {
                // Usamos la misma ruta de listar (que ya usa Redis)
                const respuesta = await fetch("/api/maquinas/listar");
                if (respuesta.ok) {
                    const maquinas = await respuesta.json();
                    // Actualizamos el número en pantalla
                    contadorRedes.innerHTML = `<strong>N° Equipos:</strong> ${maquinas.length}`;
                    console.log(`🔄 Contador actualizado: ${maquinas.length} equipos`);
                }
            } catch (error) {
                console.error("Error actualizando contador:", error);
            }
        };

        // 1. Cargar inmediatamente al entrar
        actualizarContador();

        // 2. Recargar cada 3 segundos (Polling)
        setInterval(actualizarContador, 3000);
    }
});