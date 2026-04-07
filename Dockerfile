# 1. Imagen base: Usamos una versión ligera de Python en Linux
FROM python:3.12-slim

# 2. Definimos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# 3. INSTALACIÓN DE DEPENDENCIAS DEL SISTEMA (Crucial para psycopg2 y Pandas)
# Agregamos build-essential y python3-dev para que pueda compilar librerías si es necesario
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Copiamos el archivo de requerimientos primero (para aprovechar la caché de Docker)
COPY requirements.txt .

# 5. Instalar librerías de Python
# Agregamos un upgrade de pip por si acaso, como sugería tu log
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copiamos todo nuestro código al contenedor
COPY . .

# 7. El comando que se ejecutará al iniciar el contenedor
CMD ["python", "main.py"]
