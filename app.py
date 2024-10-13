from flask import Flask, request
import requests

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
                print(f"Expanded link: {expanded_link}")  # Log link mở rộng
                # Gọi lại hàm để xác nhận rằng liên kết đã mở rộng tới liên kết cuối cùng
                full_link = expand_lazada_link(expanded_link)
                print(f"Full link: {full_link}")  # Log liên kết đầy đủ
                send_message(chat_id, full_link)
            else:
                send_message(chat_id, "Please send a valid Lazada short link.")
        return "ok", 200

def expand_lazada_link(short_link):
    """Hàm chuyển đổi link rút gọn Lazada thành link đầy đủ"""
    try:
        response = requests.get(short_link, allow_redirects=True)
        return response.url
    except requests.RequestException as e:
        print(f"Error expanding link: {e}")  # Log lỗi nếu có
        return short_link  # Trả về link gốc nếu có lỗi

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
