// =============================================================================
// DASHBOARD SIGLAB - Monitoreo de Alta Disponibilidad
// Autor: Sistema SIGLAB
// Propósito: Verificar estado de servidores API y mostrar estadísticas básicas
// =============================================================================

// CONFIGURACIÓN: Tiempos de actualización y conexión
const TIEMPO_ACTUALIZACION_MS = 3000;  // Cada 3 segundos se actualiza
const TIEMPO_ESPERA_API_MS = 2000;     // 2 segundos timeout por petición

// ELEMENTOS DEL DOM: Servidores y tráfico
const tarjetaServidor1 = document.getElementById('server1');
const tarjetaServidor2 = document.getElementById('server2');
const indicadorEstado1 = document.getElementById('status1');
const indicadorEstado2 = document.getElementById('status2');
const contadorUsuariosTotales = document.getElementById('total-requests');
const contadorServidoresActivos = document.getElementById('active-servers');
const indicadorDisponibilidad = document.getElementById('uptime');

// INICIALIZACIÓN: Iniciar el dashboard
document.addEventListener('DOMContentLoaded', () => {
    console.log('Dashboard cargado, iniciando monitoreo...');
    bucleActualizacion();
});

// FUNCIÓN: Realiza peticiones a la API con timeout
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

// FUNCIÓN: Verifica si los servidores API están activos o caídos
async function verificarEstadoServidores() {
    console.log('Verificando estado de servidores...');
    
    const promesaServidor1 = verificarServidorIndividual('/api1/api/health');
    const promesaServidor2 = verificarServidorIndividual('/api2/api/health');
    
    try {
        const [servidor1Activo, servidor2Activo] = await Promise.all([
            promesaServidor1,
            promesaServidor2
        ]);
        
        console.log(`Estado servidores - Servidor 1: ${servidor1Activo}, Servidor 2: ${servidor2Activo}`);
        
        // Actualizar la interfaz visual
        actualizarVisualServidor(1, servidor1Activo);
        actualizarVisualServidor(2, servidor2Activo);

        // Calcular y mostrar estadísticas
        const servidoresActivos = (servidor1Activo ? 1 : 0) + (servidor2Activo ? 1 : 0);
        if (contadorServidoresActivos) {
            contadorServidoresActivos.textContent = String(servidoresActivos);
        }

        // Calcular porcentaje de disponibilidad
        const porcentajeDisponibilidad = (servidoresActivos / 2) * 100;
        if (indicadorDisponibilidad) {
            indicadorDisponibilidad.textContent = `${porcentajeDisponibilidad.toFixed(0)}%`;
        }

        return { up1: servidor1Activo, up2: servidor2Activo };
    } catch (error) {
        console.error('Error verificando servidores:', error);
        return { up1: false, up2: false };
    }
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

// FUNCIÓN: Obtiene el total de usuarios activos (simulado para demostración)
async function actualizarTotalUsuarios(estadoServidores) {
    if (!estadoServidores.up1 && !estadoServidores.up2) {
        if (contadorUsuariosTotales) {
            contadorUsuariosTotales.textContent = '0';
        }
        return;
    }

    // Simular usuarios activos basado en los servidores activos
    // En un sistema real, esto vendría de una API real
    try {
        let totalUsuarios = 0;
        
        if (estadoServidores.up1) {
            // Simular entre 50-150 usuarios por servidor activo
            totalUsuarios += Math.floor(Math.random() * 100) + 50;
        }
        
        if (estadoServidores.up2) {
            // Simular entre 50-150 usuarios por servidor activo
            totalUsuarios += Math.floor(Math.random() * 100) + 50;
        }
        
        if (contadorUsuariosTotales) {
            contadorUsuariosTotales.textContent = String(totalUsuarios);
        }
        
        console.log(`Usuarios actualizados: ${totalUsuarios}`);
    } catch (error) {
        console.error('Error simulando usuarios:', error);
        if (contadorUsuariosTotales) {
            contadorUsuariosTotales.textContent = '0';
        }
    }
}

// FUNCIÓN PRINCIPAL: Bucle infinito que actualiza el dashboard
async function bucleActualizacion() {
    console.log('Iniciando ciclo de actualización...');
    
    try {
        // 1) Verificar qué servidores están activos
        const estadoServidores = await verificarEstadoServidores();

        // 2) Actualizar contador de usuarios totales
        await actualizarTotalUsuarios(estadoServidores);

        console.log('Ciclo de actualización completado');
    } catch (error) {
        console.error('Error en ciclo de actualización:', error);
    }

    // 3) Programar la próxima actualización
    console.log(`Próxima actualización en ${TIEMPO_ACTUALIZACION_MS}ms...`);
    setTimeout(bucleActualizacion, TIEMPO_ACTUALIZACION_MS);
}

console.log('Dashboard script cargado');
