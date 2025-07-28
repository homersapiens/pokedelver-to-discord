import time
import requests

# Tu URL privada de Delver Webhook Server
DELVER_URL = "https://api.delver.app/webhook/glaring-semisweet-envious-musket-despite"

# Webhook de Discord
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1399489495321284658/m0Y1OCEUBLBYsdJJU7iyIhfnTEy8zxbmSGB9XJuZVgSHGFgLG0FgZ8dbxUH7WnRJyPaW"

# Almacena IDs ya procesados para evitar duplicados
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

while True:
    try:
        res = requests.get(DELVER_URL)
        cartas = res.json()

        for carta in cartas:
            unique_id = f"{carta['name']}-{carta['number']}"
            if unique_id not in procesados:
                enviar_a_discord(carta)
                procesados.add(unique_id)

    except Exception as e:
        print("❌ Error:", e)

    time.sleep(10)
