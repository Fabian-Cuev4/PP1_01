// Sistema de pings para tracking de usuarios activos
// Sistema desactivado - ya no se usa traffic/login

(function () {
    try {
        const isAdmin = sessionStorage.getItem('is_admin');
        if (isAdmin === '1') return;

        const username = sessionStorage.getItem('username') || '';
        if (!username || username === 'admin') return;

        // Sistema desactivado - ya no se hace ping al servidor
        console.log(`Sistema de pings desactivado para usuario: ${username}`);
        
        // Opcional: mantener pings locales si se necesita
        const pingKey = `ping_${username}`;
        const now = Date.now();
        const lastPing = parseInt(sessionStorage.getItem(pingKey) || '0');
        if (now - lastPing < 15000) return;
        sessionStorage.setItem(pingKey, now.toString());
        
        function jitter(minMs, maxMs) {
            return Math.floor(minMs + Math.random() * (maxMs - minMs));
        }

        async function pingOnce() {
            // Ping desactivado - ya no se llama al servidor
            console.log('Ping desactivado - no se contacta al servidor');
        }

        // Sistema desactivado - no se inicia polling
        console.log('Sistema de pings completamente desactivado');
        
    } catch (e) {
        console.log('Error en sistema de pings:', e);
    }
})();
