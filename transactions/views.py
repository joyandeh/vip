from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from .forms import BuyTransactionForm, SellTransactionForm
from .models import Transaction

from core.services import get_crypto_prices
from core.models import CryptoApiSetting, SiteSetting


@login_required
def buy_crypto(request):
    """خرید از سایت - فرم ساده با درگاه بانکی"""
    if not request.user.is_verified:
        messages.error(request, "برای ثبت درخواست، حساب شما باید توسط مدیریت تایید شود.")
        return redirect("profile")

    site_settings = SiteSetting.get_solo()

    if request.method == "POST":
        form = BuyTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.request_type = Transaction.BUY
            
            # Calculate prices
            prices = get_crypto_prices()
            setting = CryptoApiSetting.objects.filter(active=True).first()
            toman_rate = setting.toman_rate if setting else 85000
            usd_price = prices.get(transaction.crypto_name, 0)
            unit_price = Decimal(usd_price * toman_rate)
            total_price = unit_price * transaction.amount
            
            transaction.unit_price = unit_price
            transaction.total_price = total_price
            transaction.status = 'paid'  # پرداخت شده
            transaction.save()
            
            messages.success(request, "درخواست خرید شما با موفقیت ثبت شد.")
            return redirect("request_history")
    else:
        form = BuyTransactionForm()

    return render(request, "transactions/buy_crypto.html", {
        "form": form,
        "site_settings": site_settings,
    })


@login_required
def sell_crypto(request):
    """فروش به سایت - فرم با فیلدهای کامل"""
    if not request.user.is_verified:
        messages.error(request, "برای ثبت درخواست، حساب شما باید توسط مدیریت تایید شود.")
        return redirect("profile")

    site_settings = SiteSetting.get_solo()

    if request.method == "POST":
        form = SellTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.request_type = Transaction.SELL
            transaction.unit_price = Decimal(0)
            transaction.total_price = Decimal(0)
            transaction.status = 'paid'  # پرداخت شده (منتظر بررسی)
            transaction.save()
            
            messages.success(request, "درخواست فروش شما با موفقیت ثبت شد.")
            return redirect("request_history")
    else:
        form = SellTransactionForm()

    return render(request, "transactions/sell_crypto.html", {
        "form": form,
        "site_settings": site_settings,
    })


@login_required
def request_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    active_transactions = transactions.exclude(status='completed')
    completed_transactions = transactions.filter(status='completed')

    return render(request, 'transactions/history.html', {
        'transactions': transactions,
        'active_transactions': active_transactions,
        'completed_transactions': completed_transactions,
        'telegram_url': 'https://t.me/tronlnd_support',
    })


@login_required
def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    return render(request, "transactions/detail.html", {"transaction": transaction})