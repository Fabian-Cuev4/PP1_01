// Script k6 para agregar máquinas - Configurable con variables

import http from 'k6/http';
import { sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://nginx_balancer:80';

// Variables configurables
const MACHINES_PER_GROUP = 20;  // Máquinas por grupo
const PAUSE_BETWEEN_MACHINES = 1;  // Segundos entre máquinas
const REST_BETWEEN_GROUPS = 10;  // Segundos de reposo (reducido para prueba)
const TOTAL_GROUPS = 2;  // Número de grupos

// Contador global para numeración secuencial
let machineCounter = 1;

// Generar datos de máquina válidos
function generateMaquinaData() {
  const tipos = ['PC', 'IMP'];  // Tipos que espera el backend
  const estados = ['Operativo', 'Mantenimiento', 'Dañado'];
  const areas = ['IT', 'Ventas', 'Marketing', 'RH', 'Finanzas'];
  
  // Generar código único con timestamp para evitar duplicados
  const timestamp = Date.now();
  const codigoSecuencial = `TM-${timestamp}-${String(machineCounter).padStart(3, '0')}`;
  machineCounter++; // Incrementar contador para próxima máquina
  
  // Formato de fecha compatible: YYYY-MM-DD
  const today = new Date();
  const fechaFormateada = today.toISOString().split('T')[0];
  
  return {
    codigo_equipo: codigoSecuencial,
    tipo_equipo: tipos[Math.floor(Math.random() * tipos.length)],
    estado_actual: estados[Math.floor(Math.random() * estados.length)],
    area: areas[Math.floor(Math.random() * areas.length)],
    fecha: fechaFormateada
    // Quitamos el campo usuario para evitar problemas
  };
}

export default function () {
  // Headers simples sin autenticación
  const headers = {
    'Content-Type': 'application/json',
  };
  
  for (let group = 1; group <= TOTAL_GROUPS; group++) {
    console.log(`Iniciando grupo ${group} de ${MACHINES_PER_GROUP} máquinas...`);
    
    // Agregar máquinas del grupo actual
    for (let i = 0; i < MACHINES_PER_GROUP; i++) {
      const payload = JSON.stringify(generateMaquinaData());

      // Enviar POST request para agregar máquina
      const response = http.post(`${BASE_URL}/api/maquinas/agregar`, payload, headers);
      console.log(`Grupo ${group} - Máquina ${i + 1}/${MACHINES_PER_GROUP} - Status: ${response.status}`);
      
      // Pausa entre peticiones
      sleep(PAUSE_BETWEEN_MACHINES);
    }
    
    // Reposo entre grupos (excepto el último)
    if (group < TOTAL_GROUPS) {
      console.log(`Reposo de ${REST_BETWEEN_GROUPS} segundos...`);
      sleep(REST_BETWEEN_GROUPS);
    }
  }
  
  const totalMachines = MACHINES_PER_GROUP * TOTAL_GROUPS;
  console.log(`Prueba completada: ${totalMachines} máquinas agregadas en total`);
}
