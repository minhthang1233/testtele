import os
import requests
from urllib.parse import quote
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Khởi tạo ứng dụng Flask
app = Flask(__name__)

# Bot token từ BotFather
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Hàm chuyển đổi từ link ngắn sang link đầy đủ
def convert_link(short_link):
    try:
        # Thực hiện yêu cầu HEAD để lấy link đầy đủ
        response = requests.head(short_link, allow_redirects=True)
        full_url = response.url

        # Tạo link Lazada đầy đủ với affiliate
        affiliate_id = "ktheme"  # Thay thế bằng ID tiếp thị liên kết của bạn
        encoded_url = quote(full_url, safe='')
        long_link = f"https://c.lazada.vn/t/c.Ywv1?url={encoded_url}&sub_aff_id={affiliate_id}"

        return long_link
    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}"

# Hàm xử lý lệnh start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Chào bạn! Gửi cho tôi một liên kết Lazada để tôi chuyển đổi nó!")

# Hàm xử lý khi người dùng gửi link
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    if "https://s.lazada.vn/" in user_message:
        converted_link = convert_link(user_message)
        await update.message.reply_text(f"Liên kết đầy đủ: {converted_link}")
    else:
        await update.message.reply_text("Vui lòng gửi một liên kết hợp lệ từ Lazada.")

# Khởi tạo bot Telegram
async def telegram_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Thêm các handler cho bot
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    await application.start()
    await application.updater.idle()

# Khởi động ứng dụng Flask
@app.route('/')
def index():
    return "Bot đang chạy!"

if __name__ == "__main__":
    # Khởi động bot Telegram
    import asyncio
    asyncio.run(telegram_bot())
    
    # Khởi chạy Flask
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
