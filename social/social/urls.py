"""social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import core.authors.api_views as author_views
import core.inbox.api_views as inbox_views
import core.posts.api_views as post_views
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import include, path
from rest_framework_nested import routers

# from rest_framework import routers


# from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r"authors", author_views.AuthorViewSet)

author_router = routers.NestedSimpleRouter(router, r"authors", lookup="author")
author_router.register(r"posts", post_views.PostViewSet, basename="posts")
post_router = routers.NestedSimpleRouter(author_router, r"posts", lookup="post")
post_router.register(r"comments", post_views.CommentViewSet, basename="comments")

urlpatterns = [
    path("", include("core.urls")),
    path("", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path(r"api/authors/<author1>/followers/<author2>/", author_views.follow_view),
    path(r"api/authors/<recipient_id>/inbox/", inbox_views.InboxView.as_view()),
    path(r"api/follow-request", author_views.follow_request_view),
    path("api/", include(router.urls)),
    path("api/", include(author_router.urls)),
    path("api/", include(post_router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
