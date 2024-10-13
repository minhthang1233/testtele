from flask import Flask, request
import requests
from urllib.parse import quote

app = Flask(__name__)

# Trang chủ đơn giản
@app.route('/')
def index():
    return "Hello! This is a Lazada link conversion bot."

# Webhook để xử lý yêu cầu từ Telegram Bot
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        # Kiểm tra xem có dữ liệu từ Telegram gửi về không
        if 'message' in data and 'text' in data['message']:
            chat_id = data['message']['chat']['id']
            message = data['message']['text']

            # Xử lý nếu tin nhắn là link rút gọn Lazada
            if "https://s.lazada.vn/" in message:
                expanded_link = expand_lazada_link(message)
                full_link = convert_to_full_lazada_link(expanded_link)
                send_message(chat_id, full_link)
            else:
                send_message(chat_id, "Please send a valid Lazada short link.")
        return "ok", 200

def expand_lazada_link(short_link):
    """Hàm chuyển đổi link rút gọn Lazada thành link đầy đủ bằng cách mở rộng liên kết"""
    response = requests.get(short_link, allow_redirects=True)  # Thay đổi từ requests.head sang requests.get
    return response.url

def convert_to_full_lazada_link(expanded_link):
    """Hàm chuyển đổi link đầy đủ thành link Lazada có mã affiliate"""
    affiliate_id = 'ktheme'  # Thay thế bằng mã affiliate của bạn
    # Sử dụng urllib để mã hóa URL thành định dạng đúng
    encoded_url = quote(expanded_link, safe='')
    full_link = f"https://c.lazada.vn/t/c.Ywv1?url={encoded_url}&sub_aff_id={affiliate_id}"
    return full_link

def send_message(chat_id, text):
    """Gửi tin nhắn qua Telegram"""
    token = '7628217923:AAE1nGUDGxhPLmVr0fYyAcz7b88N8LOsMZ0'  # Thay thế bằng token bot của bạn
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(debug=True)
