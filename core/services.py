import requests


def get_usd_to_toman_rate():
    """دریافت نرخ دلار به تومان از API، در صورت خطا None برمی‌گرداند"""
    from core.models import CryptoApiSetting
    
    setting = CryptoApiSetting.objects.filter(active=True).first()
    if not setting or not setting.usd_toman_api_url:
        return None

    url = setting.usd_toman_api_url

    try:
        response = requests.get(url, timeout=8)
        data = response.json()

        # exchangerate-api.com فرمت: {"rates": {"IRR": 42000000}} (ریال)
        if "rates" in data and "IRR" in data["rates"]:
            # تبدیل ریال به تومان (تقسیم بر 10)
            return int(data["rates"]["IRR"]) // 10

        # freecurrencyapi.com فرمت: {"data": {"IRR": 42000000}} (ریال)
        if "data" in data and "IRR" in data["data"]:
            return int(data["data"]["IRR"]) // 10

        # ارزهای دیگر که ممکن است IRR برگردانند
        if "rates" in data:
            for key, value in data["rates"].items():
                if key.upper() in ("IRR", "TOMAN", "IRT"):
                    # اگر TOMAN برگرداند مستقیم استفاده کن، اگر IRR برگرداند تقسیم بر 10
                    if key.upper() == "TOMAN":
                        return int(value)
                    return int(value) // 10

    except Exception:
        pass

    return None


def get_fallback_toman_rate():
    """دریافت نرخ دستی از تنظیمات (اولویت: تنظیمات با نرخ غیر پیش‌فرض که اخیراً بروزرسانی شده، سپس فعال، سپس پیش‌فرض)"""
    from core.models import CryptoApiSetting
    
    # First priority: most recently updated setting with non-default rate (user is configuring this)
    custom_rate_setting = CryptoApiSetting.objects.exclude(toman_rate=85000).order_by('-updated_at').first()
    if custom_rate_setting:
        return custom_rate_setting.toman_rate
    
    # Second priority: active setting
    active_setting = CryptoApiSetting.objects.filter(active=True).first()
    if active_setting:
        return active_setting.toman_rate
    
    # Third priority: most recently updated setting
    latest_setting = CryptoApiSetting.objects.order_by('-updated_at').first()
    if latest_setting:
        return latest_setting.toman_rate
    
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