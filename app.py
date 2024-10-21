import time
import requests
import random
from bs4 import BeautifulSoup
from telegram import Bot

# Token từ BotFather và ID nhóm Telegram để gửi thông báo
TOKEN = '7628217923:AAE1nGUDGxhPLmVr0fYyAcz7b88N8LOsMZ0'
GROUP_CHAT_ID = 'https://t.me/thutele1234'  # ID nhóm Telegram để gửi thông báo

# Hàm lấy danh sách các shop ngẫu nhiên từ Shopee Mall
def get_random_shop():
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    
    # URL của Shopee Mall hoặc trang danh sách shop
    mall_url = 'https://shopee.vn/mall'
    
    try:
        response = requests.get(mall_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm các thẻ chứa thông tin shop (dựa trên cấu trúc HTML của trang)
        shops = soup.find_all('a', class_='shop-link')  # Điều chỉnh class CSS cho đúng
        
        if shops:
            # Chọn ngẫu nhiên một shop từ danh sách
            random_shop = random.choice(shops)
            shop_url = 'https://shopee.vn' + random_shop['href']
            return shop_url
        else:
            return None
    except Exception as e:
        print(f"Lỗi khi truy cập Shopee Mall: {e}")
        return None

# Hàm để truy cập vào shop Shopee và tìm kiếm mã giảm giá
def search_shopee_shop(shop_url):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    
    try:
        response = requests.get(shop_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Lọc mã giảm giá từ trang shop (cần kiểm tra cấu trúc cụ thể của Shopee)
        discount_section = soup.find_all('div', class_='discount-info')  # Điều chỉnh class CSS cho đúng
        discount_links = []
        
        for discount in discount_section:
            code = discount.find('span', class_='discount-code').text
            link = discount.find('a', href=True)['href']
            discount_links.append(f"Mã: {code}, Link: {link}")
        
        return discount_links
    except Exception as e:
        print(f"Lỗi khi truy cập shop {shop_url}: {e}")
        return []

# Hàm gửi thông báo về các mã giảm giá tìm được
def send_discount_message(bot, chat_id, shop_url, discounts):
    message = f"Mã giảm giá từ shop {shop_url}:\n" + "\n".join(discounts)
    bot.send_message(chat_id=chat_id, text=message)

# Hàm chính để lấy shop ngẫu nhiên và tìm mã giảm giá
def main():
    bot = Bot(token=TOKEN)
    
    found_discounts = set()
    
    while True:
        shop_url = get_random_shop()  # Lấy shop ngẫu nhiên từ Shopee Mall
        
        if shop_url:
            print(f"Đang kiểm tra shop: {shop_url}")
            discounts = search_shopee_shop(shop_url)
            
            if discounts:
                # Kiểm tra nếu mã giảm giá mới chưa được gửi
                discount_hash = tuple(discounts)
                if discount_hash not in found_discounts:
                    found_discounts.add(discount_hash)
                    send_discount_message(bot, GROUP_CHAT_ID, shop_url, discounts)
        
        # Chờ một khoảng thời gian trước khi kiểm tra lại (ví dụ 30 phút)
        time.sleep(1800)

if __name__ == '__main__':
    main()
