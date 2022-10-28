from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='myPosts'),
    path('editPost/', views.createPost, name='editPost'),
    path('createPost/', views.postType, name='createPost'),
    path('friends/', views.friends, name="friends")
    # path('info/', views.info, name='info'),
    # path('info/', views.info, name='info'),
    # path('favicon.ico/', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.png'))),
]