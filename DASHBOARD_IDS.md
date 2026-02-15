# 📊 IDs Únicos para Dashboard

## **✅ Solución Aplicada:**

```yaml
environment:
  SERVER_ID: ${HOSTNAME:-backend}  # ID único por contenedor
```

## **🔍 Cómo Funciona:**

### **IDs de Réplica:**
- **Réplica 1**: `backend_1` (hostname del contenedor)
- **Réplica 2**: `backend_2` 
- **Réplica 3**: `backend_3`

### **Para el Dashboard:**

```python
# En tu endpoint de dashboard
@router.get("/dashboard/stats")
async def dashboard_stats():
    server_id = os.getenv('SERVER_ID', 'unknown')
    
    stats = {
        "server_id": server_id,           # backend_1, backend_2, backend_3
        "active_connections": get_connections(),
        "requests_processed": get_requests_count(),
        "memory_usage": get_memory_usage(),
        "cpu_usage": get_cpu_usage()
    }
    
    return stats
```

## **📈 Ejemplo de Datos para Dashboard:**

```json
{
  "server_id": "backend_1",
  "active_connections": 15,
  "requests_processed": 1250,
  "memory_usage": "245MB",
  "cpu_usage": "12%"
}
```

## **🎯 Beneficios para Dashboard:**

1. **Identificación única** de cada réplica
2. **Monitoreo individual** por servidor
3. **Balanceo de carga visible**
4. **Performance por réplica**
5. **Debugging específico**

## **🧪 Verificación:**

```bash
# Ver IDs de cada réplica
docker exec backend_1 env | grep SERVER_ID
docker exec backend_2 env | grep SERVER_ID
docker exec backend_3 env | grep SERVER_ID

# Salida esperada:
# SERVER_ID=backend_1
# SERVER_ID=backend_2
# SERVER_ID=backend_3
```

¡Perfecto para tu dashboard! Ahora cada réplica tiene su propio ID único. 🎯
