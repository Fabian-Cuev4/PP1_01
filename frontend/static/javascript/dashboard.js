// =============================================================================
// DASHBOARD SIGLAB - Monitoreo de Alta Disponibilidad con Datos de Máquinas
// Autor: Sistema SIGLAB con Redis Cache y Polling
// Propósito: Verificar estado de servidores Y mostrar estadísticas de máquinas en tiempo real
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

// ELEMENTOS DEL DOM: Estadísticas de máquinas (NUEVOS)
let dashboardMaquinas = null; // Se creará dinámicamente
let totalMaquinasElement = null;
let maquinasPorEstadoElement = null;

// Cache para datos de máquinas
let datosMaquinasCache = {
    total_maquinas: 0,
    maquinas_por_estado: {},
    maquinas_por_tipo: {},
    maquinas_por_area: {},
    timestamp: null
};

// INICIALIZACIÓN: Crear elementos para estadísticas de máquinas
document.addEventListener('DOMContentLoaded', () => {
    console.log('Dashboard cargado, iniciando configuración...');
    crearSeccionMaquinas();
    bucleActualizacion();
});

// FUNCIÓN: Crear la sección de estadísticas de máquinas en el dashboard
function crearSeccionMaquinas() {
    console.log('Creando sección de máquinas...');
    const dashboardGrid = document.querySelector('.dashboard-grid');
    if (!dashboardGrid) {
        console.error('No se encontró .dashboard-grid');
        return;
    }

    console.log('Dashboard grid encontrado, creando tarjeta de máquinas...');

    // Crear tarjeta para estadísticas de máquinas
    const maquinasCard = document.createElement('div');
    maquinasCard.className = 'server-card maquinas-stats-card';
    maquinasCard.innerHTML = `
        <div class="server-header">
            <div class="server-name">Estadísticas de Máquinas</div>
        </div>
        <div class="maquinas-stats-content">
            <div class="stats-grid-horizontal">
                <div class="stat-item">
                    <div class="stat-value" id="total-maquinas">0</div>
                    <div class="stat-label">Total Máquinas</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="maquinas-operativas">0</div>
                    <div class="stat-label">Operativas</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="maquinas-mantenimiento">0</div>
                    <div class="stat-label">Mantenimiento</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="maquinas-fuera-servicio">0</div>
                    <div class="stat-label">Fuera de Servicio</div>
                </div>
            </div>
            
            <div class="last-update">
                <small>Última actualización: <span id="maquinas-timestamp">--:--:--</span></small>
            </div>
        </div>
    `;

    // Insertar después de la tarjeta del Load Balancer
    const loadBalancerCard = document.querySelector('.load-balancer-card');
    if (loadBalancerCard) {
        loadBalancerCard.parentNode.insertBefore(maquinasCard, loadBalancerCard.nextSibling);
        console.log('Tarjeta de máquinas insertada correctamente después del Load Balancer');
    } else {
        console.error('No se encontró .load-balancer-card, insertando al final del grid');
        dashboardGrid.appendChild(maquinasCard);
    }

    // Guardar referencias a los elementos
    totalMaquinasElement = document.getElementById('total-maquinas');
    maquinasPorEstadoElement = {
        operativas: document.getElementById('maquinas-operativas'),
        mantenimiento: document.getElementById('maquinas-mantenimiento'),
        fueraServicio: document.getElementById('maquinas-fuera-servicio')
    };

    console.log('Elementos de máquinas guardados:', {
        totalMaquinasElement,
        maquinasPorEstadoElement
    });
}

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

// FUNCIÓN: Obtiene datos del dashboard de máquinas usando el endpoint de polling
async function obtenerDatosMaquinas() {
    try {
        const response = await obtenerDatosAPI('/api/maquinas/polling/dashboard');
        
        if (response.status === 'ok') {
            datosMaquinasCache = {
                total_maquinas: response.total_maquinas || 0,
                maquinas_por_estado: response.maquinas_por_estado || {},
                maquinas_por_tipo: response.maquinas_por_tipo || {},
                maquinas_por_area: response.maquinas_por_area || {},
                timestamp: response.timestamp
            };
            
            actualizarInterfazMaquinas();
            return true;
        } else {
            console.error('Error en respuesta de máquinas:', response.mensaje);
            return false;
        }
    } catch (error) {
        console.error('Error obteniendo datos de máquinas:', error);
        return false;
    }
}

