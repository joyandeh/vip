from django.shortcuts import render

from .services import get_crypto_prices
from .models import CryptoApiSetting


def index(request):

    setting = CryptoApiSetting.objects.filter(
        active=True
    ).first()

    toman_rate = 85000

    if setting:
        toman_rate = setting.toman_rate

    prices = get_crypto_prices()

    cryptos = []

    for symbol, usd_price in prices.items():

        cryptos.append({
            "symbol": symbol,
            "price_usd": usd_price,
            "price_toman": int(
                usd_price * toman_rate
            )
        })

    return render(
        request,
        "core/index.html",
        {
            "cryptos": cryptos,
            "toman_rate": toman_rate,
        }
    )