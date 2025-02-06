from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
#url mapping
urlpatterns = [
    path('', views.movie_list, name = 'movie_list'),
    # path('', views.homepage, name='home'), #Define the route for the homepage.
    path('current-shows/', views.current_shows, name='current_shows'),
    path('<int:movie_id>/theaters', views.theater_list, name = 'theater_list'),
    # path('theaters/<int:theater_id>/seats/book/', views.book_Seats, name = 'book_Seats'),
    path('theaters/<int:theater_id>/seats/', views.book_Seats, name = 'book_Seats'),
    path('theaters/<int:theater_id>/dynamic-price/', views.get_dynamic_price, name='get_dynamic_price'),
    # path('movies/', include('movies.urls')),
    # path('book_Seats/<int:theater_id>/', views.book_Seats, name='book_Seats'),
    path('api/today-shows/', views.api_today_shows, name='api_today_shows'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset'),
]