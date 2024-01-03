from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models

from bookings.validators import validate_check_in_date, validate_check_out_date
from rooms.models import TYPE, Room
from utils.models import DateMixin

User = get_user_model()


class Booking(DateMixin):
    uuid = models.UUIDField(
        default=uuid4, max_length=10, primary_key=True, unique=True, verbose_name='Унікальний ідентифікатор'
    )
    user = models.ForeignKey(User, models.PROTECT, verbose_name='Користувач')
    rooms = models.ManyToManyField(Room, verbose_name='Номери')
    persons = models.PositiveSmallIntegerField(default=1, verbose_name='Кількість осіб')
    type = models.PositiveSmallIntegerField(choices=TYPE.choices, default=TYPE.STANDARD, verbose_name='Тип')
    has_children = models.BooleanField(default=False, verbose_name='Чи є діти')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    check_in = models.DateField(verbose_name='Дата заїзду')
    check_out = models.DateField(verbose_name='Дата виїзду')

    def clean(self):
        validate_check_in_date(self.check_in)
        validate_check_out_date(self.check_out, self.check_in)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Бронювання'
        verbose_name_plural = 'Бронювання'

    def __str__(self):
        return str(self.uuid)

    def get_str_rooms(self):
        rooms = [room.number for room in self.rooms.all()]
        return ', '.join(rooms)

    def get_total_price(self):
        prices = [room.room_data.price for room in self.rooms.all()]
        return sum(prices)

    def get_str_type(self):
        return TYPE.choices[self.type][1]
