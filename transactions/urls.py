from django.urls import path
from . import views

urlpatterns = [

    path(
        'request/',
        views.create_request,
        name='request_crypto'
    ),

    path(
        'history/',
        views.request_history,
        name='request_history'
    ),

    path(
        'detail/<int:pk>/',
        views.transaction_detail,
        name='transaction_detail'
    ),
]
