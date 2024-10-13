from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    # Kiểm tra xem tin nhắn có trong dữ liệu hay không
    if 'message' in data and 'text' in data['message']:
        user_message = data['message']['text']
        print(f"Received message: {user_message}")  # Ghi lại tin nhắn nhận được
        
        # Kiểm tra nếu tin nhắn có liên kết Lazada
        if "lazada" in user_message:
            expanded_link = expand_lazada_link(user_message)
            print(f"Expanded link: {expanded_link}")  # Ghi lại liên kết mở rộng
            return jsonify({"text": f"Expanded link: {expanded_link}"}), 200

    return jsonify({"text": "No valid Lazada link found."}), 200

def expand_lazada_link(short_link):
    try:
        # Gửi yêu cầu GET đến liên kết ngắn
        response = requests.get(short_link, allow_redirects=True, timeout=10)
        
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
