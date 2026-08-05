from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
import random
import io

from transactions.models import Transaction
from accounts.models import CustomUser
from core.models import CryptoApiSetting, HomePageSection, SiteSetting
from core.forms import HomePageSectionForm, CryptoApiSettingForm, SiteSettingForm

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


@staff_member_required
def admin_dashboard(request):

    # --- POST: فرم‌های مدیریت صفحه اصلی / تنظیمات ---
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
            return redirect('admin_dashboard')

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
            return redirect('admin_dashboard')

        if form_type == 'delete_section':
            section_id = request.POST.get('section_id')
            section = get_object_or_404(HomePageSection, id=section_id)
            section.delete()
            messages.success(request, "بخش مورد نظر حذف شد.")
            return redirect('admin_dashboard')

        if form_type == 'site_setting':
            form = SiteSettingForm(
                request.POST,
                instance=SiteSetting.get_solo(),
                prefix='site'
            )
            if form.is_valid():
                form.save()
                messages.success(request, "تنظیمات سایت ذخیره شد.")
            else:
                messages.error(request, "خطایی در ذخیره تنظیمات سایت رخ داد.")
            return redirect('admin_dashboard')

        if form_type == 'crypto_setting':
            setting = CryptoApiSetting.objects.filter(active=True).first()
            form = CryptoApiSettingForm(
                request.POST,
                instance=setting or CryptoApiSetting(),
                prefix='crypto'
            )
            if form.is_valid():
                form.save()
                messages.success(request, "تنظیمات قیمت‌گذاری ذخیره شد.")
            else:
                messages.error(request, "خطایی در ذخیره تنظیمات قیمت‌گذاری رخ داد.")
            return redirect('admin_dashboard')

    # --- آمارهای کلی ---
    total_users = CustomUser.objects.count()
    total_transactions = Transaction.objects.count()
    verified_users = CustomUser.objects.filter(is_verified=True).count()
    unverified_users = CustomUser.objects.filter(is_verified=False).count()

    pending_transactions_count = Transaction.objects.filter(status='paid').count()
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

    pending_volume = Transaction.objects.filter(status='paid').aggregate(
        total=Sum('total_price')
    )['total'] or 0

    # --- آمار امروز ---
    today = timezone.now().date()
    today_start = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
    today_transactions = Transaction.objects.filter(created_at__gte=today_start).count()
    today_volume = Transaction.objects.filter(
        created_at__gte=today_start, status='done'
    ).aggregate(total=Sum('total_price'))['total'] or 0

    # --- فیلتر تراکنش‌ها ---
    tx_status_filter = request.GET.get('tx_status', '')
    tx_type_filter = request.GET.get('tx_type', '')
    tx_search = request.GET.get('tx_search', '')

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

    # --- فیلتر کاربران ---
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

    # --- لیست‌ها ---
    pending_tx_list = Transaction.objects.filter(status='paid').order_by('created_at')
    unverified_users_list = CustomUser.objects.filter(is_verified=False).order_by('date_joined')
    homepage_sections = HomePageSection.objects.order_by('section_key', 'order', '-created_at')

    # --- فرم‌ها برای نمایش ---
    active_crypto_setting = CryptoApiSetting.objects.filter(active=True).first()
    crypto_form = CryptoApiSettingForm(
        instance=active_crypto_setting or CryptoApiSetting(),
        prefix='crypto'
    )

    site_form = SiteSettingForm(
        instance=SiteSetting.get_solo(),
        prefix='site'
    )

    section_form = HomePageSectionForm(prefix='section')

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
        'all_transactions_list': all_transactions_list,
        'all_users_list': all_users_list,
        'homepage_sections': homepage_sections,
        'crypto_form': crypto_form,
        'site_form': site_form,
        'section_form': section_form,
        'tx_status_filter': tx_status_filter,
        'tx_type_filter': tx_type_filter,
        'tx_search': tx_search,
        'user_search': user_search,
        'user_status_filter': user_status_filter,
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


@staff_member_required
@require_POST
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if user != request.user:
        username = user.username
        user.delete()
        messages.success(request, f"کاربر {username} با موفقیت حذف شد.")
    else:
        messages.error(request, "امکان حذف حساب کاربری خود وجود ندارد.")
    return redirect('admin_dashboard')


