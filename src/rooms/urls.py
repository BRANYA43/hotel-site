from django.urls import path

from rooms import views

app_name = 'rooms'
urlpatterns: list = [
    path('list/', views.RoomDataListView.as_view(), name='room-list'),
]
