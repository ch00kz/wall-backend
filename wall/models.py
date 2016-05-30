from django_extensions.db.models import TimeStampedModel

from django.db import models
from django.contrib.auth.models import User


class Post(TimeStampedModel):
    content = models.TextField()
    user = models.ForeignKey(User, editable=False, related_name="posts")
    emotion = models.ForeignKey('Emotion', related_name="posts")
    parent = models.ForeignKey('Post', editable=False, blank=True, null=True,
                               related_name='replies')


class Emotion(models.Model):
    name = models.CharField(max_length=50)


class Like(TimeStampedModel):
    post = models.ForeignKey('Post', related_name='likes')
    user = models.ForeignKey(User, editable=False, related_name="likes")


class Notification(TimeStampedModel):
    METHODS = (
        ('email', 'Email'),
        ('wall', 'Wall'),
    )
    TRIGGERS = (
        ('like', 'Like'),
        ('reply', 'Reply'),
    )
    content = models.TextField()
    method = models.CharField(max_length=50, choices=METHODS)
    trigger = models.CharField(max_length=50, choices=TRIGGERS)
    user = models.ForeignKey(User, editable=False,
                             related_name="notifications")

