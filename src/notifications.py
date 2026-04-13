import requests
import json

class SlackNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_message(self, text, status="info"):
        # Elegimos un color según el estado
        color = "#36a64f" if status == "success" else "#ff0000" if status == "error" else "#439FE0"
        emoji = "✅" if status == "success" else "❌" if status == "error" else "ℹ️"

        payload = {
            "attachments": [
                {
                    "color": color,
                    "title": f"{emoji} Pipeline Update",
                    "text": text,
                    "footer": "News Pipeline - Fase 2"
                }
            ]
        }

        try:
            response = requests.post(
                self.webhook_url, 
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error enviando a Slack: {e}")
            return False