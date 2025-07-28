from flask import Flask
from flask_cors import CORS
import requests
import time
from threading import Thread

app = Flask(__name__)
CORS(app)

DELVER_URL = "https://api.delver.app/webhook/glaring-semisweet-envious-musket-despite"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1399489495321284658/m0Y1OCEUBLBYsdJJU7iyIhfnTEy8zxbmSGB9XJuZVgSHGFgLG0FgZ8dbxUH7WnRJyPaW"

procesados = set()
bucle_iniciado = False

def enviar_a_discord(carta):
    contenido = {
        "embeds": [
            {
                "title": f"{carta.get('name', 'Sin nombre')}",
                "description": f"**Set:** {carta.get('expansion', 'Desconocido')} ({carta.get('expansion_abbr', '')})\n**Número:** {carta.get('number', '?')}",
                "image": {"url": carta.get("image_url", "")}
            }
        ]
    }
    r = requests.post(DISCORD_WEBHOOK_URL, json=contenido)
    print(f"✅ Enviada: {carta.get('name', 'Sin nombre')} ({carta.get('number', '?')}) - {r.status_code}")

def bucle_delver():
    print("🟢 Bucle Delver iniciado.")
    while True:
        try:
            print("🔄 Bucle activo, esperando nuevas cartas...")
            res = requests.get(DELVER_URL)
            try:
                cartas = res.json()
                print("📥 Cartas recibidas:", cartas)
                if not isinstance(cartas, list):
                    print("⚠️ El contenido no es una lista. Abortando iteración.")
                    time.sleep(10)
                    continue
            except Exception as e:
                print("❌ Error interpretando JSON:", e)
                time.sleep(10)
                continue

            for carta in cartas:
                if not isinstance(carta, dict):
                    print("⚠️ Entrada inválida, no es un diccionario:", carta)
                    continue

                unique_id = f"{carta.get('name', '')}-{carta.get('number', '')}"
                if unique_id not in procesados:
                    enviar_a_discord(carta)
                    procesados.add(unique_id)

        except Exception as e:
            print("❌ Error en el bucle:", e)

        time.sleep(10)

@app.route("/", methods=["GET"])
def index():
    return "🟢 Servidor Flask activo", 200

@app.route("/iniciar", methods=["GET"])
def iniciar_bucle():
    global bucle_iniciado
    if not bucle_iniciado:
        print("🟢 Lanzando hilo en segundo plano desde /iniciar...")
        hilo = Thread(target=bucle_delver)
        hilo.daemon = True
        hilo.start()
        bucle_iniciado = True
        return "🟢 Hilo iniciado", 200
    else:
        return "⚠️ Ya estaba iniciado", 200
