from django.contrib import admin

from .models import Booking, BookingSeat, Seat

admin.site.register(Booking)
admin.site.register(Seat)
admin.site.register(BookingSeat)
