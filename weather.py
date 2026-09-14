import os
import requests

# 讀取 GitHub Secrets
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# 指定地點：桃園
LATITUDE = 24.9937
LONGITUDE = 121.3010

# Open-Meteo API
url = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUDE}"
    f"&longitude={LONGITUDE}"
    "&daily=precipitation_probability_max"
    "&timezone=Asia%2FTaipei"
    "&forecast_days=1"
)

# 取得天氣資料
response = requests.get(url)
data = response.json()

# 取得今天最高降雨機率
rain_probability = data["daily"]["precipitation_probability_max"][0]

print(f"今天降雨機率：{rain_probability}%")

# 判斷是否超過 70%
if rain_probability > 70:

    message = f"☔ 今天降雨機率 {rain_probability}%，記得帶傘喔！"

    telegram_url = (
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    )

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    requests.post(telegram_url, data=payload)

    print("已發送 Telegram 通知！")

else:
    print("今天降雨機率未超過 70%，不用發送通知。")
