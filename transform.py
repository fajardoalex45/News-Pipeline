import pandas as pd
import json
import os
from glob import glob

class NewsTransformer:
    def __init__(self):
        self.landing_path = "data/landing"
        self.processed_path = "data/processed"
        os.makedirs(self.processed_path, exist_ok=True)

    def get_latest_file(self):
        """Busca el archivo JSON más reciente en la carpeta landing."""
        files = glob(f"{self.landing_path}/*.json")
        if not files:
            return None
        return max(files, key=os.path.getctime)

    def transform_from_json(self, file_path: str) -> pd.DataFrame:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No encontré el archivo: {file_path}")
            
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        df_raw = pd.DataFrame(data)
        
        # Llamamos al "Cerebro"
        return self.transform_logic(df_raw)

    def transform_logic(self, df):
        """Este método es el 'corazón' y es el que testeamos."""
        # Aplanar fuente
        df['source_name'] = df['source'].apply(lambda x: x.get('name') if isinstance(x, dict) else 'Unknown')
        
        # Solo nos quedamos con las columnas que son texto simple o fecha.
        # Eliminamos 'source' porque es un diccionario.
        columns_to_keep = [
            'title', 
            'author', 
            'description', 
            'url', 
            'publishedAt', 
            'source_name',  # Usamos nuestra versión limpia
            'content'
        ]
        
        # Filtramos el DataFrame
        df = df[columns_to_keep].copy()

        # Limpiar nulos
        df['author'] = df['author'].fillna('Anonymous')
        df['description'] = df['description'].fillna('No description provided')
        
        # Estandarizar fecha
        df['publishedAt'] = pd.to_datetime(df['publishedAt']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Filtrar basura
        df = df[df['title'] != "[Removed]"]
        
        return df


    def save_processed(self, df, filename):
        path = f"{self.processed_path}/{filename}.csv"
        df.to_csv(path, index=False)
        print(f"✅ Datos limpios guardados en: {path}")

if __name__ == "__main__":
    transformer = NewsTransformer()
    latest_file = transformer.get_latest_file()
    
    if latest_file:
        with open(latest_file, "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        df_cleaned = transformer.transform_logic(df)
        # Mostramos un preview de los datos
        print("\n--- Preview de datos limpios ---")
        print(df_cleaned.head())
        
        transformer.save_processed(df_cleaned, "cleaned_news")
    else:
        print("⚠️ No se encontraron archivos para transformar.")