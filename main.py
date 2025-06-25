from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route('/')
def home():
    return "✅ RC Service Bot is Running"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("📩 Received:", data, flush=True)

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '').lower()

        if text == "/start":
            reply = "👋 Welcome! Choose an option:"
            buttons = {
                "inline_keyboard": [
                    [{"text": "📝 Make a Complaint", "callback_data": "make_complaint"}],
                    [{"text": "ℹ️ Help", "callback_data": "help"}]
                ]
            }
            requests.post(f"{API_URL}/sendMessage", json={
                "chat_id": chat_id,
                "text": reply,
                "reply_markup": buttons
            })

        else:
            # fallback text handling
            requests.post(f"{API_URL}/sendMessage", json={
                "chat_id": chat_id,
                "text": "❌ Unknown command. Type /start to begin."
            })

    elif 'callback_query' in data:
        callback = data['callback_query']
        chat_id = callback['message']['chat']['id']
        action = callback['data']

        if action == "make_complaint":
            reply = (
                "📝 Please send your complaint like:\n"
                "Type: Water\n"
                "Description: Tap leaking\n"
                "Location: Room 101"
            )
        elif action == "help":
            reply = (
                "ℹ️ This is the RC Service Bot.\n"
                "Use it to raise complaints in your colony.\n"
                "Tap 'Make a Complaint' to get started."
            )
        else:
            reply = "⚠️ Unknown action."

        requests.post(f"{API_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": reply
        })

    return {"ok": True}


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
BOT_TOKEN = os.getenv("BOT_TOKEN")
