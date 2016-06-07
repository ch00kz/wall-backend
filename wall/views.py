from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, parsers, renderers, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from wall.models import Post, Like, Notification
from wall.serializers import (
    PostSerializer, LikeSerializer, NotificationSerializer,
    UserSerializer
)


# Override this view to add the user to the response
class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        return Response({'token': token.key, 'user': user_serializer.data})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(parent=None).order_by('-date')
    serializer_class = PostSerializer

    @detail_route(methods=['post'])  # POST to reply to post
    def reply(self, request, *args, **kwargs):
        # get user and post data from request
        parent = Post.objects.get(pk=kwargs.get('pk'))
        # create a new post and set this post as the parent
        reply = Post.objects.create(
            user=request.user,
            content=request.data.get('content'),
            date=request.data.get('date'),
            parent=parent,
        )

        return Response(
            {'success' : True, 'reply_pk': reply.pk }
        )

    @detail_route(methods=['post'])  # POST to like post
    def like(self, request, *args, **kwargs):
        user = request.user
        post = get_object_or_404(Post, pk=kwargs.get('pk'))
        like_action = request.data.get('like', False)
        already_liked = post.likes.filter(user=user).exists()
        like_post = like_action and not already_liked
        if like_post:
            Like.objects.create(user=user, post=post)
        else:
            post.likes.filter(user=user).delete()
        return Response(
            {'message' : "Post Succesfully {}.".format("Liked" if like_post else "Unliked")}
        )

    @detail_route(methods=['get'])  # GET to get detailed like data for a post
    def likes(self, request, *args, **kwargs):
        post = self.get_object()
        likes = post.likes
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)


class LikeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class PostOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        from pprint import pprint
        return request._request.method == 'POST'


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (PostOnlyPermission,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
