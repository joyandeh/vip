import requests


def get_crypto_prices():

    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=bitcoin,ethereum,tether"
        "&vs_currencies=usd"
    )

    try:

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        return {
            "BTC": data["bitcoin"]["usd"],
            "ETH": data["ethereum"]["usd"],
            "USDT": data["tether"]["usd"],
        }

    except Exception:

        return {
            "BTC": 0,
            "ETH": 0,
            "USDT": 0,
        }