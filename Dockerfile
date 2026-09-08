# 1. Usar una imagen oficial de Python en su versión slim
FROM python:3.11-slim

# 2. Definir variables de entorno para optimizar Python dentro del contenedor
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Establecer el directorio de trabajo
WORKDIR /code

# 4. Instalar dependencias del sistema requeridas para libpq (driver de PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiar el archivo de requerimientos
COPY requirements.txt /code/

# 6. Instalar dependencias
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 7. Copiar el código de la aplicación
COPY ./app /code/app

# 8. Exponer el puerto predeterminado (informativo)
EXPOSE 8000

# 9. Comando de inicio para producción:
# - Se usa la variable $PORT si el host en la nube la provee; si no, por defecto usa 8000.
# - Se remueve la bandera --reload.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]