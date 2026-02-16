const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const axios = require('axios');
const { Kafka } = require('kafkajs');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

const PORT = process.env.PORT || 3000;
const KAFKA_BROKER = process.env.KAFKA_BROKER || 'localhost:9092';
const NGINX_STATS_URL = process.env.NGINX_STATS_URL || 'http://localhost:8080/nginx_status';

// Configuración Kafka
const kafka = new Kafka({
  clientId: 'dashboard',
  brokers: [KAFKA_BROKER]
});

const consumer = kafka.consumer({ groupId: 'dashboard-group' });

// Estado de servidores
let serverStats = {
  'backend-1': { requests: 0, active: true, responseTime: 0, errors: 0 },
  'backend-2': { requests: 0, active: true, responseTime: 0, errors: 0 },
  'backend-3': { requests: 0, active: true, responseTime: 0, errors: 0 }
};

// Servir archivos estáticos
app.use(express.static('public'));

// API endpoint para obtener estadísticas
app.get('/api/stats', (req, res) => {
  res.json(serverStats);
});

// API endpoint para obtener stats de Nginx
app.get('/api/nginx-stats', async (req, res) => {
  try {
    const response = await axios.get(NGINX_STATS_URL);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Error obteniendo stats de Nginx' });
  }
});

// WebSocket para actualizaciones en tiempo real
io.on('connection', (socket) => {
  console.log('Cliente conectado al dashboard');
  
  // Enviar estadísticas actuales
  socket.emit('stats', serverStats);
  
  socket.on('disconnect', () => {
    console.log('Cliente desconectado del dashboard');
  });
});

// Función para actualizar estadísticas
function updateStats(serverId, requests, responseTime, status) {
  if (serverStats[serverId]) {
    serverStats[serverId].requests += requests;
    serverStats[serverId].responseTime = responseTime;
    serverStats[serverId].active = status < 500;
    if (status >= 500) {
      serverStats[serverId].errors++;
    }
    
    // Emitir a todos los clientes conectados
    io.emit('stats', serverStats);
  }
}

// Consumir eventos de Kafka
async function startKafkaConsumer() {
  try {
    await consumer.connect();
    await consumer.subscribe({ topic: 'load-balancer-events', fromBeginning: false });
    
    await consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        const event = JSON.parse(message.value.toString());
        console.log('Evento recibido:', event);
        
        // Actualizar estadísticas basadas en el evento
        const serverId = event.serverId || 'backend-1';
        updateStats(serverId, 1, event.responseTime || 0, event.status || 200);
      },
    });
  } catch (error) {
    console.error('Error en consumidor Kafka:', error);
    // Reintentar conexión
    setTimeout(startKafkaConsumer, 5000);
  }
}

// Simulación de datos para demostración
function simulateData() {
  const servers = ['backend-1', 'backend-2', 'backend-3'];
  
  setInterval(() => {
    servers.forEach(serverId => {
      const randomRequests = Math.floor(Math.random() * 10);
      const randomResponseTime = Math.random() * 200;
      const randomStatus = Math.random() > 0.95 ? 500 : 200;
      
      if (randomRequests > 0) {
        updateStats(serverId, randomRequests, randomResponseTime, randomStatus);
      }
    });
  }, 2000);
}

// Iniciar servidor
server.listen(PORT, () => {
  console.log(`Dashboard corriendo en puerto ${PORT}`);
  
  // Iniciar consumidor Kafka
  startKafkaConsumer();
  
  // Iniciar simulación para demostración
  simulateData();
});
