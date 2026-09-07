import requests
import re


def get_usd_to_toman_rate():
    """دریافت نرخ دلار به تومان:
    - اگر تنظیم فعالی وجود داشته باشد: نرخ دستی (toman_rate)
    - وگرنه: اسکرپ از tgju.org
    - هیچ پیش‌فرضی وجود ندارد
    """
    from core.models import CryptoApiSetting
    
    # First: check for active setting
    active_setting = CryptoApiSetting.objects.filter(active=True).first()
    if active_setting:
        return active_setting.toman_rate

    # Second: scrape from tgju.org (no auth required)
    try:
        response = requests.get('https://www.tgju.org/profile/price_dollar_rl', timeout=8)
        html = response.text
        
        # Extract current price from HTML: <div class="price" data-col="info.last_trade.PDrCotVal">2,236,650</div>
        match = re.search(r'class="price"\s+data-col="info\.last_trade\.PDrCotVal">([0-9,]+)', html)
        if match:
            rial_str = match.group(1).replace(',', '')
            rial_value = int(rial_str)
            return rial_value // 10  # Convert Rial to Toman
    except Exception:
        pass

    return None


def get_fallback_toman_rate():
    """سازگاری - استفاده نکنید. منطق در get_usd_to_toman_rate یکپارچه شده."""
    return None


def get_crypto_prices():

    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=bitcoin,ethereum,tether,tron,binancecoin,solana,ripple,the-open-network"
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
            "TRX": data["tron"]["usd"],
            "BNB": data["binancecoin"]["usd"],
            "SOL": data["solana"]["usd"],
            "XRP": data["ripple"]["usd"],
            "TON": data["the-open-network"]["usd"],
            "UTOPIA": 1.0,
        }

    except Exception:

        return {
            "BTC": 0,
            "ETH": 0,
            "USDT": 0,
            "TRX": 0,
            "BNB": 0,
            "SOL": 0,
            "XRP": 0,
            "TON": 0,
            "UTOPIA": 1.0,
        }