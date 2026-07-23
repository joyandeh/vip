from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.http import HttpResponseForbidden
from datetime import timedelta

from transactions.models import Transaction
from accounts.models import CustomUser
from core.models import CryptoApiSetting, HomePageSection, SiteSetting
from core.forms import HomePageSectionForm, CryptoApiSettingForm, SiteSettingForm


@staff_member_required
def dashboard(request):
    """داشبورد اصلی پنل مدیریت"""
    
    # --- آمارهای کلی ---
    total_users = CustomUser.objects.count()
    total_transactions = Transaction.objects.count()
    verified_users = CustomUser.objects.filter(is_verified=True).count()
    unverified_users = CustomUser.objects.filter(is_verified=False).count()

    pending_transactions_count = Transaction.objects.filter(status='pending_review').count()
    completed_transactions = Transaction.objects.filter(status='completed').count()
    rejected_transactions = Transaction.objects.filter(status='rejected').count()

    buy_count = Transaction.objects.filter(request_type='BUY').count()
    sell_count = Transaction.objects.filter(request_type='SELL').count()

    # --- آمارهای مالی ---
    total_volume = Transaction.objects.filter(status='completed').aggregate(
        total=Sum('total_price')
    )['total'] or 0

    buy_volume = Transaction.objects.filter(status='completed', request_type='BUY').aggregate(
        total=Sum('total_price')
    )['total'] or 0

    sell_volume = Transaction.objects.filter(status='completed', request_type='SELL').aggregate(
        total=Sum('total_price')
    )['total'] or 0

    pending_volume = Transaction.objects.filter(status__in=['pending_review', 'pending_transfer']).aggregate(
        total=Sum('total_price')
    )['total'] or 0

    # --- آمار امروز ---
    today = timezone.now().date()
    today_start = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
    today_transactions = Transaction.objects.filter(created_at__gte=today_start).count()
    today_volume = Transaction.objects.filter(
        created_at__gte=today_start, status='completed'
    ).aggregate(total=Sum('total_price'))['total'] or 0

    # --- لیست‌های خلاصه ---
    pending_tx_list = Transaction.objects.filter(
        status__in=['pending_review', 'pending_transfer']
    ).order_by('created_at')[:10]
    
    unverified_users_list = CustomUser.objects.filter(is_verified=False).order_by('date_joined')[:10]

    context = {
        'total_users': total_users,
        'total_transactions': total_transactions,
        'verified_users': verified_users,
        'unverified_users': unverified_users,
        'pending_transactions': pending_transactions_count,
        'completed_transactions': completed_transactions,
        'rejected_transactions': rejected_transactions,
        'buy_count': buy_count,
        'sell_count': sell_count,
        'total_volume': total_volume,
        'buy_volume': buy_volume,
        'sell_volume': sell_volume,
        'pending_volume': pending_volume,
        'today_transactions': today_transactions,
        'today_volume': today_volume,
        'pending_transactions_list': pending_tx_list,
        'unverified_users_list': unverified_users_list,
    }

    return render(request, 'admin_panel/dashboard.html', context)


@staff_member_required
def users_list(request):
    """لیست کاربران"""
    user_search = request.GET.get('user_search', '')
    user_status_filter = request.GET.get('user_status', '')

    all_users_list = CustomUser.objects.order_by('-date_joined')
    if user_status_filter == 'verified':
        all_users_list = all_users_list.filter(is_verified=True)
    elif user_status_filter == 'unverified':
        all_users_list = all_users_list.filter(is_verified=False)
    if user_search:
        all_users_list = all_users_list.filter(
            Q(username__icontains=user_search) |
            Q(full_name__icontains=user_search) |
            Q(mobile__icontains=user_search)
        )

    context = {
        'users': all_users_list,
        'user_search': user_search,
        'user_status_filter': user_status_filter,
    }
    return render(request, 'admin_panel/users.html', context)


@staff_member_required
def transactions_list(request):
    """لیست تراکنش‌ها"""
    tx_status_filter = request.GET.get('tx_status', '')
    tx_type_filter = request.GET.get('tx_type', '')
    tx_search = request.GET.get('tx_search', '')
    tx_date_from = request.GET.get('date_from', '')
    tx_date_to = request.GET.get('date_to', '')

    all_transactions_list = Transaction.objects.select_related('user').order_by('-created_at')
    if tx_status_filter:
        all_transactions_list = all_transactions_list.filter(status=tx_status_filter)
    if tx_type_filter:
        all_transactions_list = all_transactions_list.filter(request_type=tx_type_filter)
    if tx_search:
        all_transactions_list = all_transactions_list.filter(
            Q(user__username__icontains=tx_search) |
            Q(user__full_name__icontains=tx_search) |
            Q(crypto_name__icontains=tx_search)
        )
    if tx_date_from:
        from datetime import datetime
        try:
            date_from = datetime.strptime(tx_date_from, '%Y-%m-%d')
            all_transactions_list = all_transactions_list.filter(created_at__gte=date_from)
        except ValueError:
            pass
    if tx_date_to:
        from datetime import datetime
        try:
            date_to = datetime.strptime(tx_date_to, '%Y-%m-%d')
            date_to = date_to.replace(hour=23, minute=59, second=59)
            all_transactions_list = all_transactions_list.filter(created_at__lte=date_to)
        except ValueError:
            pass

    context = {
        'transactions': all_transactions_list,
        'tx_status_filter': tx_status_filter,
        'tx_type_filter': tx_type_filter,
        'tx_search': tx_search,
        'tx_date_from': tx_date_from,
        'tx_date_to': tx_date_to,
    }
    return render(request, 'admin_panel/transactions.html', context)


