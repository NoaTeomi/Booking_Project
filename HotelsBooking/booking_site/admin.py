from django.contrib import admin


from .models import Hotel

admin.site.register(Hotel)

from .models import Room

admin.site.register(Room)

from .models import Reservation
admin.site.register(Reservation)
