from django.shortcuts import render

from .services import get_crypto_prices
from .models import CryptoApiSetting, HomePageSection, SiteSetting


CRYPTO_NAMES = {
    'BTC': 'بیت‌کوین',
    'ETH': 'اتریوم',
    'USDT': 'تتر',
    'BNB': 'بایننس کوین',
    'TRX': 'ترون',
}


def index(request):

    setting = CryptoApiSetting.objects.filter(
        active=True
    ).first()

    toman_rate = 85000
    sell_buy_rate = 500  # اختلاف قیمت خرید و فروش به تومان

    if setting:
        toman_rate = setting.toman_rate
        sell_buy_rate = getattr(setting, 'sell_buy_rate', 500)

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

    site_setting = SiteSetting.get_solo()

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
            "site_setting": site_setting,
            "homepage_sections": homepage_sections,
            "unreads_count": 0,
            "telegram_url": "https://t.me/tronlnd_support",
        }
    )
