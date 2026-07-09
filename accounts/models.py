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


class UserProfile(models.Model):
    KYC_STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('reviewing', 'در حال بررسی'),
        ('approved', 'تایید شده'),
        ('rejected', 'رد شده'),
    ]

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="کاربر"
    )
    card_number = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        verbose_name="شماره کارت"
    )
    sheba_number = models.CharField(
        max_length=26,
        blank=True,
        null=True,
        verbose_name="شماره شبا"
    )
    kyc_status = models.CharField(
        max_length=20,
        choices=KYC_STATUS_CHOICES,
        default='pending',
        verbose_name="وضعیت احراز هویت"
    )

    def __str__(self):
        return f"پروفایل {self.user.username}"

    class Meta:
        verbose_name = "پروفایل کاربر"
        verbose_name_plural = "پروفایل‌های کاربران"


# سیگنال‌ها برای ایجاد خودکار پروفایل کاربر
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            card_number=instance.card_number,
            sheba_number=instance.iban,
            kyc_status='approved' if instance.is_verified else 'pending'
        )

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
