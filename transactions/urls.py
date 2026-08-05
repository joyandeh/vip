from django.urls import path
from . import views

urlpatterns = [
    path('buy/', views.buy_crypto, name='buy_crypto'),
    path('sell/', views.sell_crypto, name='sell_crypto'),
    path('history/', views.request_history, name='request_history'),
    path('detail/<int:pk>/', views.transaction_detail, name='transaction_detail'),
]