from django.db import models


class CryptoApiSetting(models.Model):

    api_url = models.URLField()

    api_key = models.CharField(
        max_length=255,
        blank=True
    )

    toman_rate = models.PositiveIntegerField(
        default=85000,
        verbose_name="قیمت دلار به تومان"
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.api_url