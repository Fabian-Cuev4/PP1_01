// Dashboard SIGLAB - Monitoreo de Alta Disponibilidad
// Verifica estado de servidores API y muestra estadísticas básicas

// Configuración: tiempos de actualización y conexión
const TIEMPO_ACTUALIZACION_MS = 1000;
const TIEMPO_ESPERA_API_MS = 1500;

// Sistema de usuarios automático - desactivado
let usuarioActual = null;
let sesionIniciada = false;

// Funciones de tracking desactivadas - ya no se usan
function registrarUsuarioActivo(username) {
    // Tracking desactivado - ya no se usa traffic/login
    console.log(`Usuario ${username} ha iniciado sesión`);
}

function registrarUsuarioInactivo() {
    // Tracking desactivado - ya no se usa traffic/logout
    console.log(`Usuario ${usuarioActual} ha cerrado sesión`);
    usuarioActual = null;
    sesionIniciada = false;
}

// Detecta cuando usuario entra al sistema (login)
function detectarLoginUsuario() {
    // Buscar formularios de login en página
    const loginForms = document.querySelectorAll('form');
    const usernameInputs = document.querySelectorAll('input[type="text"], input[name*="user"], input[name*="username"]');
    
    loginForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const formData = new FormData(form);
            const username = formData.get('username') || formData.get('user') || formData.get('email');
            
            if (username && username !== 'admin') {
                registrarUsuarioActivo(username);
            }
        });
    });
    
    // Detectar inputs de username para login automático
    usernameInputs.forEach(input => {
        input.addEventListener('change', (e) => {
            const username = e.target.value;
            if (username && username !== 'admin') {
                setTimeout(() => registrarUsuarioActivo(username), 1000);
            }
        });
    });
}

// Detecta cuando usuario sale del sistema (logout)
function detectarLogoutUsuario() {
    // Detectar botones de logout
    const logoutButtons = document.querySelectorAll('button[onclick*="logout"], a[href*="logout"], button[onclick*="salir"], a[href*="salir"]');
    
    logoutButtons.forEach(button => {
        button.addEventListener('click', () => {
            setTimeout(() => registrarUsuarioInactivo(), 500);
        });
    });
    
    // Detectar cuando usuario cierra pestaña o ventana
    window.addEventListener('beforeunload', () => {
        if (sesionIniciada) {
            registrarUsuarioInactivo();
        }
    });
    
    // Detectar inactividad (sin movimiento mouse/teclado por 30 segundos)
    let inactivityTimer;
    function resetInactivityTimer() {
        clearTimeout(inactivityTimer);
        inactivityTimer = setTimeout(() => {
            if (sesionIniciada) {
                console.log('🕐 Usuario inactivo por 30 segundos, cerrando sesión automáticamente');
                registrarUsuarioInactivo();
            }
        }, 30000);
    }
    
    // Reiniciar timer con actividad del usuario
    document.addEventListener('mousemove', resetInactivityTimer);
    document.addEventListener('keypress', resetInactivityTimer);
    document.addEventListener('click', resetInactivityTimer);
    document.addEventListener('scroll', resetInactivityTimer);
    
    resetInactivityTimer();
}

// Elementos del DOM: servidores y medidor de velocidad
const tarjetaServidor1 = document.getElementById('server1');
const tarjetaServidor2 = document.getElementById('server2');
const tarjetaServidor3 = document.getElementById('server3');
const indicadorEstado1 = document.getElementById('status1');
const indicadorEstado2 = document.getElementById('status2');
const indicadorEstado3 = document.getElementById('status3');
const nombreServidor1 = document.getElementById('name1');
const nombreServidor2 = document.getElementById('name2');
const nombreServidor3 = document.getElementById('name3');
const speedFill = document.getElementById('speed-fill');
const speedValue = document.getElementById('speed-value');
const speedArrow = document.getElementById('speed-arrow');

