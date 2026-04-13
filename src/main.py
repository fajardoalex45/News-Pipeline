from extract import NewsExtractor
from transform import NewsTransformer
from load import NewsLoader
from s3_manager import S3Manager  # <--- Importamos la nueva utilidad
from data_validation import DataValidator # <--- Importamos el validador
from notifications import SlackNotifier
from datetime import datetime, timezone
import pandas as pd
import json
import os

def run_pipeline():
    print(f"--- Iniciando Pipeline: {datetime.now()} ---")
    
    # 1. Extracción
    ext = NewsExtractor()
    tra = NewsTransformer()
    load= NewsLoader()
    s3_manager = S3Manager()
    
    SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")
    notifier = SlackNotifier(SLACK_WEBHOOK)


    try:
        ext.smoke_test() # Si falla, lanza Exception -> Airflow ROJO
        
        topic = "Artificial Intelligence"
        noticias = ext.fetch_news(topic)

    # Lógica de Negocio: Si la lista está vacía, no es error, es un día lento.
        if not noticias or len(noticias) == 0:
            print(f"✅ Finalizado: No se encontraron noticias nuevas para '{topic}'.")
            return # Airflow VERDE
    
        # Nombre del archivo extraido con Timestamp para evitar colisiones
        # Esto obtiene la hora Y le pega la etiqueta oficial de UTC
        now = datetime.now(timezone.utc)
        filename = f"news_{now.strftime('%Y%m%d_%H%M%S')}.json"

        # Guardamos el JSON crudo en la carpeta de landing y obtenemos la ruta completa para el siguiente paso
        full_path_landing = ext.save_news(noticias, filename)

        # 1.1 Subida a S3 (Capa Bronze)
        
        # Ruta con particiones (Year/Month/Day)
        # Esto facilita muchísimo el uso de herramientas como AWS Athena o Spark
        partition_path = f"year={now.year}/month={now.month:02d}/day={now.day:02d}"
        s3_target_key = f"bronze/{partition_path}/{filename}"
        s3_manager.upload_to_s3(full_path_landing, s3_target_key)

        # 2. Transformación

        # Smoke Test: ¿El archivo que acabamos de crear existe realmente?
        if not os.path.exists(full_path_landing):
            raise FileNotFoundError(f"❌ El extractor dijo éxito, pero {full_path_landing} no existe.")

        print("🧹 Iniciando proceso de transformación...")
        # Delegamos la carga y limpieza al transformador
        df_cleaned = tra.transform_from_json(full_path_landing)
        
        # 🔍 NUEVO: Validación con Great Expectations
        validator = DataValidator(df_cleaned)
        if not validator.validate_silver_data():
            raise ValueError("❌ Los datos no cumplen con los estándares de calidad definidos.")

        # Si pasa la validación, continuamos...  
        # 💾 GUARDADO INTERMEDIO (Capa Silver)
        # Es vital guardar antes de intentar subir a la base de datos
        full_path_processed = tra.save_processed(df_cleaned, "cleaned_news")
        print("✅ Archivo procesado guardado localmente.")

        # 2.1 Subida a S3 (Capa Silver)
        s3_target_key_silver = f"silver/{partition_path}/cleaned_news_{now.strftime('%Y%m%d_%H%M%S')}.csv"
        s3_manager.upload_to_s3(full_path_processed, s3_target_key_silver)

        # 3. Carga

        #Smoke Test: ¿Postgres está vivo?
        load.smoke_test_db() # Si falla -> Airflow ROJO
        
        load.load_to_postgres(df_cleaned)
        print(f"\n✅ PIPELINE FINALIZADO EXITOSAMENTE A LAS {datetime.now().strftime('%H:%M:%S')}")

    except Exception as e:
        error_message = f"❌ PIPELINE FALLÓ: {e}"
        print(error_message)
        notifier.send_message(error_message, status="error") # Enviar notificación a Slack
        raise e  # Re-lanzamos la excepción para que Airflow marque el DAG como fallido


if __name__ == "__main__":
    run_pipeline()