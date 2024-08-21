from django.db import models
import random
import string
from django.db.models.signals import post_save
from django.urls import reverse
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from accounts.models import User

class Hotel(models.Model):
    name = models.TextField(default='')
    rank = models.IntegerField(default=3,validators=[MinValueValidator(1), MaxValueValidator(5)])
    country = models.TextField(default='')
    city = models.TextField(default='')

    def __str__(self):
        return self.name[0:40]

    @property
    def num_of_rooms(self):
        return self.rooms_list.count()
    
    def get_rooms(self):
        return self.rooms_list.all()
    
    def get_absolute_url(self):
        return reverse("hotel_details", kwargs={'pk':self.pk})
    

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms_list',null=True)
    name = models.TextField(default='1')
    serial_number = models.IntegerField()
    max_guests = models.IntegerField()
    price_for_night = models.IntegerField()
    size = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name[0:20]
    
    def get_absolute_url(self):
        return reverse('room_details', kwargs={'pk': self.pk})
    

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, max_length=100)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    confirmation_number = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user}'s reservation for {self.room.name}"
    
    def get_absolute_url(self):
        return reverse('order_confirmation', kwargs={'reservation_id': self.pk})

    def clean(self):
        if not self.check_in_date or not self.check_out_date:
            raise ValidationError('Both check-in and check-out dates are required.')
        if self.check_in_date >= self.check_out_date:
            raise ValidationError('Check-out date must be after check-in date.')

    def calculate_total_price(self):
        num_nights = (self.check_out_date - self.check_in_date).days
        price_per_night = self.room.price_for_night
        total_price = (num_nights * price_per_night) * 1.17  # Adding 17% taxes
        return total_price

    def generate_confirmation_number(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                       
    def save(self, *args, **kwargs):
        if not self.confirmation_number:
            self.confirmation_number = self.generate_confirmation_number()
        self.full_clean()  # This ensures clean() is called and validations are applied
        if not self.total_price:
            self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)
