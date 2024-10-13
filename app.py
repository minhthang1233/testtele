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
        return f"{base_url}?{'&'.join(filtered_params)}"
    else:
        return base_url  # Nếu không còn tham số nào, trả về chỉ base_url

# Hàm xử lý nhiều liên kết
def process_links(message):
    parts = message.split(" ")
    converted_message = []
    
    for part in parts:
        # Nếu không phải là liên kết bắt đầu bằng s.shopee.vn hoặc shope.ee
        if not (part.startswith("https://s.shopee.vn") or part.startswith("https://shope.ee")):
            converted_message.append(part)
        else:
            # Lấy link cuối cùng
            final_url = get_final_link(part)
            if part.startswith("https://s.shopee.vn"):
                origin_link = final_url.split("?")[0]  # Bỏ đi các tham số sau '?'
                result_link = f"https://shope.ee/an_redir?origin_link={origin_link}&affiliate_id=17305270177&sub_id=huong"
            else:
                # Trả về link shope.ee với định dạng yêu cầu và loại bỏ tham số không mong muốn
                final_url_with_params = get_final_link(part)  # Lấy final_url có các tham số
                origin_link = final_url_with_params.split("?")[0]  # Lấy base_url
                additional_params = final_url_with_params.split("?")[1] if "?" in final_url_with_params else ""
                
                # Lọc và thêm tham số cần thiết
                filtered_params = filter_unwanted_parameters(final_url_with_params)
                result_link = f"https://shope.ee/an_redir?origin_link={origin_link}{filtered_params}&affiliate_id=17305270177&sub_id=huong"
                
            converted_message.append(result_link)
    
    # Nếu không có liên kết hợp lệ
    if not any(link.startswith("https://s.shopee.vn") or link.startswith("https://shope.ee") for link in parts):
        return "Vui lòng nhập link bắt đầu bằng s.shopee.vn hoặc shope.ee. Những link khác gửi thẳng vào nhóm => https://zalo.me/g/rycduw016"
    
    return " ".join(converted_message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
