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
        self.stats = {}
        self.server_mapping = {}
        self.last_data_time = time.time()
        self.active_servers = set()
        self.dead_servers = set()
        self.current_algorithm = "unknown"  # Se detectará automáticamente
        self.request_sequence = []  # Para seguir el orden de peticiones
        self.server_status = {}  # Nuevo: track status de cada servidor
        self.last_seen = {}  # Nuevo: track última vez visto de cada servidor
        self.app = web.Application()
        self.websockets = set()
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
        
        # Patrón regex para extraer información del log (peticiones y errores)
        log_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+) - - \[.*?\] "POST /api/maquinas/agregar HTTP/1\.\d" (\d{3})'
        error_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+).*?(failed|timeout|connection refused|upstream timed out)'
        
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
                        line = line.strip()
                        match = re.search(log_pattern, line)
                        error_match = re.search(error_pattern, line, re.IGNORECASE)
                        
                        # Detectar errores de conexión inmediatos
                        if error_match:
                            upstream_addr = error_match.group(1)
                            if upstream_addr in self.server_mapping:
                                server_name = self.server_mapping[upstream_addr]
                                if server_name not in self.dead_servers:
                                    self.dead_servers.add(server_name)
                                    self.server_status[server_name] = "dead"
                                    logger.info(f"Servidor caído detectado INMEDIATAMENTE: {server_name} ({upstream_addr})")
                                    
                                    # Enviar actualización de estado inmediata
                                    data = {
                                        'server_ip': upstream_addr,
                                        'server_name': server_name,
                                        'status': 000,
                                        'server_health': 'dead',
                                        'timestamp': time.time(),
                                        'stats': self.stats.copy(),
                                        'total_requests': sum(self.stats.values()),
                                        'server_died': True
                                    }
                                    await self.broadcast(data)
                        
                        # Procesar peticiones normales
                        elif match:
                            groups = match.groups()
                            
                            # Extraer IP y status (solo peticiones normales)
                            upstream_addr = groups[0]
                            status = groups[1]
                            
                            # Mapeo dinámico por IP: si no existe, crear nuevo servidor
                            if upstream_addr not in self.server_mapping:
                                server_name = f"Server_{len(self.server_mapping) + 1}"
                                self.server_mapping[upstream_addr] = server_name
                                self.stats[server_name] = 0
                                self.server_status[server_name] = "alive"  # Nuevo: inicializar status
                                logger.info(f"Nuevo servidor detectado: {upstream_addr} -> {server_name}")
                            else:
                                server_name = self.server_mapping[upstream_addr]
                            
                            # Actualizar última vez visto
                            self.last_seen[upstream_addr] = time.time()
                            
                            # Actualizar estadísticas solo si es status 200
                            if int(status) == 200:
                                self.stats[server_name] += 1
                                # Registrar secuencia para detectar algoritmo
                                self.request_sequence.append(server_name)
                                # Marcar como vivo si estaba muerto
                                if server_name in self.dead_servers:
                                    self.dead_servers.remove(server_name)
                                    self.server_status[server_name] = "alive"
                                    logger.info(f"Servidor revivido: {server_name}")
                            
                            # Actualizar tiempo de última actividad
                            self.last_data_time = time.time()
                            
                            # Enviar datos a clientes con status del servidor
                            data = {
                                'server_ip': upstream_addr,
                                'server_name': server_name,
                                'status': int(status),
                                'server_health': self.server_status.get(server_name, "alive"),
                                'timestamp': time.time(),
                                'stats': self.stats.copy(),
                                'total_requests': sum(self.stats.values())
                            }
                            
                            await self.broadcast(data)
                            logger.info(f"Petición detectada: {server_name} ({upstream_addr}) - Status: {status}")
                            
            except Exception as e:
                logger.error(f"Error leyendo log: {e}")
                await asyncio.sleep(5)
    
    async def monitor_server_health(self):
        """Monitorear salud de servidores detectando cuáles no aparecen en logs"""
        while True:
            await asyncio.sleep(3)  # Revisar cada 3 segundos (más reactivo)
            
            current_time = time.time()
            
            # Verificar servidores conocidos que no han aparecido recientemente
            for upstream_addr, server_name in list(self.server_mapping.items()):
                last_seen_time = self.last_seen.get(upstream_addr, 0)
                
                if current_time - last_seen_time > 5:  # 5 segundos sin actividad (más rápido)
                    if server_name not in self.dead_servers:
                        self.dead_servers.add(server_name)
                        self.server_status[server_name] = "dead"
                        logger.info(f"Servidor caído detectado: {server_name} ({upstream_addr})")
                        
                        # Enviar actualización de estado inmediata
                        data = {
                            'server_ip': upstream_addr,
                            'server_name': server_name,
                            'status': 000,  # Código especial para caído
                            'server_health': 'dead',
                            'timestamp': current_time,
                            'stats': self.stats.copy(),
                            'total_requests': sum(self.stats.values()),
                            'server_died': True
                        }
                        await self.broadcast(data)
    
    def redistribuir_segun_algoritmo(self, servidor_caído, peticiones_a_redistribuir, servidores_activos):
        """Redistribuir peticiones analizando el patrón de distribución actual"""
        
        # Analizar el patrón de distribución real de las últimas peticiones
        patron_distribucion = self.analizar_patron_distribucion(servidores_activos)
        
        if patron_distribucion["tipo"] == "ciclico_uniforme":
            # Round Robin: distribuir equitativamente
            self.redistribuir_round_robin(servidor_caído, peticiones_a_redistribuir, servidores_activos)
        
        elif patron_distribucion["tipo"] == "pesado":
            # Weighted: distribuir según pesos detectados
            self.redistribuir_weighted(servidor_caído, peticiones_a_redistribuir, servidores_activos, patron_distribucion["pesos"])
        
        elif patron_distribucion["tipo"] == "hash":
            # Hash: todo a un solo servidor
            self.redistribuir_hash(servidor_caído, peticiones_a_redistribuir, servidores_activos)
        
        elif patron_distribucion["tipo"] == "least_conn":
            # Least Connections: al menos cargado
            self.redistribuir_least_connections(servidor_caído, peticiones_a_redistribuir, servidores_activos)
        
        else:
            # Patrón desconocido: redistribución proporcional
            self.redistribuir_proporcional(servidor_caído, peticiones_a_redistribuir, servidores_activos)
    
    def analizar_patron_distribucion(self, servidores_activos):
        """Analiza el patrón de distribución real de las últimas peticiones"""
        
        if len(self.request_sequence) < 10:
            return {"tipo": "desconocido", "pesos": {}}
        
        # Analizar últimas 20 peticiones o todas si hay menos
        ultimas_peticiones = self.request_sequence[-20:]
        
        # Contar frecuencia de cada servidor
        frecuencia = {}
        for servidor in ultimas_peticiones:
            if servidor in servidores_activos:
                frecuencia[servidor] = frecuencia.get(servidor, 0) + 1
        
        if not frecuencia:
            return {"tipo": "desconocido", "pesos": {}}
        
        # Detectar patrón Hash: un servidor domina (>80%)
        max_freq = max(frecuencia.values())
        total_peticiones = sum(frecuencia.values())
        
        if max_freq / total_peticiones > 0.8:
            return {"tipo": "hash", "servidor_dominante": max(frecuencia, key=frecuencia.get)}
        
        # Detectar patrón Round Robin: distribución uniforme
        valores = list(frecuencia.values())
        if len(valores) > 1:
            diferencia_max_min = max(valores) - min(valores)
            if diferencia_max_min <= 1:  # Diferencia máxima de 1 petición
                return {"tipo": "ciclico_uniforme", "pesos": frecuencia}
        
        # Detectar patrón Weighted: diferencias consistentes
        if len(valores) >= 2:
            # Verificar si hay proporciones consistentes
            min_val = min(valores)
            if min_val > 0:
                proporciones = [v / min_val for v in valores]
                # Si las proporciones son números enteros o casi enteros
                if all(abs(p - round(p)) < 0.1 for p in proporciones):
                    pesos_enteros = {k: int(round(v/min_val)) for k, v in frecuencia.items()}
                    return {"tipo": "pesado", "pesos": pesos_enteros}
        
        # Si no hay patrón claro, asumir Least Connections
        return {"tipo": "least_conn", "pesos": frecuencia}
    
    def redistribuir_round_robin(self, servidor_caído, peticiones_a_redistribuir, servidores_activos):
        """Redistribución equitativa para Round Robin"""
        total_activos = len(servidores_activos)
        base = peticiones_a_redistribuir // total_activos
        remainder = peticiones_a_redistribuir % total_activos
        
        for i, servidor in enumerate(servidores_activos):
            extra = base + (1 if i < remainder else 0)
            self.stats[servidor] += extra
            
        logger.info(f"Patrón: Round Robin - Redistribuidas {peticiones_a_redistribuir} peticiones de {servidor_caído} equitativamente entre {total_activos} servidores")
    
    def redistribuir_weighted(self, servidor_caído, peticiones_a_redistribuir, servidores_activos, pesos_detectados):
        """Redistribución según pesos detectados"""
        total_peso = sum(pesos_detectados.get(s, 1) for s in servidores_activos)
        
        for servidor in servidores_activos:
            peso = pesos_detectados.get(servidor, 1)
            proporcion = peso / total_peso
            adicionales = int(peticiones_a_redistribuir * proporcion)
            self.stats[servidor] += adicionales
        
        logger.info(f"Patrón: Weighted - Redistribuidas {peticiones_a_redistribuir} peticiones de {servidor_caído} según pesos detectados {pesos_detectados}")
    
    def redistribuir_hash(self, servidor_caído, peticiones_a_redistribuir, servidores_activos):
        """Redistribución para Hash: todo al servidor más frecuente"""
        if servidores_activos:
            # Encontrar el servidor que más recibe peticiones (simulando el hash)
            frecuencias = {}
            for servidor in self.request_sequence[-50:]:  # Últimas 50 peticiones
                if servidor in servidores_activos:
                    frecuencias[servidor] = frecuencias.get(servidor, 0) + 1
            
            if frecuencias:
                servidor_hash = max(frecuencias, key=frecuencias.get)
                self.stats[servidor_hash] += peticiones_a_redistribuir
                logger.info(f"Patrón: Hash - Redistribuidas {peticiones_a_redistribuir} peticiones de {servidor_caído} a {servidor_hash}")
            else:
                # Fallback: primer servidor activo
                self.stats[servidores_activos[0]] += peticiones_a_redistribuir
    
    def redistribuir_least_connections(self, servidor_caído, peticiones_a_redistribuir, servidores_activos):
        """Redistribución para Least Connections: al servidor con menos carga"""
        if servidores_activos:
            servidor_menos_cargado = min(servidores_activos, key=lambda s: self.stats[s])
            self.stats[servidor_menos_cargado] += peticiones_a_redistribuir
            logger.info(f"Patrón: Least Connections - Redistribuidas {peticiones_a_redistribuir} peticiones de {servidor_caído} a {servidor_menos_cargado} (menos cargado)")
    
    def redistribuir_proporcional(self, servidor_caído, peticiones_a_redistribuir, servidores_activos):
        """Redistribución proporcional genérica"""
        total_peso = sum(self.stats[s] for s in servidores_activos)
        
        if total_peso > 0:
            for servidor in servidores_activos:
                peso = self.stats[servidor]
                proporcion = peso / total_peso
                adicionales = int(peticiones_a_redistribuir * proporcion)
                self.stats[servidor] += adicionales
            
            # Distribuir residuo
            redistribuidas = sum(int(self.stats[s] * peticiones_a_redistribuir / total_peso) for s in servidores_activos)
            residuo = peticiones_a_redistribuir - redistribuidas
            
            for i, servidor in enumerate(servidores_activos[:residuo]):
                self.stats[servidor] += 1
                
            logger.info(f"Patrón: Proporcional - Redistribuidas {peticiones_a_redistribuir} peticiones de {servidor_caído} proporcionalmente")
        else:
            # Si todos en 0, distribuir equitativamente
            total_activos = len(servidores_activos)
            base = peticiones_a_redistribuir // total_activos
            remainder = peticiones_a_redistribuir % total_activos
            
            for i, servidor in enumerate(servidores_activos):
                extra = base + (1 if i < remainder else 0)
                self.stats[servidor] += extra
    
                    
    async def reset_checker(self):
        """Verificar si hay que resetear estadísticas por inactividad"""
        while True:
            await asyncio.sleep(1)
            
            # Si pasan 7 segundos sin datos, resetear
            if time.time() - self.last_data_time > 7:
                if any(self.stats.values()):  # Solo si hay datos que limpiar
                    # Limpiar servidores que no tienen estadísticas
                    active_servers = {k: v for k, v in self.stats.items() if v > 0}
                    self.stats = {k: 0 for k in active_servers}
                    
                    await self.broadcast({
                        'reset': True,
                        'stats': self.stats.copy(),
                        'total_requests': 0
                    })
                    logger.info("Estadísticas reseteadas por inactividad")
                    
    async def start_background_tasks(self):
        """Iniciar tareas en segundo plano"""
        asyncio.create_task(self.watch_log_file())
        asyncio.create_task(self.reset_checker())
        asyncio.create_task(self.monitor_server_health())
        
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
