import os
import logging
import requests
from flask import Flask, request

app = Flask(__name__)

# Cấu hình logging
logging.basicConfig(level=logging.INFO)

# Lấy token từ biến môi trường
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

@app.route('/webhook', methods=['POST'])
def webhook():
    # Lấy dữ liệu từ Telegram
    update = request.get_json()
    logging.info(f"Received update: {update}")

    # Kiểm tra xem có tin nhắn không
    if 'message' in update:
        chat_id = update['message']['chat']['id']
        text = update['message'].get('text', '')

        # Xử lý tin nhắn
        if "lazada" in text.lower():
            full_link = convert_short_link(text)  # Hàm chuyển đổi link ngắn
            send_message(chat_id, full_link)

    return '', 200

def convert_short_link(short_link):
    # Thay thế hàm này bằng logic thực tế để chuyển đổi link ngắn
    # Đây chỉ là ví dụ, hãy thay đổi để phù hợp với yêu cầu của bạn
    return f"Đây là link đầy đủ: {short_link.replace('short.lazada', 'www.lazada.vn')}"

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=payload)
    logging.info(f"Sent message: {text}, Response: {response.json()}")

if __name__ == '__main__':
    app.run(debug=True)
