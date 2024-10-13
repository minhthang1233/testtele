import requests
from flask import Flask, request
import telebot

# Khởi tạo Flask app và bot Telegram
app = Flask(__name__)
bot_token = '7628217923:AAE1nGUDGxhPLmVr0fYyAcz7b88N8LOsMZ0'  # Thay thế bằng token bot của bạn
bot = telebot.TeleBot(bot_token)

# Hàm mở rộng link
def expand_link(short_url):
    try:
        # Gửi yêu cầu tới link ngắn với allow_redirects=True để tự động theo dõi chuyển hướng
        response = requests.get(short_url, allow_redirects=True)
        # Trả về URL cuối cùng
        return response.url if response.status_code == 200 else "Không thể mở rộng liên kết."
    except Exception as e:
        return f"Lỗi: {str(e)}"

# Xử lý khi có tin nhắn gửi đến bot
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Chào mừng bạn! Gửi một link ngắn Lazada và tôi sẽ mở rộng nó cho bạn.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    short_url = message.text
    expanded_url = expand_link(short_url)
    bot.reply_to(message, expanded_url)

# Xử lý webhook từ Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_data(as_text=True)
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    return "OK", 200

if __name__ == '__main__':
    app.run()
