from django_extensions.db.models import TimeStampedModel
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver


class Post(TimeStampedModel):
    content = models.TextField()
    date = models.DateTimeField()
    user = models.ForeignKey(User, related_name="posts")
    parent = models.ForeignKey('Post', blank=True, null=True,
                               related_name='replies')

    class Meta:
        ordering = ["date"]

    @property
    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return "{} - {}".format(self.user, self.pk)


class Like(TimeStampedModel):
    post = models.ForeignKey('Post', related_name='likes')
    user = models.ForeignKey(User, related_name="likes")


class Notification(TimeStampedModel):
    METHODS = (
        ('email', 'Email'),
        ('wall', 'Wall'),
    )
    TRIGGERS = (
        ('like', 'Like'),
        ('reply', 'Reply'),
        ('registration', 'Registration'),
    )
    content = models.TextField()
    method = models.CharField(max_length=50, choices=METHODS)
    trigger = models.CharField(max_length=50, choices=TRIGGERS)
    user = models.ForeignKey(User, related_name="notifications")

    @staticmethod
    def welcome(user):
        title = 'Welcome to ./rant'
        body = 'Welcome {} {}!! Try to be civil.'.format(user.first_name,
                                                         user.last_name)
        recipient = [user.email]

        Notification.objects.create(
            user=user,
            content=body,
            trigger='registration',
            method='email',
        )
        try:
            send_mail(title, body, 'dotSlashRant@ch00kz.mailgun.com',
                      recipient)
        except Exception as e:
            print(e)


# Generates Token when user is created
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Notification.welcome(instance)
        Token.objects.create(user=instance)
