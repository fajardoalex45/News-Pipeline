import unittest
import pandas as pd
from src.transform import NewsTransformer  # <--- AQUÍ invocamos tu código real

class TestNewsTransform(unittest.TestCase):
    
    def setUp(self):
        """Se ejecuta antes de cada test para preparar el ambiente."""
        self.transformer = NewsTransformer()
        # Creamos un dato de ejemplo que simula lo que viene del JSON crudo
        self.raw_mock_data = [
            {
                "title": "Data Engineering is awesome",
                "author": None,           # Caso de prueba: autor nulo
                "description": None,      # Caso de prueba: descripción nula
                "url": "http://test.com",
                "publishedAt": "2026-02-18T10:00:00Z",
                "source": {"name": "TechCrunch"} # Caso de prueba: diccionario anidado
            },
            {
                "title": "[Removed]",     # Caso de prueba: artículo basura
                "author": "ABC",
                "description": "Deleted",
                "url": "http://trash.com",
                "publishedAt": "2026-02-18T11:00:00Z",
                "source": {"name": "Bot"}
            }
        ]

    def test_transformation_logic(self):
        """PRUEBA REAL: Invoca la lógica de transformación de tu clase."""
        # 1. Convertimos el mock a DataFrame para pasarlo al transformador
        df_raw = pd.DataFrame(self.raw_mock_data)
        
        # 2. Invocamos el método de tu clase (asegúrate de que este método exista)
        # Nota: Si tu transform.py lee de archivos, lo ideal es separar la lógica
        # en un método como 'clean_dataframe(df)' para poder testearlo así:
        df_cleaned = self.transformer.transform_logic(df_raw)

        # 3. ASSERTS: ¿Tu código hizo lo que debía?
        
        # Verificación 1: ¿Filtró el artículo '[Removed]'?
        self.assertEqual(len(df_cleaned), 1, "Debería haber quedado solo 1 artículo")
        
        # Verificación 2: ¿Llenó el autor nulo con 'Anonymous'?
        self.assertEqual(df_cleaned.iloc[0]['author'], 'Anonymous')
        
        # Verificación 3: ¿Aplanó el nombre de la fuente?
        self.assertEqual(df_cleaned.iloc[0]['source_name'], 'TechCrunch')
        
        # Verificación 4: ¿El formato de fecha es el correcto?
        self.assertEqual(df_cleaned.iloc[0]['publishedAt'], '2026-02-18 10:00:00')

if __name__ == "__main__":
    unittest.main()