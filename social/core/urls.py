# from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="Social Distribution API",
        default_version="1.0.0",
        description="API documentation of App",
    ),
    public=True,
)

urlpatterns = [
    path("", views.showFeed, name="feed"),
    path("publicFeed/", views.publicFeed, name="publicFeed"),
    path("editPost/", views.createPost, name="editPost"),
    path("createPost/", views.postType, name="createPost"),
    path("deletePost/", views.deletePost, name="deletePost"),
    path("postContent/", views.postContent, name="postContent"),
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("user/followers/", views.follower_view, name="follower_view"),
    path("user/following/", views.following_view, name="following_view"),
    path("allUsers", views.all_users_view, name="all_users_view"),
    path("logout", views.logout_user, name="logout"),
    path("user/<userID>", views.viewUser, name="viewUser"),
    path("user/", views.viewCurrentUser, name="viewCurrentUser"),
    path(
        "api/docs",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("user/edit/", views.editUser, name="editUser"),
    # path('info/', views.info, name='info'),
    # path('info/', views.info, name='info'),
    # path('favicon.ico/',
    # RedirectView.as_view(url=staticfiles_storage.url('img/favicon.png'))),
]
