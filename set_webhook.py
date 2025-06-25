import requests

BOT_TOKEN = "8120217348:AAFo7KKaRXPdL-uh43J2sFIP6Ook4bWkHug"
WEBHOOK_URL = "https://github.com/VALOKING/rcservice-bot"

response = requests.get(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}"
)

print(response.text)
