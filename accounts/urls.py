from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('wallet/', views.wallet, name='wallet'),
    path('wallet/update/', views.update_wallet_address, name='update_wallet_address'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('captcha/image/', views.generate_captcha_image, name='captcha_image'),
    path('captcha/refresh/', views.refresh_captcha, name='refresh_captcha'),
    path('dashboard/admin/transaction/<int:tx_id>/update/', views.change_transaction_status, name='change_transaction_status'),
    path('dashboard/admin/user/<int:user_id>/verify/', views.change_user_verification, name='change_user_verification'),
    path('dashboard/admin/user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
]