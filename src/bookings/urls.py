from django.urls import path

from bookings import views
from utils.tests import imitating_view

app_name = 'bookings'

urlpatterns = [
    path('create/', views.BookingCreateView.as_view(), name='booking-create'),
    path('list/', imitating_view, name='booking-list'),
]
