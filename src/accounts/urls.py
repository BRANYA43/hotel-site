from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('sing-up/', views.UserRegisterView.as_view(), name='user-register'),
]
