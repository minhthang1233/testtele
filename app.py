from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Hàm xử lý webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    
    # Kiểm tra xem có tin nhắn mới không
    if 'message' in update:
        chat_id = update['message']['chat']['id']
        message_text = update['message'].get('text', '')

        # Gọi hàm để xử lý liên kết
        response_text = process_links(message_text)

        # Gửi phản hồi về Telegram
        send_message(chat_id, response_text)

    return jsonify({"status": "ok"})

# Hàm gửi tin nhắn đến bot Telegram
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot7628217923:AAE1nGUDGxhPLmVr0fYyAcz7b88N8LOsMZ0/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

# Hàm lấy link cuối cùng từ URL
def get_final_link(link):
    try:
        # Gửi yêu cầu để lấy link cuối
        response = requests.get(link, allow_redirects=True)
        return response.url  # Trả về link cuối cùng
    except requests.exceptions.RequestException as e:
        return str(e)  # Trả về lỗi nếu có

# Hàm lọc các tham số không mong muốn
def filter_unwanted_parameters(url):
    # Chỉ giữ lại tham số utm_source
    allowed_params = [
        "utm_source"
    ]
    
    url_parts = url.split('?')
    
    if len(url_parts) < 2:
        return url  # Không có tham số thì trả về nguyên URL
    
    base_url = url_parts[0]
    params = url_parts[1].split('&')
    
    # Chỉ giữ lại các tham số được phép
    filtered_params = [param for param in params if any(param.startswith(allowed) for allowed in allowed_params)]
    
    # Tạo lại URL
    if filtered_params:
        return f"?{'&'.join(filtered_params)}"
    else:
        return ""  # Nếu không còn tham số nào, trả về rỗng

# Hàm xử lý nhiều liên kết
def process_links(message):
    parts = message.split(" ")
    converted_message = []
    
    for part in parts:
        # Kiểm tra và tự động thêm tiền tố https:// nếu thiếu
        if part.startswith("s.shopee.vn") or part.startswith("shope.ee"):
            part = "https://" + part

        # Nếu không phải là liên kết hợp lệ của Shopee
        if not (part.startswith("https://s.shopee.vn") or part
