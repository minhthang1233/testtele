from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Token bot Telegram của bạn
TELEGRAM_BOT_TOKEN = '7628217923:AAE1nGUDGxhPLmVr0fYyAcz7b88N8LOsMZ0'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Kiểm tra nếu không có dữ liệu
    if 'message' not in data:
        return jsonify({"error": "No message found"}), 400

    chat_id = data['message']['chat']['id']
    text = data['message'].get('text', '')

    # Kiểm tra nếu tin nhắn chứa link ngắn
    if 'lazada.vn' in text:
        long_link = expand_link(text)
        send_message(chat_id, long_link)
    else:
        send_message(chat_id, "Vui lòng gửi link Lazada ngắn để chuyển đổi.")

    return jsonify({"status": "success"}), 200

def expand_link(short_url):
    try:
        response = requests.get(short_url, allow_redirects=False)
        # Lấy URL đầy đủ từ phản hồi
        if response.status_code == 302:
            return response.headers['Location']
        else:
            return "Không thể mở rộng liên kết."
    except Exception as e:
        return f"Lỗi: {str(e)}"

def send_message(chat_id, text):
    url = TELEGRAM_API_URL + 'sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(debug=True)
