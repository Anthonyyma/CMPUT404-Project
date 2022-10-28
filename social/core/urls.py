from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.PostList.as_view(), name='myPosts'),
    path('editPost/', views.createPost, name='editPost'),
    path('createPost/', views.postType, name='createPost'),
    path('deletePost/', views.deletePost, name='deletePost'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register')
    # path('info/', views.info, name='info'),
    # path('info/', views.info, name='info'),
    # path('favicon.ico/', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.png'))),
]