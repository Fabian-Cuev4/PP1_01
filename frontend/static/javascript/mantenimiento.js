// Mantenimiento SIGLAB - Lista de Máquinas con Polling Estable
// Carga, muestra y actualiza máquinas automáticamente cada 2 segundos

// Configuración: tiempos de polling y conexión
const TIEMPO_POLLING_MS = 2000;
const TIEMPO_ESPERA_API_MS = 1500;
let pollingInterval = null;
let maquinasCache = [];

// Elementos del DOM
let contenedorMaquinas = null;
let inputBusqueda = null;

// Inicialización cuando carga la página
document.addEventListener("DOMContentLoaded", async () => {
    contenedorMaquinas = document.getElementById("contenedor-principal-maquinas");
    inputBusqueda = document.getElementById("input-busqueda");
    
    // Configurar buscador
    if (inputBusqueda) {
        inputBusqueda.addEventListener("input", filtrarMaquinas);
        
        // Atajos de teclado
        inputBusqueda.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                filtrarMaquinas();
            } else if (e.key === "Escape") {
                inputBusqueda.value = "";
                filtrarMaquinas();
            }
        });
    }
    
    // Iniciar polling automático
    await iniciarPolling();
    
    // Limpiar polling cuando se sale de la página
    window.addEventListener('beforeunload', () => {
        if (pollingInterval) {
            clearInterval(pollingInterval);
        }
    });
});

// FUNCIÓN: Inicia el polling automático de máquinas
async function iniciarPolling() {
    console.log("Iniciando polling automático de máquinas...");
    
    // Carga inicial
    await cargarMaquinasPolling();
    
    // Configurar polling continuo
    pollingInterval = setInterval(async () => {
        await cargarMaquinasPolling();
    }, TIEMPO_POLLING_MS);
    
    // Mostrar indicador de polling activo
    mostrarIndicadorPolling();
}

// FUNCIÓN: Carga máquinas usando el endpoint de polling
async function cargarMaquinasPolling() {
    if (!contenedorMaquinas) return;
    
    try {
        // Usar el NUEVO endpoint de polling con cache inteligente
        const response = await fetch('/api/maquinas/polling/lista', {
            method: 'GET',
            headers: {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Content-Type': 'application/json'
            },
            signal: AbortSignal.timeout(TIEMPO_ESPERA_API_MS)
        });
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Verificar estructura de respuesta del polling
        if (data.status !== 'ok') {
            console.error("Error en respuesta del polling:", data.mensaje);
            mostrarError(data.mensaje || "Error al cargar máquinas");
            return;
        }
        
        // Actualizar cache local
        maquinasCache = data.datos || [];
        
        // Renderizar máquinas
        renderizarMaquinas(maquinasCache);
        
        // Actualizar timestamp
        actualizarTimestamp(data.timestamp);
        
        console.log(`Polling exitoso: ${maquinasCache.length} máquinas cargadas`);
        
    } catch (error) {
        console.error("Error en polling de máquinas:", error);
        
        // Si falla el polling, intentar con el endpoint legacy
        await cargarMaquinasLegacy();
    }
}

// FUNCIÓN: Fallback al endpoint antiguo si el polling falla
async function cargarMaquinasLegacy() {
    try {
        const response = await fetch(`/api/maquinas/listar?_t=${Date.now()}`, {
            method: 'GET',
            headers: {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            }
        });
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const maquinas = await response.json();
        
        if (!Array.isArray(maquinas)) {
            throw new Error("La respuesta no es un array");
        }
        
        maquinasCache = maquinas;
        renderizarMaquinas(maquinasCache);
        
        console.log("Usando endpoint legacy como fallback");
        
    } catch (error) {
        console.error("Error crítico cargando máquinas:", error);
        mostrarError("No se pudieron cargar las máquinas. Intente recargar la página.");
    }
}

