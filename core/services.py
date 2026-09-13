import requests
import logging
from decimal import Decimal
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)

# Cache keys
CACHE_KEY_USD_TOMAN = 'rate:usd_toman'
CACHE_KEY_CRYPTO_PRICES = 'rate:crypto_prices'
CACHE_KEY_LAST_UPDATE = 'rate:last_update'

# Cache TTLs
CACHE_TTL_USD_TOMAN = 300      # 5 minutes
CACHE_TTL_CRYPTO = 300         # 5 minutes
CACHE_TTL_LAST_UPDATE = 86400  # 24 hours


def fetch_usd_toman_rate():
    """
    Fetch USD to Toman rate from multiple API sources.
    Returns (rate: Decimal, source: str) or (None, None) if all fail.
    """
    sources = [
        ('nobitex', 'https://api.nobitex.ir/v2/orderbook/USDTIRT', parse_nobitex),
        ('nerkh.io', 'https://api.nerkh.io/v2/prices/json/lite/currency', parse_nerkh_io),
        ('tgju.org', 'https://www.tgju.org/profile/price_dollar_rl', parse_tgju_html),
    ]
    
    for source_name, url, parser in sources:
        try:
            response = requests.get(url, timeout=3)
            response.raise_for_status()
            data = response.json() if 'json' in response.headers.get('content-type', '') else response.text
            rate = parser(data)
            if rate and rate > Decimal('10000'):
                logger.info(f"Fetched USD/Toman rate from {source_name}: {rate}")
                return rate, source_name
        except Exception as e:
            logger.warning(f"Failed to fetch USD/Toman from {source_name}: {e}")
            continue
    
    return None, None


def parse_nerkh_io(data):
    """Parse nerkh.io response: {'usd': {'price': 58500000, ...}} - price in Rial"""
    try:
        if 'usd' in data and 'price' in data['usd']:
            rial = Decimal(str(data['usd']['price']))
            return rial / Decimal('10')  # Rial to Toman
    except Exception:
        pass
    return None


def parse_nobitex(data):
    """Parse nobitex response: {'status': 'ok', 'lastTrade': '5850000'} - in Rial"""
    try:
        if data.get('status') == 'ok' and 'lastTrade' in data:
            rial = Decimal(str(data['lastTrade']))
            return rial / Decimal('10')  # Rial to Toman
    except Exception:
        pass
    return None


def parse_tgju_html(data):
    """Parse tgju.org HTML response to extract USD price in Rial"""
    import re
    try:
        html = data
        # Look for the price pattern in HTML
        match = re.search(r'class="price"\s+data-col="info\.last_trade\.PDrCotVal">([0-9,]+)', html)
        if match:
            rial_str = match.group(1).replace(',', '')
            rial = Decimal(rial_str)
            return rial / Decimal('10')  # Rial to Toman
    except Exception:
        pass
    return None


def fetch_crypto_prices():
    """
    Fetch crypto prices from CoinGecko.
    Returns (prices_dict: dict, source: str) or (None, None) if fail.
    """
    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=bitcoin,ethereum,tether,tron,binancecoin,solana,ripple,the-open-network"
        "&vs_currencies=usd"
    )
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        prices = {
            'BTC': Decimal(str(data['bitcoin']['usd'])),
            'ETH': Decimal(str(data['ethereum']['usd'])),
            'USDT': Decimal(str(data['tether']['usd'])),
            'TRX': Decimal(str(data['tron']['usd'])),
            'BNB': Decimal(str(data['binancecoin']['usd'])),
            'SOL': Decimal(str(data['solana']['usd'])),
            'XRP': Decimal(str(data['ripple']['usd'])),
            'TON': Decimal(str(data['the-open-network']['usd'])),
            'UTOPIA': Decimal('1.0'),
        }
        
        logger.info(f"Fetched {len(prices)} crypto prices from coingecko")
        return prices, 'coingecko'
    except Exception as e:
        logger.warning(f"Failed to fetch crypto prices from coingecko: {e}")
        return None, None


