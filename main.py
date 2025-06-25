from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Set your bot token directly or use env variable
BOT_TOKEN = os.getenv("BOT_TOKEN", "8120217348:AAFo7KKaRXPdL-uh43J2sFIP6Ook4bWkHug")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route('/')
def home():
    return "✅ RC Service Bot is Running"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("📩 Received:", data, flush=True)

    # Handle normal text messages
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
            send_message(chat_id, reply, buttons)
        else:
            send_message(chat_id, "❌ Unknown command. Type /start to begin.")

    # Handle button click (callback query)
    elif 'callback_query' in data:
        callback = data['callback_query']
        chat_id = callback['message']['chat']['id']
        action = callback['data']
        print("🎯 Callback received:", action, flush=True)

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

        send_message(chat_id, reply)

    return {"ok": True}


# Helper function to send messages
def send_message(chat_id, text, buttons=None):
    payload = {
        "chat_id": chat_id,
        "text": text
    }

    if buttons:
        payload["reply_markup"] = buttons

    response = requests.post(f"{API_URL}/sendMessage", json=payload)
    print("📤 Sent:", response.text, flush=True)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
