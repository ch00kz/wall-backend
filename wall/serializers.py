from rest_framework import serializers

from django.contrib.auth.models import User

from wall.models import Post, Like, Notification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'email', 'username')


class PostSerializer(serializers.ModelSerializer):
    user_data = UserSerializer(source='user', read_only=True)
    id = serializers.ReadOnlyField(source='pk')

    class Meta:
        model = Post
        fields = ('id', 'content', 'user', 'user_data',  'date', 'parent',
                  'like_count', 'liked')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('post', 'user')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('content', 'method', 'trigger', 'user')
