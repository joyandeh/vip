from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    full_name = models.CharField(
        max_length=200,
        verbose_name="نام کامل"
    )

    mobile = models.CharField(
        max_length=11,
        unique=True,
        verbose_name="شماره موبایل"
    )

    national_card_image = models.ImageField(
        upload_to='national_cards/',
        blank=True,
        null=True
    )

    selfie_image = models.ImageField(
        upload_to='selfies/',
        blank=True,
        null=True
    )

    card_number = models.CharField(
        max_length=16,
        blank=True
    )

    iban = models.CharField(
        max_length=26,
        blank=True
    )

    is_verified = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.username