from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1399390861346996346/Lz1IkbuiIMMAyMvbRIZDuVJzsQ0N9GdQtpA8tYJw58osxDhJWw5igdF6uD6WVHEZg9X1"

@app.route("/", methods=["POST"])
def recibir_carta():
    data = request.get_json(force=True)

    print("📩 JSON recibido:")
    print(data)

    nombre = data.get("name", "Carta desconocida")
    numero = data.get("number", "?")
    imagen = data.get("image_url", "")
    expansion = data.get("expansion", "Set desconocido")
    expansion_abbr = data.get("expansion_abbr", "")

    contenido = {
        "embeds": [
            {
                "title": f"{nombre}",
                "description": f"**Set:** {expansion} ({expansion_abbr})\n**Número:** {numero}",
                "image": {"url": imagen}
            }
        ]
    }

    try:
        r = requests.post(DISCORD_WEBHOOK_URL, json=contenido)
        print("✅ Enviado a Discord:", r.status_code)
    except Exception as e:
        print("❌ Error al enviar a Discord:", e)

    return {"ok": True}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
