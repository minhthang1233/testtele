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
    """Hàm mở rộng link rút gọn Lazada để lấy link đầy đủ."""
    try:
        response = requests.get(short_link, allow_redirects=True)
        response.raise_for_status()  # Kiểm tra xem yêu cầu có thành công không
        return response.url  # Trả về URL cuối cùng
    except requests.RequestException as e:
        print(f"Error expanding link: {e}")
        return None  # Trả về None nếu có lỗi

def convert_to_full_lazada_link(expanded_link):
    """Hàm tạo link Lazada đầy đủ với mã affiliate."""
    if expanded_link:
        affiliate_id = 'ktheme'  # Thay thế bằng mã affiliate của bạn
        # Mã hóa URL đầy đủ để sử dụng trong link
        encoded_url = quote(expanded_link, safe='')
        full_link = f"https://c.lazada.vn/t/c.Ywv1?url={encoded_url}&sub_aff_id={affiliate_id}"
        return full_link
    else:
        return "Could not retrieve the expanded link."  # Thông báo lỗi

def send_message(chat_id, text):
    """Gửi tin nhắn qua Telegram."""
    token = '7628217923:AAE1nGUDGxhPLmVr0fYyAcz7b88N8LOsMZ0'  # Thay thế bằng token bot của bạn
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(debug=True)
