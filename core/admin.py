from django.contrib import admin
from .models import CryptoApiSetting, HomePageSection, SiteSetting


@admin.register(CryptoApiSetting)
class CryptoApiSettingAdmin(admin.ModelAdmin):

    list_display = (
        'api_url',
        'toman_rate',
        'active',
    )


@admin.register(HomePageSection)
class HomePageSectionAdmin(admin.ModelAdmin):

    list_display = (
        'section_key',
        'title',
        'order',
        'is_active',
        'updated_at',
    )

    list_filter = (
        'section_key',
        'is_active',
    )

    search_fields = (
        'title',
        'subtitle',
        'content',
    )


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):

    list_display = (
        'site_name',
        'contact_phone',
        'contact_telegram',
    )
