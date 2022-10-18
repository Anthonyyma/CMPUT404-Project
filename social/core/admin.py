from core.models import Comment, Follow, FollowRequest, Inbox, Like, Post, User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    # display the profile_image in the admin panel for users
    fieldsets = ((None, {"fields": ("profile_image",)}), *BaseUserAdmin.fieldsets)


class FollowAdmin(admin.ModelAdmin):
    list_display = ("follower", "followee")


class FollowRequestAdmin(admin.ModelAdmin):
    list_display = ("follower", "followee")


class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "published", "friends_only", "unlisted")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "published")
    # fields = ("author", "post", "content", "content_type", "published")


class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "comment", "published")


class InboxAdmin(admin.ModelAdmin):
    list_display = ("user", "post")


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(FollowRequest, FollowRequestAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Inbox, InboxAdmin)
