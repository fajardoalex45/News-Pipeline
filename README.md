# 📰 News ETL Pipeline: From Local Docker to Cloud Lakehouse

Este proyecto demuestra la evolución de un pipeline de ingeniería de datos, escalando desde una arquitectura Local Contenerizada hasta un Modern Data Stack utilizando Databricks, Airflow y AWS.

## 🏗️ Evolución de la Arquitectura

### 📍 Fase 1: MVP Local & Contenedores (Completada)

* Enfoque: Portabilidad y rapidez de desarrollo.

* Infraestructura: Docker Compose.

* Ingestión: Script de Python extrayendo datos de NewsAPI.

* Almacenamiento: PostgreSQL para datos estructurados y volúmenes locales para archivos crudos.

* Aprendizaje: Implementación de un flujo ETL básico y manejo de persistencia de datos en contenedores.

### 🚀 Fase 2: Orquestación y Resiliencia (En Progreso)

* Enfoque: Automatización y desacoplamiento.

* Orquestador: Migración de ejecución manual a Apache Airflow.

* Cloud Storage: Implementación de AWS S3 como Data Lake (Landing Zone), eliminando la dependencia de almacenamiento local.

* Calidad: Integración de Great Expectations para validar esquemas y calidad de datos antes de la carga.

* Valor: Manejo de reintentos automáticos y observabilidad del pipeline.

### 🧱 Fase 3: Procesamiento Distribuido (Próximamente)

* Enfoque: Escalabilidad de Big Data y arquitectura de Medallón.

* Cómputo: Migración del procesamiento pesado a Databricks (PySpark).

* Storage: Implementación de Delta Lake sobre S3.

* Estructura: Organización de datos en capas Bronze (crudo), Silver (limpio) y Gold (agregado).

* Valor: Uso de transacciones ACID y "Time Travel" en el Data Lake.

### ☁️ Fase 4: Insights y CI/CD (Meta Final)

* Enfoque: Entrega de valor y automatización total.

* BI: Conexión de Databricks SQL con herramientas de visualización.

* DevOps: Pipeline de CI/CD con GitHub Actions para despliegue automático de Notebooks y DAGs.

* Monitoreo: Alertas proactivas en Slack/Discord sobre la salud de los datos.

### 🛠️ Stack Tecnológico

* Lenguajes: Python (Pandas, PySpark), SQL.

* Infraestructura: Docker, AWS (S3).

* Herramientas de Datos: Apache Airflow, Databricks, Delta Lake, PostgreSQL.

### 💡 ¿Por qué esta evolución?

En el mundo real (como mi experiencia en Globant/Citibank), los datos crecen y los sistemas locales fallan. Este proyecto refleja el proceso de transformar un script funcional en una plataforma empresarial capaz de procesar millones de noticias de forma eficiente, segura y automatizada.
