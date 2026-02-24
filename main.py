# main.py
from extract import NewsExtractor
from transform import NewsTransformer
from load import NewsLoader
from datetime import datetime
import pandas as pd
import json
import os

def run_pipeline():
    print(f"--- Iniciando Pipeline: {datetime.now()} ---")
    
    # 1. Extracción
    ext = NewsExtractor()
    if not ext.smoke_test:
        print("🛑 Abortando: Error de conectividad con la fuente.")
        return 
    
    topic = "Artificial Intelligence"
    noticias = ext.fetch_news(topic)

    if not noticias:
        print(f"⚠️ No se encontraron noticias para '{topic}'. Fin del proceso.")
        return
 
    # Guardamos y obtenemos la ruta completa del archivo
    filename = f"news_{datetime.now().strftime('%Y%m%d')}.json"
    ext.save_news(noticias, filename)
    # IMPORTANTE: Construimos la ruta donde quedó el archivo
    full_path_landing = os.path.join("data", "landing", filename)

    
    # 2. Transformación
    tra = NewsTransformer()
    # Smoke Test: ¿El archivo que acabamos de crear existe realmente?
    if not os.path.exists(full_path_landing):
        print(f"❌ Error: El archivo {full_path_landing} no se generó.")
        return

    print("🧹 Iniciando proceso de transformación...")
    # Delegamos la carga y limpieza al transformador
    df_cleaned = tra.transform_from_json(full_path_landing)
    
    if df_cleaned.empty:
        print("⚠️ El DataFrame está vacío tras la transformación. Abortando.")
        return
        
    # 💾 GUARDADO INTERMEDIO (Capa Silver)
    # Es vital guardar antes de intentar subir a la base de datos
    tra.save_processed(df_cleaned, "cleaned_news")
    print("✅ Archivo procesado guardado localmente.")

    # 3. Carga
    load = NewsLoader()

    #Smoke Test: ¿Postgres está vivo?
    if not load.smoke_test_db:
        print("❌ Error crítico: No se pudo conectar a la base de datos. Abortando.")
        return 
    
    load.load_to_postgres(df_cleaned)
    print(f"\n✅ PIPELINE FINALIZADO EXITOSAMENTE A LAS {datetime.now().strftime('%H:%M:%S')}")


if __name__ == "__main__":
    run_pipeline()