@staff_member_required
def site_settings(request):
    """تنظیمات سایت"""
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'site_setting':
            form = SiteSettingForm(
                request.POST,
                instance=SiteSetting.get_solo(),
                prefix='site'
            )
            if form.is_valid():
                form.save()
                messages.success(request, "تنظیمات سایت ذخیره شد.")
                return redirect('panel_settings')
            else:
                messages.error(request, "خطایی در ذخیره تنظیمات سایت رخ داد.")

        elif form_type == 'crypto_setting':
            setting = CryptoApiSetting.objects.filter(active=True).first()
            form = CryptoApiSettingForm(
                request.POST,
                instance=setting or CryptoApiSetting(),
                prefix='crypto'
            )
            if form.is_valid():
                form.save()
                messages.success(request, "تنظیمات قیمت‌گذاری ذخیره شد.")
                return redirect('panel_settings')
            else:
                messages.error(request, "خطایی در ذخیره تنظیمات قیمت‌گذاری رخ داد.")

        elif form_type == 'bank_setting':
            site = SiteSetting.get_solo()
            site.site_card_number = request.POST.get('site_card_number', '')
            site.site_iban = request.POST.get('site_iban', '')
            site.site_account_holder = request.POST.get('site_account_holder', '')
            site.support_phone = request.POST.get('support_phone', '')
            site.save()
            messages.success(request, "اطلاعات بانکی ذخیره شد.")
            return redirect('panel_settings')

    site_form = SiteSettingForm(
        instance=SiteSetting.get_solo(),
        prefix='site'
    )

    active_crypto_setting = CryptoApiSetting.objects.filter(active=True).first()
    crypto_form = CryptoApiSettingForm(
        instance=active_crypto_setting or CryptoApiSetting(),
        prefix='crypto'
    )

    site_settings = SiteSetting.get_solo()

    context = {
        'site_form': site_form,
        'crypto_form': crypto_form,
        'site_settings': site_settings,
    }
    return render(request, 'admin_panel/settings.html', context)


@staff_member_required
def manage_sections(request):
    """مدیریت بخش‌های صفحه اصلی"""
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'add_section':
            form = HomePageSectionForm(
                request.POST,
                request.FILES,
                prefix='section'
            )
            if form.is_valid():
                form.save()
                messages.success(request, "بخش جدید با موفقیت اضافه شد.")
            else:
                messages.error(request, "خطایی در ثبت بخش جدید رخ داد.")
            return redirect('panel_sections')

        if form_type == 'edit_section':
            section_id = request.POST.get('section_id')
            section = get_object_or_404(HomePageSection, id=section_id)
            form = HomePageSectionForm(
                request.POST,
                request.FILES,
                instance=section,
                prefix='section'
            )
            if form.is_valid():
                form.save()
                messages.success(request, "بخش مورد نظر به‌روزرسانی شد.")
            else:
                messages.error(request, "خطایی در ویرایش بخش رخ داد.")
            return redirect('panel_sections')

        if form_type == 'delete_section':
            section_id = request.POST.get('section_id')
            section = get_object_or_404(HomePageSection, id=section_id)
            section.delete()
            messages.success(request, "بخش مورد نظر حذف شد.")
            return redirect('panel_sections')

    homepage_sections = HomePageSection.objects.order_by('section_key', 'order', '-created_at')
    section_form = HomePageSectionForm(prefix='section')

    context = {
        'homepage_sections': homepage_sections,
        'section_form': section_form,
    }
    return render(request, 'admin_panel/sections.html', context)


@staff_member_required
@require_POST
def change_transaction_status(request, tx_id):
    """تغییر وضعیت تراکنش"""
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

    return redirect('panel_transactions')


@staff_member_required
@require_POST
def add_transaction_note(request, tx_id):
    """افزودن یادداشت به تراکنش"""
    transaction = get_object_or_404(Transaction, id=tx_id)
    note = request.POST.get('admin_note', '')
    transaction.admin_note = note
    transaction.save()
    messages.success(request, "یادداشت با موفقیت ذخیره شد.")
    return redirect('panel_transactions')


@staff_member_required
@require_POST
def change_user_verification(request, user_id):
    """تغییر وضعیت تایید هویت کاربر"""
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

    return redirect('panel_users')


@staff_member_required
@require_POST
def delete_user(request, user_id):
    """حذف کاربر"""
    user = get_object_or_404(CustomUser, id=user_id)
    if user != request.user:
        username = user.username
        user.delete()
        messages.success(request, f"کاربر {username} با موفقیت حذف شد.")
    else:
        messages.error(request, "امکان حذف حساب کاربری خود وجود ندارد.")
    return redirect('panel_users')


@staff_member_required
@require_POST
def reset_user_password(request, user_id):
    """ریست رمز عبور کاربر"""
    user = get_object_or_404(CustomUser, id=user_id)
    new_password = request.POST.get('new_password', '')

    if not new_password or len(new_password) < 6:
        messages.error(request, "رمز عبور جدید باید حداقل ۶ کاراکتر باشد.")
    else:
        user.set_password(new_password)
        user.save()
        messages.success(request, f"رمز عبور کاربر {user.username} با موفقیت تغییر یافت.")

    return redirect('panel_users')