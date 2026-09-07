# 先導入後面會用到的套件
import requests
from bs4 import BeautifulSoup
import time

# 要爬的股票
stock = ["1101","2330","1102"]

for i in range(len(stock)):

    # 現在處理的股票
    stockid = stock[i]

    # 網址塞入股票編號
    url = "https://tw.stock.yahoo.com/quote/" + stockid + ".TW"

    # 發送請求
    r = requests.get(url)

    # 解析回應的 HTML
    soup = BeautifulSoup(r.text, "html.parser")

    # 定位股價
    price = soup.find(
        "span",
        class_="Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)"
    )

    # 如果找不到股價
    if price is None:
        print("找不到股票 " + stockid + " 的股價")
        continue

    # 取得文字
    price = price.get_text(strip=True)

    # 回報的訊息
    message = "股票 " + stockid + " 即時股價為 " + price

    # bot token
    token = "你的 bot token"

    # 使用者 id
    chat_id = "你的 telegram id"

    # bot 送訊息
    telegram_url = (
        f"https://api.telegram.org/bot{token}/sendMessage"
        f"?chat_id={chat_id}&text={message}"
    )

    requests.get(telegram_url)

    print(message)

    # 每次停 3 秒
    time.sleep(3)
