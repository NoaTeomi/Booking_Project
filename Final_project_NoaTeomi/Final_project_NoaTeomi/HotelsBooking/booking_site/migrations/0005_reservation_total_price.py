# Generated by Django 4.2.13 on 2024-05-31 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_site', '0004_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
