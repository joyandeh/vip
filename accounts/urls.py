from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    
    # حتماً مطمئن شوید این دو خط در این فایل وجود دارند:
    path('dashboard/admin/transaction/<int:tx_id>/update/', views.change_transaction_status, name='change_transaction_status'),
    path('dashboard/admin/user/<int:user_id>/verify/', views.change_user_verification, name='change_user_verification'),
]