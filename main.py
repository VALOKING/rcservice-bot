from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN"
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route('/')
def home():
    return "✅ RC Service Bot is running"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    chat_id = data['message']['chat']['id']
    message = data['message'].get('text', '')

    if "complaint" in message.lower():
        reply = "📝 Send your complaint like:\nType: Water\nDescription: Tap leaking\nLocation: Room 101"
    elif "Type:" in message:
        reply = "✅ Complaint registered. We'll fix it!"
    else:
        reply = "👋 Hi! Type 'Complaint' to begin."

    requests.post(URL, json={"chat_id": chat_id, "text": reply})
    return {"ok": True}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
