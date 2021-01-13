import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from requests import get
from movies.settings import APIKEY

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M', )

ENDPOINTS = {
    'ENDPOINT': f'http://www.omdbapi.com/?apikey={APIKEY}',
}


@login_required
@cache_page(60*1)
@csrf_protect
def movies(request):
    """
    :param
    :return
    """
    if request.method == "POST":
        return resolve_request(request,  request.POST)
    if request.method == 'GET':
        if 'page' in request.GET and 'film_title' in request.GET:
            return resolve_request(request, request.GET, request.GET['page'])

        return render(request, template_name='movies/movies.html', context={'user': request.user})


def resolve_request(request, request_type, page=None):
    movies_list = get_movies(request_type['film_title'], page)
    return render(request, template_name='search_results/search_results.html',
                  context={'movies': movies_list,
                           'pages': range(1, int(int(movies_list['totalResults']) / 10) - 1),
                           'film_title': request_type['film_title'],
                           'user': request.user})


def get_movies(title, page=None):
    """
    :return
    """
    searched_movies = get(ENDPOINTS['ENDPOINT']+f'&s={title}')
    if page:
        searched_movies = get(ENDPOINTS['ENDPOINT'] + f'&s={title}&page={page}')
    return searched_movies.json()