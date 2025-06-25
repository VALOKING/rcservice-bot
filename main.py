from flask import Flask, request
import requests
import os
import json
import random

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8120217348:AAFo7KKaRXPdL-uh43J2sFIP6Ook4bWkHug")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Track user state (per chat_id)
user_state = {}
staff = {
    "water": ["Ramesh", "Kumar"],
    "electricity": ["Suresh", "Anil"],
    "road": ["Ganesh", "Vikram"],
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
        text = data['message'].get('text', '')

        state = user_state.get(chat_id, {})

        # 1️⃣ Start
        if text == "/start":
            user_state.pop(chat_id, None)
            reply = "👋 Welcome! Choose an option:"
            buttons = {
                "inline_keyboard": [
                    [{"text": "📝 Make a Complaint", "callback_data": "make_complaint"}],
                    [{"text": "ℹ️ Help", "callback_data": "help"}]
                ]
            }
            send_message(chat_id, reply, buttons)

        # 2️⃣ Waiting for Description
        elif state.get("step") == "awaiting_description":
            user_state[chat_id]["description"] = text
            user_state[chat_id]["step"] = "awaiting_location"
            send_message(chat_id, "📍 Please share your location (e.g., Block A, Room 101):")

        # 3️⃣ Waiting for Location
        elif state.get("step") == "awaiting_location":
            user_state[chat_id]["location"] = text
            complete_complaint(chat_id)

        else:
            send_message(chat_id, "❌ Unknown command. Type /start to begin.")

    elif 'callback_query' in data:
        callback = data['callback_query']
        chat_id = callback['message']['chat']['id']
        action = callback['data']
        print("🎯 Callback received:", action, flush=True)

        if action == "make_complaint":
            reply = "🚨 What type of complaint?"
            buttons = {
                "inline_keyboard": [
                    [{"text": "💧 Water", "callback_data": "type_water"}],
                    [{"text": "⚡ Electricity", "callback_data": "type_electricity"}],
                    [{"text": "🛣️ Road", "callback_data": "type_road"}]
                ]
            }
            send_message(chat_id, reply, buttons)

        elif action.startswith("type_"):
            complaint_type = action.split("_")[1]
            user_state[chat_id] = {
                "step": "awaiting_description",
                "type": complaint_type
            }
            send_message(chat_id, "📋 Please describe your issue briefly:")

        elif action == "help":
            reply = "ℹ️ Use this bot to raise complaints in your colony. Tap 'Make a Complaint' to begin."
            send_message(chat_id, reply)

        else:
            send_message(chat_id, "⚠️ Unknown action.")

    return {"ok": True}

def complete_complaint(chat_id):
    state = user_state.get(chat_id)
    if not state:
        send_message(chat_id, "❌ Something went wrong. Please try again.")
        return

    complaint_type = state.get("type", "general").title()
    description = state.get("description", "")
    location = state.get("location", "")
    assigned = random.choice(staff.get(state["type"], ["Supervisor"]))

    reply = (
        f"✅ Complaint noted.\n"
        f"Type: {complaint_type}\n"
        f"Description: {description}\n"
        f"Location: {location}\n"
        f"Assigned to: {assigned} ({complaint_type} Department)\n"
        f"ETA: Within 2 hours"
    )

    send_message(chat_id, reply)
    user_state.pop(chat_id, None)  # clear state after completion

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
