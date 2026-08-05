from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="ایمیل",
        required=True,
        help_text="ایمیل معتبر برای بازیابی حساب",
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle',
            'placeholder': 'example@domain.com'
        })
    )

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'full_name',
            'mobile',
            'email',
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
        
        # ترجمه پیام‌های خطای پیش‌فرض جنگو
        self.fields['username'].error_messages = {
            'required': 'نام کاربری الزامی است.',
            'unique': 'این نام کاربری قبلاً ثبت شده است.',
            'invalid': 'نام کاربری فقط می‌تواند شامل حروف، اعداد و @/./+/-/_ باشد.',
        }
        self.fields['mobile'].error_messages = {
            'required': 'شماره موبایل الزامی است.',
            'unique': 'این شماره موبایل قبلاً ثبت شده است.',
            'invalid': 'شماره موبایل معتبر وارد کنید.',
        }
        self.fields['email'].error_messages = {
            'required': 'ایمیل الزامی است.',
            'invalid': 'فرمت ایمیل معتبر نیست.',
            'unique': 'این ایمیل قبلاً ثبت شده است.',
        }
        self.fields['full_name'].error_messages = {
            'required': 'نام و نام خانوادگی الزامی است.',
        }
        self.fields['password1'].error_messages = {
            'required': 'رمز عبور الزامی است.',
        }
        self.fields['password2'].error_messages = {
            'required': 'تکرار رمز عبور الزامی است.',
            'password_mismatch': 'رمز عبور و تکرار آن مطابقت ندارند.',
        }
        self.fields['national_card_image'].error_messages = {
            'required': 'تصویر کارت ملی الزامی است.',
            'invalid_image': 'فایل آپلود شده معتبر نیست.',
        }
        self.fields['selfie_image'].error_messages = {
            'required': 'تصویر سلفی الزامی است.',
            'invalid_image': 'فایل آپلود شده معتبر نیست.',
        }

    # متد اعتبارسنجی حجم عکس (اصلاح تو رفتگی برای قرارگیری داخل کلاس)
    def clean_national_card_image(self):
        image = self.cleaned_data.get('national_card_image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("حداکثر حجم فایل 5 مگابایت است.")
        return image

    def clean_selfie_image(self):
        image = self.cleaned_data.get('selfie_image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("حداکثر حجم فایل 5 مگابایت است.")
        return image