from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction

        fields = [
            'request_type',
            'crypto_name',
            'amount',
            'tx_hash',
            'fiat_deposit_type',
            'fiat_amount',
            'depositor_card_number',
            'depositor_shaba_number'
        ]

        widgets = {
            'request_type': forms.HiddenInput(),
            'crypto_name': forms.Select(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'placeholder': 'مقدار رمزارز', 'step': 'any'}),
            'tx_hash': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'placeholder': 'هش تراکنش'}),
            'fiat_deposit_type': forms.HiddenInput(),
            'fiat_amount': forms.NumberInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'placeholder': 'مبلغ واریزی به ریال', 'step': 'any'}),
            'depositor_card_number': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'placeholder': 'شماره کارت شما'}),
            'depositor_shaba_number': forms.TextInput(attrs={'class': 'form-control form-control-sm bg-dark text-white border-secondary-subtle', 'placeholder': 'شماره شبا شما (IR...)'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields not required by default, then set required based on form_type in view
        for field_name in self.fields:
            self.fields[field_name].required = False


class FiatDepositForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["fiat_deposit_type", "fiat_amount", "depositor_card_number", "depositor_shaba_number"]
        widgets = {
            "fiat_deposit_type": forms.HiddenInput(),
            "fiat_amount": forms.NumberInput(attrs={
                "class": "form-control form-control-sm bg-dark text-white border-secondary-subtle",
                "placeholder": "مبلغ واریزی به ریال",
                "step": "any"
            }),
            "depositor_card_number": forms.TextInput(attrs={
                "class": "form-control form-control-sm bg-dark text-white border-secondary-subtle",
                "placeholder": "شماره کارت خود را وارد کنید"
            }),
            "depositor_shaba_number": forms.TextInput(attrs={
                "class": "form-control form-control-sm bg-dark text-white border-secondary-subtle",
                "placeholder": "شماره شبا خود را وارد کنید"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = True


class CryptoToRialConversionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "crypto_name",
            "amount",
            "wallet_address",
            "tx_hash"
        ]
        widgets = {
            "crypto_name": forms.Select(attrs={
                "class": "form-select form-select-sm bg-dark text-white border-secondary-subtle",
                "placeholder": "ارز مورد نظر"
            }),
            "amount": forms.NumberInput(attrs={
                "class": "form-control form-control-sm bg-dark text-white border-secondary-subtle",
                "placeholder": "مقدار ارز",
                "step": "any"
            }),
            "wallet_address": forms.TextInput(attrs={
                "class": "form-control form-control-sm bg-dark text-white border-secondary-subtle",
                "placeholder": "آدرس کیف پول شما"
            }),
            "tx_hash": forms.TextInput(attrs={
                "class": "form-control form-control-sm bg-dark text-white border-secondary-subtle",
                "placeholder": "هش تراکنش"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = True



