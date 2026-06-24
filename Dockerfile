# 1. Usar una imagen oficial de Python en su versión slim (ligera y segura)
FROM python:3.11-slim

# 2. Definir variables de entorno para optimizar Python dentro del contenedor
# Evita que Python escriba archivos .pyc en el disco
ENV PYTHONDONTWRITEBYTECODE=1
# Evita que Python guarde en buffer las salidas de consola (logs inmediatos)
ENV PYTHONUNBUFFERED=1

# 3. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /code

# 4. Instalar dependencias del sistema necesarias si se requiere compilar algo (ej: para algunas extensiones de psycopg2/asyncpg)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiar únicamente el archivo de requerimientos primero
COPY requirements.txt /code/

# 6. Instalar las dependencias de Python sin almacenar caché para reducir el tamaño de la imagen
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 7. Copiar el resto del código de la aplicación
COPY ./app /code/app

# 8. Exponer el puerto en el que correrá la aplicación
EXPOSE 8000

# 9. Comando por defecto para iniciar Uvicorn apuntando a la aplicación FastAPI/Flask
# Se incluye --host 0.0.0.0 para escuchar conexiones externas y --reload para desarrollo en tiempo real
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "000", "--reload"]