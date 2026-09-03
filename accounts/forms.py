from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.validators import UnicodeUsernameValidator
from .models import CustomUser, UserProfile


class PersianUsernameValidator(UnicodeUsernameValidator):
    """UnicodeUsernameValidator با پیام‌های خطای فارسی"""
    message = 'نام کاربری فقط می‌تواند شامل حروف، اعداد و @/./+/-/_ باشد.'
    code = 'invalid'


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

    # Override error_messages from UserCreationForm for password_mismatch
    error_messages = {
        'password_mismatch': 'رمز عبور و تکرار آن مطابقت ندارند.',
    }

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

        # ترجمه پیام‌های خطای پیش‌فرض جنگو برای تمام فیلدها
        self.fields['username'].error_messages = {
            'required': 'نام کاربری الزامی است.',
            'unique': 'این نام کاربری قبلاً ثبت شده است.',
            'invalid': 'نام کاربری فقط می‌تواند شامل حروف، اعداد و @/./+/-/_ باشد.',
            'max_length': 'نام کاربری نمی‌تواند بیش از ۱۵۰ کاراکتر باشد.',
        }
        # جایگزینی validator پیش‌فرض username با validator فارسی
        self.fields['username'].validators = [PersianUsernameValidator()]
        self.fields['mobile'].error_messages = {
            'required': 'شماره موبایل الزامی است.',
            'unique': 'این شماره موبایل قبلاً ثبت شده است.',
            'invalid': 'شماره موبایل معتبر وارد کنید.',
            'max_length': 'شماره موبایل نمی‌تواند بیش از ۱۱ رقم باشد.',
        }
        self.fields['email'].error_messages = {
            'required': 'ایمیل الزامی است.',
            'invalid': 'فرمت ایمیل معتبر نیست.',
            'unique': 'این ایمیل قبلاً ثبت شده است.',
            'max_length': 'ایمیل نمی‌تواند بیش از ۲۵۴ کاراکتر باشد.',
        }
        self.fields['full_name'].error_messages = {
            'required': 'نام و نام خانوادگی الزامی است.',
            'max_length': 'نام و نام خانوادگی نمی‌تواند بیش از ۲۰۰ کاراکتر باشد.',
        }
        self.fields['password1'].error_messages = {
            'required': 'رمز عبور الزامی است.',
            'max_length': 'رمز عبور نمی‌تواند بیش از ۱۲۸ کاراکتر باشد.',
        }
        self.fields['password2'].error_messages = {
            'required': 'تکرار رمز عبور الزامی است.',
            'password_mismatch': 'رمز عبور و تکرار آن مطابقت ندارند.',
            'max_length': 'رمز عبور نمی‌تواند بیش از ۱۲۸ کاراکتر باشد.',
        }
        self.fields['national_card_image'].error_messages = {
            'required': 'تصویر کارت ملی الزامی است.',
            'invalid_image': 'فایل آپلود شده معتبر نیست.',
            'missing': 'تصویر کارت ملی الزامی است.',
            'empty': 'فایل انتخاب شده خالی است.',
            'invalid': 'فایل آپلود شده معتبر نیست.',
        }
        self.fields['selfie_image'].error_messages = {
            'required': 'تصویر سلفی الزامی است.',
            'invalid_image': 'فایل آپلود شده معتبر نیست.',
            'missing': 'تصویر سلفی الزامی است.',
            'empty': 'فایل انتخاب شده خالی است.',
            'invalid': 'فایل آپلود شده معتبر نیست.',
        }
        # فیلدهای اختیاری - فقط خطاهای احتمالی
        optional_fields = [
            'card_number', 'iban'
        ]
        for field_name in optional_fields:
            if field_name in self.fields:
                self.fields[field_name].error_messages = {
                    'max_length': f'مقدار وارد شده برای {self.fields[field_name].label} خیلی طولانی است.',
                    'invalid': f'مقدار وارد شده برای {self.fields[field_name].label} معتبر نیست.',
                }

    # متد اعتبارسنجی حجم عکس
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


