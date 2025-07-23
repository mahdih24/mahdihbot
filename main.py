from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_URL = os.environ.get("API_URL")

@app.route("/", methods=["GET"])
def home():
    return "ربات کارگزینی در حال اجراست"

@app.route("/", methods=["POST"])
def receive_message():
    data = request.get_json()
    print(f"📥 داده دریافتی از بله: {data}")

    try:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')

        if text == "/start":
            send_message(chat_id, "سلام! به ربات کارگزینی خوش آمدید. یکی از گزینه‌ها را انتخاب کنید 👇", buttons=[
                [{"text": "📝 ثبت درخواست", "command": "/submit"}],
                [{"text": "📋 پیگیری وضعیت", "command": "/status"}],
            ])
        elif text == "/submit":
            send_message(chat_id, "لطفاً اطلاعات خود را برای ثبت درخواست وارد کنید.")
        elif text == "/status":
            send_message(chat_id, "برای پیگیری وضعیت، شماره پیگیری خود را ارسال نمایید.")
        else:
            send_message(chat_id, "دستور نامعتبر است. لطفاً از دکمه‌ها استفاده کنید.")
    except Exception as e:
        print("❌ خطا:", e)

    return jsonify({"status": "ok"})

def send_message(chat_id, text, buttons=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
    }

    if buttons:
        payload["reply_markup"] = {
            "inline_keyboard": buttons
        }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BOT_TOKEN}"
    }

    response = requests.post(f"{API_URL}/sendMessage", json=payload, headers=headers)
    print("📤 پیام ارسال شد:", response.text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
