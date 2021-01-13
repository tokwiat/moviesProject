from django.db import models


class Favourite(models.Model):
    user_name = models.CharField(max_length=200)
    film_title = models.CharField(max_length=200)
    is_favourite = models.BooleanField(default=False)
