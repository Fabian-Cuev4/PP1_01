# Dockerfile para el contenedor de saturación k6
FROM loadimpact/k6:latest

# Establecer el directorio de trabajo
WORKDIR /scripts

# Copiar el script de prueba k6
COPY maquina-saturator.js /scripts/

# Comando por defecto para ejecutar la prueba
CMD ["run", "/scripts/maquina-saturator.js"]
