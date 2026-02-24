import unittest
import os
from extract import NewsExtractor
from unittest.mock import patch 
from requests.exceptions import HTTPError, Timeout, ConnectionError

class TestNewsExtractor(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.extractor = NewsExtractor()

    def test_get_params_structure(self):
        """Criterio: Los parámetros deben incluir el tópico y la API Key."""
        topic = "Bitcoin"
        params = self.extractor.get_params(topic)
        
        self.assertEqual(params["q"], topic)
        self.assertIn("apiKey", params)
        self.assertEqual(params["language"], "en")

    def test_get_params_empty_topic(self):
        """Criterio: Debe lanzar un error si el tópico está vacío."""
        with self.assertRaises(ValueError):
            self.extractor.get_params("")

    def test_save_news_empty_data(self):
        """Criterio: No debe crear archivos si la lista de datos está vacía."""
        result = self.extractor.save_news([], "test_fail.json")
        self.assertFalse(result)

    def test_save_news_creates_file(self):
        """Criterio: Debe crear un archivo físico si hay datos."""
        test_data = [{"title": "Test"}]
        filename = "test_success.json"
        
        self.extractor.save_news(test_data, filename)
        path = f"data/landing/{filename}"
        
        # Verificamos si el archivo existe
        file_exists = os.path.exists(path)
        self.assertTrue(file_exists)
        
        # Limpieza: Borrar el archivo de prueba después del test
        if file_exists:
            os.remove(path)

    @patch('extract.requests.get')
    def test_fetch_news_lanza_404(self, mock_get):
        
        # --- 1. CONFIGURAMOS EL CLON (MOCK) ---
        
        # Le decimos al clon: "Tu atributo status_code será 404"
        mock_get.return_value.status_code = 404
        
        # Le decimos al clon: "Cuando llamen a tu método raise_for_status(), explota a propósito"
        mock_get.return_value.raise_for_status.side_effect = HTTPError("Simulated 404 Not Found Error")

        # --- 2. EJECUTAMOS TU CÓDIGO REAL ---
        
        # Llamamos a la función. Aquí es donde el Mock entra en acción y bloquea el internet.
        resultado = self.extractor.fetch_news("Data Engineering")

        # --- 3. VALIDAMOS EL RESULTADO ---
        
        # Verificamos que tu bloque 'except HTTPError:' hizo su trabajo 
        # y devolvió una lista vacía en lugar de romper el programa.
        self.assertEqual(resultado, [])

    @patch('extract.requests.get')
    def test_fetch_news_lanza_timeout(self, mock_get):
        
        # 1. Configuramos el clon para que explote INMEDIATAMENTE con un Timeout
        mock_get.side_effect = Timeout("El servidor tardó más de 10 segundos")
        
        # 2. Ejecutamos tu código real
        resultado = self.extractor.fetch_news("Data Engineering")
        
        # 3. Validamos que el bloque 'except Timeout:' hizo su trabajo
        self.assertEqual(resultado, [])

    @patch('extract.requests.get')
    def test_fetch_news_lanza_connection_error(self, mock_get):
        
        # 1. Configuramos el clon para que finja que no hay internet
        mock_get.side_effect = ConnectionError("No se pudo conectar al host (Fallo de DNS/WiFi)")
        
        # 2. Ejecutamos tu código real
        resultado = self.extractor.fetch_news("Data Engineering")
        
        # 3. Validamos que el bloque 'except ConnectionError:' nos protegió
        self.assertEqual(resultado, [])

if __name__ == "__main__":
    unittest.main()