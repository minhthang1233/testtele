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

# Hàm xử lý liên kết
def process_links(message):
    parts = message.split(" ")
    result = []

    for part in parts:
        # Kiểm tra tên miền bắt đầu bằng s.shopee.vn hoặc shope.ee
        if part.startswith("https://s.shopee.vn") or part.startswith("https://shope.ee"):
            # Lấy link cuối cùng nếu là tên miền hợp lệ
            final_url = get_final_link(part)
            # Chỉ giữ lại tên miền và đường dẫn của link cuối cùng
            origin_link = final_url.split("?")[0]  # Bỏ đi các tham số sau '?'
            # Tạo liên kết cuối
            result_link = f"https://shope.ee/an_redir?origin_link={origin_link}&affiliate_id=17305270177&sub_id=huong"
            result.append(result_link)
        else:
            result.append(part)  # Giữ nguyên các phần khác không phải là link

    return " ".join(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
