from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Theater, Seat, Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from datetime import date, datetime, timedelta #importing for displaying date wise movies
from django.utils.timezone import localdate, now
from django.http import JsonResponse
import json
from decimal import Decimal  

def current_shows(request):
    current_date = date.today()
    # print(f"DEBUG: Current Date - {current_date}")  # Debug today's date

    current_shows = Theater.objects.filter(date=current_date).order_by('time').values(
        'movie__id', 'movie__name', 'name', 'date', 'time'
    )
    # print(f"DEBUG: Current Shows Query Result - {list(current_shows)}")  # Debug query result
    return render(request, 'movies/current_shows.html', {'current_shows': current_shows})
    # return JsonResponse(list(current_shows), safe=False)


def movie_list(request):
    search_query = request.GET.get('search')
    if search_query:
        movies = Movie.objects.filter(name__icontains = search_query)
    else:
        movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})


def theater_list(request, movie_id):
    movie = get_object_or_404(Movie, id = movie_id)
    theaters = Theater.objects.filter(movie = movie).order_by('date')
    return render(request, 'movies/theater_list.html', {'movie': movie, 'theaters': theaters})


def calculate_dynamic_price(theaters):
    """Adjust price dynamically based on available seats and time remaining"""
    
    #Get remaining seats
    total_seats = theaters.total_seats
    booked_seats = Seat.objects.filter(theaters=theaters, is_booked=True).count()
    remaining_seats = total_seats - booked_seats

    #Default price is the base price
    # price_multiplier = 1.0  # No increase initially
    price_multiplier = Decimal('1.0')  # Convert float to Decimal

    #Fix: If `time` is None, return base price directly
    if theaters.time is None:
        return round(theaters.base_price, 2)

    #If more than 80% seats are booked → Increase price by 20%
    if remaining_seats / total_seats < 0.2:
        price_multiplier = Decimal('1.2')  # Convert to Decimal
    
    #If the show starts in less than 2 hours → Increase price by 15%
    show_datetime = datetime.combine(theaters.date, theaters.time)
    time_remaining = show_datetime - datetime.now()

    if time_remaining < timedelta(hours=2):
        price_multiplier *= Decimal('1.15')  # Further increase price

    #Calculate final dynamic price
    dynamic_price = theaters.base_price * price_multiplier
    return round(dynamic_price, 2)


def get_dynamic_price(request, theater_id):
    theaters = get_object_or_404(Theater, id=theater_id)
    price = calculate_dynamic_price(theaters)
    return JsonResponse({'price': price})


# booking seats function
@login_required(login_url = '/login/')
def book_Seats(request, theater_id):
    theaters = get_object_or_404(Theater, id = theater_id)
    seats = Seat.objects.filter(theaters = theaters)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON from frontend
            selected_seat_ids = data.get('seats', [])
            error_seats = []

            for seat_id in selected_seat_ids:
                seat = get_object_or_404(Seat, id=seat_id, theaters=theaters)
            
                if seat.is_booked:
                    error_seats.append(seat.seat_number)
                else:
                    Booking.objects.create(
                        user = request.user,
                        seat = seat,
                        theaters = theaters,
                        movie = theaters.movie
                    )
                    print(f"Seat {seat.seat_number} is_booked BEFORE: {seat.is_booked}")
                    seat.is_booked = True
                    seat.save(update_fields=['is_booked'])
                    print(f"Seat {seat.seat_number} is_booked AFTER: {seat.is_booked}")


            if error_seats:
                return JsonResponse({"success": False, "error_seats": error_seats})

            return JsonResponse({"success": True})
        except Exception as e:
            # Catch any unexpected errors
            print(f"Error booking seats: {e}")
            return JsonResponse({"success": False, "error": str(e)})

    return render(request, 'movies/seat_selection.html', {'seats': seats, 'theaters': theaters})


def api_today_shows(request):
    current_date = date.today()
    today_shows = Theater.objects.filter(date=current_date).order_by('time').values('movie__name', 'name', 'time')
    return JsonResponse(list(today_shows), safe=False)


def latest_bookings(request):
    bookings = Booking.objects.order_by('-booked_at')  # Order by latest booking first
    return render(request, 'movies/profile.html', {'bookings': bookings})
