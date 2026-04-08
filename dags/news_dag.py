from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# 1. Definimos las reglas del juego (Argumentos por defecto)
default_args = {
    'owner': 'alex',
    'depends_on_past': False, # Si falla ayer, ¿igual corro hoy? (False = sí)
    'start_date': datetime(2026, 1, 1), # Desde cuándo empieza a contar
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1, # Cuántas veces lo intento si fallo
    'retry_delay': timedelta(minutes=1), # Cuánto espero entre intentos
}

# 2. Creamos el DAG (El contenedor de tareas)
with DAG(
    'news_extraction_pipeline', # El nombre que verás en la web de Airflow
    default_args=default_args,
    description='Pipeline diario para extraer noticias de IA',
    schedule_interval='0 6 * * *', # Se ejecuta todos los días a las 6:00 AM
    catchup=False, # No intentes recuperar días pasados perdidos
    tags=['news', 'etl'],
) as dag:

    # 3. Definimos la Tarea: Ejecutar tu main.py
    # Como mapeamos toda tu carpeta en /opt/airflow/project, Airflow puede ver tu archivo main.py
    run_etl = BashOperator(
        task_id='run_main_python_script',
        bash_command='python /opt/airflow/project/main.py',
    )

    # 4. El orden de ejecución (Si tuviéramos más tareas, aquí haríamos las flechitas)
    run_etl