from django.shortcuts import render
from .services import get_crypto_prices, get_usd_toman_rate, get_rates_status
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
    # Get rates from cache/DB (no API calls in request path)
    toman_rate = get_usd_toman_rate()
    prices = get_crypto_prices()
    
    active_setting = CryptoApiSetting.objects.filter(active=True).first()
    sell_buy_rate = getattr(active_setting, 'sell_buy_rate', 500) if active_setting else 500

    cryptos = []

    if prices:
        for symbol, usd_price in prices.items():
            price_toman = None
            if toman_rate and usd_price:
                price_toman = int(usd_price * toman_rate)
            
            cryptos.append({
                "symbol": symbol,
                "name": CRYPTO_NAMES.get(symbol, symbol),
                "price_usd": float(usd_price) if usd_price else None,
                "price_toman": price_toman,
            })

    # Add PM (Perfect Money) as 1 USD = toman_rate
    if toman_rate:
        cryptos.append({
            "symbol": "PM",
            "name": "پرفکت مانی",
            "price_usd": 1.0,
            "price_toman": toman_rate,
        })

    site_settings = SiteSetting.get_solo()
    rates_status = get_rates_status()

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
            "rates_status": rates_status,
        }
    )