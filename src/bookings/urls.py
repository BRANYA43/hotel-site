from django.urls import path

from bookings import views

app_name = 'bookings'

urlpatterns = [
    path('create/', views.BookingCreateView.as_view(), name='booking-create'),
    path('list/', views.BookingListView.as_view(), name='booking-list'),
]
