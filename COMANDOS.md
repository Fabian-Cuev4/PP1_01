# 🚀 UN SOLO COMANDO

## **Inicia Todo Junto:**
```bash
docker-compose --profile all up --build
```

**✅ Qué incluye:**
- MySQL (13306)
- MongoDB (27018)
- Backend simple (18000) ← Frontend se conecta aquí (red exclusiva)
- Backend con 3 réplicas (solo para nginx)
- Nginx balanceador (8888, 8080)
- Frontend (18080)

---

## **🔗 Accesos:**

| Servicio | URL | Destino |
|----------|-----|---------|
| Frontend | http://localhost:18080 | → backend-simple (18000) |
| Backend Simple | http://localhost:18000/docs | Directo |
| Máquinas (Balanceado) | http://localhost:8888/api/maquinas/* | → nginx → backend réplicas |
| Login (Simple) | http://localhost:18000/api/auth/login | Directo |
| Nginx Status | http://localhost:8080/nginx_status | nginx |

**Arquitectura de Redes:**
- **Frontend + backend-simple**: red exclusiva `frontend_network`
- **Backend réplicas + nginx + DBs**: red `siglab_network`
- **Máquinas**: frontend → backend-simple | nginx → backend réplicas

---

## **� Para Detener:**
```bash
docker-compose --profile all down
```

---

## **🧪 k6 por Separado (asumiendo que todo ya corre):**
```bash
docker-compose --profile load-test up --build
```

**✅ Qué incluye:**
- k6-saturator

**❌ NO incluye:**
- Bases de datos
- Backends
- Frontend
- Nginx

---

## **📋 Escalar Backend:**
```yaml
# En docker-compose.yml cambiar:
backend:
  deploy:
    replicas: 5  # Número de réplicas
```

¡Un solo comando para todo! 🎯
