from django.core.management.base import BaseCommand
from core.services import get_usd_toman_rate, get_crypto_prices


class Command(BaseCommand):
    help = 'Preload crypto prices and USD/Toman rate into cache'

    def handle(self, *args, **options):
        self.stdout.write('Preloading USD/Toman rate...')
        rate = get_usd_toman_rate()
        self.stdout.write(f'  USD/Toman rate: {rate:,} تومان')

        self.stdout.write('Preloading crypto prices...')
        prices = get_crypto_prices()
        for symbol, price in prices.items():
            self.stdout.write(f'  {symbol}: ${price:,.2f}')

        self.stdout.write(self.style.SUCCESS('Cache preloaded successfully'))