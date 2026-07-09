from django.db import models
from django.conf import settings

class Transaction(models.Model):
    BUY = 'BUY'
    SELL = 'SELL'

    TYPE_CHOICES = [
        (BUY, 'خرید'),
        (SELL, 'فروش'),
    ]

    STATUS_CHOICES = [
        ('pending_transfer', 'در انتظار ارسال'),
        ('pending_review', 'در انتظار بررسی'),
        ('reviewing', 'در حال بررسی'),
        ('completed', 'تکمیل شده'),
        ('rejected', 'رد شده'),
    ]

    # استفاده از تنظیمات برای ارجاع به مدل کاربر
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name="کاربر"
    )

    request_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name="نوع تراکنش"
    )

    CRYPTO_CHOICES = [
        ("BTC", "Bitcoin"),
        ("ETH", "Ethereum"),
        ("USDT", "Tether"),
        ("BNB", "BNB"),
        ("SOL", "Solana"),
        ("TRX", "Tron"),
    ]

    crypto_name = models.CharField(
        max_length=20,
        choices=CRYPTO_CHOICES,
        blank=True,
        null=True,
        verbose_name="نوع ارز"
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name="مقدار"
    )

    unit_price = models.DecimalField(
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name="قیمت واحد"
    )

    total_price = models.DecimalField(
        max_digits=25,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name="قیمت کل"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="وضعیت"
    )

    tx_hash = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="هش تراکنش"
    )

    wallet_address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="آدرس کیف پول"
    )

    transfer_reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="شناسه واریز"
    )

    admin_note = models.TextField(
        blank=True,
        null=True,
        verbose_name="یادداشت مدیریت"
    )

    final_approval = models.BooleanField(
        default=False,
        verbose_name="تایید نهایی مدیریت"
    )

    # Fields for fiat deposits
    fiat_deposit_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=[("CARD_TO_CARD", "کارت به کارت"), ("SHABA", "واریز از طریق شبا")],
        verbose_name="نوع واریز ریالی"
    )
    fiat_amount = models.DecimalField(
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name="مبلغ ریالی"
    )
    depositor_card_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="شماره کارت واریز کننده"
    )
    depositor_shaba_number = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="شماره شبا واریز کننده"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        crypto = self.crypto_name if self.crypto_name else "Fiat"
        return f"{self.user.username} - {crypto} - {self.get_status_display()}"

    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش‌ها"
        ordering = ['-created_at']