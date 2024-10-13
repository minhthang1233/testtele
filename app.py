import os
import logging
import requests
from flask import Flask, request

app = Flask(__name__)

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG)

# Token bot Telegram
TOKEN = os.environ.get('BOT_TOKEN')  # Đảm bảo đã thiết lập biến môi trường này trên Heroku
if TOKEN is None:
    logging.error("BOT_TOKEN is not set.")
    raise ValueError("BOT_TOKEN must be set in environment variables.")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = request.get_json()
    logging.debug(f"Received update: {update}")
    
    chat_id = update['message']['chat']['id']
    message_text = update['message']['text']

    if message_text.startswith('https://s.lazada.vn'):
        full_link = convert_link(message_text)
        send_message(chat_id, full_link)
    else:
        send_message(chat_id, "Liên kết không hợp lệ. Vui lòng gửi liên kết Lazada.")

    return '', 200

def convert_link(short_link):
    try:
        response = requests.get(short_link, allow_redirects=False)
        if response.status_code == 302:
            return response.headers['Location']
        else:
            return "Không thể mở rộng liên kết."
    except Exception as e:
        logging.error(f"Error in converting link: {e}")
        return "Có lỗi xảy ra khi mở rộng liên kết."

def send_message(chat_id, text):
    url = BASE_URL + 'sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    try:
        requests.post(url, json=payload)
        logging.debug(f"Sent message: {text} to chat_id: {chat_id}")
    except Exception as e:
        logging.error(f"Error in sending message: {e}")

if __name__ == '__main__':
    app.run(debug=True)