// FUNCIÓN: Renderiza las máquinas en el DOM
function renderizarMaquinas(maquinas) {
    if (!contenedorMaquinas) return;
    
    // Obtener referencias a los botones de acción
    const btnAgregarMaquina = document.getElementById('btn-agregar-maquina');
    const btnReportes = document.getElementById('btn-reportes');
    const btnRegresar = document.getElementById('btn-regresar');
    
    // Si no hay máquinas, mostrar mensaje y ocultar botones innecesarios
    if (!maquinas || maquinas.length === 0) {
        // Solo mostrar el mensaje si no existe el contenedor de no-maquinas
        if (!contenedorMaquinas.querySelector('.no-maquinas-container')) {
            contenedorMaquinas.innerHTML = `
                <div class="no-maquinas-container">
                    <div class="no-maquinas-icon">PC</div>
                    <h3>No hay equipos registrados</h3>
                    <p>Parece que aún no tienes máquinas en el sistema.</p>
                    <button class="btn-create" onclick="irAAgregarMaquina()">
                        Agregar primera máquina
                    </button>
                </div>
            `;
        }
        
        // Ocultar botones de reportes y agregar máquina temporalmente
        if (btnAgregarMaquina) btnAgregarMaquina.style.display = 'none';
        if (btnReportes) btnReportes.style.display = 'none';
        // Mantener visible el botón de regresar
        return;
    }
    
    // Si hay máquinas, mostrar todos los botones
    if (btnAgregarMaquina) btnAgregarMaquina.style.display = 'inline-block';
    if (btnReportes) btnReportes.style.display = 'inline-block';
    if (btnRegresar) btnRegresar.style.display = 'inline-block';
    
    // Verificar si ya existen las tarjetas para evitar recrearlas
    const tarjetasExistentes = contenedorMaquinas.querySelectorAll('.detail-container');
    
    // Si el número de máquinas coincide con las tarjetas existentes, solo actualizar contenido
    if (tarjetasExistentes.length === maquinas.length) {
        tarjetasExistentes.forEach((tarjeta, index) => {
            const maquina = maquinas[index];
            if (maquina) {
                // Actualizar solo el contenido de la tarjeta, sin recrearla
                actualizarTarjetaExistente(tarjeta, maquina);
            }
        });
    } else {
        // Si el número no coincide, limpiar y recrear todo
        contenedorMaquinas.innerHTML = '';
        maquinas.forEach(maquina => {
            const tarjeta = crearTarjetaMaquina(maquina);
            contenedorMaquinas.appendChild(tarjeta);
        });
    }
    
    // Aplicar filtro actual si hay búsqueda activa
    if (inputBusqueda && inputBusqueda.value.trim()) {
        filtrarMaquinas();
    }
}

// FUNCIÓN: Actualiza el contenido de una tarjeta existente sin recrearla
function actualizarTarjetaExistente(tarjeta, maquina) {
    const claseEstado = obtenerClaseEstado(maquina.estado_actual || maquina.estado);
    
    // Actualizar información principal sin recrear elementos
    const infoContainer = tarjeta.querySelector('.card-info');
    if (infoContainer) {
        // Actualizar solo los textos necesarios para evitar parpadeos
        const codigoElement = infoContainer.querySelector('h3');
        const estadoElement = infoContainer.querySelector('.status-badge');
        const areaElement = infoContainer.querySelector('p:nth-child(1)'); // Área
        const fechaElement = infoContainer.querySelector('p:nth-child(2)'); // Fecha
        const tipoElement = infoContainer.querySelector('p:nth-child(3)'); // Tipo
        
        // Actualizar elementos si existen - SIN EFECTOS VISUALES
        if (codigoElement) codigoElement.textContent = maquina.codigo_equipo || maquina.codigo;
        if (estadoElement) {
            // Actualizar tanto el texto como la clase CSS - SIN EFECTOS
            estadoElement.className = `status-badge ${claseEstado}`;
            estadoElement.textContent = maquina.estado_actual || maquina.estado;
        }
        if (areaElement) areaElement.textContent = maquina.area;
        if (fechaElement) fechaElement.textContent = maquina.fecha;
        if (tipoElement) tipoElement.textContent = maquina.tipo_equipo || maquina.tipo;
    }
}

