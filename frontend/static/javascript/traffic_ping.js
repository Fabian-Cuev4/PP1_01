(function () {
    try {
        const isAdmin = sessionStorage.getItem('is_admin');
        if (isAdmin === '1') {
            return;
        }

        const username = sessionStorage.getItem('username') || '';
        if (!username || username === 'admin') {
            return;
        }

        // Evitar múltiples pestañas del mismo usuario enviando pings
        const pingKey = `ping_${username}`;
        const now = Date.now();
        const lastPing = parseInt(sessionStorage.getItem(pingKey) || '0');
        // Solo permitir un ping cada 15 segundos por pestaña para evitar duplicados
        if (now - lastPing < 15000) {
            return;
        }
        sessionStorage.setItem(pingKey, now.toString());

        function jitter(minMs, maxMs) {
            return Math.floor(minMs + Math.random() * (maxMs - minMs));
        }

        async function pingOnce() {
            try {
                await fetch(`/api/traffic/ping?username=${encodeURIComponent(username)}&is_admin=0`, {
                    method: 'POST',
                    cache: 'no-store'
                });
            } catch (e) {
            }
        }

        pingOnce();

        const base = jitter(1200, 2600);
        setInterval(pingOnce, base);

        document.addEventListener('click', () => {
            pingOnce();
        });

        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                pingOnce();
            }
        });
    } catch (e) {
    }
})();
