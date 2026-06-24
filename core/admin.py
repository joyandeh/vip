from django.contrib import admin
from .models import CryptoApiSetting


@admin.register(CryptoApiSetting)
class CryptoApiSettingAdmin(admin.ModelAdmin):

    list_display = (
        'api_url',
        'toman_rate',
        'active',
    )