class UserProfileForm(forms.ModelForm):
    """فرم ویرایش پروفایل کاربر (بدون رمز عبور)"""

    class Meta:
        model = CustomUser
        fields = [
            'full_name',
            'mobile',
            'email',
            'card_number',
            'iban',
            'trx_address',
            'usdt_address',
            'btc_address',
            'eth_address',
            'sol_address',
            'bnb_address',
            'xrp_address',
            'pm_address',
        ]
        labels = {
            'full_name': 'نام و نام خانوادگی',
            'mobile': 'شماره موبایل',
            'email': 'ایمیل',
            'card_number': 'شماره کارت',
            'iban': 'شماره شبا',
            'trx_address': 'آدرس ترون (TRX)',
            'usdt_address': 'آدرس تتر (USDT)',
            'btc_address': 'آدرس بیت کوین (BTC)',
            'eth_address': 'آدرس اتریوم (ETH)',
            'sol_address': 'آدرس سولانا (SOL)',
            'bnb_address': 'آدرس بینانس (BNB)',
            'xrp_address': 'آدرس ریپل (XRP)',
            'pm_address': 'آدرس پرفکت مانی (PM)',
        }
        help_texts = {
            'mobile': 'مثال: 09123456789',
            'card_number': 'شماره ۱۶ رقمی کارت بانکی.',
            'iban': 'شماره شبا بدون IR.',
            'trx_address': 'آدرس کیف پول ترون (شروع با T)',
            'usdt_address': 'آدرس کیف پول تتر (ERC20/TRC20)',
            'btc_address': 'آدرس کیف پول بیت کوین',
            'eth_address': 'آدرس کیف پول اتریوم (شروع با 0x)',
            'sol_address': 'آدرس کیف پول سولانا',
            'bnb_address': 'آدرس کیف پول بینانس (BEP20)',
            'xrp_address': 'آدرس کیف پول ریپل (شامل Tag)',
            'pm_address': 'آدرس/شناسه پرفکت مانی',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
            'iban': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
            'trx_address': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
            'usdt_address': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
            'btc_address': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
            'eth_address': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
            'sol_address': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
            'bnb_address': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
            'xrp_address': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
            'pm_address': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
        }


class AdminUserForm(forms.ModelForm):
    """فرم ادمین برای ویرایش کاربر شامل فیلدهای کیف پول"""

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'full_name',
            'mobile',
            'email',
            'is_verified',
            'is_staff',
            'is_active',
            'card_number',
            'iban',
            'trx_address',
            'usdt_address',
            'btc_address',
            'eth_address',
            'sol_address',
            'bnb_address',
            'xrp_address',
            'pm_address',
        ]
        labels = {
            'username': 'نام کاربری',
            'full_name': 'نام و نام خانوادگی',
            'mobile': 'شماره موبایل',
            'email': 'ایمیل',
            'is_verified': 'احراز هویت شده',
            'is_staff': 'دسترسی ادمین',
            'is_active': 'فعال',
            'card_number': 'شماره کارت',
            'iban': 'شماره شبا',
            'trx_address': 'آدرس ترون (TRX)',
            'usdt_address': 'آدرس تتر (USDT)',
            'btc_address': 'آدرس بیت کوین (BTC)',
            'eth_address': 'آدرس اتریوم (ETH)',
            'sol_address': 'آدرس سولانا (SOL)',
            'bnb_address': 'آدرس بینانس (BNB)',
            'xrp_address': 'آدرس ریپل (XRP)',
            'pm_address': 'آدرس پرفکت مانی (PM)',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
            'iban': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
            'trx_address': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
            'usdt_address': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
            'btc_address': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
            'eth_address': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
            'sol_address': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
            'bnb_address': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
            'xrp_address': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
            'pm_address': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}),
        }