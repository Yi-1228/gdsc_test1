import requests
import os

# 要查詢的股票
stocks = ["1101", "2330", "1102"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Telegram 設定
bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
chat_id = "8980222635"

# Telegram 訊息
message = "📈 股票即時股價\n\n"

for stockid in stocks:

    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stockid}.TW"

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        result = data["chart"]["result"]

        if not result:
            print(f"找不到股票 {stockid}")
            message += f"❌ {stockid}：找不到股票\n"
            continue

        meta = result[0]["meta"]

        price = meta.get("regularMarketPrice")

        if price is None:
            print(f"找不到股票 {stockid} 的股價")
            message += f"❌ {stockid}：找不到股價\n"
            continue

        print(f"股票 {stockid} 股價：{price}")

        # 加入 Telegram 訊息
        message += f"📊 {stockid}：{price}\n"

    except requests.exceptions.Timeout:
        print(f"股票 {stockid}：連線逾時")
        message += f"❌ {stockid}：連線逾時\n"

    except requests.exceptions.HTTPError as e:
        print(f"股票 {stockid}：HTTP 錯誤：{e}")
        message += f"❌ {stockid}：HTTP 錯誤\n"

    except requests.exceptions.RequestException as e:
        print(f"股票 {stockid}：網路連線失敗：{e}")
        message += f"❌ {stockid}：網路連線失敗\n"

    except (KeyError, TypeError, ValueError) as e:
        print(f"股票 {stockid}：資料解析失敗：{e}")
        message += f"❌ {stockid}：資料解析失敗\n"

    except Exception as e:
        print(f"股票 {stockid}：發生錯誤：{e}")
        message += f"❌ {stockid}：發生錯誤\n"


# 傳送 Telegram 訊息
telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

telegram_data = {
    "chat_id": chat_id,
    "text": message
}

try:
    telegram_response = requests.post(
        telegram_url,
        data=telegram_data,
        timeout=10
    )

    telegram_response.raise_for_status()

    print("✅ Telegram 訊息已成功傳送")

except requests.exceptions.RequestException as e:
    print(f"❌ Telegram 傳送失敗：{e}")