@login_required
def profile(request):
    if request.method == 'POST':
        edit_field = request.POST.get('edit_field')
        value = request.POST.get('value', '')

        if edit_field == 'email':
            request.user.email = value.strip()
            request.user.save()
            return JsonResponse({'success': True})

        elif edit_field == 'card_number':
            request.user.card_number = value.strip()
            request.user.save()
            return JsonResponse({'success': True})

        elif edit_field == 'password':
            if len(value) < 8:
                return JsonResponse({'success': False, 'error': 'رمز عبور باید حداقل ۸ کاراکتر باشد.'})
            request.user.set_password(value)
            request.user.save()
            update_session_auth_hash(request, request.user)
            return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'error': 'فیلد نامعتبر'})

    return render(request, 'accounts/profile.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # اگر کاربر لاگین کرده و می‌خواهد مدارک را دوباره ارسال کند
            if request.user.is_authenticated and request.POST.get('reupload') == '1':
                user = request.user
                # فقط فیلدهای مدارک را آپدیت کن
                if 'national_card_image' in request.FILES:
                    user.national_card_image = request.FILES['national_card_image']
                if 'selfie_image' in request.FILES:
                    user.selfie_image = request.FILES['selfie_image']
                if request.POST.get('card_number'):
                    user.card_number = request.POST['card_number'].strip()
                if request.POST.get('iban'):
                    user.iban = request.POST['iban'].strip()
                user.save()
                messages.success(request, 'مدارک شما با موفقیت آپدیت شدند و مجدداً برای بررسی ارسال شدند.')
                return redirect('profile')
            else:
                user = form.save()
                login(request, user)
                messages.success(request, 'ثبت نام شما با موفقیت انجام شد و وارد حساب کاربری خود شدید.')
                return redirect('/')
    else:
        form = RegisterForm()

    # check if user came from profile to reupload documents
    from_profile = request.GET.get('reupload') == '1' and request.user.is_authenticated

    return render(request, 'accounts/register.html', {'form': form, 'from_profile': from_profile})


def user_login(request):
    if request.method == "POST":
        # Check if this is captcha verification step
        if request.POST.get('login_step') == '2':
            form = AuthenticationForm(request, data=request.POST)
            form.error_messages = {
                'invalid_login': 'نام کاربری یا رمز عبور اشتباه است.',
                'inactive': 'این حساب کاربری غیرفعال است.',
            }
            form.fields['username'].error_messages = {'required': 'نام کاربری یا ایمیل الزامی است.'}
            form.fields['password'].error_messages = {'required': 'رمز عبور الزامی است.'}
            
            # Get username/email and password from the form
            login_identifier = request.POST.get('username', '').strip()
            password = request.POST.get('password', '')
            captcha_code = request.POST.get('captcha_code', '')
            
            if not login_identifier or not password:
                messages.error(request, 'نام کاربری/ایمیل و رمز عبور الزامی است.')
                # Generate captcha for retry
                new_captcha = ''.join(str(random.randint(0, 9)) for _ in range(4))
                request.session['captcha_code'] = new_captcha
                return render(request, 'accounts/login.html', {
                    'form': form,
                    'show_captcha': True,
                    'captcha_code': new_captcha
                })
            
            if not captcha_code or len(captcha_code) != 4:
                messages.error(request, 'کد کپچای ۴ رقمی را وارد کنید.')
                # Generate new captcha for retry
                new_captcha = ''.join(str(random.randint(0, 9)) for _ in range(4))
                request.session['captcha_code'] = new_captcha
                return render(request, 'accounts/login.html', {
                    'form': form,
                    'show_captcha': True,
                    'captcha_code': new_captcha
                })
            
            # Verify captcha from session
            session_captcha = request.session.get('captcha_code', '')
            if captcha_code != session_captcha:
                messages.error(request, 'کد کپچا اشتباه است.')
                # Generate new captcha for retry
                new_captcha = ''.join(str(random.randint(0, 9)) for _ in range(4))
                request.session['captcha_code'] = new_captcha
                return render(request, 'accounts/login.html', {
                    'form': form,
                    'show_captcha': True,
                    'captcha_code': new_captcha
                })
            
            # Verify credentials - support both username and email
            from django.contrib.auth import authenticate
            from accounts.models import CustomUser
            
            # Try to find user by username or email
            user = None
            if '@' in login_identifier:
                # Looks like an email
                try:
                    user_obj = CustomUser.objects.get(email__iexact=login_identifier)
                    username = user_obj.username
                except CustomUser.DoesNotExist:
                    username = login_identifier
            else:
                username = login_identifier
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                # Clear captcha from session
                if 'captcha_code' in request.session:
                    del request.session['captcha_code']
                messages.success(request, 'ورود شما با موفقیت انجام شد.')
                return redirect('/')
            else:
                messages.error(request, 'نام کاربری/ایمیل یا رمز عبور اشتباه است.')
                # Generate new captcha for retry
                new_captcha = ''.join(str(random.randint(0, 9)) for _ in range(4))
                request.session['captcha_code'] = new_captcha
                return render(request, 'accounts/login.html', {
                    'form': form,
                    'show_captcha': True,
                    'captcha_code': new_captcha
                })
        
        # Step 1: Initial login attempt
        else:
            form = AuthenticationForm(request, data=request.POST)
            form.error_messages = {
                'invalid_login': 'نام کاربری یا رمز عبور اشتباه است.',
                'inactive': 'این حساب کاربری غیرفعال است.',
            }
            form.fields['username'].error_messages = {'required': 'نام کاربری یا ایمیل الزامی است.'}
            form.fields['password'].error_messages = {'required': 'رمز عبور الزامی است.'}
            
            if form.is_valid():
                # Get the identifier (username or email)
                login_identifier = form.cleaned_data['username'].strip()
                from accounts.models import CustomUser
                
                # Try to find user by username or email
                user = None
                if '@' in login_identifier:
                    try:
                        user = CustomUser.objects.get(email__iexact=login_identifier)
                    except CustomUser.DoesNotExist:
                        user = form.get_user()  # fallback to normal auth
                else:
                    user = form.get_user()
                
                # Generate initial captcha for step 2
                captcha_code = ''.join(str(random.randint(0, 9)) for _ in range(4))
                request.session['captcha_code'] = captcha_code
                return render(request, 'accounts/login.html', {
                    'form': form,
                    'show_captcha': True,
                    'username': user.username,
                    'password': form.cleaned_data['password'],
                    'captcha_code': captcha_code
                })
    else:
        # GET request - show captcha immediately
        form = AuthenticationForm()
        form.fields['username'].label = 'نام کاربری یا ایمیل'
        # Generate initial captcha for immediate display
        captcha_code = ''.join(str(random.randint(0, 9)) for _ in range(4))
        request.session['captcha_code'] = captcha_code
        return render(request, 'accounts/login.html', {
            'form': form,
            'show_captcha': True,
            'captcha_code': captcha_code
        })


def user_logout(request):
    logout(request)
    return redirect('/')


def generate_captcha_image(request):
    """Generate a 4-digit captcha image and store in session."""
    # Generate 4-digit code
    captcha_code = ''.join(str(random.randint(0, 9)) for _ in range(4))
    request.session['captcha_code'] = captcha_code
    
    if PIL_AVAILABLE:
        # Create image with PIL
        width, height = 160, 60
        image = Image.new('RGB', (width, height), color=(11, 14, 20))
        draw = ImageDraw.Draw(image)
        
        # Add noise/background
        for _ in range(30):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.line([x1, y1, x2, y2], fill=(0, 229, 255, 50), width=1)
        
        # Add dots
        for _ in range(50):
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw.point([x, y], fill=(0, 230, 118, 80))
        
        # Draw captcha text
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        except:
            font = ImageFont.load_default()
        
        for i, char in enumerate(captcha_code):
            x = 20 + i * 35 + random.randint(-3, 3)
            y = 10 + random.randint(-5, 5)
            # Shadow
            draw.text((x+2, y+2), char, font=font, fill=(0, 0, 0, 180))
            # Main text
            draw.text((x, y), char, font=font, fill=(0, 229, 255, 255))
        
        # Add some distortion lines
        for _ in range(3):
            y = random.randint(10, 50)
            draw.line([0, y, width, y], fill=(0, 229, 255, 100), width=2)
        
        # Apply slight blur
        image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # Save to bytes
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)
        
        response = HttpResponse(buffer.getvalue(), content_type='image/png')
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response
    else:
        # Fallback: return a simple SVG
        svg = f'''<svg width="160" height="60" xmlns="http://www.w3.org/2000/svg">
            <rect width="100%" height="100%" fill="#0B0E14"/>
            <text x="80" y="38" text-anchor="middle" font-family="monospace" font-size="32" font-weight="bold" fill="#00E5FF" letter-spacing="8">{captcha_code}</text>
            <line x1="0" y1="20" x2="160" y2="20" stroke="#00E676" stroke-width="1" opacity="0.3"/>
            <line x1="0" y1="40" x2="160" y2="40" stroke="#00E5FF" stroke-width="1" opacity="0.3"/>
        </svg>'''
        response = HttpResponse(svg, content_type='image/svg+xml')
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response


@require_POST
def refresh_captcha(request):
    """Generate new captcha code and store in session"""
    captcha_code = ''.join(str(random.randint(0, 9)) for _ in range(4))
    request.session['captcha_code'] = captcha_code
    return JsonResponse({'captcha_code': captcha_code})
