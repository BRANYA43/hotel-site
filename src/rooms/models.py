from django.db import models

from utils.models import DateMixin


class TYPE(models.IntegerChoices):
    ECONOMY = 0, 'Economy'
    STANDARD = 1, 'Standard'
    DELUXE = 2, 'Deluxe'
    LUXE = 3, 'Luxe'


class RoomData(DateMixin):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    type = models.PositiveSmallIntegerField(choices=TYPE.choices, default=TYPE.STANDARD)
    single_beds = models.PositiveSmallIntegerField(null=True)
    double_beds = models.PositiveSmallIntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['type']

    def __str__(self):
        return self.slug

    @property
    def persons(self):
        if self.single_beds and self.double_beds:
            return self.single_beds + (self.double_beds * 2)
        return 0


class STATUS(models.IntegerChoices):
    FREE = 0, 'Free'
    BOOKED = 1, 'Booked'


class Room(DateMixin):
    room_data = models.ForeignKey(RoomData, models.PROTECT)
    number = models.CharField(max_length=10, unique=True)
    status = models.PositiveSmallIntegerField(choices=STATUS.choices, default=STATUS.FREE)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return self.number
