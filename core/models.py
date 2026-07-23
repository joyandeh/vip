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


class HomePageSection(models.Model):

    SECTION_CHOICES = [
        ('hero', 'بخش Hero (تیتر اصلی)'),
        ('features', 'بخش ویژگی‌ها'),
        ('about', 'بخش درباره ما'),
        ('cta', 'بخش دعوت به اقدام (CTA)'),
        ('contact', 'بخش ارتباط با ما / فوتر'),
    ]

    section_key = models.CharField(
        max_length=50,
        choices=SECTION_CHOICES,
        verbose_name="کلید بخش",
        db_index=True,
    )

    title = models.CharField(
        max_length=255,
        verbose_name="عنوان",
        blank=True,
    )

    subtitle = models.CharField(
        max_length=500,
        verbose_name="زیرعنوان / توضیح کوتاه",
        blank=True,
    )

    content = models.TextField(
        verbose_name="محتوا",
        blank=True,
    )

    icon = models.CharField(
        max_length=100,
        verbose_name="کلاس آیکون (FontAwesome)",
        blank=True,
        help_text="مثال: fa-solid fa-bolt",
    )

    image = models.ImageField(
        upload_to='home_sections/',
        verbose_name="تصویر",
        blank=True,
        null=True,
    )

    link_url = models.URLField(
        verbose_name="لینک",
        blank=True,
    )

    link_text = models.CharField(
        max_length=100,
        verbose_name="متن لینک",
        blank=True,
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="ترتیب نمایش",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال؟",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "بخش صفحه اصلی"
        verbose_name_plural = "بخش‌های صفحه اصلی"
        ordering = ['section_key', 'order', '-created_at']

    def __str__(self):
        return f"{self.get_section_key_display()} - {self.title or 'بدون عنوان'}"


class SiteSetting(models.Model):

    site_name = models.CharField(
        max_length=100,
        default="tronlnd",
        verbose_name="نام سایت",
    )

    home_hero_title = models.CharField(
        max_length=255,
        default="بازار معاملاتی tronlnd",
        verbose_name="تیتر اصلی صفحه اول",
    )

    home_hero_subtitle = models.CharField(
        max_length=500,
        default="خرید و فروش سریع و امن ارزهای دیجیتال",
        verbose_name="زیرتیتر صفحه اول",
    )

    home_cta_text = models.CharField(
        max_length=100,
        default="همین حالا شروع کنید",
        verbose_name="متن دکمه اصلی",
    )

    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="شماره پشتیبانی",
    )

    contact_telegram = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="آی‌دی تلگرام",
    )
    usdt_wallet_address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="آدرس کیف پول تتر (TRC20)"
    )
    trx_wallet_address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="آدرس کیف پول تزون (TRX)"
    )
    btc_wallet_address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="آدرس کیف پول بیتکوین (BTC)"
    )
    eth_wallet_address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="آدرس کیف پول اتریوم (ERC20)"
    )
    sol_wallet_address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="آدرس کیف پول سولانا (SOL)"
    )
    site_card_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="شماره کارت سایت (برای خرید)"
    )
    site_iban = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="شماره شبا سایت (برای خرید)"
    )
    site_account_holder = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="نام صاحب حساب"
    )
    support_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="شماره تلفن پشتیبانی"
    )

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"

    def __str__(self):
        return "تنظیمات سایت"