// Inicialización del dashboard
document.addEventListener('DOMContentLoaded', () => {
    console.log('Dashboard cargado, iniciando monitoreo...');
    console.log('Elementos encontrados:', {
        tarjetaServidor1: !!tarjetaServidor1,
        tarjetaServidor2: !!tarjetaServidor2,
        tarjetaServidor3: !!tarjetaServidor3,
        indicadorEstado1: !!indicadorEstado1,
        indicadorEstado2: !!indicadorEstado2,
        indicadorEstado3: !!indicadorEstado3,
        nombreServidor1: !!nombreServidor1,
        nombreServidor2: !!nombreServidor2,
        nombreServidor3: !!nombreServidor3,
        speedFill: !!speedFill,
        speedValue: !!speedValue,
        speedArrow: !!speedArrow
    });
    
    // Iniciar sistema de detección automática de usuarios
    detectarLoginUsuario();
    detectarLogoutUsuario();
    
    // Iniciar bucle de actualización
    bucleActualizacion();
});

// Realiza peticiones a API con timeout
async function obtenerDatosAPI(url) {
    const controlador = new AbortController();
    const temporizador = setTimeout(() => controlador.abort(), TIEMPO_ESPERA_API_MS);
    
    try {
        console.log(`Haciendo petición a: ${url}`);
        const respuesta = await fetch(url, {
            cache: 'no-store',
            signal: controlador.signal,
        });
        
        if (!respuesta.ok) {
            throw new Error(`Error HTTP ${respuesta.status}`);
        }
        
        const datos = await respuesta.json();
        console.log(`Respuesta de ${url}:`, datos);
        return datos;
    } catch (error) {
        console.error(`Error en petición a ${url}:`, error);
        throw error;
    } finally {
        clearTimeout(temporizador);
    }
}

// Verifica si servidores API están activos o caídos (3 servidores)
async function verificarEstadoServidores() {
    console.log('Verificando estado de servidores...');
    
    const promesaServidor1 = verificarServidorIndividual('/api1/api/health');
    const promesaServidor2 = verificarServidorIndividual('/api2/api/health');
    const promesaServidor3 = verificarServidorIndividual('/api3/api/health');
    
    try {
        const [servidor1Activo, servidor2Activo, servidor3Activo] = await Promise.allSettled([
            promesaServidor1,
            promesaServidor2,
            promesaServidor3
        ]);
        
        const estadoServidores = {
            up1: servidor1Activo.status === 'fulfilled' && servidor1Activo.value,
            up2: servidor2Activo.status === 'fulfilled' && servidor2Activo.value,
            up3: servidor3Activo.status === 'fulfilled' && servidor3Activo.value
        };
        
        console.log(`Estado servidores - Servidor 1: ${estadoServidores.up1}, Servidor 2: ${estadoServidores.up2}, Servidor 3: ${estadoServidores.up3}`);
        
        // Actualizar la interfaz visual
        actualizarVisualServidor(1, estadoServidores.up1);
        actualizarVisualServidor(2, estadoServidores.up2);
        actualizarVisualServidor(3, estadoServidores.up3);

        // Actualizar nombres de servidores dinámicamente
        await actualizarNombresServidores();

        // Calcular disponibilidad basada en 3 servidores
        const servidoresActivos = (estadoServidores.up1 ? 1 : 0) + (estadoServidores.up2 ? 1 : 0) + (estadoServidores.up3 ? 1 : 0);
        const disponibilidad = Math.round((servidoresActivos / 3) * 100);
        
        // Actualizar medidor de velocidad
        actualizarMedidorVelocidad(disponibilidad);
        
        return estadoServidores;
    } catch (error) {
        console.error('Error verificando servidores:', error);
        return { up1: false, up2: false, up3: false };
    }
}

// FUNCIÓN: Actualiza los nombres de los servidores dinámicamente (uno por uno)
async function actualizarNombresServidores() {
    try {
        // Actualizar nombre de cada servidor individualmente
        await actualizarNombreServidorIndividual(1, '/api1/api/health', nombreServidor1);
        await actualizarNombreServidorIndividual(2, '/api2/api/health', nombreServidor2);
        await actualizarNombreServidorIndividual(3, '/api3/api/health', nombreServidor3);
        
        console.log('Nombres de servidores actualizados individualmente');
    } catch (error) {
        console.error('Error actualizando nombres de servidores:', error);
    }
}

