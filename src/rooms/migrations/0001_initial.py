# Generated by Django 5.0 on 2023-12-30 16:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies: list = []

    operations = [
        migrations.CreateModel(
            name='RoomData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                (
                    'type',
                    models.PositiveSmallIntegerField(
                        choices=[(0, 'Economy'), (1, 'Standard'), (2, 'Deluxe'), (3, 'Luxe')], default=1
                    ),
                ),
                ('single_beds', models.PositiveSmallIntegerField(null=True)),
                ('double_beds', models.PositiveSmallIntegerField(null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['type'],
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('number', models.CharField(max_length=10, unique=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Free'), (1, 'Booked')], default=0)),
                ('is_available', models.BooleanField(default=True)),
                ('room_data', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rooms.roomdata')),
            ],
            options={
                'ordering': ['number'],
            },
        ),
    ]
