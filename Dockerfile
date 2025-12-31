# Usamos una imagen base oficial de Python ligera
FROM python:3.12-slim

# Evita que Python genere archivos .pyc y buffee la salida (logs en tiempo real)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos dependencias del sistema necesarias para compilar driver de Postgres (si fuera necesario)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiamos requerimientos e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Exponemos el puerto
EXPOSE 8000

# Comando por defecto:
# 1. Ejecuta el script de crear tablas (init_db)
# 2. Levanta el servidor Uvicorn en 0.0.0.0 (necesario para Docker)
CMD ["sh", "-c", "python -m app.core.init_db && uvicorn app.main:app --host 0.0.0.0 --port 8000"]