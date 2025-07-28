from flask import Flask, request
from flask_cors import CORS
import requests
import datetime

app = Flask(__name__)
CORS(app)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1399489495321284658/m0Y1OCEUBLBYsdJJU7iyIhfnTEy8zxbmSGB9XJuZVgSHGFgLG0FgZ8dbxUH7WnRJyPaW"

@app.route("/", methods=["POST"])
def recibir_carta():
    try:
        # Extraer datos del formulario
        nombre = request.form.get("name", "SIN nombre")
        numero = request.form.get("number", "SIN número")
        expansion = request.form.get("expansion", "SIN expansión")
        abbr = request.form.get("expansion_abbr", "")
        imagen = request.form.get("image_url", "")

        hora = datetime.datetime.now().strftime("%H:%M:%S")

        print("✅ Nombre:", nombre)
        print("✅ Número:", numero)
        print("✅ Set:", expansion)
        print("✅ Imagen:", imagen)

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
        print("❌ Error procesando:", e)

    return {"ok": True}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
