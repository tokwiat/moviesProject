import re

from django.contrib.auth.models import User
from django.test import TestCase
from movies_list.views import *
from django.test import RequestFactory


class MoviesTest(TestCase):
    def remove_csrf(self, html_code):
        csrf_regex = r'name="csrfmiddlewaretoken" value=".*"'
        return re.sub(csrf_regex, '', html_code)

    def test_get_movies_user_panel(self):
        expected_output = '<!-- templates/movies.html-->\n<!-- templates/base.html -->\n<!DOCTYPE html>\n<html>\n<head>\n  <meta charset="utf-8">\n  <title>Movies Search</title>\n</head>\n<body>\n  <main>\n    \n\n    Hi jacob!\n    </br>\n    \n  <p><a href="/accounts/logout/">Log Out</a></p>\n  </br>\n  Type keyword to search matching films:\n  </br>\n  <form action="" method="post"><input type="hidden" name="csrfmiddlewaretoken" value="XZnqWBOObzc5EY1kwHpU6IJUcoyCOky1BD9wFrxYnGd79R3AT4c5TndU8VKDOJ3r">\n     </br>\n     <input name="film_query" type="text" placeholder="Search...">\n     <input type="submit" value="OK">\n  </form>\n\n\n  </main>\n</body>\n</html>'
        self.user = User.objects.create_user(
            username='jacob', email='jacob@test.com', password='top_secret')
        req = RequestFactory().get('/')
        req.user = self.user
        resp = movies_user_panel(req)
        self.assertEqual(self.remove_csrf(resp.content.decode()), self.remove_csrf(expected_output))

    def test_get_with_film_page(self):
        # self.user = User.objects.create_user(
        #     username='jacob', email='jacob@test.com', password='top_secret')
        # req = RequestFactory().get('/movies/?page=1&film_query=test')
        # req.user = self.user
        # resp = movies_user_panel(req)
        # print(resp.content)
        pass