from os import listdir
from os.path import join, isdir

from django.conf.urls import include, url

from restshop_project.settings import BASE_DIR

API_DIR = 'restshop/api/'
entities = [directory
            for directory in listdir(join(BASE_DIR, API_DIR))
            if (isdir(join(BASE_DIR, API_DIR, directory))
                and directory != '__pycache__')]

urlpatterns = [
    url(r'^', include('restshop.api.{}.urls'.format(entity)))
    for entity in entities
]
