from flask import Flask, request
import requests

app = Flask(__name__)

# Hàm mở rộng liên kết Lazada
def expand_lazada_link(short_link):
    try:
        # Gửi yêu cầu GET đến liên kết ngắn
        response = requests.get(short_link, allow_redirects=True)
        # Kiểm tra nếu có redirect
        if response.history:
            # Trả về URL cuối cùng sau tất cả các redirect
            return response.url
        else:
            # Nếu không có redirect, trả về liên kết ngắn ban đầu
            return short_link
    except requests.RequestException as e:
        print(f"Error expanding link: {e}")
        return short_link

# Đường dẫn webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    # Lấy thông tin tin nhắn từ webhook
    message = data.get('message')
    chat_id = message.get('chat', {}).get('id')
    text = message.get('text')
    
    if text:
        # Kiểm tra xem có phải là liên kết Lazada không
        if "lazada" in text:
            # Mở rộng liên kết
            full_link = expand_lazada_link(text)
            reply_text = f"Full link: {full_link}"
        else:
            reply_text = "Please send a Lazada link."
        
        # Gửi phản hồi trở lại
        send_message(chat_id, reply_text)

    return '', 200

# Hàm gửi tin nhắn trở lại Telegram
def send_message(chat_id, text):
    token = '7628217923:AAE1nGUDGxhPLmVr0fYyAcz7b88N8LOsMZ0'  # Thay 'YOUR_TELEGRAM_BOT_TOKEN' bằng token bot của bạn
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'  # Sử dụng Markdown để định dạng tin nhắn (tùy chọn)
    }
    requests.post(url, json=data)

if __name__ == '__main__':
    app.run(debug=True)
