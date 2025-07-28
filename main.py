from flask import Flask, request
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

DISCORD_WEBHOOK_URL = os.environ.get("https://discord.com/api/webhooks/1399390861346996346/Lz1IkbuiIMMAyMvbRIZDuVJzsQ0N9GdQtpA8tYJw58osxDhJWw5igdF6uD6WVHEZg9X1")

@app.route("/", methods=["POST"])
def recibir_carta():
    data = request.json or {}

    print("📩 Recibido de Pokédelver:", data)

    nombre = data.get("name", "Carta desconocida")
    set_name = data.get("set", {}).get("name", "Set desconocido")
    number = data.get("collector_number", "?")
    image_url = data.get("image_url", "")

    contenido = {
        "embeds": [
            {
                "title": nombre,
                "description": f"Set: {set_name}\nNúmero: {number}",
                "image": {"url": image_url}
            }
        ]
    }

    if DISCORD_WEBHOOK_URL:
        try:
            r = requests.post(DISCORD_WEBHOOK_URL, json=contenido)
            print("✅ Enviado a Discord:", r.status_code)
        except Exception as e:
            print("❌ Error al enviar a Discord:", e)

    return {"ok": True}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
