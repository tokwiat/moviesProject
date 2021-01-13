from django.urls import path

from . import views

app_name = 'movies_list'
urlpatterns = [
    path('', views.movies, name='movies'),
    path('movies/', views.movies, name='movies'),
    path('movies/?page=<int:i>&film_title=<str:film_title>', views.movies, name='movies'),
]
