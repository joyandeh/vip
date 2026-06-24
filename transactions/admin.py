from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'crypto_name',
        'request_type',
        'amount',
        'status',
        'created_at'
    )

    list_filter = (
        'status',
        'request_type'
    )

    search_fields = (
        'user__username',
        'crypto_name'
    )