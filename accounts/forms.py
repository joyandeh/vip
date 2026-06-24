from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'full_name',
            'mobile',
            'national_card_image',
            'selfie_image',
            'card_number',
            'iban',
        ]
        
        # ۱. فارسی‌سازی ساده و روان عناوین فیلدها
        labels = {
            'username': 'نام کاربری',
            'full_name': 'نام و نام خانوادگی',
            'mobile': 'شماره موبایل',
            'national_card_image': 'تصویر کارت ملی',
            'selfie_image': 'تصویر سلفی',
            'card_number': 'شماره کارت',
            'iban': 'شماره شبا',
        }

        # ۲. متون راهنمای مختصر، ساده و روان فارسی (جایگزین متون انگلیسی جنگو)
        help_texts = {
            'username': 'فقط حروف انگلیسی و اعداد.',
            'mobile': 'مثال: 09123456789',
            'national_card_image': 'تصویر واضح (حداکثر ۵ مگابایت).',
            'selfie_image': 'سلفی همراه با کارت ملی.',
            'card_number': 'شماره ۱۶ رقمی کارت بانکی.',
            'iban': 'شماره شبا بدون IR.',
        }

    # تغییر برچسب و متون راهنمای فیلدهای رمز عبور ارث‌بری شده از UserCreationForm
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['password1'].label = "رمز عبور"
        self.fields['password1'].help_text = "حداقل ۸ کاراکتر (ترکیب حروف و اعداد)."
        
        self.fields['password2'].label = "تکرار رمز عبور"
        self.fields['password2'].help_text = "رمز عبور را مجدداً وارد کنید."

    # متد اعتبارسنجی حجم عکس (اصلاح تو رفتگی برای قرارگیری داخل کلاس)
    def clean_national_card_image(self):
        image = self.cleaned_data.get('national_card_image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("حداکثر حجم فایل 5 مگابایت است.")
        return image