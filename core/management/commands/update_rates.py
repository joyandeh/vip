from django.core.management.base import BaseCommand
from core.services import update_all_rates, get_rates_status


class Command(BaseCommand):
    help = 'Fetch and cache all rates from external APIs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--status',
            action='store_true',
            help='Show current rates status instead of fetching',
        )

    def handle(self, *args, **options):
        if options['status']:
            self.show_status()
        else:
            self.fetch_rates()

    def fetch_rates(self):
        self.stdout.write('Fetching rates from APIs...')
        results = update_all_rates()
        
        if results['usd_toman']:
            self.stdout.write(
                f"USD/Toman: {results['usd_toman']['rate']:,} (source: {results['usd_toman']['source']})"
            )
        else:
            self.stderr.write('USD/Toman: FAILED')
        
        if results['crypto_prices']:
            self.stdout.write(
                f"Crypto prices: {results['crypto_prices']['count']} symbols (source: {results['crypto_prices']['source']})"
            )
        else:
            self.stderr.write('Crypto prices: FAILED')
        
        if results['errors']:
            for error in results['errors']:
                self.stderr.write(f'Error: {error}')
        
        if not results['errors']:
            self.stdout.write('All rates updated successfully')
        else:
            self.stdout.write('Some rates failed to update')

    def show_status(self):
        self.stdout.write('Current rates status:')
        status = get_rates_status()
        
        usd = status['usd_toman']
        if usd['available']:
            self.stdout.write(f"  USD/Toman: {usd['rate']:,} تومان ✓")
        else:
            self.stderr.write('  USD/Toman: NOT AVAILABLE')
        
        crypto = status['crypto_prices']
        if crypto['available']:
            self.stdout.write(f"  Crypto prices: {crypto['count']} symbols ✓")
        else:
            self.stderr.write('  Crypto prices: NOT AVAILABLE')
        
        if status['last_update']:
            self.stdout.write(f"  Last update: {status['last_update']}")
        else:
            self.stdout.write('  Last update: NEVER')