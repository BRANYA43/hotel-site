from django.views import generic

from rooms.models import RoomData


class RoomDataListView(generic.ListView):
    model = RoomData
    template_name = 'rooms/list.html'
