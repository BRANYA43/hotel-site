# Generated by Django 5.0 on 2024-01-02 15:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0004_alter_user_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_confirmed_email',
            new_name='email_is_confirmed',
        ),
    ]