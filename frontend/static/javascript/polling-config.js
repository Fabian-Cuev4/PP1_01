// Configuración de polling para actualizaciones en tiempo real
// Define intervalos y endpoints para polling del frontend

const POLLING_CONFIG = {
    // Intervalos en milisegundos
    INTERVALOS: {
        RAPIDO: 2000,      // 2 segundos para datos críticos
        NORMAL: 5000,     // 5 segundos para datos normales
        LENTO: 10000      // 10 segundos para datos secundarios
    },
    
    // Endpoints para polling
    ENDPOINTS: {
        MAQUINAS: {
            LISTAR: "/api/maquinas/listar?polling=true",
            DASHBOARD: "/api/maquinas/polling/dashboard",
            BUSCAR: "/api/maquinas/polling/buscar"
        },
        MANTENIMIENTO: {
            HISTORIAL: "/api/mantenimiento/listar/{codigo}?polling=true",
            INFORME: "/api/mantenimiento/informe-general?polling=true",
            INFORME_ESTADISTICAS: "/api/mantenimiento/polling/informe"
        },
        SISTEMA: {
            HEALTH: "/api/health",
            CACHE_STATUS: "/api/maquinas/cache/status"
        }
    }
};