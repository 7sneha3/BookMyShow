# Generated by Django 5.1.4 on 2025-01-26 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_seat_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seat',
            name='category',
        ),
    ]
