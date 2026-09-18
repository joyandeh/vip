from django.core.management.base import BaseCommand
from core.services import get_usd_toman_rate
from core.models import CryptoApiSetting


class Command(BaseCommand):
    help = 'اسکرپ نرخ دلار از tgju.org و ذخیره در تنظیمات'

    def handle(self, *args, **options):
        rate = get_usd_toman_rate()
        
        if rate is None:
            self.stdout.write(self.style.ERROR('نرخ دلار یافت نشد'))
            return
        
        # Store in the first CryptoApiSetting record (or create one)
        setting = CryptoApiSetting.objects.first()
        if not setting:
            setting = CryptoApiSetting.objects.create(
                toman_rate=rate,
                active=False,
                usd_toman_api_url='https://www.tgju.org/profile/price_dollar_rl'
            )
        else:
            setting.toman_rate = rate
            setting.save(update_fields=['toman_rate', 'updated_at'])
        
        self.stdout.write(
            self.style.SUCCESS(f'نرخ دلار به‌روزرسانی شد: {rate:,} تومان')
        )