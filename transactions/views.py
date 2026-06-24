from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .forms import TransactionForm
from .models import Transaction

from core.services import get_crypto_prices
from core.models import CryptoApiSetting


@login_required
def create_request(request):

    if request.method == 'POST':

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
                'درخواست شما ثبت شد. کارشناسان ما به زودی با شما تماس خواهند گرفت.'
            )

            return redirect(
                'request_history'
            )

    else:
        if not request.user.is_verified:

            return HttpResponseForbidden(
        "حساب شما هنوز توسط مدیریت تایید نشده است."
    )
    form = TransactionForm()

    return render(
        request,
        'transactions/request_crypto.html',
        {
            'form': form
        }
    )


@login_required
def request_history(request):

    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'transactions/history.html',
        {
            'transactions': transactions
        }
    )