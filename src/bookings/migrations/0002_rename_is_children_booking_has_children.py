# Generated by Django 5.0 on 2024-01-02 16:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='is_children',
            new_name='has_children',
        ),
    ]
