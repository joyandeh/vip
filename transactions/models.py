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
        ('pending', 'در دست بررسی'),
        ('done', 'تمام شده'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    request_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES
    )

    
    CRYPTO_CHOICES = [
    ('BTC', 'Bitcoin'),
    ('ETH', 'Ethereum'),
    ('USDT', 'Tether'),
    ('BNB', 'BNB'),
    ('SOL', 'Solana'),
]

    crypto_name = models.CharField(
    max_length=20,
    choices=CRYPTO_CHOICES
)

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=8
    )

    unit_price = models.DecimalField(
        max_digits=20,
        decimal_places=0
    )

    total_price = models.DecimalField(
        max_digits=25,
        decimal_places=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.crypto_name}"