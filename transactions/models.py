from django.db import models
from django.conf import settings

class Transaction(models.Model):
    BUY = 'BUY'
    SELL = 'SELL'

    TYPE_CHOICES = [
        (BUY, 'خرید'),
        (SELL, 'فروش'),
    ]

    # Updated status choices: پرداخت شده، رد شد، انجام شد
    STATUS_CHOICES = [
        ('paid', 'پرداخت شده'),
        ('rejected', 'رد شد'),
        ('completed', 'انجام شد'),
    ]

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
        default='paid',  # Default to "پرداخت شده"
        verbose_name="وضعیت"
    )

    tx_hash = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="هش تراکنش"
    )

    # --- NEW FIELDS FOR BUY (خرید) ---
    purchaser_full_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="نام و نام خانوادگی خریدار")
    purchaser_card_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="شماره کارت خریدار")
    purchaser_shaba_number = models.CharField(max_length=30, blank=True, null=True, verbose_name="شماره شبا خریدار")
    destination_address = models.CharField(max_length=255, blank=True, null=True, verbose_name="آدرس مقصد")
    deposit_reference = models.CharField(max_length=100, blank=True, null=True, verbose_name="شناسه واریزی بانکی")

    # --- NEW FIELDS FOR SELL (فروش) ---
    seller_full_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="نام و نام خانوادگی فروشنده")
    seller_card_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="شماره کارت فروشنده")
    seller_shaba_number = models.CharField(max_length=30, blank=True, null=True, verbose_name="شماره شبا فروشنده")
    # Wallet addresses for specific coins in sell
    wallet_address_bnb = models.CharField(max_length=255, blank=True, null=True, verbose_name="آدرس کیف پول BNB")
    wallet_address_btc = models.CharField(max_length=255, blank=True, null=True, verbose_name="آدرس کیف پول BTC")
    wallet_address_sol = models.CharField(max_length=255, blank=True, null=True, verbose_name="آدرس کیف پول SOL")

    admin_note = models.TextField(
        blank=True,
        null=True,
        verbose_name="یادداشت مدیریت"
    )

    final_approval = models.BooleanField(
        default=False,
        verbose_name="تایید نهایی مدیریت"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        crypto = self.crypto_name if self.crypto_name else "Fiat"
        return f"{self.user.username} - {crypto} - {self.get_status_display()}"

    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش‌ها"
        ordering = ['-created_at']