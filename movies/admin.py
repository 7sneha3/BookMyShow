from django.contrib import admin

# Register your models here.
from .models import Movie, Theater, Seat, Booking

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    # list_display = ['name', 'image', 'rating', 'cast', 'description']
    list_display = ['name', 'rating', 'cast', 'description']

@admin.register(Theater)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie', 'time']

@admin.register(Seat)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['theaters', 'seat_number', 'is_booked']

@admin.register(Booking)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['user', 'seat', 'movie', 'theaters', 'booked_at']
