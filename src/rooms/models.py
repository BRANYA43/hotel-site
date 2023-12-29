from django.db import models
from django.db.models import IntegerChoices


class STATUS(IntegerChoices):
    FREE = 0, 'Free'
    OCCUPIED = 1, 'Occupied'


class TYPE(IntegerChoices):
    ECONOMY = 0, 'Economy'
    STANDARD = 1, 'Standard'
    DELUXE = 2, 'Deluxe'
    LUXE = 3, 'Luxe'


class Room(models.Model):
    type = models.PositiveSmallIntegerField(choices=TYPE.choices, default=TYPE.STANDARD)
    status = models.PositiveSmallIntegerField(choices=STATUS.choices, default=STATUS.FREE)
    single_beds = models.IntegerField(default=0)
    double_beds = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def persons(self):
        return self.single_beds + (self.double_beds * 2)


class Number(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    number = models.IntegerField(unique=True)
    is_available = models.BooleanField(default=True)
