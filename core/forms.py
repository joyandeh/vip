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
            'btc_wallet_address',
            'eth_wallet_address',
            'sol_wallet_address',
            'bnb_wallet_address',
            'xrp_wallet_address',
            'pm_wallet_address',
            'site_card_number',
            'toman_rate',
            'site_iban',
            'site_account_holder',
            'support_phone',
            # Announcements
            'announcement_1_title',
            'announcement_1_text',
            'announcement_1_icon',
            'announcement_1_color',
            'announcement_1_active',
            'announcement_2_title',
            'announcement_2_text',
            'announcement_2_icon',
            'announcement_2_color',
            'announcement_2_active',
            'announcement_3_title',
            'announcement_3_text',
            'announcement_3_icon',
            'announcement_3_color',
            'announcement_3_active',
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
            'btc_wallet_address': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}
            ),
            'eth_wallet_address': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}
            ),
            'sol_wallet_address': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}
            ),
            'site_card_number': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}
            ),
            'toman_rate': forms.NumberInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}
            ),
            'site_iban': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}
            ),
            'site_account_holder': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle'}
            ),
            'support_phone': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'dir': 'ltr'}
            ),
            # Announcement widgets
            'announcement_1_title': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle'}
            ),
            'announcement_1_text': forms.Textarea(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'rows': 3}
            ),
            'announcement_1_icon': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'placeholder': 'fa-solid fa-bullhorn'}
            ),
            'announcement_1_color': forms.Select(
                choices=[
                    ('cyan', 'فیروزه‌ای (Cyan)'),
                    ('green', 'سبز (Green)'),
                    ('coral', 'مرجانی (Coral)'),
                    ('warning', 'زرد/نارنجی (Warning)'),
                ],
                attrs={'class': 'form-select bg-dark text-white border-secondary-subtle'}
            ),
            'announcement_1_active': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'announcement_2_title': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle'}
            ),
            'announcement_2_text': forms.Textarea(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'rows': 3}
            ),
            'announcement_2_icon': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'placeholder': 'fa-solid fa-gift'}
            ),
            'announcement_2_color': forms.Select(
                choices=[
                    ('cyan', 'فیروزه‌ای (Cyan)'),
                    ('green', 'سبز (Green)'),
                    ('coral', 'مرجانی (Coral)'),
                    ('warning', 'زرد/نارنجی (Warning)'),
                ],
                attrs={'class': 'form-select bg-dark text-white border-secondary-subtle'}
            ),
            'announcement_2_active': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'announcement_3_title': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle'}
            ),
            'announcement_3_text': forms.Textarea(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'rows': 3}
            ),
            'announcement_3_icon': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white border-secondary-subtle', 'placeholder': 'fa-solid fa-bolt'}
            ),
            'announcement_3_color': forms.Select(
                choices=[
                    ('cyan', 'فیروزه‌ای (Cyan)'),
                    ('green', 'سبز (Green)'),
                    ('coral', 'مرجانی (Coral)'),
                    ('warning', 'زرد/نارنجی (Warning)'),
                ],
                attrs={'class': 'form-select bg-dark text-white border-secondary-subtle'}
            ),
            'announcement_3_active': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }