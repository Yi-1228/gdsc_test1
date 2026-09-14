import requests

# 要查詢的股票
stocks = ["1101", "2330", "1102"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

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
            continue

        meta = result[0]["meta"]

        price = meta.get("regularMarketPrice")

        if price is None:
            print(f"找不到股票 {stockid} 的股價")
            continue

        print(f"股票 {stockid} 股價：{price}")

    except requests.exceptions.Timeout:
        print(f"股票 {stockid}：連線逾時")

    except requests.exceptions.HTTPError as e:
        print(f"股票 {stockid}：HTTP 錯誤：{e}")

    except requests.exceptions.RequestException as e:
        print(f"股票 {stockid}：網路連線失敗：{e}")

    except (KeyError, TypeError, ValueError) as e:
        print(f"股票 {stockid}：資料解析失敗：{e}")

    except Exception as e:
        print(f"股票 {stockid}：發生錯誤：{e}")

