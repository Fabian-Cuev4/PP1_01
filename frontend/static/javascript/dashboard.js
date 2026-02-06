// =============================================================================
// DASHBOARD SIGLAB - Monitoreo de Alta Disponibilidad
// Autor: Estudiante de Programación Avanzada
// Propósito: Verificar estado de servidores y mostrar estadísticas en tiempo real
// =============================================================================

// PROTECCIÓN: Solo el usuario admin puede ver el dashboard
// Usamos sessionStorage para que cada pestaña tenga su propia sesión
// Esto evita que un usuario normal acceda al dashboard del admin
const esUsuarioAdmin = sessionStorage.getItem('is_admin');
if (esUsuarioAdmin !== '1') {
    window.location.href = "http://localhost:8080/pagina/inicio";
}

// CONFIGURACIÓN: Tiempos de actualización y conexión
const TIEMPO_ACTUALIZACION_MS = 1500;  // Cada 1.5 segundos se actualiza
const TIEMPO_ESPERA_API_MS = 200;     // Ultra rápido: 0.2 segundos por petición

// ELEMENTOS DEL DOM: Guardamos referencias para no buscarlas cada vez
const tarjetaServidor1 = document.getElementById('server1');
const tarjetaServidor2 = document.getElementById('server2');
const indicadorEstado1 = document.getElementById('status1');
const indicadorEstado2 = document.getElementById('status2');
const contadorUsuariosTotales = document.getElementById('total-requests');
const contadorServidoresActivos = document.getElementById('active-servers');
const indicadorDisponibilidad = document.getElementById('uptime');

// FUNCIÓN: Actualiza la apariencia visual de las tarjetas de servidor
// Parámetros: numeroServidor (1 o 2), estaActivo (true/false)
function actualizarVisualServidor(numeroServidor, estaActivo) {
    // Seleccionar la tarjeta y el indicador correctos según el número
    const tarjeta = numeroServidor === 1 ? tarjetaServidor1 : tarjetaServidor2;
    const indicador = numeroServidor === 1 ? indicadorEstado1 : indicadorEstado2;

    // Cambiar la barra superior (verde si está activo, rojo si está caído)
    tarjeta.classList.remove('up', 'down');
    tarjeta.classList.add(estaActivo ? 'up' : 'down');

    // Cambiar el badge de estado (UP/DOWN) con colores apropiados
    indicador.classList.remove('status-up', 'status-down');
    indicador.classList.add(estaActivo ? 'status-up' : 'status-down');
    indicador.textContent = estaActivo ? 'UP' : 'DOWN';
}

// FUNCIÓN: Realiza peticiones a la API con timeout para no esperar indefinidamente
// Parámetro: url - La dirección de la API a consultar
// Retorna: Promise con los datos JSON o error si falla
async function obtenerDatosAPI(url) {
    const controlador = new AbortController();
    const temporizador = setTimeout(() => controlador.abort(), TIEMPO_ESPERA_API_MS);
    
    try {
        const respuesta = await fetch(url, {
            cache: 'no-store',  // No usar caché para obtener datos frescos
            signal: controlador.signal,
        });
        
        if (!respuesta.ok) {
            throw new Error(`Error HTTP ${respuesta.status}`);
        }
        
        return await respuesta.json();
    } finally {
        clearTimeout(temporizador);  // Limpiar el timeout siempre
    }
}

// FUNCIÓN: Verifica si los servidores API están activos o caídos
// Ahora usa Promise.all para verificar ambos servidores SIMULTÁNEAMENTE
// Usa las rutas del Load Balancer para verificar servidores reales
// Retorna: Objeto con estado de cada servidor { up1: boolean, up2: boolean }
async function verificarEstadoServidores() {
    // Creamos las promesas para verificar ambos servidores a través del Load Balancer
    const promesaServidor1 = verificarServidorIndividual('/api1/api/health');
    const promesaServidor2 = verificarServidorIndividual('/api2/api/health');
    
    try {
        // Esperamos que terminen ambas al mismo tiempo (máximo 200ms total)
        const [servidor1Activo, servidor2Activo] = await Promise.all([
            promesaServidor1,
            promesaServidor2
        ]);
        
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
// Parámetro: url - La URL del servidor a verificar
// Retorna: Promise<boolean> - true si está activo, false si está caído
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
// Optimización ULTRA: Solo pide estadísticas de servidores que realmente están activos
// Usa las rutas del Load Balancer para obtener datos reales
// Parámetro: estadoServidores - objeto con { up1, up2 } de la función anterior
async function actualizarTotalUsuarios(estadoServidores) {
    // Si no hay servidores activos, ponemos 0 inmediatamente
    if (!estadoServidores.up1 && !estadoServidores.up2) {
        if (contadorUsuariosTotales) {
            contadorUsuariosTotales.textContent = '0';
        }
        return;
    }

    // Creamos un array solo con las promesas de servidores ACTIVOS a través del Load Balancer
    const promesasActivas = [];
    
    if (estadoServidores.up1) {
        promesasActivas.push(obtenerEstadisticasServidor('/api1/api/traffic/stats'));
    }
    
    if (estadoServidores.up2) {
        promesasActivas.push(obtenerEstadisticasServidor('/api2/api/traffic/stats'));
    }
    
    try {
        // Esperamos solo las promesas de servidores activos
        const resultados = await Promise.all(promesasActivas);
        
        // Sumamos los usuarios de los servidores que respondieron
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
        
        // Mostramos el total
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
// Parámetro: url - La URL del servidor a consultar
// Retorna: Promise con los datos o null si hay error
async function obtenerEstadisticasServidor(url) {
    try {
        return await obtenerDatosAPI(url);
    } catch (error) {
        console.log(`No se pudieron obtener estadísticas de ${url}:`, error.message);
        return null;
    }
}

// FUNCIÓN PRINCIPAL: Bucle infinito que actualiza el dashboard
// Se ejecuta cada 1.5 segundos para mantener datos frescos
async function bucleActualizacion() {
    // 1) Verificar qué servidores están activos
    const estadoServidores = await verificarEstadoServidores();

    // 2) Actualizar contador de usuarios totales
    await actualizarTotalUsuarios(estadoServidores);

    // 3) Programar la próxima actualización
    setTimeout(bucleActualizacion, TIEMPO_ACTUALIZACION_MS);
}

// INICIO: Arrancar el monitoreo cuando carga la página
bucleActualizacion();
