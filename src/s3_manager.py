import boto3
import os
from botocore.exceptions import ClientError

class S3Manager:
    def __init__(self):
        # Boto3 buscará automáticamente las variables AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY
        # que ya configuramos en el docker-compose.
        self.s3 = boto3.client(
            's3',
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )
        self.bucket_name = os.getenv("S3_BUCKET_NAME")

    def upload_to_s3(self, local_file_path, s3_target_key):
        """
        Sube un archivo local a S3.
        :param local_file_path: Ruta del archivo en el contenedor (ej: /data/landing/archivo.json)
        :param s3_target_key: Ruta destino en el bucket (ej: bronze/2026/archivo.json)
        """
        try:
            print(f"☁️ Subiendo {local_file_path} a s3://{self.bucket_name}/{s3_target_key}...")
            self.s3.upload_file(local_file_path, self.bucket_name, s3_target_key)
            print("✅ Subida exitosa a S3.")
            return True
        except ClientError as e:
            # Si las llaves están mal o el bucket no existe, esto lanzará el error para Airflow
            raise ConnectionError(f"❌ Error de AWS S3: {e}")
        except Exception as e:
            raise Exception(f"❌ Error inesperado al subir a S3: {e}")