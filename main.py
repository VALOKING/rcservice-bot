from flask import Flask, request
import requests
import os
app = Flask(__name__)
BOT_TOKEN = "8120217348:AAFo7KKaRXPdL-uh43J2sFIP6Ook4bWkHug"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
@app.route('/')
def home():
    return "✅ RC Service Bot is Running"
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("🔔 Webhook triggered", flush=True)
    print("📩 Received:", data, flush=True)
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '').lower()
        if "complaint" in text:
            reply = (
                "📝 Please send your complaint like:\n"
                "Type: Water\n"
                "Description: Tap leaking\n"
                "Location: Room 101"
            )
        elif "type:" in text:
            reply = "✅ Complaint received. Team will check soon."
        else:
            reply = "👋 Hi! Type 'Complaint' to begin."
        # Send message back to user
        requests.post(
            TELEGRAM_API_URL,
            json={"chat_id": chat_id, "text": reply}
        )
    return {"ok": True}
# Run app with dynamic port for Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
