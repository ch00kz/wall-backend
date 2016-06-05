from django.contrib import admin
from wall.models import Post, Like, Notification


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'parent')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('method', 'trigger', 'user')