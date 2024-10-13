from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message']['text']

        if text.startswith("https://s.lazada.vn/"):
            full_link = expand_link(text)
            response_text = full_link if full_link else "Không thể mở rộng liên kết."
        else:
            response_text = "Vui lòng gửi liên kết Lazada hợp lệ."

        send_message(chat_id, response_text)

    return jsonify({'status': 'ok'})

def expand_link(short_link):
    try:
        response = requests.get(short_link, allow_redirects=False)
        if response.status_code == 302:
            return response.headers['Location']
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def send_message(chat_id, text):
    # Thay 'YOUR_BOT_TOKEN' bằng token của bot Telegram của bạn
    token = '7628217923:AAE1nGUDGxhPLmVr0fYyAcz7b88N8LOsMZ0'
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(debug=True)
