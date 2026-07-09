from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.middleware.csrf import get_token
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'crypto_name',
        'request_type',
        'amount',
        'status',
        'created_at',
        'action_buttons'
    )

    list_filter = (
        'status',
        'request_type'
    )

    search_fields = (
        'user__username',
        'crypto_name'
    )

    actions = ['mark_as_done']

    def mark_as_done(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, "Selected transactions marked as completed.")
    mark_as_done.short_description = "Mark selected transactions as completed"

    def action_buttons(self, obj):
        if obj.status == 'pending':
            # We need to construct a dummy request to get the CSRF token
            # This is a workaround for generating CSRF token in admin list view
            # In a real scenario, consider using a custom admin view for actions
            from django.http import HttpRequest
            dummy_request = HttpRequest()
            dummy_request.META['SERVER_NAME'] = 'localhost'
            dummy_request.META['SERVER_PORT'] = '8000'
            dummy_request.method = 'GET'
            csrf_token = get_token(dummy_request)

            return format_html(
                '<form action="{}" method="post" style="display:inline;">' 
                + '<input type="hidden" name="csrfmiddlewaretoken" value="{}">' 
                + '<button type="submit" name="status" value="completed" class="button">Mark as Completed</button>'
                + '</form>',
                reverse('admin:transactions_transaction_change', args=[obj.pk]),
                csrf_token
            )
        return ""


# Ensure Transaction is registered with the custom Admin class

