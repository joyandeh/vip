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

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "fiat_deposit":
            form = FiatDepositForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.request_type = Transaction.BUY # Fiat deposit is essentially buying site credit
                transaction.crypto_name = None # Not crypto related
                transaction.amount = None
                transaction.unit_price = None
                transaction.total_price = transaction.fiat_amount # Total price is the fiat amount
                transaction.status = "pending_review"
                transaction.save()
                messages.success(
                    request,
                    "درخواست واریز ریالی شما ثبت شد. منتظر بررسی و تأیید باشید."
                )
                return redirect("request_history")

        elif form_type == "crypto_to_rial_conversion":
            form = CryptoToRialConversionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.request_type = Transaction.SELL # Selling crypto to the site
                # crypto_name, amount, transaction_hash are already set by the form
                # unit_price and total_price will be calculated based on current rates or filled by admin
                # For now, set them to 0 or None, and let admin update
                transaction.unit_price = Decimal(0)
                transaction.total_price = Decimal(0)
                transaction.status = "pending_transfer"
                transaction.save()
                messages.success(
                    request,
                    "درخواست تبدیل دارایی شما ثبت شد. منتظر بررسی و تأیید باشید."
                )
                return redirect("request_history")

        # Default form for crypto buy/sell if no specific form_type is provided or matched
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
                transaction.save()
                messages.success(
                    request,
                    "درخواست فروش ارز ثبت شد. پس از بررسی هش و تراکنش، تسویه انجام خواهد شد."
                )
                return redirect("request_history")
                transaction.status = "pending_review"
                transaction.save()
                messages.success(
                    request,
                    "درخواست خرید یا فروش شما با موفقیت ثبت شد."
                )
                return redirect("request_history")

    else: # GET request
        form = TransactionForm()
        fiat_deposit_form = FiatDepositForm()
        crypto_to_rial_form = CryptoToRialConversionForm()

    return render(
        request,
        "transactions/request_crypto.html",
        {
            "form": form,
            "fiat_deposit_form": fiat_deposit_form,
            "crypto_to_rial_form": crypto_to_rial_form,
            "site_settings": site_settings # Pass site settings to template
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
