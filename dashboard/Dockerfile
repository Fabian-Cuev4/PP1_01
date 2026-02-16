FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Exponer puertos
EXPOSE 18081 8001

# Comando para iniciar el servidor
CMD ["python", "server.py"]
