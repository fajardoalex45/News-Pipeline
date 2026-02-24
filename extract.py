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
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2/everything"

    def get_params(self, topic: str):
        """LÓGICA TESTEABLE: Retorna los parámetros de la API."""
        if not topic:
            raise ValueError("El tópico no puede estar vacío")
        return {
            "q": topic,
            "sortBy": "publishedAt",
            "apiKey": self.api_key,
            "language": "en"
        }

    def smoke_test(self):
        """
        Verifica la salud de la conexión y las credenciales.
        Retorna True si la API responde correctamente.
        """
        print("🔍 Ejecutando Smoke Test de Extracción...")
        
        # Hacemos una petición mínima (solo 1 noticia) para no gastar cuota
        test_params = {
            "q": "test",
            "pageSize": 1,
            "apiKey": self.api_key
        }
        
        try:
            # Usamos un timeout de 5 segundos para que el pipeline no se quede colgado
            response = requests.get(self.base_url, params=test_params, timeout=5)
            
            # Si el status es 200, todo está OK
            response.raise_for_status() 
            print("✅ Smoke Test Extract: PASSED (Conexión exitosa)")
            return True
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                print("❌ Smoke Test Extract: FAILED (API Key inválida)")
            else:
                print(f"❌ Smoke Test Extract: FAILED (Error HTTP: {e})")
            return False
        except Exception as e:
            print(f"❌ Smoke Test Extract: FAILED (Error inesperado: {e})")
            return False
        
    def fetch_news(self, topic: str):
        """EJECUCIÓN: Realiza la llamada (Difícil de testear sin mockear)."""
        params = self.get_params(topic)
        print(f"🚀 Iniciando extracción para: {topic}...")
        
        try:
            # timeout=10 significa: "Si en 10 segundos no respondes, aborta"
            response = requests.get(self.base_url, params=params, timeout=10)
            
            # El Guardián: Lanza un error si el status no es 200 OK
            response.raise_for_status() 
            
            data = response.json()
            articles = data.get("articles", [])
            print(f"✅ Éxito: Se encontraron {len(articles)} artículos.")
            return articles

        # --- INICIO DEL MANEJO DE ERRORES GRANULAR ---
        
        except HTTPError as e:
            # Errores del servidor (400s y 500s)
            status = response.status_code
            if status == 404:
                print("❌ Error 404: El endpoint (URL) de la API no existe.")
            elif status == 401:
                print("❌ Error 401: Tu API Key es inválida o expiró. ¡Revisa tu .env!")
            elif status == 429:
                print("❌ Error 429: Límite de peticiones alcanzado (Too Many Requests).")
            else:
                print(f"❌ Error HTTP (Servidor): {e}")
            return []

        except Timeout:
            # El servidor tardó demasiado
            print("⏳ Timeout: La API de noticias tardó más de 10 segundos en responder.")
            return []

        except ConnectionError:
            # Problemas físicos de red / WiFi
            print("🔌 Error de Conexión: Revisa tu internet o la configuración de red y DNS.")
            return []

        except RequestException as e:
            # La red gigante de seguridad final
            print(f"🚨 Error crítico de requests no clasificado: {e}")
            return []

        # --- FIN DEL MANEJO DE ERRORES ---

    def save_news(self, data: list, filename: str):
        """PERSISTENCIA: Guarda los datos."""
        if not data:
            print("⚠️ No hay datos para guardar.")
            return False
            
        os.makedirs("data/landing", exist_ok=True)
        path = f"data/landing/{filename}"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ Datos guardados en: {path}")
        return True

# --- ZONA DE SEGURIDAD (El Ejecutor) ---
if __name__ == "__main__":
    extractor = NewsExtractor()
    
    # 1. Extraemos
    noticias = extractor.fetch_news("Data Engineering")
    
    # 2. Guardamos (si la extracción no devolvió una lista vacía por un error)
    if noticias:
        extractor.save_news(noticias, "data_engineering")
    else:
        print("🛑 El proceso se detuvo porque no se pudieron extraer las noticias.")