# Generated by Django 4.2.13 on 2024-06-02 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_site', '0006_alter_room_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='confirmation_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
