# 先導入後面會用到的套件
import requests
from bs4 import BeautifulSoup

# 要爬的股票
stock = ["1101","2330","1102"]

# 模擬瀏覽器請求，避免被網站攔截
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for i in range(len(stock)):
    # 現在處理的股票
    stockid = stock[i]

    # 網址塞入股票編號
    url = "https://tw.stock.yahoo.com/quote/" + stockid + ".TW"

    # 發送請求，帶上headers
    r = requests.get(url, headers=headers)

    # 解析回應的HTML
    soup = BeautifulSoup(r.text, "html.parser")

    # 抓取股價，使用較穩定的標籤屬性，不寫死容易變動的css class
    price = soup.find("span", attrs={"data-testid": "q-quote-price"})

    # 如果找不到股價
    if price is None:
        print("找不到股票 " + stockid + " 的股價")
        continue

    print(f"股票 {stockid} 股價：{price.text}")
