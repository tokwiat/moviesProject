import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from requests import get
from movies.settings import APIKEY
from .models import Favourite

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M', )

ENDPOINTS = {
    'ENDPOINT': f'http://www.omdbapi.com/?apikey={APIKEY}',
}

@login_required
def movies_user_panel(request):
    """
    :param
    :return
    """
    if request.method == "POST":
        return resolve_request(request,  request.POST, page=1)
    if request.method == 'GET':
        favourite = fetch_favourite_for_user()

        if 'page' in request.GET and 'film_query' in request.GET and 'store_favourite' not in request.GET:
            return resolve_request(request, request.GET, request.GET['page'])

        if 'store_favourite' in request.GET:
            handle_favourite_update(request)
            return resolve_request(request, request.GET, request.GET['page'],
                                   store_favourite=request.GET['store_favourite'],
                                   is_favourite=request.GET['is_favourite'])

        return render(request, template_name='movies/movies.html', context={'user': request.user,
                                                                            'favourite': favourite})

@login_required
@cache_page(60*1)
def movies(request):
    """
    :param
    :return
    """
    if request.method == "POST":
        return resolve_request(request,  request.POST, page=1)
    if request.method == 'GET':
        if 'page' in request.GET and 'film_query' in request.GET and 'store_favourite' not in request.GET:
            return resolve_request(request, request.GET, request.GET['page'])

        if 'store_favourite' in request.GET:
            handle_favourite_update(request)
            return resolve_request(request, request.GET, request.GET['page'])

        return render(request, template_name='movies/movies.html', context={'user': request.user})


def resolve_request(request, request_type, page=None, **kwargs):
    movies_list = get_movies(request_type['film_query'], page)
    if movies_list['Response'] == 'True':
        return render(request, template_name='search_results/search_results.html',
                      context={'movies': movies_list,
                               'pages': range(1, int(int(movies_list['totalResults']) / 10) - 1),
                               'film_query': request_type['film_query'],
                               'current_page': page,
                               'user': request.user,
                               **kwargs
                               })
    else:
        return render(request, template_name='search_results/search_results.html',
               context={'movies': movies_list,
                        'film_query': request_type['film_query'],
                        'user': request.user})


def handle_favourite_update(request):
    favourite = Favourite.objects.filter(user_name=request.user,
                                         film_title=request.GET['store_favourite'])
    if favourite:
        favourite = Favourite.objects.get(user_name=request.user,
                                          film_title=request.GET['store_favourite'])
        favourite.is_favourite = request.GET['is_favourite']
        favourite.save()
    else:
        favourite = Favourite()
        favourite.user_name = request.user
        favourite.film_title = request.GET['store_favourite']
        favourite.is_favourite = request.GET['is_favourite']
        favourite.save()


def fetch_favourite_for_user():
    favourite = Favourite.objects.filter(is_favourite=True)
    return favourite


def get_movies(title, page=None):
    """
    :return
    """
    searched_movies = get(ENDPOINTS['ENDPOINT']+f'&s={title}')
    if page:
        searched_movies = get(ENDPOINTS['ENDPOINT'] + f'&s={title}&page={page}')

    return searched_movies.json()