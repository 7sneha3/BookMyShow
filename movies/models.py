from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    name = models.CharField(max_length = 255)
    image = models.ImageField(upload_to = "movies/")
    rating = models.DecimalField(max_digits = 3, decimal_places = 1)
    cast = models.TextField()
    description = models.TextField(blank = True, null = True) #optional

    def __str__(self):
        return self.name
    
class Theater(models.Model):
    name = models.CharField(max_length = 255)
    # movie = models.ForeignKey(Movie, on_delete = models.CASCADE, related_name = 'theaters')
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    # time = models.DateTimeField()
    date = models.DateField()  # Date of the show; Ensure the Theater model includes a date field to store the show date; nsure that date is stored in the database for filtering.
    time = models.TimeField()  # Show timing
    total_seats = models.IntegerField(default=100)  # Set a default value
    base_price = models.DecimalField(max_digits=6, decimal_places=2, default=300.00)  # Default price

    def __str__(self):
        return f'{self.name} - {self.movie.name} on {self.date} at {self.time}'

class Seat(models.Model):
    theaters = models.ForeignKey(Theater, on_delete = models.CASCADE, related_name = 'seats')
    seat_number = models.CharField(max_length = 10)
    is_booked = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.seat_number} - {self.theaters.name}'
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    seat = models.OneToOneField(Seat, on_delete = models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    theaters = models.ForeignKey(Theater, on_delete = models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'Booking by {self.user.username} for {self.seat.seat_number} at {self.theaters.name}'

