from flask import Flask
from flask_cors import CORS
import requests
import time
from threading import Thread

app = Flask(__name__)
CORS(app)

# Webhook de Delver
DELVER_URL = "https://api.delver.app/webhook/glaring-semisweet-envious-musket-despite"

# Webhook de Discord
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1399489495321284658/m0Y1OCEUBLBYsdJJU7iyIhfnTEy8zxbmSGB9XJuZVgSHGFgLG0FgZ8dbxUH7WnRJyPaW"

# Lista para evitar duplicados
procesados = set()

def enviar_a_discord(carta):
    contenido = {
        "embeds": [
            {
                "title": f"{carta['name']}",
                "description": f"**Set:** {carta['expansion']} ({carta['expansion_abbr']})\n**Número:** {carta['number']}",
                "image": {"url": carta["image_url"]}
            }
        ]
    }
    r = requests.post(DISCORD_WEBHOOK_URL, json=contenido)
    print(f"✅ Enviada: {carta['name']} ({carta['number']}) - {r.status_code}")

def bucle_delver():
    print("🟢 Bucle Delver iniciado.")
    while True:
        try:
            print("🔄 Bucle activo, esperando nuevas cartas...")
            res = requests.get(DELVER_URL)
            cartas = res.json()
            print("📥 Cartas recibidas:", cartas)

            for carta in cartas:
                unique_id = f"{carta['name']}-{carta['number']}"
                if unique_id not in procesados:
                    enviar_a_discord(carta)
                    procesados.add(unique_id)

        except Exception as e:
            print("❌ Error en el bucle:", e)

        time.sleep(10)

@app.route("/", methods=["GET"])
def index():
    return "🟢 Pokédelver to Discord activo", 200

# Lanzar el bucle una vez al recibir la primera petición
@app.before_first_request
def lanzar_bucle():
    print("🟢 Lanzando hilo en segundo plano...")
    hilo = Thread(target=bucle_delver)
    hilo.daemon = True
    hilo.start()
