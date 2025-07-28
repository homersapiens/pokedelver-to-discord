from flask import Flask, request
from flask_cors import CORS
import requests
import json
import datetime

app = Flask(__name__)
CORS(app)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1399489495321284658/m0Y1OCEUBLBYsdJJU7iyIhfnTEy8zxbmSGB9XJuZVgSHGFgLG0FgZ8dbxUH7WnRJyPaW"

@app.route("/", methods=["POST"])
def recibir_carta():
    try:
        # Detectar si viene como raw string
        raw_data = request.data.decode("utf-8")
        print("🟡 Cuerpo recibido bruto:", raw_data)

        try:
            # Si viene como JSON puro
            data = json.loads(raw_data)
        except:
            # Si viene en formato form-urlencoded como "payload={...}"
            if raw_data.startswith("payload="):
                payload_str = raw_data[8:]  # quitar "payload="
                payload_str = payload_str.replace("+", " ")  # form decode
                payload_str = requests.utils.unquote(payload_str)
                data = json.loads(payload_str)
            else:
                data = {}

        print("📩 JSON limpio:", data)

        nombre = data.get("name", "SIN nombre")
        numero = data.get("number", "SIN número")
        imagen = data.get("image_url", "")
        expansion = data.get("expansion", "SIN expansión")
        abbr = data.get("expansion_abbr", "")

        hora = datetime.datetime.now().strftime("%H:%M:%S")

        contenido = {
            "embeds": [
                {
                    "title": f"{nombre} - {hora}",
                    "description": f"**Set:** {expansion} ({abbr})\n**Número:** {numero}",
                    "image": {"url": imagen}
                }
            ]
        }

        r = requests.post(DISCORD_WEBHOOK_URL, json=contenido)
        print("✅ Enviado a Discord:", r.status_code)

    except Exception as e:
        print("❌ Error general:", e)

    return {"ok": True}, 200

