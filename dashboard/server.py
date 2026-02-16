#!/usr/bin/env python3
"""
Dashboard de monitoreo para SIGLAB - Servidor WebSocket
Monitorea las peticiones al endpoint /api/maquinas/agregar
"""

import asyncio
import json
import re
import time
from pathlib import Path
from aiohttp import web, WSMsgType
import aiofiles
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DashboardServer:
    def __init__(self):
        self.app = web.Application()
        self.websockets = set()
        self.last_data_time = time.time()
        self.server_mapping = {
            '172.19.0.6:8000': 'Backend 1',  # pp1_01-backend-1
            '172.19.0.5:8000': 'Backend 2',  # pp1_01-backend-2
            '172.19.0.4:8000': 'Backend 3'   # pp1_01-backend-3
        }
        self.stats = {
            'Backend 1': 0,
            'Backend 2': 0,
            'Backend 3': 0
        }
        self.setup_routes()
        
    def setup_routes(self):
        """Configurar rutas HTTP y WebSocket"""
        self.app.router.add_get('/', self.index_handler)
        self.app.router.add_get('/ws', self.websocket_handler)
        self.app.router.add_static('/', path='.', name='static')
        
    async def index_handler(self, request):
        """Servir página principal"""
        return web.FileResponse('index.html')
        
    async def websocket_handler(self, request):
        """Manejar conexiones WebSocket"""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        self.websockets.add(ws)
        logger.info(f"Nuevo cliente conectado. Total: {len(self.websockets)}")
        
        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    # Podríamos implementar comandos desde el cliente aquí
                    pass
                elif msg.type == WSMsgType.ERROR:
                    logger.error(f'WebSocket error: {ws.exception()}')
        except Exception as e:
            logger.error(f"Error en WebSocket: {e}")
        finally:
            self.websockets.discard(ws)
            logger.info(f"Cliente desconectado. Total: {len(self.websockets)}")
            
        return ws
        
    async def broadcast(self, data):
        """Enviar datos a todos los clientes WebSocket conectados"""
        if not self.websockets:
            return
            
        message = json.dumps(data)
        disconnected = set()
        
        for ws in self.websockets:
            try:
                await ws.send_str(message)
            except Exception as e:
                logger.error(f"Error enviando a cliente: {e}")
                disconnected.add(ws)
                
        # Limpiar conexiones rotas
        self.websockets -= disconnected
        
    async def watch_log_file(self):
        """Monitorear archivo de log en tiempo real"""
        log_path = '/var/log/nginx/balanceo_siglab.log'
        
        # Esperar a que el archivo exista
        while not Path(log_path).exists():
            logger.info(f"Esperando archivo de log: {log_path}")
            await asyncio.sleep(2)
            
        logger.info(f"Monitoreando log: {log_path}")
        
        # Patrón regex para extraer información del log
        log_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+) - - \[.*?\] "POST /api/maquinas/agregar HTTP/1\.\d" (\d{3})'
        
        while True:
            try:
                async with aiofiles.open(log_path, 'r') as f:
                    # Ir al final del archivo
                    await f.seek(0, 2)
                    
                    while True:
                        line = await f.readline()
                        if not line:
                            await asyncio.sleep(0.1)
                            continue
                            
                        # Procesar línea del log
                        match = re.search(log_pattern, line.strip())
                        if match:
                            upstream_addr, status = match.groups()
                            
                            # Mapear dirección a nombre de servidor
                            server_name = self.server_mapping.get(upstream_addr, 'Desconocido')
                            
                            # Actualizar estadísticas
                            if server_name in self.stats:
                                self.stats[server_name] += 1
                            
                            # Actualizar tiempo de última actividad
                            self.last_data_time = time.time()
                            
                            # Enviar datos a clientes
                            data = {
                                'server_id': server_name,
                                'status': int(status),
                                'timestamp': time.time(),
                                'stats': self.stats.copy()
                            }
                            
                            await self.broadcast(data)
                            logger.info(f"Petición detectada: {server_name} - Status: {status}")
                            
            except Exception as e:
                logger.error(f"Error leyendo log: {e}")
                await asyncio.sleep(5)
                
    async def reset_checker(self):
        """Verificar si hay que resetear estadísticas por inactividad"""
        while True:
            await asyncio.sleep(1)
            
            # Si pasan 7 segundos sin datos, resetear
            if time.time() - self.last_data_time > 7:
                if any(self.stats.values()):  # Solo si hay datos que limpiar
                    self.stats = {k: 0 for k in self.stats}
                    await self.broadcast({
                        'reset': True,
                        'stats': self.stats.copy()
                    })
                    logger.info("Estadísticas reseteadas por inactividad")
                    
    async def start_background_tasks(self):
        """Iniciar tareas en segundo plano"""
        asyncio.create_task(self.watch_log_file())
        asyncio.create_task(self.reset_checker())
        
    async def start(self):
        """Iniciar servidor"""
        await self.start_background_tasks()
        
        runner = web.AppRunner(self.app)
        await runner.setup()
        
        # HTTP para el frontend
        site_http = web.TCPSite(runner, '0.0.0.0', 18081)
        await site_http.start()
        
        # WebSocket nativo en puerto 8001
        site_ws = web.TCPSite(runner, '0.0.0.0', 8001)
        await site_ws.start()
        
        logger.info("Dashboard iniciado:")
        logger.info("  - HTTP: http://0.0.0.0:18081")
        logger.info("  - WebSocket: ws://0.0.0.0:8001/ws")
        
        return runner

if __name__ == '__main__':
    server = DashboardServer()
    
    async def main():
        runner = await server.start()
        
        try:
            # Mantener el servidor corriendo
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Apagando servidor...")
        finally:
            await runner.cleanup()
            
    asyncio.run(main())
