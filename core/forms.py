from django import forms
from .models import HomePageSection, CryptoApiSetting, SiteSetting


class HomePageSectionForm(forms.ModelForm):

    class Meta:
        model = HomePageSection
        fields = [
            'section_key',
            'title',
            'subtitle',
            'content',
            'icon',
            'image',
            'link_url',
            'link_text',
            'order',
            'is_active',
        ]

        widgets = {
            'section_key': forms.Select(
                attrs={'class': 'form-select bg-dark text-white border-secondary-subtle'}
            ),
            'title': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle'}
            ),
            'subtitle': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle'}
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control bg-dark text-white border-secondary-subtle',
                    'rows': 4,
                }
            ),
            'icon': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle'}
            ),
            'image': forms.ClearableFileInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle'}
            ),
            'link_url': forms.URLInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}
            ),
            'link_text': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle'}
            ),
            'order': forms.NumberInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle'}
            ),
            'is_active': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }


class CryptoApiSettingForm(forms.ModelForm):

    class Meta:
        model = CryptoApiSetting
        fields = [
            'api_url',
            'api_key',
            'toman_rate',
            'active',
        ]

        widgets = {
            'api_url': forms.URLInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}
            ),
            'api_key': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}
            ),
            'toman_rate': forms.NumberInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}
            ),
            'is_active': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }


class SiteSettingForm(forms.ModelForm):

    class Meta:
        model = SiteSetting
        fields = [
            'site_name',
            'home_hero_title',
            'home_hero_subtitle',
            'home_cta_text',
            'contact_phone',
            'contact_telegram',
            'usdt_wallet_address',
            'trx_wallet_address',
        ]

        widgets = {
            'site_name': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle'}
            ),
            'home_hero_title': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle'}
            ),
            'home_hero_subtitle': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle'}
            ),
            'home_cta_text': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle'}
            ),
            'contact_phone': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}
            ),
            'contact_telegram': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}
            ),
            'usdt_wallet_address': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}
            ),
            'trx_wallet_address': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}
            ),
        }