def save_rate_to_db(rate_type, symbol, value, source):
    """Save fetched rate to database for persistence"""
    from core.models import CachedRate
    try:
        CachedRate.objects.create(
            rate_type=rate_type,
            symbol=symbol,
            value=value,
            source=source
        )
    except Exception as e:
        logger.error(f"Failed to save rate to DB: {e}")


def get_latest_rate_from_db(rate_type, symbol=''):
    """Get latest rate from database"""
    from core.models import CachedRate
    try:
        rate = CachedRate.objects.filter(rate_type=rate_type, symbol=symbol).first()
        if rate:
            return rate.value, rate.source, rate.fetched_at
    except Exception as e:
        logger.error(f"Failed to get rate from DB: {e}")
    return None, None, None


def update_all_rates():
    """
    Fetch all rates from APIs and store in Redis + Database.
    This should be called periodically (e.g., via cron/celery).
    Returns dict with results.
    """
    results = {'usd_toman': None, 'crypto_prices': None, 'errors': []}
    
    # Fetch USD/Toman
    rate, source = fetch_usd_toman_rate()
    if rate:
        cache.set(CACHE_KEY_USD_TOMAN, rate, CACHE_TTL_USD_TOMAN)
        save_rate_to_db('usd_toman', '', rate, source)
        results['usd_toman'] = {'rate': rate, 'source': source}
    else:
        results['errors'].append('Failed to fetch USD/Toman rate')
    
    # Fetch Crypto Prices
    prices, source = fetch_crypto_prices()
    if prices:
        cache.set(CACHE_KEY_CRYPTO_PRICES, prices, CACHE_TTL_CRYPTO)
        for symbol, price in prices.items():
            save_rate_to_db('crypto_price', symbol, price, source)
        results['crypto_prices'] = {'count': len(prices), 'source': source}
    else:
        results['errors'].append('Failed to fetch crypto prices')
    
    # Update last successful update timestamp
    if not results['errors']:
        cache.set(CACHE_KEY_LAST_UPDATE, timezone.now().isoformat(), CACHE_TTL_LAST_UPDATE)
    
    return results


def get_usd_toman_rate():
    """
    Get USD/Toman rate from cache, then database.
    Returns Decimal or None (no fallback).
    """
    # Try Redis cache first
    rate = cache.get(CACHE_KEY_USD_TOMAN)
    if rate is not None:
        return rate
    
    # Try database
    rate, source, fetched_at = get_latest_rate_from_db('usd_toman')
    if rate is not None:
        # Warm up cache
        cache.set(CACHE_KEY_USD_TOMAN, rate, CACHE_TTL_USD_TOMAN)
        return rate
    
    return None


def get_crypto_prices():
    """
    Get crypto prices from cache, then database.
    Returns dict or None (no fallback).
    """
    # Try Redis cache first
    prices = cache.get(CACHE_KEY_CRYPTO_PRICES)
    if prices is not None:
        return prices
    
    # Try database - get latest for each symbol
    from core.models import CachedRate
    try:
        symbols = ['BTC', 'ETH', 'USDT', 'TRX', 'BNB', 'SOL', 'XRP', 'TON', 'UTOPIA']
        prices = {}
        for symbol in symbols:
            rate, source, fetched_at = get_latest_rate_from_db('crypto_price', symbol)
            if rate is not None:
                prices[symbol] = rate
        
        if prices:
            cache.set(CACHE_KEY_CRYPTO_PRICES, prices, CACHE_TTL_CRYPTO)
            return prices
    except Exception as e:
        logger.error(f"Failed to get crypto prices from DB: {e}")
    
    return None


def get_last_update_time():
    """Get timestamp of last successful rate update"""
    return cache.get(CACHE_KEY_LAST_UPDATE)


def get_rates_status():
    """Get status info for monitoring/admin"""
    usd_rate = get_usd_toman_rate()
    crypto_prices = get_crypto_prices()
    last_update = get_last_update_time()
    
    return {
        'usd_toman': {
            'available': usd_rate is not None,
            'rate': float(usd_rate) if usd_rate else None,
        },
        'crypto_prices': {
            'available': crypto_prices is not None,
            'count': len(crypto_prices) if crypto_prices else 0,
        },
        'last_update': last_update,
    }