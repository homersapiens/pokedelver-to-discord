@app.route("/", methods=["POST"])
def recibir_carta():
    data = request.json or {}

    print("📩 Recibido de Pokédelver:")
    print(data)  # Imprime el contenido completo para verlo en los logs

    nombre = data.get("name", "Carta desconocida")
    set_info = data.get("set") or {}
    set_name = set_info.get("name", "Set desconocido")
    number = data.get("collector_number", "?")
    image_url = data.get("image_url") or data.get("images", {}).get("large", "")

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
            print("Contenido enviado:", contenido)
        except Exception as e:
            print("❌ Error al enviar a Discord:", e)

    return {"ok": True}, 200

