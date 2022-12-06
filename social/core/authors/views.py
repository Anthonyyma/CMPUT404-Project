from core.client import sync_external_authors
from core.models import User
from django.shortcuts import render


def all_users_view(request):
    sync_external_authors()

    all_users = User.objects.order_by("username")
    context = {"users": all_users}
    return render(request, "all_users.html", context)
