from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1399390861346996346/Lz1IkbuiIMMAyMvbRIZDuVJzsQ0N9GdQtpA8tYJw58osxDhJWw5igdF6uD6WVHEZg9X1"

@app.route("/", methods=["POST"])
def recibir_carta():
    try:
        data = request.get_json(force=True)
        print("📩 JSON recibido:", data)

        # Acceso limpio a los campos
        nombre = str(data["name"]) if "name" in data else "SIN nombre"
        numero = str(data["number"]) if "number" in data else "SIN número"
        imagen = str(data["image_url"]) if "image_url" in data else ""
        expansion = str(data["expansion"]) if "expansion" in data else "SIN expansión"
        abbr = str(data["expansion_abbr"]) if "expansion_abbr" in data else ""

        print("🧪 Nombre:", nombre)
        print("🧪 Número:", numero)
        print("🧪 Imagen:", imagen)

        contenido = {
            "embeds": [
                {
                    "title": nombre,
                    "description": f"Set: {expansion} ({abbr})\nNúmero: {numero}",
                    "image": {"url": imagen}
                }
            ]
        }

        r = requests.post(DISCORD_WEBHOOK_URL, json=contenido)
        print("✅ Discord Status:", r.status_code)

    except Exception as e:
        print("❌ Error procesando:", e)

    return {"ok": True}, 200

if __name__ == "__main__":
    app.r
