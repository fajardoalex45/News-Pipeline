# Usamos la imagen de Airflow específicamente con Python 3.12
FROM apache/airflow:2.9.0-python3.12

# Copiamos tus librerías
COPY requirements.txt /

# Instalamos tus librerías de Python encima de Airflow
RUN pip install --no-cache-dir -r /requirements.txt