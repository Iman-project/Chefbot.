# app.py
from flask import Flask, request
import os
import json
import requests
from agent import handle_message
from flask import Flask
from dashboard_blueprint import dashboard_bp   # <-- correct import

app = Flask(__name__)
app.secret_key = "your-secret-key"

app.register_blueprint(dashboard_bp, url_prefix="/dashboard")   # <-- correct variable


# Load environment variables from .env
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")  # e.g., "chefbot_secret"

# ----------------------------
# VERIFY WEBHOOK (GET)
# ----------------------------
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("WEBHOOK VERIFIED")
            return challenge, 200
        else:
            return "Verification token mismatch", 403
    return "Hello CHEFBOT", 200

# ----------------------------
# RECEIVE MESSAGES (POST)
# ----------------------------
@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    print("Received:", json.dumps(data, indent=2))

    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        messages = value.get("messages")
        if messages:
            for msg in messages:
                phone_number = msg["from"]
                text = msg["text"]["body"]
                
                # Example: restaurant token included in message like: "TOKEN1 Hi"
                if " " in text:
                    restaurant_token, user_text = text.split(" ", 1)
                else:
                    restaurant_token, user_text = "TOKEN1", text  # default token

                # Get AI response
                response_text = handle_message(phone_number, user_text, restaurant_token)

                # Send back via WhatsApp Cloud API
                send_whatsapp_message(phone_number, response_text)

    except Exception as e:
        print("Error processing message:", e)

    return "EVENT_RECEIVED", 200

# ----------------------------
# SEND MESSAGE FUNCTION
# ----------------------------
def send_whatsapp_message(to, text):
    url = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    r = requests.post(url, json=payload, headers=headers)
    print("Sent:", r.status_code, r.text)
    return r.status_code, r.text

# ----------------------------
if __name__ == "__main__":
    app.run(port=5000)
