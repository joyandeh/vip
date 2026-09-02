from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserProfileForm, RegisterForm
from .models import CustomUser


def register(request):
    """ثبت‌نام کاربر جدید"""
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد. به پنل کاربری خوش آمدید!')
            return redirect('profile')
    else:
        form = RegisterForm()
   
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def user_login(request):
    """ورود کاربر"""
    import random
    
    def get_captcha():
        return ''.join(str(random.randint(0, 9)) for _ in range(4))
    
    if request.method == 'POST':
        # Check if this is step 2 (captcha verification)
        login_step = request.POST.get('login_step', '1')
        
        if login_step == '2':
            # Step 2: Verify captcha
            captcha_code = request.POST.get('captcha_code', '')
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            
            # Verify captcha (in production, compare with server-side stored captcha)
            # For now, we'll accept any 4-digit code for demo purposes
            if len(captcha_code) == 4 and captcha_code.isdigit():
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'ورود با موفقیت انجام شد.')
                    return redirect('home')
                else:
                    messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
                    return redirect('login')
            else:
                messages.error(request, 'کد امنیتی نامعتبر است.')
                # Re-render with captcha
                form = AuthenticationForm(request, data={'username': username})
                return render(request, 'accounts/login.html', {'form': form, 'show_captcha': True, 'captcha_code': get_captcha(), 'username': username})
        else:
            # Step 1: Initial username/password check
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                # Show captcha for step 2
                return render(request, 'accounts/login.html', {
                    'form': form, 
                    'show_captcha': True, 
                    'captcha_code': get_captcha(),
                    'username': user.username
                })
            else:
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
                # Show form with captcha even on step 1 failure
                return render(request, 'accounts/login.html', {'form': form, 'show_captcha': True, 'captcha_code': get_captcha()})
    else:
        form = AuthenticationForm()
        # Generate captcha for initial page load
        return render(request, 'accounts/login.html', {'form': form, 'show_captcha': True, 'captcha_code': get_captcha()})


@login_required
def user_logout(request):
    """خروج کاربر"""
    logout(request)
    messages.success(request, 'شما از حساب کاربری خود خارج شدید.')
    return redirect('home')


@login_required
def wallet(request):
    """صفحه کیف پول کاربر - نمایش آدرس‌ها و موجودی‌ها"""
    user = request.user
    # Prepare asset data for display
    assets = [
        {
            'name': 'ترون',
            'icon': 'fa-solid fa-t',
            'color': 'coral',          
            'withdraw_bg': '#EA580C',   # Coral red
            'withdraw_text': '#FFFFFF',
            'watermark_color': '#EA580C',
            'address': user.trx_address or '─',
            'balance': user.trx_balance,
            'address_field': 'trx_address',
            'balance_field': 'trx_balance',
            'id': 1,
        },
        {
            'name': 'تتر',
            'icon': 'fa-solid fa-coins',
            'color': 'green',          
            'withdraw_bg': '#16A34A',   # Warm green
            'withdraw_text': '#FFFFFF',
            'watermark_color': '#16A34A',
            'address': user.usdt_address or '─',
            'balance': user.usdt_balance,
            'address_field': 'usdt_address',
            'balance_field': 'usdt_balance',
            'id': 2,
        },
        {
            'name': 'بیت کوین',
            'icon': 'fa-brands fa-bitcoin',
            'color': 'coral',          
            'withdraw_bg': '#F7931A',   # Bitcoin orange
            'withdraw_text': '#FFFFFF',
            'watermark_color': '#F7931A',
            'address': user.btc_address or '─',
            'balance': user.btc_balance,
            'address_field': 'btc_address',
            'balance_field': 'btc_balance',
            'id': 3,
        },
        {
            'name': 'اتریوم',
            'icon': 'fa-brands fa-ethereum',
            'color': 'purple',         
            'withdraw_bg': '#627EEA',   # Ethereum purple
            'withdraw_text': '#FFFFFF',
            'watermark_color': '#627EEA',
            'address': user.eth_address or '─',
            'balance': user.eth_balance,
            'address_field': 'eth_address',
            'balance_field': 'eth_balance',
            'id': 4,
        },
        {
            'name': 'سولانا',
            'icon': 'fa-solid fa-sun',
            'color': 'warning',        
            'withdraw_bg': '#9945FF',   # Solana purple
            'withdraw_text': '#FFFFFF',
            'watermark_color': '#9945FF',
            'address': user.sol_address or '─',
            'balance': user.sol_balance,
            'address_field': 'sol_address',
            'balance_field': 'sol_balance',
            'id': 5,
        },
        {
            'name': 'بینانس',
            'icon': 'fa-solid fa-coins',
            'color': 'warning',        
            'withdraw_bg': '#F3BA2F',   # BNB yellow
            'withdraw_text': '#1C1917',
            'watermark_color': '#F3BA2F',
            'address': user.bnb_address or '─',
            'balance': user.bnb_balance,
            'address_field': 'bnb_address',
            'balance_field': 'bnb_balance',
            'id': 6,
        },
        {
            'name': 'ریپل',
            'icon': 'fa-solid fa-xmark',
            'color': 'warning',        
            'withdraw_bg': '#0077B5',   # XRP blue
            'withdraw_text': '#FFFFFF',
            'watermark_color': '#0077B5',
            'address': user.xrp_address or '─',
            'balance': user.xrp_balance,
            'address_field': 'xrp_address',
            'balance_field': 'xrp_balance',
            'id': 7,
        },
        {
            'name': 'perfect money',
            'icon': 'fa-solid fa-dollar-sign',
            'color': 'neon-green',     
            'withdraw_bg': '#16A34A',   # Warm green
            'withdraw_text': '#FFFFFF',
            'watermark_color': '#16A34A',
            'address': user.pm_address or '─',
            'balance': user.pm_balance,
            'address_field': 'pm_address',
            'balance_field': 'pm_balance',
            'id': 8,
        },
    ]
    context = {
        'user': user,
        'assets': assets,
    }
    return render(request, 'accounts/wallet.html', context)


