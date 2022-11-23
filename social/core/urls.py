# from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path

from . import views

# from django.views.generic.base import RedirectView


urlpatterns = [
    path("", views.PostList.as_view(), name="myPosts"),
    path("editPost/", views.createPost, name="editPost"),
    path("createPost/", views.postType, name="createPost"),
    path("deletePost/", views.deletePost, name="deletePost"),
    path("postContent/", views.postContent, name="postContent"),
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("user/<userID>", views.viewUser, name="viewUser"),
    path("user/", views.viewCurrentUser, name="viewCurrentUser"),
    path("user/edit/", views.editUser, name="editUser"),
    # path('info/', views.info, name='info'),
    # path('info/', views.info, name='info'),
    # path('favicon.ico/',
    # RedirectView.as_view(url=staticfiles_storage.url('img/favicon.png'))),
]
