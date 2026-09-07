from django.shortcuts import render
from .services import get_crypto_prices, get_usd_to_toman_rate, get_fallback_toman_rate
from .models import CryptoApiSetting, HomePageSection, SiteSetting


CRYPTO_NAMES = {
    'BTC': 'بیت‌کوین',
    'ETH': 'اتریوم',
    'USDT': 'تتر',
    'BNB': 'بایننس کوین',
    'TRX': 'ترون',
    'SOL': 'سولانا',
    'XRP': 'ریپل',
    'PM': 'پرفکت مانی',
    'TON': 'تون کوین',
    'UTOPIA': 'یوتوپیا',
}


def index(request):

    # Get active setting for API URL
    active_setting = CryptoApiSetting.objects.filter(active=True).first()

    # اولویت: ۱) نرخ API، ۲) تنظیمات دستی پنل (fallback), ۳) پیش‌فرض ۸۵۰۰۰
    api_rate = get_usd_to_toman_rate()
    if api_rate:
        toman_rate = api_rate
    else:
        fallback_rate = get_fallback_toman_rate()
        if fallback_rate:
            toman_rate = fallback_rate
        else:
            toman_rate = 85000

    sell_buy_rate = getattr(active_setting, 'sell_buy_rate', 500) if active_setting else 500

    prices = get_crypto_prices()

    cryptos = []

    for symbol, usd_price in prices.items():

        cryptos.append({
            "symbol": symbol,
            "name": CRYPTO_NAMES.get(symbol, symbol),
            "price_usd": usd_price,
            "price_toman": int(
                usd_price * toman_rate
            )
        })

    # Add PM (Perfect Money) as 1 USD = toman_rate
    cryptos.append({
        "symbol": "PM",
        "name": "پرفکت مانی",
        "price_usd": 1,
        "price_toman": toman_rate
    })

    site_settings = SiteSetting.get_solo()

    homepage_sections = HomePageSection.objects.filter(
        is_active=True
    ).order_by('order', '-created_at')

    return render(
        request,
        "core/index.html",
        {
            "cryptos": cryptos,
            "toman_rate": toman_rate,
            "sell_buy_rate": sell_buy_rate,
            "site_settings": site_settings,
            "homepage_sections": homepage_sections,
            "unreads_count": 0,
            "telegram_url": "https://t.me/tronlnd_support",
        }
    )
