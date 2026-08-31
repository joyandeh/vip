from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    # Wallet addresses for 8 assets
    trx_address = models.CharField(max_length=100, blank=True, verbose_name="آدرس ترون")
    trx_balance = models.DecimalField(max_digits=20, decimal_places=8, default=0, verbose_name="موجودی ترون")
    usdt_address = models.CharField(max_length=100, blank=True, verbose_name="آدرس تتر")
    usdt_balance = models.DecimalField(max_digits=20, decimal_places=8, default=0, verbose_name="موجودی تتر")
    btc_address = models.CharField(max_length=100, blank=True, verbose_name="آدرس بیت کوین")
    btc_balance = models.DecimalField(max_digits=20, decimal_places=8, default=0, verbose_name="موجودی بیت کوین")
    eth_address = models.CharField(max_length=100, blank=True, verbose_name="آدرس اتریوم")
    eth_balance = models.DecimalField(max_digits=20, decimal_places=8, default=0, verbose_name="موجودی اتریوم")
    sol_address = models.CharField(max_length=100, blank=True, verbose_name="آدرس سولانا")
    sol_balance = models.DecimalField(max_digits=20, decimal_places=8, default=0, verbose_name="موجودی سولانا")
    bnb_address = models.CharField(max_length=100, blank=True, verbose_name="آدرس بینانس")
    bnb_balance = models.DecimalField(max_digits=20, decimal_places=8, default=0, verbose_name="موجودی بینانس")
    xrp_address = models.CharField(max_length=100, blank=True, verbose_name="آدرس ریپل")
    xrp_balance = models.DecimalField(max_digits=20, decimal_places=8, default=0, verbose_name="موجودی ریپل")
    pm_address = models.CharField(max_length=100, blank=True, verbose_name="آدرس perfect money")
    pm_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name="موجودی پرفکت مانی")

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


class AdminMessage(models.Model):
    """پیام ارسالی ادمین به کاربر"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admin_messages', verbose_name="کاربر")
    subject = models.CharField(max_length=200, verbose_name="موضوع")
    body = models.TextField(verbose_name="متن پیام")
    is_read = models.BooleanField(default=False, verbose_name="خوانده شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")

    class Meta:
        verbose_name = "پیام ادمین"
        verbose_name_plural = "پیام‌های ادمین"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} → {self.user.username}"


# سیگنال‌ها برای ایجاد خودکار پروفایل کاربر
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