import requests
from bs4 import BeautifulSoup

# 要爬的股票
stocks = ["1101", "2330", "1102"]

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

for stockid in stocks:

    url = f"https://tw.stock.yahoo.com/quote/{stockid}.TW"

    try:
        # 發送請求
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        # 檢查 HTTP 狀態
        response.raise_for_status()

        # 解析 HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # 找股價
        price = soup.find(
            "span",
            attrs={"data-testid": "q-quote-price"}
        )

        if price is None:
            print(f"找不到股票 {stockid} 的股價")
            continue

        print(f"股票 {stockid} 股價：{price.get_text(strip=True)}")

    except requests.exceptions.Timeout:
        print(f"股票 {stockid}：連線逾時")

    except requests.exceptions.HTTPError as e:
        print(f"股票 {stockid}：HTTP 錯誤")

    except requests.exceptions.RequestException:
        print(f"股票 {stockid}：網路連線失敗")

    except Exception as e:
        print(f"股票 {stockid}：發生未知錯誤 {e}")
