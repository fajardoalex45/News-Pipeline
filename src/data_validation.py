import pandas as pd
import re

class DataValidator:
    def __init__(self, df):
        self.df = df
        self.errors = []

    def validate_silver_data(self):
        print("🔍 Iniciando validación de calidad de datos...")
        
        # 1. Validar que no esté vacío
        if self.df.empty:
            self.errors.append("La tabla está vacía.")

        # 2. Validar que el título no sea nulo
        null_titles = self.df['title'].isnull().sum()
        if null_titles > 0:
            self.errors.append(f"Se encontraron {null_titles} títulos nulos.")

        # 3. Validar formato de URL (regex simple)
        url_pattern = re.compile(r'^https?://.+')
        invalid_urls = self.df[~self.df['url'].str.match(url_pattern, na=False)]
        if not invalid_urls.empty:
            self.errors.append(f"Se encontraron {len(invalid_urls)} URLs con formato inválido.")

        # 4. Validar columnas mínimas requeridas
        required_cols = ["title", "url", "source", "published_at"]
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        if missing_cols:
            self.errors.append(f"Faltan columnas requeridas: {missing_cols}")

        # --- RESULTADO ---
        if self.errors:
            print("❌ FALLÓ LA VALIDACIÓN DE DATOS")
            for error in self.errors:
                print(f"   - {error}")
            return False
        
        print("✅ Validación de Calidad: PASADA")
        return True