# Generated by Django 4.2.13 on 2024-05-31 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_site', '0005_reservation_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.TextField(default='1'),
        ),
    ]
