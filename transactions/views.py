from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .forms import TransactionForm, FiatDepositForm, CryptoToRialConversionForm # Import new forms
from .models import Transaction

from core.services import get_crypto_prices
from core.models import CryptoApiSetting, SiteSetting


@login_required
def create_request(request):
    if not request.user.is_verified:
        messages.error(
            request,
            "برای ثبت درخواست، حساب شما باید توسط مدیریت تایید شود."
        )
        return redirect("profile")

    # Get site settings for wallet addresses
    site_settings = SiteSetting.objects.first()

    # Initialize all forms for both GET and POST
    form = TransactionForm()
    fiat_deposit_card_form = FiatDepositForm(initial={"fiat_deposit_type": "CARD"})
    fiat_deposit_shaba_form = FiatDepositForm(initial={"fiat_deposit_type": "SHABA"})
    crypto_to_rial_form = CryptoToRialConversionForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "fiat_deposit":
            fiat_deposit_card_form = FiatDepositForm(request.POST)
            fiat_deposit_shaba_form = FiatDepositForm(request.POST)
            # Check which one is being submitted
            deposit_type = request.POST.get("fiat_deposit_type", "CARD")
            if deposit_type == "CARD":
                form_to_use = fiat_deposit_card_form
            else:
                form_to_use = fiat_deposit_shaba_form
            
            if form_to_use.is_valid():
                transaction = form_to_use.save(commit=False)
                transaction.user = request.user
                transaction.request_type = Transaction.BUY
                transaction.save()
                messages.success(
                    request,
                    "درخواست واریز ریالی شما ثبت شد. منتظر بررسی و تأیید باشید."
                )
                return redirect("request_history")

        elif form_type == "crypto_to_rial_conversion":
            crypto_to_rial_form = CryptoToRialConversionForm(request.POST)
            if crypto_to_rial_form.is_valid():
                transaction = crypto_to_rial_form.save(commit=False)
                transaction.user = request.user
                transaction.request_type = Transaction.SELL
                transaction.unit_price = Decimal(0)
                transaction.total_price = Decimal(0)
                transaction.status = "pending_transfer"
                transaction.save()
                messages.success(
                    request,
                    "درخواست تبدیل دارایی شما ثبت شد. منتظر بررسی و تأیید باشید."
                )
                return redirect("request_history")

        else:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                prices = get_crypto_prices()
                setting = CryptoApiSetting.objects.filter(
                    active=True
                ).first()
                toman_rate = setting.toman_rate
                usd_price = prices.get(
                    transaction.crypto_name,
                    0
                )
                unit_price = Decimal(
                    usd_price * toman_rate
                )
                total_price = (
                    unit_price *
                    transaction.amount
                )
                transaction.user = request.user
                transaction.unit_price = unit_price
                transaction.total_price = total_price
                transaction.status = "pending_review"
                transaction.save()
                messages.success(
                    request,
                    "درخواست خرید یا فروش شما با موفقیت ثبت شد."
                )
                return redirect("request_history")

    # Determine which form section to show based on query param
    request_type = request.GET.get('type', 'all')

    return render(
        request,
        "transactions/request_crypto.html",
        {
            "form": form,
            "fiat_deposit_card_form": fiat_deposit_card_form,
            "fiat_deposit_shaba_form": fiat_deposit_shaba_form,
            "crypto_to_rial_form": crypto_to_rial_form,
            "site_settings": site_settings,
            "request_type": request_type,
        }
    )


@login_required
def request_history(request):

    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-created_at')

    active_transactions = transactions.exclude(status='completed')
    completed_transactions = transactions.filter(status='completed')

    return render(
        request,
        'transactions/history.html',
        {
            'transactions': transactions,
            'active_transactions': active_transactions,
            'completed_transactions': completed_transactions,
            'telegram_url': 'https://t.me/tronlnd_support',
        }
    )


@login_required
def transaction_detail(request, pk):
    transaction = get_object_or_404(
        Transaction,
        pk=pk,
        user=request.user
    )

    if request.method == "POST" and not transaction.final_approval:
        tx_hash = request.POST.get("tx_hash")

        if tx_hash:
            transaction.tx_hash = tx_hash
            transaction.save()

            messages.success(
                request,
                "هش تراکنش با موفقیت بروزرسانی شد."
            )

        return redirect("transaction_detail", pk=transaction.pk)

    return render(
        request,
        "transactions/detail.html",
        {
            "transaction": transaction
        }
    )