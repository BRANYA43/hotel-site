from django import forms
from django.core.exceptions import ValidationError

from bookings.models import Booking

NO_PERSONS_ERROR_MESSAGE = 'Persons can only be 1 and more.'


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['persons', 'type', 'is_children', 'check_in', 'check_out']
        widgets = {'user': forms.HiddenInput()}

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_persons(self):
        persons = self.cleaned_data.get('persons')

        if persons <= 0:
            raise ValidationError(NO_PERSONS_ERROR_MESSAGE)

        return persons

    def save(self, commit=True):
        self.instance.user = self.user
        return super().save(commit)