@login_required
def admin_dashboard(request):
    """Admin dashboard redirect to panel dashboard"""
    return redirect('panel_dashboard')


@login_required
def profile(request):
    """صفحه پروفایل کاربر - ویرایش اطلاعات و آدرس‌های کیف پول"""
    user = request.user
    
    # Prepare wallet assets data (same as wallet view)
    wallet_assets = [
        {
            'name': 'ترون',
            'icon': 'fa-solid fa-t',
            'color': 'cyan',
            'address': user.trx_address or '─',
            'balance': user.trx_balance,
            'address_field': 'trx_address',
            'balance_field': 'trx_balance',
            'id': 1,
        },
        {
            'name': 'تتر',
            'icon': 'fa-solid fa-coins',
            'color': 'cyan',
            'address': user.usdt_address or '─',
            'balance': user.usdt_balance,
            'address_field': 'usdt_address',
            'balance_field': 'usdt_balance',
            'id': 2,
        },
        {
            'name': 'بیت کوین',
            'icon': 'fa-brands fa-bitcoin',
            'color': 'coral',
            'address': user.btc_address or '─',
            'balance': user.btc_balance,
            'address_field': 'btc_address',
            'balance_field': 'btc_balance',
            'id': 3,
        },
        {
            'name': 'اتریوم',
            'icon': 'fa-brands fa-ethereum',
            'color': 'cyan',
            'address': user.eth_address or '─',
            'balance': user.eth_balance,
            'address_field': 'eth_address',
            'balance_field': 'eth_balance',
            'id': 4,
        },
        {
            'name': 'سولانا',
            'icon': 'fa-solid fa-sun',
            'color': 'warning',
            'address': user.sol_address or '─',
            'balance': user.sol_balance,
            'address_field': 'sol_address',
            'balance_field': 'sol_balance',
            'id': 5,
        },
        {
            'name': 'بینانس',
            'icon': 'fa-solid fa-coins',
            'color': 'warning',
            'address': user.bnb_address or '─',
            'balance': user.bnb_balance,
            'address_field': 'bnb_address',
            'balance_field': 'bnb_balance',
            'id': 6,
        },
        {
            'name': 'ریپل',
            'icon': 'fa-solid fa-xmark',
            'color': 'warning',
            'address': user.xrp_address or '─',
            'balance': user.xrp_balance,
            'address_field': 'xrp_address',
            'balance_field': 'xrp_balance',
            'id': 7,
        },
        {
            'name': 'perfect money',
            'icon': 'fa-solid fa-dollar-sign',
            'color': 'neon-green',
            'address': user.pm_address or '─',
            'balance': user.pm_balance,
            'address_field': 'pm_address',
            'balance_field': 'pm_balance',
            'id': 8,
        },
    ]
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات پروفایل با موفقیت به‌روزرسانی شد.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
  
    context = {
        'form': form,
        'user': user,
        'wallet_assets': wallet_assets,
    }
    return render(request, 'accounts/profile.html', context)


def generate_captcha_image(request):
    """Simple captcha image placeholder"""
    from django.http import HttpResponse
    # Return a 1x1 transparent pixel (or a simple text for testing)
    return HttpResponse("CAPTCHA", content_type="image/png")


def refresh_captcha(request):
    """Refresh captcha endpoint"""
    from django.http import JsonResponse
    return JsonResponse({'status': 'ok'})


@login_required
def change_transaction_status(request, tx_id):
    """Placeholder for transaction status change"""
    from django.http import HttpResponseNotAllowed
    if request.method == 'POST':
        # TODO: implement
        messages.success(request, f'Transaction {tx_id} status updated.')
        return redirect('panel_transactions')
    return HttpResponseNotAllowed(['POST'])


@login_required
def update_wallet_address(request):
    """AJAX endpoint to update wallet address (balance editing removed)"""
    from django.http import JsonResponse
    from decimal import Decimal
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    import json
    try:
        data = json.loads(request.body)
        address_field = data.get('address_field')
        address = data.get('address', '').strip()
        
        # Validate fields
        valid_address_fields = ['trx_address', 'usdt_address', 'btc_address', 'eth_address', 
                                'sol_address', 'bnb_address', 'xrp_address', 'pm_address']
        
        # Check if address_field is provided and valid
        if not address_field or address_field not in valid_address_fields:
            return JsonResponse({'success': False, 'error': 'Invalid field'}, status=400)
        
        # Update user - only address
        user = request.user
        setattr(user, address_field, address)
        user.save()
        
        return JsonResponse({'success': True, 'message': 'آدرس کیف پول با موفقیت به‌روزرسانی شد.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
def change_user_verification(request, user_id):
    """Placeholder for user verification change"""
    from django.http import HttpResponseNotAllowed
    if request.method == 'POST':
        # TODO: implement
        messages.success(request, f'User {user_id} verification updated.')
        return redirect('panel_users')
    return HttpResponseNotAllowed(['POST'])


@login_required
def delete_user(request, user_id):
    """Placeholder for user deletion"""
    from django.http import HttpResponseNotAllowed
    if request.method == 'POST':
        # TODO: implement
        messages.success(request, f'User {user_id} deleted.')
        return redirect('panel_users')
    return HttpResponseNotAllowed(['POST'])