from django.contrib.auth import mixins
from django.urls import reverse_lazy
from django.views import generic

from bookings import forms
from bookings.models import Booking


class BookingCreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = Booking
    form_class = forms.BookingCreateForm
    template_name = 'bookings/create_form.html'
    success_url = reverse_lazy('bookings:booking-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class BookingListView(mixins.LoginRequiredMixin, generic.ListView):
    model = Booking
    template_name = 'bookings/list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
