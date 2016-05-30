from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from wall.models import Post, Emotion, Like, Notification
from wall.serializers import (
    PostSerializer, EmotionSerializer, LikeSerializer, NotificationSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @detail_route()  # POST to reply to post
    def reply(self, request, *args, **kwargs):
        return Response("Not Implemented")

    @detail_route()  # POST to like post
    def like(self, request, *args, **kwargs):
        return Response("Not Implemented")

    @detail_route()  # GET to get detailed like data for a post
    def likes(self, request, *args, **kwargs):
        post = self.get_object()
        likes = post.likes
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)


class EmotionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer


class LikeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
