from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

from transactions.models import Transaction
from accounts.models import CustomUser


@staff_member_required
def admin_dashboard(request):
    total_users = CustomUser.objects.count()
    total_transactions = Transaction.objects.count()
    
    pending_transactions_count = Transaction.objects.filter(status='pending').count()
    completed_transactions = Transaction.objects.filter(status='done').count()
    
    buy_count = Transaction.objects.filter(request_type='BUY').count()
    sell_count = Transaction.objects.filter(request_type='SELL').count()

    # واکشی داده‌های لیست برای مدیریت در صفحه (رفع خطای متد ناموجود)
    pending_tx_list = Transaction.objects.filter(status='pending').order_by('-created_at')
    unverified_users_list = CustomUser.objects.filter(is_verified=False).order_by('-date_joined')

    context = {
        'total_users': total_users,
        'total_transactions': total_transactions,
        'pending_transactions': pending_transactions_count,
        'completed_transactions': completed_transactions,
        'buy_count': buy_count,
        'sell_count': sell_count,
        'pending_transactions_list': pending_tx_list,
        'unverified_users_list': unverified_users_list,
    }

    return render(request, 'accounts/admin_dashboard.html', context)


@staff_member_required
@require_POST
def change_transaction_status(request, tx_id):
    transaction = get_object_or_404(Transaction, id=tx_id)
    new_status = request.POST.get('status')
    
    if new_status in dict(Transaction.STATUS_CHOICES):
        transaction.status = new_status
        transaction.save()
        messages.success(
            request, 
            f"وضعیت تراکنش {transaction.id} با موفقیت به '{transaction.get_status_display()}' تغییر یافت."
        )
    else:
        messages.error(request, "وضعیت ارسالی نامعتبر است.")
        
    return redirect('admin_dashboard')


@staff_member_required
@require_POST
def change_user_verification(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    action = request.POST.get('action')
    
    if action == 'verify':
        user.is_verified = True
        user.save()
        messages.success(request, f"حساب کاربری {user.username} تایید هویت شد.")
    elif action == 'reject':
        user.is_verified = False
        user.save()
        messages.warning(request, f"وضعیت تایید هویت {user.username} لغو یا رد شد.")
        
    return redirect('admin_dashboard')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'ثبت نام شما با موفقیت انجام شد.')
            return redirect('register')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/')