// FUNCIÓN: Crea una tarjeta HTML para una máquina
function crearTarjetaMaquina(maquina) {
    const tarjeta = document.createElement('div');
    tarjeta.className = 'detail-container';
    tarjeta.dataset.codigo = maquina.codigo;
    
    const claseEstado = obtenerClaseEstado(maquina.estado_actual || maquina.estado);
    
    tarjeta.innerHTML = `
        <div class="card-space">
            <div class="card-icon"></div>
            <div class="card-info">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <h3 style="font-size: 22px; color: #2c3e50; margin: 0;">${maquina.codigo_equipo || maquina.codigo}</h3>
                    <span class="status-badge ${claseEstado}">${maquina.estado_actual || maquina.estado}</span>
                </div>
                <div style="display: flex; gap: 40px; font-size: 14px; color: #555;">
                    <p><strong>Área:</strong> ${maquina.area}</p>
                    <p><strong>Adquisición:</strong> ${maquina.fecha}</p>
                    <p><strong>Tipo:</strong> ${maquina.tipo_equipo || maquina.tipo}</p>
                </div>
            </div>
        </div>
        
        <div class="side-buttons">
            <button class="btn-action btn-yellow-history" onclick="verHistorial('${maquina.codigo_equipo || maquina.codigo}')">
                Historial
            </button>
            <button class="btn-action btn-blue-act" onclick="irAMantenimiento('${maquina.codigo_equipo || maquina.codigo}')">
                Mantenimiento
            </button>
            <button class="btn-action btn-green" onclick="actualizarMaquina('${maquina.codigo_equipo || maquina.codigo}')">
                Actualizar
            </button>
        </div>
    `;
    
    return tarjeta;
}

// FUNCIÓN: Decide el color del badge según el estado
function obtenerClaseEstado(estado) {
    if (!estado) return "status-fuera-servicio";
    const e = estado.toLowerCase();
    if (e.includes("operativa")) return "status-operativa";
    if (e.includes("mantenimiento")) return "status-mantenimiento"; 
    if (e.includes("fuera de servicio") || e.includes("baja")) return "status-fuera-servicio";
    return "status-mantenimiento";
}

// FUNCIÓN: Filtra las máquinas según el buscador
function filtrarMaquinas() {
    if (!inputBusqueda || !contenedorMaquinas) return;
    
    const filtro = inputBusqueda.value.toLowerCase().trim();
    const tarjetas = contenedorMaquinas.querySelectorAll(".detail-container");
    
    tarjetas.forEach(tarjeta => {
        const textoTarjeta = tarjeta.innerText.toLowerCase();
        
        if (filtro === "") {
            tarjeta.style.display = "flex";
        } else {
            tarjeta.style.display = textoTarjeta.includes(filtro) ? "flex" : "none";
        }
    });
}

// FUNCIÓN: Actualiza el timestamp de última actualización
function actualizarTimestamp(timestamp) {
    let indicador = document.getElementById('polling-indicator');
    }

// FUNCIÓN: Muestra mensaje de error
function mostrarError(mensaje) {
    if (!contenedorMaquinas) return;
    
    contenedorMaquinas.innerHTML = `
        <div class="error-container">
            <div class="error-icon">X</div>
            <h3>Error de conexión</h3>
            <p>${mensaje}</p>
            <button class="btn-create" onclick="location.reload()">
                Reintentar
            </button>
        </div>
    `;
}

// FUNCIÓN: Navegación - Ver historial
function verHistorial(codigo) {
    window.location.href = `/pagina/maquinas/historial?codigo=${encodeURIComponent(codigo)}`;
}

// FUNCIÓN: Navegación - Ir a mantenimiento
function irAMantenimiento(codigo) {
    window.location.href = `/pagina/maquinas/mantenimiento?codigo=${encodeURIComponent(codigo)}`;
}

// FUNCIÓN: Navegación - Actualizar máquina
function actualizarMaquina(codigo) {
    window.location.href = `/pagina/maquinas/actualizar?codigo=${encodeURIComponent(codigo)}`;
}

// FUNCIÓN: Navegación - Agregar máquina (usada en el mensaje de "no hay máquinas")
function irAAgregarMaquina() {
    window.location.href = "/pagina/maquinas/agregar";
}

// EXPORTAR para uso global
window.cargarMaquinasPolling = cargarMaquinasPolling;
window.verHistorial = verHistorial;
window.irAMantenimiento = irAMantenimiento;
window.actualizarMaquina = actualizarMaquina;
window.irAAgregarMaquina = irAAgregarMaquina;
