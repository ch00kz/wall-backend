from rest_framework import serializers

from django.contrib.auth.models import User

from wall.models import Post, Emotion, Like, Notification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'email', 'username')


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    id = serializers.ReadOnlyField(source='pk')

    class Meta:
        model = Post
        fields = ('id', 'content', 'user', 'emotion', 'parent')


class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ('name',)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('post', 'user')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('content', 'method', 'trigger', 'user')