// FUNCIÓN: Actualiza la interfaz con los datos de máquinas
function actualizarInterfazMaquinas() {
    if (!totalMaquinasElement) {
        console.error('Elementos de máquinas no encontrados');
        return;
    }

    console.log('Actualizando interfaz de máquinas con:', datosMaquinasCache);

    // Actualizar total de máquinas
    totalMaquinasElement.textContent = String(datosMaquinasCache.total_maquinas);

    // Actualizar máquinas por estado
    const estado = datosMaquinasCache.maquinas_por_estado;
    if (maquinasPorEstadoElement.operativas) {
        maquinasPorEstadoElement.operativas.textContent = String(estado.Operativa || estado.operativa || 0);
    }
    if (maquinasPorEstadoElement.mantenimiento) {
        maquinasPorEstadoElement.mantenimiento.textContent = String(estado.Mantenimiento || estado.mantenimiento || 0);
    }
    if (maquinasPorEstadoElement.fueraServicio) {
        maquinasPorEstadoElement.fueraServicio.textContent = String(estado['Fuera de Servicio'] || estado.fuera_servicio || 0);
    }

    // Actualizar timestamp
    const timestampElement = document.getElementById('maquinas-timestamp');
    if (timestampElement && datosMaquinasCache.timestamp) {
        const fecha = new Date(datosMaquinasCache.timestamp);
        timestampElement.textContent = fecha.toLocaleTimeString();
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

// FUNCIÓN: Obtiene el total de usuarios activos en ambos servidores
async function actualizarTotalUsuarios(estadoServidores) {
    if (!estadoServidores.up1 && !estadoServidores.up2) {
        if (contadorUsuariosTotales) {
            contadorUsuariosTotales.textContent = '0';
        }
        return;
    }

    const promesasActivas = [];
    
    if (estadoServidores.up1) {
        promesasActivas.push(obtenerEstadisticasServidor('/api1/api/traffic/stats'));
    }
    
    if (estadoServidores.up2) {
        promesasActivas.push(obtenerEstadisticasServidor('/api2/api/traffic/stats'));
    }
    
    try {
        const resultados = await Promise.all(promesasActivas);
        
        let totalUsuarios = 0;
        
        if (estadoServidores.up1 && resultados[0]) {
            totalUsuarios += (typeof resultados[0].active_users === 'number') ? resultados[0].active_users : 0;
        }
        
        if (estadoServidores.up2) {
            const indexServidor2 = estadoServidores.up1 ? 1 : 0;
            if (resultados[indexServidor2]) {
                totalUsuarios += (typeof resultados[indexServidor2].active_users === 'number') ? resultados[indexServidor2].active_users : 0;
            }
        }
        
        if (contadorUsuariosTotales) {
            contadorUsuariosTotales.textContent = String(totalUsuarios);
        }
    } catch (error) {
        console.error('Error obteniendo estadísticas:', error);
        if (contadorUsuariosTotales) {
            contadorUsuariosTotales.textContent = '0';
        }
    }
}

// FUNCIÓN AUXILIAR: Obtiene estadísticas de un servidor
async function obtenerEstadisticasServidor(url) {
    try {
        return await obtenerDatosAPI(url);
    } catch (error) {
        console.log(`No se pudieron obtener estadísticas de ${url}:`, error.message);
        return null;
    }
}

// FUNCIÓN PRINCIPAL: Bucle infinito que actualiza el dashboard
async function bucleActualizacion() {
    console.log('Iniciando ciclo de actualización...');
    
    // 1) Verificar qué servidores están activos
    const estadoServidores = await verificarEstadoServidores();

    // 2) Actualizar contador de usuarios totales
    await actualizarTotalUsuarios(estadoServidores);

    // 3) NUEVO: Obtener datos de máquinas en tiempo real
    await obtenerDatosMaquinas();

    // 4) Programar la próxima actualización
    console.log(`Próxima actualización en ${TIEMPO_ACTUALIZACION_MS}ms...`);
    setTimeout(bucleActualizacion, TIEMPO_ACTUALIZACION_MS);
}

console.log('Dashboard script cargado');
