from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'full_name',
        'mobile',
        'is_verified',
        'is_staff'
    )

    list_filter = (
        'is_verified',
        'is_staff'
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            'اطلاعات تکمیلی',
            {
                'fields': (
                    'full_name',
                    'mobile',
                    'national_card_image',
                    'selfie_image',
                    'card_number',
                    'iban',
                    'is_verified'
                )
            }
        ),
    )