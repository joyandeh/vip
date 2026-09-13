from django.contrib import admin
from .models import CryptoApiSetting, HomePageSection, SiteSetting, CachedRate


@admin.register(CachedRate)
class CachedRateAdmin(admin.ModelAdmin):
    list_display = ('rate_type', 'symbol', 'value', 'source', 'fetched_at')
    list_filter = ('rate_type', 'source', 'fetched_at')
    search_fields = ('symbol',)
    readonly_fields = ('rate_type', 'symbol', 'value', 'source', 'fetched_at')
    ordering = ('-fetched_at',)
    
    def has_add_permission(self, request):
        return False  # Read-only, populated by API fetcher


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
