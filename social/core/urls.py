# from django.contrib.staticfiles.storage import staticfiles_storage
import core.authors.views as author_views
import core.posts.views as post_views
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
    # path(
    # 'authors/<str:author_id>/posts/<str:post_id>/image/',
    # views.ImagePostView.as_view()),
    path("", views.showFeed, name="feed"),
    path("publicFeed/", views.publicFeed, name="publicFeed"),
    path("editPost/", views.createPost, name="editPost"),
    path("createPost/", views.postType, name="createPost"),
    path("deletePost/", views.deletePost, name="deletePost"),
    path("postContent/", post_views.post_detail, name="postContent"),
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("user/followers/", views.follower_view, name="follower_view"),
    path("user/following/", views.following_view, name="following_view"),
    path("allUsers/", author_views.all_users_view, name="all_users_view"),
    path("logout", views.logout_user, name="logout"),
    path("user/", author_views.user_detail, name="viewUser"),
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
