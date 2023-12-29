from django.db import models
from django.db.models import IntegerChoices

from utils.models import DateMixin


class STATUS(IntegerChoices):
    FREE = 0, 'Free'
    OCCUPIED = 1, 'Occupied'


class TYPE(IntegerChoices):
    ECONOMY = 0, 'Economy'
    STANDARD = 1, 'Standard'
    DELUXE = 2, 'Deluxe'
    LUXE = 3, 'Luxe'


class Room(DateMixin):
    slug = models.SlugField(max_length=50)
    type = models.PositiveSmallIntegerField(choices=TYPE.choices, default=TYPE.STANDARD)
    status = models.PositiveSmallIntegerField(choices=STATUS.choices, default=STATUS.FREE)
    single_beds = models.IntegerField(default=0)
    double_beds = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.slug

    @property
    def persons(self):
        return self.single_beds + (self.double_beds * 2)


class Number(DateMixin):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    number = models.IntegerField(unique=True)
    is_available = models.BooleanField(default=True)
