from flask import Flask, request
import requests
import os
import json
import random

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8120217348:AAFo7KKaRXPdL-uh43J2sFIP6Ook4bWkHug")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

staff = {
    "water": ["Ramesh", "Kumar"],
    "electricity": ["Suresh", "Anil"],
    "road": ["Ganesh", "Vikram"],
    "general": ["Supervisor"]
}

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
            send_message(chat_id, reply, reply_markup=buttons)

        else:
            send_message(chat_id, "❌ Unknown command. Type /start to begin.")

    elif 'callback_query' in data:
        callback = data['callback_query']
        chat_id = callback['message']['chat']['id']
        action = callback['data']
        print("🎯 Callback received:", action, flush=True)

        # When user presses "Make a Complaint"
        if action == "make_complaint":
            reply = "🚨 What type of complaint?"
            buttons = {
                "inline_keyboard": [
                    [{"text": "💧 Water", "callback_data": "type_water"}],
                    [{"text": "⚡ Electricity", "callback_data": "type_electricity"}],
                    [{"text": "🛣️ Road", "callback_data": "type_road"}]
                ]
            }
            send_message(chat_id, reply, reply_markup=buttons)

        elif action.startswith("type_"):
            complaint_type = action.split("_")[1]  # water / electricity / road
            assigned_staff = random.choice(staff.get(complaint_type, ["Supervisor"]))

            reply = (
                f"✅ Complaint noted.\n"
                f"Assigned to: {assigned_staff.title()} ({complaint_type.title()} Department)\n"
                f"ETA: Within 2 hours"
            )
            send_message(chat_id, reply)

        elif action == "help":
            reply = (
                "ℹ️ This is the RC Service Bot.\n"
                "Use it to raise complaints in your colony.\n"
                "Tap 'Make a Complaint' to get started."
            )
            send_message(chat_id, reply)

        else:
            send_message(chat_id, "⚠️ Unknown action.")

    return {"ok": True}

def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text
    }

    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)

    response = requests.post(f"{API_URL}/sendMessage", json=payload)
    print("📤 Sent:", response.text, flush=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
