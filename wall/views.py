from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from wall.models import Post, Like, Notification
from wall.serializers import (
    PostSerializer, LikeSerializer, NotificationSerializer,
    UserSerializer
)

from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


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
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @detail_route(methods=['post'])  # POST to reply to post
    def reply(self, request, *args, **kwargs):
        # get user and post data from request
        # create a new post and set this post as the parent
        return Response("Not Implemented")

    @detail_route(methods=['post'])  # POST to like post
    def like(self, request, *args, **kwargs):
        return Response("Not Implemented")

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
