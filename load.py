import pandas as pd
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

class NewsLoader:
    def __init__(self):
        # Cargamos credenciales del .env (Asegúrate de agregarlas)
        self.user = os.getenv("DB_USER", "postgres")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = os.getenv("DB_PORT", "5432")
        self.db = os.getenv("DB_NAME", "news_db")
        
        # Creamos la URL de conexión para SQLAlchemy
        self.connection_url = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        self.engine = create_engine(self.connection_url)

    def smoke_test_db(self):
        """Verifica si la base de datos está disponible."""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Smoke Test DB: Conexión exitosa.")
            return True
        except Exception as e:
            print(f"❌ Smoke Test DB: Falló la conexión. Error: {e}")
            return False

    def load_to_postgres(self, df, table_name="news_articles"):
        """Carga el DataFrame en la tabla de Postgres."""
        print(f"📦 Cargando {len(df)} registros en la tabla '{table_name}'...")
        try:
            # if_exists='append' agrega datos nuevos sin borrar los anteriores
            # index=False evita que se cree una columna para el índice de Pandas
            df.to_sql(table_name, con=self.engine, if_exists='append', index=False)
            print("🚀 Carga finalizada con éxito.")
        except Exception as e:
            print(f"❌ Error al cargar datos: {e}")
            raise e

if __name__ == "__main__":
    # 1. Cargar el CSV limpio del Paso 2
    processed_file = "data/processed/cleaned_news.csv"
    
    if os.path.exists(processed_file):
        df = pd.read_csv(processed_file)
        loader = NewsLoader()
        
        # 2. Ejecutar Smoke Test antes de cargar
        if loader.smoke_test_db():
            loader.load_to_postgres(df)
    else:
        print("⚠️ No se encontró el archivo procesado. Ejecuta primero transform.py")