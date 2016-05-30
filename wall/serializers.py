from rest_framework import serializers

from wall.models import Post, Emotion, Like, Notification


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('content', 'user', 'emotion', 'parent')


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
