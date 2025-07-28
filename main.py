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
    print("🟡 Headers:", dict(request.headers))
    print("🟡 Content-Type:", request.content_type)
    print("🟡 request.data:", request.data.decode("utf-8"))
    print("🟡 request.form:", request.form)
    print("🟡 request.args:", request.args)

    try:
        data = request.get_json(force=True)
        print("✅ request.get_json:", data)
    except Exception as e:
        print("❌ request.get_json error:", e)
        data = {}

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

    try:
        r = requests.post(DISCORD_WEBHOOK_URL, json=contenido)
        print("✅ Enviado a Discord:", r.status_code)
    except Exception as e:
        print("❌ Error al enviar a Discord:", e)

    return {"ok": True}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


