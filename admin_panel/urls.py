from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='panel_dashboard'),
    path('users/', views.users_list, name='panel_users'),
    path('users/<int:user_id>/verify/', views.change_user_verification, name='panel_user_verify'),
    path('users/<int:user_id>/delete/', views.delete_user, name='panel_user_delete'),
    path('transactions/', views.transactions_list, name='panel_transactions'),
    path('transactions/<int:tx_id>/update/', views.change_transaction_status, name='panel_transaction_update'),
    path('transactions/<int:tx_id>/note/', views.add_transaction_note, name='panel_transaction_note'),
    path('settings/', views.site_settings, name='panel_settings'),
    path('settings/sections/', views.manage_sections, name='panel_sections'),
]