// FUNCIÓN: Actualiza el nombre de un servidor específico
async function actualizarNombreServidorIndividual(numeroServidor, url, elementoNombre) {
    try {
        const nombre = await obtenerNombreServidor(url);
        
        // Actualizar nombre solo para este servidor específico
        if (nombre && elementoNombre) {
            elementoNombre.textContent = nombre;
        } else {
            elementoNombre.textContent = 'Servidor Desconectado';
        }
        
        console.log(`Servidor ${numeroServidor}: ${nombre || 'Desconectado'}`);
    } catch (error) {
        console.log(`No se pudo obtener nombre del servidor ${numeroServidor}:`, error.message);
        if (elementoNombre) {
            elementoNombre.textContent = 'Servidor Desconectado';
        }
    }
}

// FUNCIÓN AUXILIAR: Obtiene el nombre de un servidor individual
async function obtenerNombreServidor(url) {
    try {
        const datosServidor = await obtenerDatosAPI(url);
        return datosServidor && datosServidor.server_id ? datosServidor.server_id.trim() : null;
    } catch (error) {
        console.log(`No se pudo obtener nombre de ${url}:`, error.message);
        return null;
    }
}

// FUNCIÓN: Actualiza la visualización de un servidor individual
function actualizarVisualServidor(numeroServidor, estaActivo) {
    const tarjetaServidor = numeroServidor === 1 ? tarjetaServidor1 : numeroServidor === 2 ? tarjetaServidor2 : tarjetaServidor3;
    const indicadorEstado = numeroServidor === 1 ? indicadorEstado1 : numeroServidor === 2 ? indicadorEstado2 : indicadorEstado3;
    
    if (!tarjetaServidor || !indicadorEstado) {
        console.error(`No se encontraron elementos para servidor ${numeroServidor}`);
        return;
    }
    
    if (estaActivo) {
        // Servidor UP - verde
        indicadorEstado.textContent = 'UP';
        indicadorEstado.className = 'server-status status-up';
        tarjetaServidor.className = tarjetaServidor.className.replace(/status-down/g, '');
    } else {
        // Servidor DOWN - rojo
        indicadorEstado.textContent = 'DOWN';
        indicadorEstado.className = 'server-status status-down';
        if (!tarjetaServidor.className.includes('status-down')) {
            tarjetaServidor.className += ' status-down';
        }
    }
    
    console.log(`Servidor ${numeroServidor} actualizado: ${estaActivo ? 'UP' : 'DOWN'}`);
}

// FUNCIÓN: Actualiza el medidor de velocidad según disponibilidad
function actualizarMedidorVelocidad(disponibilidad) {
    if (!speedFill || !speedValue || !speedArrow) return;
    
    // Actualizar el texto
    speedValue.textContent = `${disponibilidad}`;
    
    // Actualizar el ancho de la barra
    speedFill.style.width = `${disponibilidad}%`;
    
    // Actualizar colores según nivel
    speedFill.className = 'speed-fill'; // Reset classes
    
    if (disponibilidad <= 33) {
        speedFill.classList.add('low');
    } else if (disponibilidad <= 66) {
        speedFill.classList.add('medium');
    } else {
        speedFill.classList.add('high');
    }
    
    console.log(`Medidor de velocidad actualizado: ${disponibilidad}%`);
}

// FUNCIÓN AUXILIAR: Verifica un servidor individualmente
async function verificarServidorIndividual(url) {
    try {
        const datosServidor = await obtenerDatosAPI(url);
        return datosServidor && datosServidor.status === 'ok';
    } catch (error) {
        console.log(`Servidor en ${url} no responde:`, error.message);
        return false;
    }
}

// FUNCIÓN PRINCIPAL: Bucle infinito que actualiza el dashboard
async function bucleActualizacion() {
    console.log('Iniciando ciclo de actualización...');
    
    try {
        // 1) Verificar qué servidores están activos (esto actualiza la batería automáticamente)
        const estadoServidores = await verificarEstadoServidores();

        console.log('Ciclo de actualización completado');
    } catch (error) {
        console.error('Error en ciclo de actualización:', error);
    }

    // 2) Programar la próxima actualización
    console.log(`Próxima actualización en ${TIEMPO_ACTUALIZACION_MS}ms...`);
    setTimeout(bucleActualizacion, TIEMPO_ACTUALIZACION_MS);
}

console.log('Dashboard script cargado');
