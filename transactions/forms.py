from django import forms
from .models import Transaction


class BuyTransactionForm(forms.ModelForm):
    """فرم خرید از سایت - فقط درگاه بانکی، فیلدهای اجباری"""
    class Meta:
        model = Transaction
        fields = [
            'crypto_name',
            'amount',
            'destination_address',
            'purchaser_full_name',
            'purchaser_card_number',
            'purchaser_shaba_number',
            'deposit_reference',
        ]
        widgets = {
            'crypto_name': forms.Select(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'required': True}),
            'amount': forms.NumberInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'placeholder': 'مقدار رمزارز', 'step': 'any', 'required': True}),
            'destination_address': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'placeholder': 'آدرس مقصد ( ولت )', 'required': True}),
            'purchaser_full_name': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'placeholder': 'نام و نام خانوادگی', 'required': True}),
            'purchaser_card_number': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'placeholder': 'شماره کارت واریزی', 'required': True}),
            'purchaser_shaba_number': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'placeholder': 'شماره شبا واریزی', 'required': True}),
            'deposit_reference': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'placeholder': 'شناسه واریزی بانکی', 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True


class SellTransactionForm(forms.ModelForm):
    """فرم فروش به سایت - فیلدهای اجباری، بدون آدرس کیف پول عمومی"""
    class Meta:
        model = Transaction
        fields = [
            'crypto_name',
            'amount',
            'tx_hash',
            'seller_full_name',
            'seller_card_number',
            'seller_shaba_number',
            'wallet_address_bnb',
            'wallet_address_btc',
            'wallet_address_sol',
        ]
        widgets = {
            'crypto_name': forms.Select(attrs={'class': 'form-select form-select-sm bg-dark text-white border-secondary-subtle', 'required': True}),
            'amount': forms.NumberInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'placeholder': 'مقدار ارز', 'step': 'any', 'required': True}),
            'tx_hash': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'placeholder': 'هش تراکنش', 'required': True}),
            'seller_full_name': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'placeholder': 'نام و نام خانوادگی', 'required': True}),
            'seller_card_number': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'placeholder': 'شماره کارت', 'required': True}),
            'seller_shaba_number': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'placeholder': 'شماره شبا', 'required': True}),
            'wallet_address_bnb': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'placeholder': 'آدرس کیف پول BNB', 'required': True}),
            'wallet_address_btc': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'placeholder': 'آدرس کیف پول BTC', 'required': True}),
            'wallet_address_sol': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'placeholder': 'آدرس کیف پول SOL', 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True


class AdminTransactionUpdateForm(forms.ModelForm):
    """فرم ادمین برای به‌روزرسانی وضعیت تراکنش"""
    class Meta:
        model = Transaction
        fields = ['status', 'admin_note', 'final_approval']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select form-select-sm bg-dark text-white border-secondary-subtle'}),
            'admin_note': forms.Textarea(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'rows': 3}),
            'final_approval': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }