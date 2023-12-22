from django.urls import path

from accounts import views
from utils.tests import imitating_view

app_name = 'accounts'

urlpatterns = [
    path('sing-up/', views.UserRegisterView.as_view(), name='user-register'),
    path('sing-up/success/', views.UserRegisterSuccessView.as_view(), name='user-register-success'),
    path('sing-up/confirm-email/<uidb64>/<token>/', imitating_view, name='user-confirm-email'),
]
