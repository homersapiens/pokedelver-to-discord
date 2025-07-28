@app.route("/", methods=["POST"])
def recibir_carta():
    data = request.get_json(force=True)
    
    print("📩 JSON recibido:")
    print(data)  # Mostramos en consola lo que realmente llega

    # Intentamos acceder directamente a los campos
    nombre = data.get("name", "Carta desconocida")
    numero = data.get("number", "?")
    imagen = data.get("image_url", "")

    print("🧪 Nombre:", nombre)
    print("🧪 Número:", numero)
    print("🧪 Imagen:", imagen)

    contenido = {
        "embeds": [
            {
                "title": nombre,
                "description": f"Número: {numero}",
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
