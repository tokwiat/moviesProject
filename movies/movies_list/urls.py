from django.urls import path

from . import views

app_name = 'movies_list'
urlpatterns = [
    path('', views.movies, name='movies'),
    path('movies/', views.movies_user_panel, name='movies_user_panel'),
    path('movies/?page=<int:i>&film_query=<str:film_query>', views.movies, name='movies'),
    path('movies/?page=<int:i>&film_query=<str:film_query>&store_favourite=<str:store_favourite>&is_favourite=<str:is_favourite>', views.movies, name='movies'),
]
