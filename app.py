from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.environ.get('TOKEN')

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = request.get_json()
    chat_id = update['message']['chat']['id']
    text = update['message']['text']

    if "lazada" in text:
        text = convert_lazada_link(text)  # Hàm chuyển đổi link
    else:
        text = "Chỉ hỗ trợ link Lazada."

    send_message(chat_id, text)
    return '', 200

def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload)

def convert_lazada_link(text):
    # Logic chuyển đổi link Lazada
    return "Link đã chuyển đổi: " + text

if __name__ == '__main__':
    app.run(debug=True)
