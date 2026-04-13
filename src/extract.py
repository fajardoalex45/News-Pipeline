import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
from requests.exceptions import HTTPError, Timeout, ConnectionError, RequestException

# Cargamos las variables del archivo .env
load_dotenv()

class NewsExtractor:
    def __init__(self):
        # Usamos variables de entorno directamente
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2/everything"
        
        # Validación de configuración inicial
        if not self.api_key:
            raise ValueError("❌ Error: La variable NEWS_API_KEY no está configurada.")

    def smoke_test(self):
        """
        Verifica la salud de la conexión y las credenciales.
        Lanza excepciones específicas para que Airflow se detenga de inmediato.
        """
        print("🔍 Ejecutando Smoke Test de Extracción...")
        test_params = {"q": "test", "pageSize": 1, "apiKey": self.api_key}
        
        try:
            response = requests.get(self.base_url, params=test_params, timeout=5)
            response.raise_for_status() 
            print("✅ Smoke Test Extract: PASSED")
            return True
            
        except requests.exceptions.HTTPError as e:
            status = response.status_code
            if status == 401:
                raise PermissionError("❌ Smoke Test FAILED: API Key inválida.")
            else:
                raise ConnectionError(f"❌ Smoke Test FAILED: Error HTTP {status}")
        except Exception as e:
            raise ConnectionError(f"❌ Smoke Test FAILED: Error inesperado: {e}")

    def fetch_news(self, topic: str):
        """
        Realiza la extracción. 
        Lanza excepciones técnicas y retorna lista de noticias si tiene éxito.
        """
        if not topic:
            raise ValueError("❌ El tópico de búsqueda no puede estar vacío.")

        params = {
            "q": topic,
            "sortBy": "publishedAt",
            "apiKey": self.api_key,
            "language": "en"
        }
        
        print(f"🚀 Iniciando extracción para: {topic}...")
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            
            # El Sensor: Detecta si el servidor respondió con error (4xx o 5xx)
            response.raise_for_status() 
            
            data = response.json()
            articles = data.get("articles", [])
            print(f"✅ Éxito: Se encontraron {len(articles)} artículos.")
            return articles

        # --- TRADUCTOR DE ERRORES (Desglose de 4xx) ---
        except requests.exceptions.HTTPError as e:
            status = response.status_code
            if status == 401:
                raise PermissionError("❌ Error 401: Credenciales inválidas.")
            elif status == 429:
                # Usamos RuntimeWarning para indicar que el límite se alcanzó
                raise RuntimeWarning("⏳ Error 429: Límite de peticiones excedido.")
            else:
                raise ConnectionError(f"🌐 Error en el servidor de NewsAPI (Status {status}).")

        except requests.exceptions.Timeout:
            raise TimeoutError("⏰ La API tardó demasiado tiempo en responder (Timeout).")

        except requests.exceptions.RequestException as e:
            # Aquí caen errores de red física o DNS
            raise ConnectionError(f"🔌 Error crítico de red: {e}")

    def save_news(self, data: list, filename: str):
        """
        Persistencia: Guarda los datos en el volumen.
        Retorna la ruta completa donde se guardó.
        """
        base_path = os.getenv("RAW_DATA_PATH", "/opt/airflow/data/landing")    
        os.makedirs(base_path, exist_ok=True)
        
        full_path = os.path.join(base_path, filename)
        
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"✅ Datos guardados en: {full_path}")
        return full_path

# --- BLOQUE DE TESTEO LOCAL (Para debuggear fuera de Airflow) ---
if __name__ == "__main__":
    extractor = NewsExtractor()
    try:
        extractor.smoke_test()
        noticias = extractor.fetch_news("Data Engineering")
        if noticias:
            extractor.save_news(noticias, "test_file.json")
    except Exception as e:
        print(f"💥 Error durante el test local: {e}")