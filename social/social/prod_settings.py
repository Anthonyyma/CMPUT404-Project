# isort: skip_file
# flake8: noqa # this file shouldn't be linted
import django_on_heroku
from social.settings import *
import dj_database_url

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(conn_max_age=600)
}

API_HOST_PATH = "https://c404-team8.herokuapp.com/api/"


ALLOWED_HOSTS = [
    "c404-team8.herokuapp.com"
]


django_on_heroku.settings(locals())
