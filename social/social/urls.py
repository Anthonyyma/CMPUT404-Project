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
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import include, path
from rest_framework import routers

# from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r"authors", author_views.AuthorViewSet)

urlpatterns = [
    path("", include("core.urls")),
    path("", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path(r"api/authors/<author1>/followers/<author2>/", author_views.follow_view),
    # path(r"crap/", author_views.check_follow),
    path("api/", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
