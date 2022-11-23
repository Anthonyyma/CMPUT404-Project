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

django_on_heroku.settings(locals())
