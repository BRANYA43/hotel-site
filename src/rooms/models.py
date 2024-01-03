from django.db import models

from utils.models import DateMixin


class TYPE(models.IntegerChoices):
    ECONOMY = 0, 'Economy'
    STANDARD = 1, 'Standard'
    DELUXE = 2, 'Deluxe'
    LUXE = 3, 'Luxe'


class RoomData(DateMixin):
    name = models.CharField(max_length=50, verbose_name='Назва')
    slug = models.SlugField(max_length=50, verbose_name='Слаг')
    type = models.PositiveSmallIntegerField(choices=TYPE.choices, default=TYPE.STANDARD, verbose_name='Тип')
    single_beds = models.PositiveSmallIntegerField(default=0, verbose_name='Односпальні ліжка')
    double_beds = models.PositiveSmallIntegerField(default=0, verbose_name='Двоспальні ліжка')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
    description = models.TextField(null=True, blank=True, verbose_name='Опис')

    class Meta:
        ordering = ['type']
        verbose_name = 'Дані Кімнати'
        verbose_name_plural = 'Дані Кімнат'

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
    room_data = models.ForeignKey(RoomData, models.PROTECT, verbose_name='Дані номеру')
    number = models.CharField(max_length=10, unique=True, verbose_name='Номер')
    status = models.PositiveSmallIntegerField(choices=STATUS.choices, default=STATUS.FREE, verbose_name='Статус')
    is_available = models.BooleanField(default=True, verbose_name='Доступний')

    class Meta:
        ordering = ['number']
        verbose_name = 'Кімната'
        verbose_name_plural = 'Кімнати'

    def __str__(self):
        return self.number
