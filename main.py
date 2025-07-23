from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")  # باید در railway یا runflare ست شود
API_URL = f"https://bot.bale.ai/bot{BOT_TOKEN}"

@app.route("/", methods=["GET"])
def home():
    return "ربات در حال اجراست"

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    print(f"📥 داده دریافتی از بله: {data}")

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "سلام! خوش آمدید 🌟", with_buttons=True)
        else:
            send_message(chat_id, f"شما نوشتید: {text}")

    return jsonify({"ok": True})

def send_message(chat_id, text, with_buttons=False):
    payload = {
        "chat_id": chat_id,
        "text": text
    }

    if with_buttons:
        payload["reply_markup"] = {
            "keyboard": [
                [{"text": "گزینه ۱"}, {"text": "گزینه ۲"}],
                [{"text": "راهنما"}]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": False
        }

    headers = {"Content-Type": "application/json"}
    requests.post(f"{API_URL}/sendMessage", json=payload, headers=headers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
