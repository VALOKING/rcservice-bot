from flask import Flask, request
import requests

app = Flask(__name__)
BOT_TOKEN = "8120217348:AAFo7KKaRXPdL-uh43J2sFIP6Ook4bWkHug"

@app.route('/')
def home():
    return "✅ RC Service Bot is Running"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("📩 Received:", data)  # 👈 logs the incoming message

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '').lower()

        if "complaint" in text:
            reply = "📝 Please send your complaint like:\nType: Water\nDescription: Tap leaking\nLocation: Room 101"
        elif "type:" in text:
            reply = "✅ Complaint received. Team will check soon."
        else:
            reply = "👋 Hi! Type 'Complaint' to begin."

        # send the reply
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": reply}
        )

    return {"ok": True}

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
